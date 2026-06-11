<script lang="ts">
	import Heading from "./components/ui/Heading.svelte";
	import Input from "./components/form/Input.svelte";
	import Button from "./components/ui/Button.svelte";
	import Modal from "./components/overlay/Modal.svelte";
	import Text from "./components/ui/Text.svelte";
	import Progress from "./components/ui/Progress.svelte";

	import {
		Video,
		Volume2,
		VolumeOff,
		Download,
		List,
		X,
	} from "@lucide/svelte";

	let modalOpen: boolean = $state(false);
	let inputValue: string = $state("");
	let buttonState: "idle" | "downloading" | "error" = $state("idle");
	let selectedFormat: string = $state("video+audio");
	let selectedContainer: string = $state("mp4");

	let modalTitle: string = $state("oops!!!");
	let modalText: string = $state("something went wrong!");

	let qualityModalOpen: boolean = $state(false);
	let availableQualities: number[] = $state([]);
	let qualityPromiseResolve: ((h: number | null) => void) | null = null;

	let patchnotesModalOpen: boolean = $state(false);

	let errorTimer: ReturnType<typeof setTimeout> | null = null;

	$effect(() => {
		selectedFormat;
		if (
			selectedFormat === "audio" &&
			!["mp3", "wav", "flac", "mp4"].includes(selectedContainer)
		) {
			selectedContainer = "mp4";
		} else if (
			selectedFormat !== "audio" &&
			!["mp4", "webm", "mkv"].includes(selectedContainer)
		) {
			selectedContainer = "mp4";
		}
	});

	interface QueueItem {
		id: number;
		label: string;
		status: "downloading" | "done" | "error";
		blob?: Blob;
		filename?: string;
		totalSize?: number;
		loadedSize?: number;
	}
	let nextQueueId = 1;
	let queue: QueueItem[] = $state([]);
	let queueModalOpen = $state(false);
	let doneCount = $derived(queue.filter((i) => i.status === "done").length);
	let abortControllers = new Map<number, AbortController>();

	function buttonText() {
		if (buttonState === "downloading") return "...";
		if (buttonState === "error") return "!!!";
		return "go!";
	}

	function openModal(title: string, text: string) {
		modalTitle = title;
		modalText = text;
		modalOpen = true;
	}

	function showQualityModal(qualities: number[]): Promise<number | null> {
		availableQualities = qualities;
		qualityModalOpen = true;
		return new Promise((resolve) => {
			qualityPromiseResolve = resolve;
		});
	}

	function selectQuality(height: number) {
		qualityModalOpen = false;
		qualityPromiseResolve?.(height);
		qualityPromiseResolve = null;
	}

	function cancelQuality() {
		qualityModalOpen = false;
		qualityPromiseResolve?.(null);
		qualityPromiseResolve = null;
	}

	function addToQueue(
		id: number,
		label: string,
		blob?: Blob,
		filename?: string,
	) {
		const idx = queue.findIndex((i) => i.id === id);
		if (idx !== -1) {
			queue[idx] = {
				...queue[idx],
				label,
				status: "done",
				blob,
				filename,
			};
		}
	}

	function downloadFromQueue(id: number) {
		const item = queue.find((i) => i.id === id);
		if (!item?.blob) return;
		const url = URL.createObjectURL(item.blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = item.filename ?? "download";
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}

	function removeFromQueue(id: number) {
		const item = queue.find((i) => i.id === id);
		if (!item) return;
		if (item.status === "downloading") {
			abortControllers.get(id)?.abort();
			abortControllers.delete(id);
		}
		queue = queue.filter((i) => i.id !== id);
	}

	function formatBytes(bytes: number): string {
		const mb = bytes / (1024 * 1024);
		return mb.toFixed(1) + "mb";
	}

	async function downloadVideo() {
		if (inputValue == "") {
			openModal("hold up!!!", "you need to enter a link, silly!");
			return;
		}

		if (errorTimer) clearTimeout(errorTimer);
		buttonState = "downloading";

		const qid = nextQueueId++;
		const urlLabel =
			inputValue.trim().length > 50
				? inputValue.trim().slice(0, 50) + "..."
				: inputValue.trim();

		queue = [...queue, { id: qid, label: urlLabel, status: "downloading" }];

		const ac = new AbortController();
		abortControllers.set(qid, ac);

		try {
			let selectedHeight: number | null = null;
			if (selectedFormat !== "audio") {
				try {
					const qualRes = await fetch(
						`/api/qualities?url=${encodeURIComponent(inputValue.trim())}`,
						{ signal: ac.signal },
					);
					if (qualRes.ok) {
						const data: { qualities: number[] } =
							await qualRes.json();
						if (data.qualities?.length) {
							const h = await showQualityModal(data.qualities);
							if (h === null) {
								buttonState = "idle";
								queue = queue.filter((i) => i.id !== qid);
								abortControllers.delete(qid);
								return;
							}
							selectedHeight = h;
						}
					}
				} catch (e) {
					if (ac.signal.aborted) throw e;
					console.log("failed to fetch quality options!");
				}
			}

			buttonState = "idle";

			let totalSize: number | null = null;
			try {
				const metaRes = await fetch("/api/metadata", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					signal: ac.signal,
					body: JSON.stringify({
						url: inputValue.trim(),
						format: selectedFormat,
						quality: selectedHeight,
						container: selectedContainer,
					}),
				});
				if (metaRes.ok) {
					const meta = await metaRes.json();
					totalSize = meta.size ?? null;
					if (totalSize) {
						const idx = queue.findIndex((i) => i.id === qid);
						if (idx !== -1) {
							queue[idx] = { ...queue[idx], totalSize };
						}
					}
				}
			} catch (e) {
				if (ac.signal.aborted) throw e;
			}

			const res = await fetch("/api/download", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				signal: ac.signal,
				body: JSON.stringify({
					url: inputValue.trim(),
					format: selectedFormat,
					quality: selectedHeight,
					container: selectedContainer,
				}),
			});

			if (!res.ok) {
				const err = await res.json();
				openModal("oops!!!", err.error ?? "something went wrong!");
				queue = queue.map((i) =>
					i.id === qid ? { ...i, status: "error" as const } : i,
				);
				abortControllers.delete(qid);
				return;
			}

			const reader = res.body!.getReader();
			const chunks: Uint8Array[] = [];
			let loaded = 0;
			let lastUpdate = 0;

			while (true) {
				const { done, value } = await reader.read();
				if (done) break;
				chunks.push(value);
				loaded += value.length;
				const now = Date.now();
				if (now - lastUpdate > 200) {
					lastUpdate = now;
					const idx = queue.findIndex((i) => i.id === qid);
					if (idx !== -1) {
						queue[idx] = { ...queue[idx], loadedSize: loaded };
					}
				}
			}

			{
				const idx = queue.findIndex((i) => i.id === qid);
				if (idx !== -1) {
					queue[idx] = { ...queue[idx], loadedSize: loaded };
				}
			}

			const blob = new Blob(chunks as BlobPart[], {
				type: res.headers.get("content-type") ?? undefined,
			});
			const header = res.headers.get("Content-Disposition");
			const match = header?.match(/filename="?(.+?)"?$/);
			const filename =
				match?.[1] ?? `video.${blob.type.split("/")[1] ?? "mp4"}`;

			addToQueue(qid, filename, blob, filename);

			const url = URL.createObjectURL(blob);
			const a = document.createElement("a");
			a.href = url;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);

			abortControllers.delete(qid);
		} catch (err) {
			if (err instanceof DOMException && err.name === "AbortError") {
				queue = queue.filter((i) => i.id !== qid);
				abortControllers.delete(qid);
				buttonState = "idle";
				return;
			}
			openModal("oops!!!", "could not reach the server");
			queue = queue.map((i) =>
				i.id === qid ? { ...i, status: "error" as const } : i,
			);
			abortControllers.delete(qid);
		}
	}

	$effect(() => {
		return () => {
			if (errorTimer) clearTimeout(errorTimer);
		};
	});

	if (!document.cookie.includes("seenInfo=true")) {
		openModal(
			"owo what's this?",
			"avali is a completely free youtube downloader. no paywalls, no ads, no bullshit. just paste a link, pick your format, and go!",
		);

		document.cookie =
			"seenInfo=true; max-age=31536000; path=/; SameSite=Strict";
	}
</script>

<!-- svelte-ignore a11y_invalid_attribute -->
<a
	class="patchnotes-link"
	href="#"
	onclick={(e) => {
		e.preventDefault();
		patchnotesModalOpen = true;
	}}>🎉 1.0.0 - fresh outta beta!</a
>

<Modal bind:open={modalOpen} title={modalTitle}>
	<Text size="md">{modalText}</Text>
	{#snippet footer()}
		<Button variant="primary" size="sm" onclick={() => (modalOpen = false)}
			>okay!</Button
		>
	{/snippet}
</Modal>

<Modal
	bind:open={qualityModalOpen}
	title="select quality"
	onclose={cancelQuality}
	size="sm"
>
	<div class="quality-list">
		{#each availableQualities as height}
			<Button variant="outline" onclick={() => selectQuality(height)}
				>{height}p</Button
			>
		{/each}
	</div>
	{#snippet footer()}
		<Button variant="ghost" size="sm" onclick={cancelQuality}>cancel</Button
		>
	{/snippet}
</Modal>

<Modal
	bind:open={patchnotesModalOpen}
	title="patch notes"
	onclose={() => {
		patchnotesModalOpen = false;
	}}
	size="lg"
>
	<!-- i should probably migrate this to a .md file in teh future but i really dont care right now -->
	<img src="/litten.gif" alt="litten!!!" class="patchnotes-gif" />
	<h1>🎉 fresh outta beta!</h1>
	<p>hey all! i'm glad to announce avali is now out of beta!</p>
	<p>this update brings some nice features i hope yall will enjoy!</p>
	<br />
	<h2 class="margin-shit">- 📜 download queue!</h2>
	<p>
		there's now a download queue! you can queue up videos and have them
		downloaded one after another!
	</p>
	<p>
		this queue also shows things like download progress, filesize, lets you
		redownload videos you've downloaded this session, and remove items from
		queue.
	</p>
	<h2 class="margin-shit">- 📹 format selection!</h2>
	<p>
		you can now pick which format your video downlodas at! pretty
		self-explanitory
	</p>
	<h2 class="margin-shit">- 📱 mobile improvements!</h2>
	<p>website works a lot beter on mobile now!</p>
	<h2 class="margin-shit">- 🚢 selfhosting!</h2>
	<p>you can selfhost avali now in docker!</p>

	<h2 class="margin-shit">- ❤ thanks!</h2>

	<p>thanks for using avali! - niko</p>
</Modal>

<Modal bind:open={queueModalOpen} title="download queue" size="md">
	<div class="queue-list">
		{#each queue as item (item.id)}
			<div class="queue-item">
				{#if item.status === "downloading" && item.totalSize}
					{@const pct = Math.min(
						((item.loadedSize ?? 0) / item.totalSize) * 100,
						100,
					)}
					<div class="qi-layer">
						<span class="queue-item-label">{item.label}</span>
						<span class="qi-size"
							>{formatBytes(item.loadedSize ?? 0)}/{formatBytes(
								item.totalSize,
							)}</span
						>
						<Button
							variant="ghost"
							size="sm"
							icon
							onclick={() => removeFromQueue(item.id)}
							><X size={14} /></Button
						>
					</div>
					<div class="qi-fill" style="width: {pct}%"></div>
				{:else}
					<span class="queue-item-label">{item.label}</span>
					<span class="queue-item-actions">
						{#if item.status === "downloading"}
							downloading...
						{:else if item.status === "done"}
							<Button
								variant="primary"
								size="sm"
								icon
								onclick={() => downloadFromQueue(item.id)}
								><Download size={16} /></Button
							>
						{:else}
							error
						{/if}
						<Button
							variant="ghost"
							size="sm"
							icon
							onclick={() => removeFromQueue(item.id)}
							><X size={14} /></Button
						>
					</span>
				{/if}
			</div>
		{/each}
	</div>
	{#if queue.length === 0}
		<div class="queue-empty">
			<Text size="md">woah, so empty,,,,,</Text>
		</div>
	{/if}
</Modal>

<div class="queue-btn-wrap">
	<Button variant="outline" icon onclick={() => (queueModalOpen = true)}
		><List size={20} /></Button
	>
	{#if queue.length > 0}
		<span class="queue-badge">{doneCount}/{queue.length}</span>
	{/if}
</div>

<div class="main">
	<Heading>///avali</Heading>
	<div class="input">
		<div class="flex1">
			<Input
				placeholder="paste your link here!"
				bind:value={inputValue}
			/>
		</div>
		<Button onclick={downloadVideo} disabled={buttonState !== "idle"}>
			{buttonText()}
		</Button>
	</div>
	{#if buttonState === "downloading"}
		<div class="progress-wrap">
			<Progress indeterminate size="sm" />
		</div>
	{/if}
	<div class="options">
		<Button
			variant={selectedFormat === "video+audio" ? "primary" : "outline"}
			onclick={() => (selectedFormat = "video+audio")}
			><Video size={20} /> video</Button
		>
		<Button
			variant={selectedFormat === "audio" ? "primary" : "outline"}
			onclick={() => (selectedFormat = "audio")}
			><Volume2 size={20} /> audio</Button
		>
		<Button
			variant={selectedFormat === "video" ? "primary" : "outline"}
			onclick={() => (selectedFormat = "video")}
			><VolumeOff size={20} /> mute</Button
		>
	</div>
	<div class="options container-options">
		{#if selectedFormat === "audio"}
			<Button
				variant={selectedContainer === "mp4" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "mp4")}>m4a</Button
			>
			<Button
				variant={selectedContainer === "mp3" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "mp3")}>mp3</Button
			>
			<Button
				variant={selectedContainer === "wav" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "wav")}>wav</Button
			>
			<Button
				variant={selectedContainer === "flac" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "flac")}>flac</Button
			>
		{:else}
			<Button
				variant={selectedContainer === "mp4" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "mp4")}>mp4</Button
			>
			<Button
				variant={selectedContainer === "webm" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "webm")}>webm</Button
			>
			<Button
				variant={selectedContainer === "mkv" ? "primary" : "outline"}
				onclick={() => (selectedContainer = "mkv")}>mkv</Button
			>
		{/if}
	</div>
</div>

<div class="down">
	<p>
		download responsibly! made with ❤︎ by <a
			href="https://xenon.zone"
			class="mysite"><span class="notoemoji">🦌</span>xenon</a
		>
	</p>
</div>

<style>
	.main {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.input {
		margin: 15px;
		display: flex;
		gap: 10px;
		width: min(500px, calc(100vw - 2rem));
	}
	.flex1 {
		flex: 1;
	}
	.options {
		display: flex;
		gap: 10px;
	}
	.container-options {
		margin-top: 15px;
	}
	.down {
		position: absolute;
		bottom: 10px;
		left: 0;
		right: 0;
		font-size: small;
		text-align: center;
		opacity: 50%;
	}
	.notoemoji {
		font-family: "Noto Emoji", monospace;
	}
	.progress-wrap {
		width: min(500px, calc(100vw - 2rem));
		margin-bottom: 15px;
	}
	.patchnotes-link {
		position: fixed;
		top: 15px;
		left: 50%;
		transform: translateX(-50%);
		color: var(--text-dim);
		text-decoration: none;
		cursor: pointer;
		z-index: 20;
		text-decoration: underline;
		font-size: small;
		white-space: nowrap;
	}
	.patchnotes-link:hover {
		color: var(--text-muted);
	}
	.patchnotes-gif {
		width: 100%;
		margin-bottom: 15px;
	}
	.quality-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.queue-btn-wrap {
		position: absolute;
		top: 10px;
		right: 10px;
		z-index: 10;
	}
	.queue-badge {
		position: absolute;
		top: -4px;
		right: -4px;
		font-size: 0.6rem;
		font-weight: 600;
		background: var(--text);
		color: var(--bg);
		border-radius: 999px;
		padding: 0.1rem 0.35rem;
		line-height: 1;
		pointer-events: none;
	}
	.queue-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.queue-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.75rem;
		padding: 0.5rem 0.75rem;
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 0.375rem;
		position: relative;
	}
	.queue-item-label {
		font-size: 0.8rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		flex: 1;
		min-width: 0;
	}
	.qi-layer {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		width: 100%;
		position: relative;
	}
	.qi-fill {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		background: var(--text);
		mix-blend-mode: difference;
		pointer-events: none;
		transition: width 0.15s ease;
		border-radius: inherit;
	}
	.qi-size {
		font-size: 0.75rem;
		color: var(--text-muted);
		flex-shrink: 0;
	}
	.queue-item-actions {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		gap: 0.25rem;
		font-size: 0.75rem;
		color: var(--text-muted);
	}
	.queue-empty {
		text-align: center;
		padding: 1rem;
	}

	@media (max-width: 768px) {
		.main {
			padding: 1rem;
		}
		.options {
			flex-wrap: wrap;
			justify-content: center;
		}
		.down {
			position: static;
			padding: 1rem;
		}
	}
	.margin-shit {
		margin-bottom: 10px;
		margin-top: 10px;
	}
</style>
