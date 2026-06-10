export function createCrosshair(color: string) {
  let sx = -1
  let sy = -1
  let tx = 0.5
  let ty = 0.5
  let w = 0
  let h = 0

  function setTarget(x: number, y: number) {
    tx = x; ty = y
  }

  function tick(ctx: CanvasRenderingContext2D, cw: number, ch: number) {
    w = cw; h = ch
    const cx = tx * w
    const cy = ty * h

    if (sx < 0) { sx = cx; sy = cy }

    sx += (cx - sx) * 0.25
    sy += (cy - sy) * 0.25

    ctx.strokeStyle = `rgba(${color}, 0.12)`
    ctx.lineWidth = 1

    const gap = 6

    ctx.beginPath()
    ctx.moveTo(0, sy)
    ctx.lineTo(sx - gap, sy)
    ctx.moveTo(sx + gap, sy)
    ctx.lineTo(w, sy)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(sx, 0)
    ctx.lineTo(sx, sy - gap)
    ctx.moveTo(sx, sy + gap)
    ctx.lineTo(sx, h)
    ctx.stroke()

    ctx.beginPath()
    ctx.arc(sx, sy, 2, 0, Math.PI * 2)
    ctx.stroke()
  }

  return { setTarget, tick }
}
