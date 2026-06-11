<script lang="ts">
  import { tick } from 'svelte'

  let {
    open = $bindable(false),
    title = '',
    size = 'md',
    children,
    footer,
    onclose,
    ...rest
  }: {
    open?: boolean
    title?: string
    size?: 'sm' | 'md' | 'lg'
    children?: () => any
    footer?: () => any
    onclose?: () => void
    [key: string]: any
  } = $props()

  let dialogEl: HTMLDivElement = $state(undefined!)
  let previousFocus: HTMLElement | null = null

  function close() {
    open = false
    onclose?.()
  }

  $effect(() => {
    if (!open) return
    previousFocus = document.activeElement as HTMLElement | null

    tick().then(() => {
      const first = dialogEl?.querySelector<HTMLElement>('[autofocus], button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
      first?.focus()
    })

    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') close()
      if (e.key === 'Tab') trapFocus(e)
    }
    function trapFocus(e: KeyboardEvent) {
      if (!dialogEl) return
      const focusable = dialogEl.querySelectorAll<HTMLElement>('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
      if (focusable.length === 0) return
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault()
        last.focus()
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault()
        first.focus()
      }
    }
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('keydown', onKey)
      previousFocus?.focus()
    }
  })
</script>

{#if open}
  <div class="modal-overlay" onclick={close} role="presentation"></div>
  <div class="modal modal-{size}" role="dialog" aria-modal="true" bind:this={dialogEl} {...rest}>
    {#if title}
      <div class="modal-header">
        <span class="modal-title">{title}</span>
        <button class="modal-close" onclick={close} aria-label="Close">&times;</button>
      </div>
    {/if}
    <div class="modal-body">
      {@render children?.()}
    </div>
    {#if footer}
      <div class="modal-footer">
        {@render footer?.()}
      </div>
    {/if}
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 500;
    background: rgba(0, 0, 0, 0.6);
    animation: overlay-in 0.15s ease-out;
  }
  @keyframes overlay-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 501;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    max-height: 80dvh;
    animation: modal-in 0.15s ease-out;
  }
  @keyframes modal-in {
    from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  }
	.modal-sm { width: min(20rem, calc(100vw - 2rem)); }
	.modal-md { width: min(28rem, calc(100vw - 2rem)); }
	.modal-lg { width: min(36rem, calc(100vw - 2rem)); }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem 0.75rem;
    border-bottom: 1px solid var(--border);
  }
  .modal-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
  }
  .modal-close {
    all: unset;
    cursor: pointer;
    font-size: 1.25rem;
    line-height: 1;
    color: var(--text-muted);
    transition: color 0.15s;
  }
  .modal-close:hover {
    color: var(--text);
  }
  .modal-close:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: 2px;
  }

  .modal-body {
    padding: 1.25rem;
    overflow-y: auto;
    flex: 1;
  }

  .modal-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem 1rem;
    border-top: 1px solid var(--border);
  }

	@media (max-width: 768px) {
		.modal {
			max-height: 90dvh;
			width: calc(100vw - 1rem) !important;
		}
		.modal-header {
			padding: 0.75rem 1rem 0.5rem;
		}
		.modal-body {
			padding: 1rem;
		}
		.modal-footer {
			flex-direction: column;
			padding: 0.5rem 1rem 0.75rem;
		}
		.modal-footer > :global(*) {
			width: 100%;
		}
	}
</style>
