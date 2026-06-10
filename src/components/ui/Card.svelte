<script>
  let { padding = true, children, ...rest } = $props()
</script>

<div class="card" class:card--pad={padding} {...rest}>
  {@render children?.()}
</div>

<style>
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
  }
  .card--pad {
    padding: 1.25rem;
  }
</style>
