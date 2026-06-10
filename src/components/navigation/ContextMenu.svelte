<script lang="ts">
  import { tick } from 'svelte'

  let {
    trigger,
    children,
  }: {
    trigger?: () => any
    children?: () => any
  } = $props()

  let open = $state(false)
  let x = $state(0)
  let y = $state(0)
  let menuEl: HTMLDivElement | null = $state(null)
  let triggerEl: HTMLDivElement | null = $state(null)

  function openMenu(clientX: number, clientY: number) {
    x = clientX
    y = clientY
    open = true
    tick().then(() => {
      if (!menuEl) return
      const rect = menuEl.getBoundingClientRect()
      if (rect.right > window.innerWidth) x = window.innerWidth - rect.width - 4
      if (rect.bottom > window.innerHeight) y = window.innerHeight - rect.height - 4
      if (x < 0) x = 4
      if (y < 0) y = 4
      menuEl.querySelector<HTMLElement>('button, [href], [tabindex]:not([tabindex="-1"])')?.focus()
    })
  }

  function onContextMenu(e: MouseEvent) {
    e.preventDefault()
    openMenu(e.clientX, e.clientY)
  }

  function onKeyDown(e: KeyboardEvent) {
    if (e.key === 'ContextMenu' || (e.shiftKey && e.key === 'F10')) {
      e.preventDefault()
      const rect = triggerEl!.getBoundingClientRect()
      openMenu(rect.left, rect.bottom)
    }
  }

  function close() {
    open = false
    ;(triggerEl?.querySelector('button, [href], [tabindex]:not([tabindex="-1"])') as HTMLElement)?.focus()
  }

  $effect(() => {
    if (!open) return
    function onClick(e: MouseEvent) {
      if (menuEl && !menuEl.contains(e.target as Node)) close()
    }
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') close()
    }
    function onScroll() { close() }
    document.addEventListener('click', onClick)
    document.addEventListener('keydown', onKey)
    document.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      document.removeEventListener('click', onClick)
      document.removeEventListener('keydown', onKey)
      document.removeEventListener('scroll', onScroll)
    }
  })
</script>

<div
  class="trigger"
  bind:this={triggerEl}
  oncontextmenu={onContextMenu}
  onkeydown={onKeyDown}
  role="presentation"
>
  {@render trigger?.()}
</div>

{#if open}
  <div class="backdrop" onclick={close} oncontextmenu={(e: MouseEvent) => { e.preventDefault(); close() }} role="presentation"></div>
  <div class="menu" bind:this={menuEl} style="left: {x}px; top: {y}px" role="menu">
    {@render children?.()}
  </div>
{/if}

<style>
  .trigger {
    display: inline-flex;
  }

  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 998;
  }

  .menu {
    position: fixed;
    z-index: 999;
    min-width: 10rem;
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 0.25rem 0;
    display: flex;
    flex-direction: column;
    animation: menu-in 0.12s ease-out;
    transform-origin: top left;
  }
  @keyframes menu-in {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
  }
</style>
