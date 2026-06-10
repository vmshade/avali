<script lang="ts">
  import { onMount } from 'svelte'
  import { mountCanvas } from '../../../lib/canvas.js'
  import { createOscillator } from './logic.js'

  let {
    lineCount = 3,
    opacity = 0.06,
    color = '255, 255, 255',
    amplitude = 12,
    frequency = 0.015,
    speed = 0.4,
  }: {
    lineCount?: number
    opacity?: number
    color?: string
    amplitude?: number
    frequency?: number
    speed?: number
  } = $props()

  let canvas: HTMLCanvasElement
  let osc: ReturnType<typeof createOscillator>

  onMount(() => {
    osc = createOscillator({ lineCount, opacity, color, amplitude, frequency, speed })
    const cleanup = mountCanvas(canvas, (ctx, w, h) => {
      osc?.tick(ctx, w, h)
    })
    return cleanup
  })
</script>

<canvas
  bind:this={canvas}
  style="display: block; width: 100%; height: 100%; pointer-events: none;"
  aria-hidden="true"
></canvas>
