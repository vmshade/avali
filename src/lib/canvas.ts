export function mountCanvas(
  canvas: HTMLCanvasElement,
  draw: (ctx: CanvasRenderingContext2D, w: number, h: number) => void
): () => void {
  const ctx = canvas.getContext('2d')!
  let animId: number
  let w = 0
  let h = 0

  function resize() {
    const parent = canvas.parentElement
    if (!parent) return
    w = parent.offsetWidth
    h = parent.offsetHeight
    const dpr = devicePixelRatio
    canvas.width = w * dpr
    canvas.height = h * dpr
  }

  function animate() {
    animId = requestAnimationFrame(animate)
    if (!w || !h) return
    ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0)
    ctx.clearRect(0, 0, w, h)
    draw(ctx, w, h)
  }

  resize()
  animate()

  const ro = new ResizeObserver(resize)
  ro.observe(canvas.parentElement!)

  return () => {
    cancelAnimationFrame(animId)
    ro.disconnect()
  }
}
