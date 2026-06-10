<script lang="ts">
  let {
    checked = $bindable(false),
    disabled = false,
    label = '',
    onchange,
    ...rest
  }: {
    checked?: boolean
    disabled?: boolean
    label?: string
    onchange?: (e: Event) => void
    [key: string]: any
  } = $props()
</script>

<label class="toggle-wrap" class:toggle-disabled={disabled}>
  <input type="checkbox" role="switch" {checked} {disabled} {onchange} class="toggle-input" {...rest} />
  <span class="toggle-track">
    <span class="toggle-knob"></span>
  </span>
  {#if label}
    <span class="toggle-label">{label}</span>
  {/if}
</label>

<style>
  .toggle-wrap {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
  }
  .toggle-disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  .toggle-input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }
  .toggle-track {
    width: 2rem;
    height: 1.125rem;
    background: var(--border);
    border: 1px solid var(--border-strong);
    position: relative;
    transition: background 0.15s, outline 0.15s;
    flex-shrink: 0;
  }
  .toggle-input:checked + .toggle-track {
    background: var(--text);
    border-color: var(--text);
  }
  .toggle-input:focus-visible + .toggle-track {
    outline: 1px solid var(--text);
    outline-offset: 2px;
  }
  .toggle-knob {
    position: absolute;
    top: 1px;
    left: 1px;
    width: calc(1.125rem - 4px);
    height: calc(1.125rem - 4px);
    background: var(--bg);
    transition: transform 0.15s;
  }
  .toggle-input:checked + .toggle-track .toggle-knob {
    transform: translateX(calc(2rem - 1.125rem));
  }
  .toggle-label {
    font-size: 0.875rem;
    color: var(--text);
  }
</style>
