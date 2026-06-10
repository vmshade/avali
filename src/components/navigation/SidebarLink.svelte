<script lang="ts">
  import { getContext } from 'svelte'

  let {
    href,
    active = false,
    icon,
    children,
    onclick,
    ...rest
  }: {
    href?: string
    active?: boolean
    icon?: () => any
    children?: () => any
    onclick?: (e: MouseEvent) => void
    [key: string]: any
  } = $props()

  let getExpanded = getContext<() => boolean>('sidebar-expanded')
  let closeSidebar = getContext<() => void>('sidebar-close')

  function handleClick(e: MouseEvent) {
    closeSidebar?.()
    onclick?.(e)
  }
</script>

<a class="sidelink" class:active {href} class:collapsed={!getExpanded?.()} onclick={handleClick} {...rest}>
  {#if icon}
    <span class="sidelink-icon">{@render icon?.()}</span>
  {/if}
  <span class="sidelink-label" class:hidden={!getExpanded?.()}>{@render children?.()}</span>
</a>

<style>
  .sidelink {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.15s, background 0.15s;
  }
  .sidelink:hover {
    color: var(--text);
    background: var(--surface-hover);
  }
  .sidelink.active {
    color: var(--text);
    background: var(--surface-hover);
  }

  .sidelink.collapsed {
    padding: 0.55rem 0;
    justify-content: center;
    gap: 0;
    background: none;
  }
  .sidelink.collapsed:hover,
  .sidelink.collapsed.active {
    background: none;
  }

  .sidelink-icon {
    display: inline-flex;
    width: 1rem;
    height: 1rem;
    flex-shrink: 0;
  }
  .sidelink-icon > :global(svg) {
    width: 100%;
    height: 100%;
  }

  .sidelink-label {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .sidelink-label.hidden {
    display: none;
  }
</style>
