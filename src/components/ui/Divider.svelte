<script lang="ts">
  let {
    axis = 'horizontal',
    label = '',
    ...rest
  }: {
    axis?: 'horizontal' | 'vertical'
    label?: string
    [key: string]: any
  } = $props()
</script>

{#if axis === 'horizontal'}
  <div class="divider divider-h" class:has-label={!!label} role="separator" {...rest}>
    {#if label}
      <span class="divider-label">{label}</span>
    {/if}
  </div>
{:else}
  <div class="divider divider-v" role="separator" {...rest}></div>
{/if}

<style>
  .divider-h {
    display: flex;
    align-items: center;
    width: 100%;
    height: 1px;
    background: var(--border);
  }
  .divider-h.has-label {
    background: none;
    border-top: 1px solid var(--border);
  }
  .divider-label {
    font-size: 0.7rem;
    font-weight: 500;
    color: var(--text-dim);
    padding: 0 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: transparent;
  }
  .divider-v {
    width: 1px;
    height: 100%;
    min-height: 1rem;
    background: var(--border);
    flex-shrink: 0;
  }
</style>
