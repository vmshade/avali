<script lang="ts">
  let {
    threshold = 0.15,
    animation = 'fade-up',
    once = true,
    children,
  }: {
    threshold?: number
    animation?: 'fade-up' | 'fade-in' | 'slide-up'
    once?: boolean
    children?: () => any
  } = $props()

  let el: HTMLDivElement | null = $state(null)
  let visible = $state(false)

  $effect(() => {
    const node = el
    if (!node) return
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            visible = true
            if (once) observer.disconnect()
          } else if (!once) {
            visible = false
          }
        }
      },
      { threshold }
    )
    observer.observe(node)
    return () => observer.disconnect()
  })
</script>

<div
  bind:this={el}
  class="scroll-view scroll-{animation}"
  class:visible
  role="presentation"
>
  {@render children?.()}
</div>

<style>
  .scroll-view {
    transition: opacity 0.5s ease, transform 0.5s ease;
    height: 100%;
  }

  .scroll-fade-up {
    opacity: 0;
    transform: translateY(1.5rem);
  }
  .scroll-fade-up.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .scroll-fade-in {
    opacity: 0;
  }
  .scroll-fade-in.visible {
    opacity: 1;
  }

  .scroll-slide-up {
    opacity: 0;
    transform: translateY(2rem);
  }
  .scroll-slide-up.visible {
    opacity: 1;
    transform: translateY(0);
  }
</style>
