<script lang="ts">
  let {
    size = 'lg',
    opacity = 0.08,
  }: {
    size?: 'sm' | 'md' | 'lg'
    opacity?: number
  } = $props()
</script>

<pre class="brackets brackets-{size}" style="opacity: {opacity};" role="presentation"><code>{`{  }`}</code></pre>

<style>
  .brackets {
    font-family: 'Geist Mono', monospace;
    font-weight: 700;
    line-height: 1;
    user-select: none;
    color: var(--text);
  }
  .brackets-sm { font-size: 2rem; }
  .brackets-md { font-size: 4rem; }
  .brackets-lg { font-size: 7rem; }
</style>
