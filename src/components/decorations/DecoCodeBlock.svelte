<script lang="ts">
  let {
    lines = 3,
    opacity = 0.12,
    activeLine = -1,
  }: {
    lines?: number
    opacity?: number
    activeLine?: number
  } = $props()
</script>

<div class="code-block" style="opacity: {opacity};" role="presentation">
  {#each Array(lines) as _, i}
    <div class="code-line" class:active={i === activeLine} style="width: {40 + ((i * 13 + 7) % 50)}%; animation-delay: {i * 0.4}s;"></div>
  {/each}
  <span class="cursor" class:active={activeLine >= 0}></span>
</div>

<style>
  .code-block {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;
    border: 1px solid var(--border);
    background: var(--surface);
  }
  .code-line {
    height: 0.5rem;
    background: var(--text-dim);
    animation: pulse-line 2.5s ease-in-out infinite;
  }
  .code-line.active {
    background: var(--text-muted);
    animation: none;
  }
  @keyframes pulse-line {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
  }
  .cursor {
    display: inline-block;
    width: 0.5rem;
    height: 0.75rem;
    background: var(--text-muted);
    animation: blink 1s step-end infinite;
    opacity: 0.5;
  }
  .cursor.active {
    opacity: 1;
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
</style>
