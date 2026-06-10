<script>
  let { level = 1, weight = 600, children, ...rest } = $props()
</script>

{#if level === 1}
  <h1 class="h h1" style="font-weight: {weight}" {...rest}>{@render children?.()}</h1>
{:else if level === 2}
  <h2 class="h h2" style="font-weight: {weight}" {...rest}>{@render children?.()}</h2>
{:else if level === 3}
  <h3 class="h h3" style="font-weight: {weight}" {...rest}>{@render children?.()}</h3>
{:else if level === 4}
  <h4 class="h h4" style="font-weight: {weight}" {...rest}>{@render children?.()}</h4>
{:else if level === 5}
  <h5 class="h h5" style="font-weight: {weight}" {...rest}>{@render children?.()}</h5>
{:else if level === 6}
  <h6 class="h h6" style="font-weight: {weight}" {...rest}>{@render children?.()}</h6>
{/if}

<style>
  .h {
    color: var(--text);
    line-height: 1.3;
    margin: 0;
  }
  .h1 { font-size: 1.5rem; }
  .h2 { font-size: 1.25rem; }
  .h3 { font-size: 1.125rem; }
  .h4 { font-size: 1rem; }
  .h5 { font-size: 0.875rem; }
  .h6 { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
