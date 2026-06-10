<script lang="ts">
  let {
    variant: _variant = 'primary',
    size = 'md',
    icon = false,
    disabled = false,
    children,
    ...rest
  } = $props()

  let cls = $derived(['btn', `btn-${_variant}`, `btn-${size}`, icon ? 'btn-icon' : ''].filter(Boolean).join(' '))
</script>

<button class={cls} {disabled} {...rest}>
  {@render children?.()}
</button>

<style>
  .btn {
    font-family: inherit;
    font-weight: 500;
    cursor: pointer;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4em;
    line-height: 1;
    transition: background 0.15s, border-color 0.15s;
  }
  .btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .btn > :global(svg) {
    flex-shrink: 0;
  }

  .btn-sm { font-size: 0.75rem; padding: 0.3rem 0.6rem; }
  .btn-md { font-size: 0.875rem; padding: 0.5rem 1rem; }
  .btn-lg { font-size: 1rem; padding: 0.65rem 1.25rem; }

  .btn-icon { padding: 0; }
  .btn-icon.btn-sm { width: 1.75rem; height: 1.75rem; }
  .btn-icon.btn-md { width: 2.25rem; height: 2.25rem; }
  .btn-icon.btn-lg { width: 2.75rem; height: 2.75rem; }

  .btn-primary {
    background: var(--text);
    color: var(--bg);
    border-color: var(--text);
  }
  .btn-primary:hover:not(:disabled) {
    background: var(--accent);
    border-color: var(--accent);
  }

  .btn-secondary {
    background: var(--surface);
    border-color: var(--border);
  }
  .btn-secondary:hover:not(:disabled) {
    background: var(--surface-hover);
    border-color: var(--border-strong);
  }

  .btn-ghost {
    background: transparent;
    border-color: transparent;
    color: var(--text-muted);
  }
  .btn-ghost:hover:not(:disabled) {
    background: var(--surface);
    color: var(--text);
  }

  .btn-outline {
    background: transparent;
    border-color: var(--border);
    color: var(--text-muted);
  }
  .btn-outline:hover:not(:disabled) {
    border-color: var(--text);
    color: var(--text);
  }
</style>
