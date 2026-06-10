<script lang="ts">
  import { Pin, PinOff, ChevronLeft, ChevronRight } from '@lucide/svelte'
  import { setContext } from 'svelte'

  let {
    children,
    topOffset = '0px',
  }: {
    children?: () => any
    topOffset?: string
  } = $props()

  let pinned = $state(false)
  let hovered = $state(false)
  let isMobile = $state(false)

  let expanded = $derived(pinned || hovered)

  setContext('sidebar-expanded', () => expanded)
  setContext('sidebar-close', () => { pinned = false })

  $effect(() => {
    const mq = window.matchMedia('(max-width: 768px)')
    isMobile = mq.matches
    const onChange = () => isMobile = mq.matches
    mq.addEventListener('change', onChange)
    return () => mq.removeEventListener('change', onChange)
  })

  function onToggle() {
    pinned = !pinned
  }
</script>

<aside
  class="sidebar"
  class:expanded
  class:pinned
  onmouseenter={() => { if (!isMobile) hovered = true }}
  onmouseleave={() => { if (!isMobile) hovered = false }}
  style="--sidebar-top: {topOffset}; --sidebar-height: calc(100vh - {topOffset});"
>
  <button class="toggle" onclick={onToggle} aria-expanded={expanded} aria-label={pinned ? (isMobile ? 'Close sidebar' : 'Unpin sidebar') : (isMobile ? 'Open sidebar' : 'Pin sidebar')}>
    {#if isMobile}
      {#if pinned}
        <ChevronLeft size={14} />
      {:else}
        <ChevronRight size={14} />
      {/if}
    {:else}
      {#if pinned}
        <PinOff size={14} />
      {:else}
        <Pin size={14} />
      {/if}
    {/if}
  </button>
  <div class="sidebar-content">
    {@render children?.()}
  </div>
</aside>
{#if expanded}
  <div class="sidebar-backdrop" onclick={() => pinned = false} role="presentation"></div>
{/if}

<style>
  .sidebar {
    position: sticky;
    top: var(--sidebar-top, 0px);
    height: var(--sidebar-height, 100vh);
    display: flex;
    flex-direction: column;
    background: var(--bg);
    border-right: 1px solid var(--border);
    width: 2.5rem;
    transition: width 0.2s ease;
    flex-shrink: 0;
    z-index: 50;
  }

  .sidebar-content {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    flex: 1;
    gap: 0.125rem;
    overflow-y: auto;
  }

  .toggle {
    all: unset;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 2rem;
    flex-shrink: 0;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
  }
  .toggle:hover {
    color: var(--text);
    background: var(--surface-hover);
  }
  .toggle:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: -1px;
  }

  .sidebar-backdrop {
    display: none;
  }

  @media (min-width: 769px) {
    .sidebar.expanded {
      width: 14rem;
    }
  }

  @media (max-width: 768px) {
    .sidebar.expanded {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100dvh;
      z-index: 200;
      border-right: none;
    }
    .sidebar:not(.expanded) {
      width: 0;
      border-right: none;
      overflow: hidden;
    }
    .sidebar:not(.expanded) .toggle {
      position: fixed;
      left: 0;
      top: var(--sidebar-top, 0px);
      width: 2.5rem;
      border-right: 1px solid var(--border);
      background: var(--bg);
      z-index: 50;
    }
    .sidebar-backdrop {
      display: block;
      position: fixed;
      inset: 0;
      z-index: 199;
      background: rgba(0, 0, 0, 0.5);
    }
  }
</style>
