<script lang="ts">
  let {
    href,
    active = false,
    children,
    ...rest
  }: {
    href?: string
    active?: boolean
    children?: () => any
    [key: string]: any
  } = $props()
</script>

<a class="navlink" class:active {href} {...rest}>
  {@render children?.()}
</a>

<style>
  .navlink {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-decoration: none;
    padding: 0.35rem 0.6rem;
    transition: color 0.15s, background 0.15s;
  }
  .navlink:hover {
    color: var(--text);
    background: var(--surface);
  }
  .navlink.active {
    color: var(--text);
    background: var(--surface);
  }
</style>
