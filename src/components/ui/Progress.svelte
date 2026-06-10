<script lang="ts">
  let {
    value = 0,
    max = 100,
    size = 'md',
    indeterminate = false,
    ...rest
  }: {
    value?: number
    max?: number
    size?: 'sm' | 'md' | 'lg'
    indeterminate?: boolean
    [key: string]: any
  } = $props()

  let pct = $derived(Math.min(Math.max(value / max, 0), 1) * 100)
</script>

<div class="progress progress-{size}" role="progressbar"
     aria-valuenow={indeterminate ? undefined : value}
     aria-valuemax={indeterminate ? undefined : max}
     aria-busy={indeterminate ? "true" : undefined}
     {...rest}>
  <div class="progress-bar" class:indeterminate style={indeterminate ? '' : "width: {pct}%;"}></div>
</div>

<style>
  .progress {
    background: var(--border);
    overflow: hidden;
  }
  .progress-sm { height: 0.25rem; }
  .progress-md { height: 0.5rem; }
  .progress-lg { height: 0.75rem; }
  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--text-muted), var(--text));
    background-size: 200% 100%;
    animation: progress-shimmer 2s linear infinite;
    transition: width 0.3s ease;
  }
  .progress-bar.indeterminate {
    width: 25%;
    animation: progress-indeterminate 1.5s ease-in-out infinite;
  }
  @keyframes progress-shimmer {
    from { background-position: 200% 0; }
    to { background-position: -200% 0; }
  }
  @keyframes progress-indeterminate {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(400%); }
  }
</style>
