<script lang="ts">
  let {
    animation = 'fade-up',
    delay = 0,
    duration = 0.5,
    children,
  }: {
    animation?: 'fade-up' | 'fade-in' | 'slide-up'
    delay?: number
    duration?: number
    children?: () => any
  } = $props()
</script>

<div
  class="entrance entr-{animation}"
  style="animation-delay: {delay}s; animation-duration: {duration}s;"
  role="presentation"
>
  {@render children?.()}
</div>

<style>
  .entrance {
    animation-fill-mode: both;
  }

  .entr-fade-up {
    animation-name: e-fade-up;
  }
  @keyframes e-fade-up {
    from { opacity: 0; transform: translateY(1.5rem); filter: blur(4px); }
    to   { opacity: 1; transform: translateY(0); filter: blur(0); }
  }

  .entr-fade-in {
    animation-name: e-fade-in;
  }
  @keyframes e-fade-in {
    from { opacity: 0; filter: blur(4px); }
    to   { opacity: 1; filter: blur(0); }
  }

  .entr-slide-up {
    animation-name: e-slide-up;
  }
  @keyframes e-slide-up {
    from { opacity: 0; transform: translateY(2rem); filter: blur(4px); }
    to   { opacity: 1; transform: translateY(0); filter: blur(0); }
  }
</style>
