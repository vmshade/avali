<script lang="ts">
  let { children, ...rest }: { children?: () => any; [key: string]: any } = $props()
</script>

<kbd class="kbd" {...rest}>
  {@render children?.()}
</kbd>

<style>
  .kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: inherit;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.15em 0.4em;
    background: var(--surface);
    border: 1px solid var(--border);
    border-bottom-width: 2px;
    color: var(--text-muted);
    line-height: 1.2;
    min-width: 1.4em;
  }
</style>
