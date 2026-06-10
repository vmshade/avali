<script lang="ts">
  import { onMount } from 'svelte'
  import { mountCanvas } from '../../../lib/canvas.js'
  import { createCrosshair } from './logic.js'

  let {
    mouseX = 0.5,
    mouseY = 0.5,
    color = '255, 255, 255',
  }: {
    mouseX?: number
    mouseY?: number
    color?: string
  } = $props()

  let canvas: HTMLCanvasElement
  let crosshair: ReturnType<typeof createCrosshair>

  $effect(() => {
    crosshair?.setTarget(mouseX, mouseY)
  })

  onMount(() => {
    crosshair = createCrosshair(color)
    const cleanup = mountCanvas(canvas, (ctx, w, h) => {
      crosshair?.tick(ctx, w, h)
    })
    return cleanup
  })
</script>

<canvas
  bind:this={canvas}
  style="display: block; width: 100%; height: 100%; pointer-events: none;"
  aria-hidden="true"
></canvas>
