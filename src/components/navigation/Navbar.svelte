<script lang="ts">
  let {
    brand,
    children,
    ...rest
  }: {
    brand?: () => any
    children?: () => any
    [key: string]: any
  } = $props()
</script>

<nav class="navbar" {...rest}>
  <div class="navbar-inner">
    {#if brand}
      <div class="navbar-brand">{@render brand?.()}</div>
    {/if}
    <div class="navbar-links">
      {@render children?.()}
    </div>
  </div>
</nav>

<style>
  .navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: color-mix(in srgb, var(--bg) 90%, transparent);
    backdrop-filter: blur(6px);
  }
  .navbar::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(
      to right,
      var(--text) calc(var(--navbar-progress, 0) * 100%),
      var(--border) calc(var(--navbar-progress, 0) * 100%)
    );
  }
  .navbar-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 3rem;
    padding: 0 0.75rem;
  }
  .navbar-brand {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text);
  }
  .navbar-links {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
</style>
