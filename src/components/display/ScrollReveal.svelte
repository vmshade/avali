<script lang="ts">
  let {
    items = [],
    children,
  }: {
    items?: Array<() => any>
    children?: () => any
  } = $props()
</script>

<div class="scroll-reveal">
  {#if items.length > 0}
    {#each items as item, i}
      <div class="panel" style="z-index: {items.length - i}">
        {@render item()}
      </div>
    {/each}
  {:else}
    {@render children?.()}
  {/if}
</div>

<style>
  .scroll-reveal {
    position: relative;
  }

  .panel {
    position: sticky;
    top: 0;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .panel + .panel {
    border-top: 1px solid var(--border);
  }
</style>
