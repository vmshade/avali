<script lang="ts">
  let {
    tabs = [],
    activeTab = '',
    onTabChange,
    children,
    ...rest
  }: {
    tabs?: { id: string; label: string }[]
    activeTab?: string
    onTabChange?: (id: string) => void
    children?: () => any
    [key: string]: any
  } = $props()

  let active = $state('')

  $effect(() => {
    if (activeTab) {
      active = activeTab
    } else if (tabs.length > 0 && !active) {
      active = tabs[0].id
    }
  })

  let tablistEl: HTMLDivElement

  function select(id: string) {
    active = id
    onTabChange?.(id)
  }

  function onKeyDown(e: KeyboardEvent) {
    const idx = tabs.findIndex((t) => t.id === active)
    if (idx < 0) return
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault()
      const next = (idx + 1) % tabs.length
      select(tabs[next].id)
      focusTab(next)
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault()
      const prev = (idx - 1 + tabs.length) % tabs.length
      select(tabs[prev].id)
      focusTab(prev)
    } else if (e.key === 'Home') {
      e.preventDefault()
      select(tabs[0].id)
      focusTab(0)
    } else if (e.key === 'End') {
      e.preventDefault()
      select(tabs[tabs.length - 1].id)
      focusTab(tabs.length - 1)
    }
  }

  function focusTab(idx: number) {
    const btn = tablistEl?.querySelector<HTMLButtonElement>(`[data-tab-id="${tabs[idx].id}"]`)
    btn?.focus()
  }
</script>

<div class="tabs" {...rest}>
  <div class="tabs-header" role="tablist" tabindex="0" bind:this={tablistEl} onkeydown={onKeyDown}>
    {#each tabs as tab}
      <button
        type="button"
        role="tab"
        aria-selected={active === tab.id}
        data-tab-id={tab.id}
        class="tab-btn"
        class:tab-active={active === tab.id}
        onclick={() => select(tab.id)}
      >
        {tab.label}
      </button>
    {/each}
  </div>
  {#if children}
    <div role="tabpanel" class="tabs-content" aria-label={tabs.find((t) => t.id === active)?.label}>
      {@render children?.()}
    </div>
  {/if}
</div>

<style>
  .tabs {
    display: flex;
    flex-direction: column;
    gap: 0;
  }
  .tabs-header {
    display: flex;
    border-bottom: 1px solid var(--border);
  }
  .tab-btn {
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    background: transparent;
    border: none;
    border-bottom: 1px solid transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: color 0.15s, border-color 0.15s;
    margin-bottom: -1px;
  }
  .tab-btn:hover {
    color: var(--text);
  }
  .tab-btn:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: -1px;
  }
  .tab-active {
    color: var(--text);
    border-bottom-color: var(--text);
  }
  .tabs-content {
    padding-top: 1rem;
  }
</style>
