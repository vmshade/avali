<script lang="ts">
  let {
    label = '',
    value = $bindable(''),
    placeholder = '',
    disabled = false,
    options = [],
    id = '',
    onchange,
    ...rest
  }: {
    label?: string
    value?: string
    placeholder?: string
    disabled?: boolean
    options?: { value: string; label: string }[]
    id?: string
    onchange?: (e: Event) => void
    [key: string]: any
  } = $props()

  let selectId = $derived(id || `select-${label.toLowerCase().replace(/\s+/g, '-')}-${Math.random().toString(36).slice(2, 8)}`)
</script>

<div class="select-wrap">
  {#if label}
    <label class="select-label" for={selectId}>{label}</label>
  {/if}
  <div class="select-box">
    <select {value} {disabled} {onchange} class="select" id={selectId} {...rest}>
      {#if placeholder}
        <option value="" disabled>{placeholder}</option>
      {/if}
      {#each options as opt}
        <option value={opt.value}>{opt.label}</option>
      {/each}
    </select>
  </div>
</div>

<style>
  .select-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .select-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-muted);
  }
  .select-box {
    position: relative;
  }
  .select-box::after {
    content: '';
    position: absolute;
    right: 0.65rem;
    top: 50%;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid var(--text-muted);
    pointer-events: none;
  }
  .select {
    font-family: inherit;
    font-size: 0.875rem;
    padding: 0.5rem 2rem 0.5rem 0.75rem;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    outline: none;
    width: 100%;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    cursor: pointer;
    transition: border-color 0.15s;
  }
  .select:focus {
    border-color: var(--text);
  }
  .select:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: 1px;
  }
  .select:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
</style>
