interface OscConfig {
  lineCount: number
  opacity: number
  color: string
  amplitude: number
  frequency: number
  speed: number
}

export function createOscillator(cfg: OscConfig) {
  let time = 0

  function tick(ctx: CanvasRenderingContext2D, w: number, h: number) {
    time += 0.008

    for (let i = 0; i < cfg.lineCount; i++) {
      const baseY = h * (0.2 + (i / (cfg.lineCount - 1 || 1)) * 0.6)
      const amp = cfg.amplitude * (1 + i * 0.6)
      const freq = cfg.frequency * (1 + i * 0.25)
      const spd = cfg.speed * (1 + i * 0.15)
      const phase = i * 1.2

      ctx.beginPath()
      ctx.strokeStyle = `rgba(${cfg.color}, ${cfg.opacity * (1 + i * 0.2)})`
      ctx.lineWidth = 1

      let started = false
      for (let x = 0; x <= w; x += 1) {
        const y = baseY
          + Math.sin(x * freq + time * spd + phase) * amp
          + Math.sin(x * freq * 2.3 + time * spd * 0.6 + phase) * amp * 0.35
          + Math.sin(x * freq * 0.5 + time * spd * 1.4 + phase) * amp * 0.2
        if (!started) {
          ctx.moveTo(x, y)
          started = true
        } else {
          ctx.lineTo(x, y)
        }
      }
      ctx.stroke()
    }
  }

  return { tick }
}
