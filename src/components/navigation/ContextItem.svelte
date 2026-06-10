<script lang="ts">
  let {
    onclick,
    disabled = false,
    children,
  }: {
    onclick?: () => void
    disabled?: boolean
    children?: () => any
  } = $props()

  function handleClick() {
    if (!disabled && onclick) onclick()
  }
</script>

<button
  class="item"
  {disabled}
  onclick={handleClick}
  role="menuitem"
>
  <span class="content">{@render children?.()}</span>
</button>

<style>
  .item {
    all: unset;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.75rem;
    font-family: inherit;
    font-size: 0.8rem;
    color: var(--text);
    cursor: pointer;
  }
  .item:hover:not(:disabled) {
    background: var(--surface-hover);
  }
  .item:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: -1px;
  }
  .item:disabled {
    color: var(--text-dim);
    cursor: not-allowed;
  }

  .content {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
  }
</style>
