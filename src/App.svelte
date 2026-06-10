<script lang="ts">
	import Heading from "./components/ui/Heading.svelte";
	import Input from "./components/form/Input.svelte";
	import Button from "./components/ui/Button.svelte";
	import Modal from "./components/overlay/Modal.svelte";
	import Text from "./components/ui/Text.svelte";
	import Progress from "./components/ui/Progress.svelte";

	import { Video, Volume2, VolumeOff } from "@lucide/svelte";

	let modalOpen: boolean = $state(false);
	let inputValue: string = $state("");
	let buttonState: "idle" | "downloading" | "error" = $state("idle");
	let selectedFormat: string = $state("video+audio");

	let modalTitle: string = $state("oops!!!");
	let modalText: string = $state("something went wrong!");

	let qualityModalOpen: boolean = $state(false);
	let availableQualities: number[] = $state([]);
	let qualityPromiseResolve: ((h: number | null) => void) | null = null;

	let errorTimer: ReturnType<typeof setTimeout> | null = null;

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

	async function downloadVideo() {
		if (inputValue == "") {
			openModal("hold up!!!", "you need to enter a link, silly!");
			return;
		}

		if (errorTimer) clearTimeout(errorTimer);
		buttonState = "downloading";

		try {
			let selectedHeight: number | null = null;
			if (selectedFormat !== "audio") {
				try {
					const qualRes = await fetch(
						`/api/qualities?url=${encodeURIComponent(inputValue.trim())}`,
					);
					if (qualRes.ok) {
						const data: { qualities: number[] } =
							await qualRes.json();
						if (data.qualities?.length) {
							const h = await showQualityModal(data.qualities);
							if (h === null) {
								buttonState = "idle";
								return;
							}
							selectedHeight = h;
						}
					}
				} catch {
					console.log("failed to fetch quality options!");
				}
			}

			const res = await fetch("/api/download", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					url: inputValue.trim(),
					format: selectedFormat,
					quality: selectedHeight,
				}),
			});

			if (!res.ok) {
				const err = await res.json();
				openModal("oops!!!", err.error ?? "something went wrong!");
				buttonState = "error";
				errorTimer = setTimeout(() => {
					buttonState = "idle";
				}, 3000);
				return;
			}

			const blob = await res.blob();
			const header = res.headers.get("Content-Disposition");
			const match = header?.match(/filename="?(.+?)"?$/);
			const filename =
				match?.[1] ?? `video.${blob.type.split("/")[1] ?? "mp4"}`;

			const url = URL.createObjectURL(blob);
			const a = document.createElement("a");
			a.href = url;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);

			buttonState = "idle";
		} catch {
			buttonState = "error";
			errorTimer = setTimeout(() => {
				buttonState = "idle";
			}, 3000);
			openModal("oops!!!", "could not reach the server");
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
		width: 500px;
	}
	.flex1 {
		flex: 1;
	}
	.options {
		display: flex;
		gap: 10px;
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
		width: 500px;
		margin-bottom: 15px;
	}
	.quality-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}
</style>
