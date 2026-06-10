interface Dot {
  x: number; y: number
  bx: number; by: number
}

interface FieldConfig {
  dotCount: number
  dotRadius: number
  magnetRadius: number
  maxDisplace: number
  maxOpacity: number
  baseOpacity: number
  color: string
}

export function createField(cfg: FieldConfig) {
  let dots: Dot[] = []
  let mx = 0.5
  let my = 0.5
  let w = 0
  let h = 0

  function resize(nw: number, nh: number) {
    if (nw === w && nh === h) return
    w = nw; h = nh
    dots = []
    for (let i = 0; i < cfg.dotCount; i++) {
      const x = Math.random() * w
      const y = Math.random() * h
      dots.push({ x, y, bx: x, by: y })
    }
  }

  function setMouse(x: number, y: number) {
    mx = x; my = y
  }

  function draw(ctx: CanvasRenderingContext2D, cw: number, ch: number) {
    const cx = mx * cw
    const cy = my * ch
    const maxDist = cfg.magnetRadius * cw

    for (const dot of dots) {
      const dx = cx - dot.bx
      const dy = cy - dot.by
      const dist = Math.sqrt(dx * dx + dy * dy)

      if (dist < maxDist && mx >= 0 && my >= 0) {
        const t = 1 - dist / maxDist
        const force = t * t
        const d = force * cfg.maxDisplace
        const a = Math.atan2(dy, dx)
        dot.x = dot.bx + Math.cos(a) * d
        dot.y = dot.by + Math.sin(a) * d
      } else {
        dot.x += (dot.bx - dot.x) * 0.04
        dot.y += (dot.by - dot.y) * 0.04
      }

      const tx = Math.min(dist / maxDist, 1)
      const opacity = cfg.baseOpacity + (1 - tx) * (1 - tx) * cfg.maxOpacity

      ctx.beginPath()
      ctx.arc(dot.x, dot.y, cfg.dotRadius, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(${cfg.color}, ${opacity})`
      ctx.shadowBlur = 4
      ctx.shadowColor = `rgba(${cfg.color}, ${opacity * 0.5})`
      ctx.fill()
    }
    ctx.shadowBlur = 0
  }

  return { resize, setMouse, draw }
}
