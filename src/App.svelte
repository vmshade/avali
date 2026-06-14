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
		Settings,
		Info,
		Sun,
		Moon,
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

	let settingsModalOpen: boolean = $state(false);
	let aboutModalOpen: boolean = $state(false);

	let isDark: boolean = $state(true);

	$effect(() => {
		document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
	});

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
		phase: "processing" | "downloading";
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
		settingsModalOpen = false;
		aboutModalOpen = false;
		queueModalOpen = false;
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

	function addToQueue(id: number, label: string, blob?: Blob, filename?: string) {
		const idx = queue.findIndex((i) => i.id === id);
		if (idx !== -1) {
			queue[idx] = { ...queue[idx], label, status: "done", blob, filename };
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
		if (inputValue === "") {
			openModal("hold up!!!", "you need to enter a link, silly!");
			return;
		}

		buttonState = "downloading";

		const qid = nextQueueId++;
		const urlLabel =
			inputValue.trim().length > 50
				? inputValue.trim().slice(0, 50) + "..."
				: inputValue.trim();

		queue = [
			...queue,
			{
				id: qid,
				label: urlLabel,
				status: "downloading",
				phase: "processing",
			},
		];

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
						const data: { qualities: number[] } = await qualRes.json();
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
					console.warn("failed to fetch quality options");
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
				openModal("oops!!!", err.detail ?? "something went wrong!");
				queue = queue.map((i) =>
					i.id === qid ? { ...i, status: "error" as const } : i,
				);
				abortControllers.delete(qid);
				buttonState = "idle";
				return;
			}

			const reader = res.body!.getReader();
			const chunks: Uint8Array[] = [];
			let loaded = 0;
			let lastUpdate = 0;

			const first = await reader.read();
			if (first.done) {
				openModal("oops!!!", "no data received!");
				queue = queue.map((i) =>
					i.id === qid ? { ...i, status: "error" as const } : i,
				);
				abortControllers.delete(qid);
				buttonState = "idle";
				return;
			}

			{
				const idx = queue.findIndex((i) => i.id === qid);
				if (idx !== -1) {
					queue[idx] = { ...queue[idx], phase: "downloading" };
				}
			}

			chunks.push(first.value);
			loaded += first.value.length;
			{
				const idx = queue.findIndex((i) => i.id === qid);
				if (idx !== -1) {
					queue[idx] = { ...queue[idx], loadedSize: loaded };
				}
			}
			lastUpdate = Date.now();

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
			const filename = match?.[1] ?? `video.${blob.type.split("/")[1] ?? "mp4"}`;

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
			buttonState = "idle";
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
			buttonState = "idle";
		}
	}

	if (!document.cookie.includes("seenInfo=true")) {
		openModal(
			"owo what's this?",
			"avali is a completely free youtube downloader. no paywalls, no ads, no bullshit. just paste a link, pick your format, and go!",
		);
		document.cookie = "seenInfo=true; max-age=31536000; path=/; SameSite=Strict";
	}
</script>

<Modal bind:open={modalOpen} title={modalTitle}>
	<Text size="md">{modalText}</Text>
	{#snippet footer()}
		<Button variant="primary" size="sm" onclick={() => (modalOpen = false)}>okay!</Button>
	{/snippet}
</Modal>

<Modal bind:open={qualityModalOpen} title="select quality" onclose={cancelQuality} size="sm">
	<div class="quality-list">
		{#each availableQualities as height}
			<Button variant="outline" onclick={() => selectQuality(height)}>{height}p</Button>
		{/each}
	</div>
	{#snippet footer()}
		<Button variant="ghost" size="sm" onclick={cancelQuality}>cancel</Button>
	{/snippet}
</Modal>

<Modal bind:open={settingsModalOpen} title="settings" size="sm">
	<div class="settings-list">
		<div class="settings-row">
			<span class="settings-label">theme</span>
			<button class="theme-toggle" onclick={() => (isDark = !isDark)} aria-label="toggle theme">
				{#if isDark}
					<Moon size={16} />
					<span>dark</span>
				{:else}
					<Sun size={16} />
					<span>light</span>
				{/if}
			</button>
		</div>
		<div class="settings-divider"></div>
		<div class="settings-row">
			<span class="settings-label">default format</span>
			<div class="settings-btn-group">
				<Button variant={selectedFormat === "video+audio" ? "primary" : "outline"} size="sm" onclick={() => (selectedFormat = "video+audio")}>video</Button>
				<Button variant={selectedFormat === "audio" ? "primary" : "outline"} size="sm" onclick={() => (selectedFormat = "audio")}>audio</Button>
				<Button variant={selectedFormat === "video" ? "primary" : "outline"} size="sm" onclick={() => (selectedFormat = "video")}>mute</Button>
			</div>
		</div>
		<div class="settings-divider"></div>
		<div class="settings-row">
			<span class="settings-label">default container</span>
			<div class="settings-btn-group">
				{#if selectedFormat === "audio"}
					<Button variant={selectedContainer === "mp4" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "mp4")}>m4a</Button>
					<Button variant={selectedContainer === "mp3" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "mp3")}>mp3</Button>
					<Button variant={selectedContainer === "wav" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "wav")}>wav</Button>
					<Button variant={selectedContainer === "flac" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "flac")}>flac</Button>
				{:else}
					<Button variant={selectedContainer === "mp4" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "mp4")}>mp4</Button>
					<Button variant={selectedContainer === "webm" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "webm")}>webm</Button>
					<Button variant={selectedContainer === "mkv" ? "primary" : "outline"} size="sm" onclick={() => (selectedContainer = "mkv")}>mkv</Button>
				{/if}
			</div>
		</div>
	</div>
	{#snippet footer()}
		<Button variant="primary" size="sm" onclick={() => (settingsModalOpen = false)}>done</Button>
	{/snippet}
</Modal>

<Modal bind:open={aboutModalOpen} title="about avali" size="md">
	<div class="about-content">
		<div class="about-logo">///avali</div>
		<Text size="md">a free, open-source youtube downloader. no paywalls, no ads, no tracking — just paste a link and go.</Text>
		<div class="about-divider"></div>
		<div class="about-row">
			<span class="about-key">version</span>
			<span class="about-val">1.1.0</span>
		</div>
		<div class="about-row">
			<span class="about-key">made by</span>
			<span class="about-val"><a href="https://xenon.zone" class="about-link">🦌 xenon</a></span>
		</div>
		<div class="about-row">
			<span class="about-key">formats</span>
			<span class="about-val">mp4, webm, mkv, mp3, wav, flac, m4a</span>
		</div>
		<div class="about-divider"></div>
		<Text size="md">
			avali uses <a href="https://github.com/yt-dlp/yt-dlp" class="about-link">yt-dlp</a> under the hood for downloading and ffmpeg for post-processing. please download responsibly and respect content creators.
		</Text>
		<div class="about-divider"></div>
		<div class="about-changelog">
			<span class="about-key">changelog</span>
			<div class="about-changes">
				<div class="change-entry">
					<span class="change-ver">1.1.0</span>
					<span class="change-desc">settings menu, light/dark theme, about page, mp4 audio fix</span>
				</div>
				<div class="change-entry">
					<span class="change-ver">1.0.1</span>
					<span class="change-desc">fixed 720p cap, processing animation, ui tweaks</span>
				</div>
				<div class="change-entry">
					<span class="change-ver">1.0.0</span>
					<span class="change-desc">download queue, format selection, mobile improvements, docker support</span>
				</div>
			</div>
		</div>
	</div>
	{#snippet footer()}
		<Button variant="primary" size="sm" onclick={() => (aboutModalOpen = false)}>close</Button>
	{/snippet}
</Modal>

<Modal bind:open={queueModalOpen} title="download queue" size="md">
	<div class="queue-list">
		{#each queue as item (item.id)}
			<div class="queue-item">
				{#if item.status === "downloading" && item.totalSize}
					{@const pct = item.phase === "processing" ? 100 : Math.min(((item.loadedSize ?? 0) / item.totalSize) * 100, 100)}
					<div class="qi-layer">
						<span class="queue-item-label">{item.label}</span>
						<span class="qi-size">{formatBytes(item.loadedSize ?? 0)}/{formatBytes(item.totalSize)}</span>
						<Button variant="ghost" size="sm" icon onclick={() => removeFromQueue(item.id)}><X size={14} /></Button>
					</div>
					<div class="qi-fill {item.phase === 'processing' ? 'qi-fill-processing' : ''}" style="width: {pct}%"></div>
				{:else}
					<span class="queue-item-label">{item.label}</span>
					<span class="queue-item-actions">
						{#if item.status === "downloading"}
							{item.phase === "processing" ? "processing..." : "downloading..."}
						{:else if item.status === "done"}
							<Button variant="primary" size="sm" icon onclick={() => downloadFromQueue(item.id)}><Download size={16} /></Button>
						{:else}
							error
						{/if}
						<Button variant="ghost" size="sm" icon onclick={() => removeFromQueue(item.id)}><X size={14} /></Button>
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

<div class="top-bar">
	<div class="top-bar-left">
		<Button variant="ghost" size="sm" icon onclick={() => (aboutModalOpen = true)} aria-label="about">
			<Info size={18} />
		</Button>
	</div>
	<div class="top-bar-right">
		<Button variant="ghost" size="sm" icon onclick={() => (isDark = !isDark)} aria-label="toggle theme">
			{#if isDark}
				<Sun size={18} />
			{:else}
				<Moon size={18} />
			{/if}
		</Button>
		<Button variant="ghost" size="sm" icon onclick={() => (settingsModalOpen = true)} aria-label="settings">
			<Settings size={18} />
		</Button>
		<div class="queue-btn-wrap">
			<Button variant="outline" icon onclick={() => (queueModalOpen = true)} aria-label="download queue">
				<List size={20} />
			</Button>
			{#if queue.length > 0}
				<span class="queue-badge">{doneCount}/{queue.length}</span>
			{/if}
		</div>
	</div>
</div>

<div class="main">
	<Heading>///avali</Heading>
	<div class="input">
		<div class="flex1">
			<Input placeholder="paste your link here!" bind:value={inputValue} />
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
		<Button variant={selectedFormat === "video+audio" ? "primary" : "outline"} onclick={() => (selectedFormat = "video+audio")}>
			<Video size={20} /> video
		</Button>
		<Button variant={selectedFormat === "audio" ? "primary" : "outline"} onclick={() => (selectedFormat = "audio")}>
			<Volume2 size={20} /> audio
		</Button>
		<Button variant={selectedFormat === "video" ? "primary" : "outline"} onclick={() => (selectedFormat = "video")}>
			<VolumeOff size={20} /> mute
		</Button>
	</div>
	<div class="options container-options">
		{#if selectedFormat === "audio"}
			<Button variant={selectedContainer === "mp4" ? "primary" : "outline"} onclick={() => (selectedContainer = "mp4")}>m4a</Button>
			<Button variant={selectedContainer === "mp3" ? "primary" : "outline"} onclick={() => (selectedContainer = "mp3")}>mp3</Button>
			<Button variant={selectedContainer === "wav" ? "primary" : "outline"} onclick={() => (selectedContainer = "wav")}>wav</Button>
			<Button variant={selectedContainer === "flac" ? "primary" : "outline"} onclick={() => (selectedContainer = "flac")}>flac</Button>
		{:else}
			<Button variant={selectedContainer === "mp4" ? "primary" : "outline"} onclick={() => (selectedContainer = "mp4")}>mp4</Button>
			<Button variant={selectedContainer === "webm" ? "primary" : "outline"} onclick={() => (selectedContainer = "webm")}>webm</Button>
			<Button variant={selectedContainer === "mkv" ? "primary" : "outline"} onclick={() => (selectedContainer = "mkv")}>mkv</Button>
		{/if}
	</div>
</div>

<div class="down">
	<p>
		download responsibly! made with ❤︎ by <a href="https://xenon.zone" class="mysite"><span class="notoemoji">🦌</span>xenon</a>
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
	.mysite {
		text-decoration: underline;
	}
	.notoemoji {
		font-family: "Noto Emoji", monospace;
	}
	.progress-wrap {
		width: min(500px, calc(100vw - 2rem));
		margin-bottom: 15px;
	}
	.top-bar {
		position: fixed;
		top: 16px;
		left: 0;
		right: 0;
		z-index: 20;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 12px;
		pointer-events: none;
	}
	.top-bar > * {
		pointer-events: auto;
	}
	.top-bar-left {
		display: flex;
		align-items: center;
		gap: 4px;
	}
	.top-bar-right {
		display: flex;
		align-items: center;
		gap: 4px;
	}
	.quality-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}
	.queue-btn-wrap {
		position: relative;
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
		overflow: hidden;
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
		z-index: 1;
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
	}
	@keyframes qi-pulse {
		0%, 100% { opacity: 0; }
		50% { opacity: 0.45; }
	}
	.qi-fill-processing {
		animation: qi-pulse 1.5s ease-in-out infinite;
		mix-blend-mode: normal;
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
	.settings-list {
		display: flex;
		flex-direction: column;
		gap: 0;
	}
	.settings-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 0.65rem 0;
	}
	.settings-label {
		font-size: 0.8rem;
		color: var(--text-muted);
		flex-shrink: 0;
	}
	.settings-divider {
		height: 1px;
		background: var(--border);
	}
	.settings-btn-group {
		display: flex;
		gap: 0.35rem;
		flex-wrap: wrap;
		justify-content: flex-end;
	}
	.theme-toggle {
		all: unset;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 0.4rem;
		font-size: 0.8rem;
		font-family: inherit;
		color: var(--text-muted);
		border: 1px solid var(--border);
		padding: 0.3rem 0.6rem;
		transition: border-color 0.15s, color 0.15s;
	}
	.theme-toggle:hover {
		border-color: var(--text);
		color: var(--text);
	}
	.about-content {
		display: flex;
		flex-direction: column;
		gap: 0.85rem;
	}
	.about-logo {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--text);
		letter-spacing: -0.02em;
	}
	.about-divider {
		height: 1px;
		background: var(--border);
	}
	.about-row {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: 1rem;
		font-size: 0.8rem;
	}
	.about-key {
		color: var(--text-muted);
		flex-shrink: 0;
	}
	.about-val {
		color: var(--text);
		text-align: right;
	}
	.about-link {
		color: var(--text);
		text-decoration: underline;
	}
	.about-link:hover {
		color: var(--accent);
	}
	.about-changelog {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.about-changes {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		margin-top: 0.35rem;
	}
	.change-entry {
		display: flex;
		gap: 0.75rem;
		font-size: 0.75rem;
	}
	.change-ver {
		color: var(--text-muted);
		flex-shrink: 0;
		width: 2.5rem;
	}
	.change-desc {
		color: var(--text);
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
</style>
