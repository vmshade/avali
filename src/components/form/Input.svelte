<script lang="ts">
  let {
    label = '',
    placeholder = '',
    value = $bindable(''),
    type = 'text',
    disabled = false,
    id = '',
    oninput,
    onchange,
    ...rest
  }: {
    label?: string
    placeholder?: string
    value?: string
    type?: string
    disabled?: boolean
    id?: string
    oninput?: (e: Event) => void
    onchange?: (e: Event) => void
    [key: string]: any
  } = $props()

  let inputId = $derived(id || `input-${label.toLowerCase().replace(/\s+/g, '-')}-${Math.random().toString(36).slice(2, 8)}`)
</script>

<div class="input-wrap">
  {#if label}
    <label class="input-label" for={inputId}>{label}</label>
  {/if}
  <input {type} {placeholder} bind:value {disabled} {oninput} {onchange} class="input" id={inputId} {...rest} />
</div>

<style>
  .input-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .input-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-muted);
  }
  .input {
    font-family: inherit;
    font-size: 0.875rem;
    padding: 0.5rem 0.75rem;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    outline: none;
    transition: border-color 0.15s;
  }
  .input:focus {
    border-color: var(--text);
  }
  .input:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: 1px;
  }
  .input:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  .input::placeholder {
    color: var(--text-dim);
  }
</style>
