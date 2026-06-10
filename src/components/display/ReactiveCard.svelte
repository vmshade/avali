<script lang="ts">
  let {
    padding = true,
    children,
    ...rest
  }: {
    padding?: boolean
    children?: () => any
    [key: string]: any
  } = $props()

  let el: HTMLElement

  function onMove(e: PointerEvent) {
    const rect = el.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width) * 100
    const y = ((e.clientY - rect.top) / rect.height) * 100
    el.style.setProperty('--x', `${x}%`)
    el.style.setProperty('--y', `${y}%`)
  }
</script>

<div
  bind:this={el}
  class="r-card"
  class:r-card--pad={padding}
  onpointermove={onMove}
  {...rest}
>
  {@render children?.()}
</div>

<style>
  .r-card {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    height: 100%;
  }
  .r-card::before {
    content: '';
    position: absolute;
    inset: 0;
    padding: 1px;
    background: radial-gradient(15rem circle at var(--x, 50%) var(--y, 50%), var(--text-muted), transparent 60%);
    opacity: 0;
    transition: opacity 0.25s;
    pointer-events: none;
    -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    mask-composite: exclude;
  }
  .r-card:hover::before {
    opacity: 0.5;
  }
  .r-card--pad {
    padding: 1.25rem;
  }
</style>
