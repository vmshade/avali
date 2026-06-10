<script lang="ts">
  import { onMount } from 'svelte'
  import { mountCanvas } from '../../../lib/canvas.js'
  import { createField } from './logic.js'

  let {
    mouseX = 0.5,
    mouseY = 0.5,
    dotCount = 80,
    dotRadius = 1.2,
    magnetRadius = 0.3,
    maxDisplace = 50,
    maxOpacity = 0.8,
    baseOpacity = 0.15,
    color = '255, 255, 255',
  } = $props()

  let canvas: HTMLCanvasElement
  let field: ReturnType<typeof createField>

  $effect(() => {
    field?.setMouse(mouseX, mouseY)
  })

  onMount(() => {
    field = createField({
      dotCount, dotRadius, magnetRadius, maxDisplace,
      maxOpacity, baseOpacity, color
    })
    const cleanup = mountCanvas(canvas, (ctx, w, h) => {
      field?.resize(w, h)
      field?.draw(ctx, w, h)
    })
    return cleanup
  })
</script>

<canvas
  bind:this={canvas}
  style="display: block; width: 100%; height: 100%; pointer-events: none;"
  aria-hidden="true"
></canvas>
