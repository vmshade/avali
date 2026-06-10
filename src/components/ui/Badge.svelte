<script>
  let { variant = 'default', children, ...rest } = $props()
</script>

<span class="badge badge-{variant}" {...rest}>
  {@render children?.()}
</span>

<style>
  .badge {
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.15em 0.5em;
    border: 1px solid var(--border);
    display: inline-flex;
    align-items: center;
    gap: 0.3em;
  }

  .badge-default {
    background: var(--surface);
    color: var(--text-muted);
    border-color: var(--border);
  }

  .badge-primary {
    background: var(--text);
    color: var(--bg);
    border-color: var(--text);
  }

  .badge-outline {
    background: transparent;
    color: var(--text-muted);
    border-color: var(--border);
  }
</style>
