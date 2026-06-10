<script>
  let { size = 'md', muted = false, dim = false, as = 'p', children, ...rest } = $props()
</script>

{#if as === 'p'}
  <p class="text txt-{size}" class:muted class:dim {...rest}>{@render children?.()}</p>
{:else if as === 'span'}
  <span class="text txt-{size}" class:muted class:dim {...rest}>{@render children?.()}</span>
{:else if as === 'div'}
  <div class="text txt-{size}" class:muted class:dim {...rest}>{@render children?.()}</div>
{/if}

<style>
  .text {
    color: var(--text);
    line-height: 1.6;
  }
  .muted { color: var(--text-muted); }
  .dim { color: var(--text-dim); }

  .txt-sm { font-size: 0.75rem; }
  .txt-md { font-size: 0.875rem; }
  .txt-lg { font-size: 1rem; }
</style>
