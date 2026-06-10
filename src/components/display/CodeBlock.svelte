<script lang="ts">
  import { Copy, Check } from '@lucide/svelte'

  let {
    code,
    codeHtml,
    lang = 'Svelte',
  }: {
    code: string
    codeHtml: string
    lang?: string
  } = $props()

  let copied = $state(false)

  function handleCopy() {
    navigator.clipboard.writeText(code)
    copied = true
    setTimeout(() => copied = false, 1500)
  }
</script>

<div class="code-block">
  <pre><code>{@html codeHtml}</code></pre>
  <div class="code-footer">
    <span class="code-lang">{lang}</span>
    <button class="copy-btn" onclick={handleCopy} aria-label="Copy code">
      {#if copied}
        <Check size={11} />
      {:else}
        <Copy size={11} />
      {/if}
    </button>
  </div>
</div>

<style>
  .code-block {
    border: 1px solid var(--border);
    background: var(--bg);
  }
  .code-block pre {
    padding: 0.75rem 1rem;
    overflow-x: auto;
    margin: 0;
  }
  .code-block code {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.5;
    color: var(--text-muted);
    white-space: pre;
  }
  .code-footer {
    display: flex;
    align-items: center;
    border-top: 1px solid var(--border);
    padding: 0.35rem 0.75rem;
    background: var(--bg);
  }
  .code-footer .code-lang {
    font-size: 0.65rem;
    color: var(--text-dim);
    font-family: 'Geist Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .copy-btn {
    all: unset;
    cursor: pointer;
    margin-left: auto;
    font-size: 0.65rem;
    font-family: 'Geist Mono', monospace;
    color: var(--text-muted);
    padding: 0.2rem 0.4rem;
    transition: color 0.15s;
    display: flex;
    align-items: center;
  }
  .copy-btn:hover {
    color: var(--text);
  }
  .copy-btn:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: 2px;
  }
  :global(.hl-tag) { color: var(--text); }
  :global(.hl-attr) { color: var(--text-muted); }
  :global(.hl-string) { color: var(--text-muted); }
  :global(.hl-punct) { color: var(--text-dim); }
</style>
