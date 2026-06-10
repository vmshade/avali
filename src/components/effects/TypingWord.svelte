<script lang="ts">
  import { onMount } from 'svelte'

  let {
    words = ['reactive'],
    typeSpeed = 80,
    deleteSpeed = 40,
    pauseAfterType = 2000,
    pauseAfterDelete = 300,
  }: {
    words?: string[]
    typeSpeed?: number
    deleteSpeed?: number
    pauseAfterType?: number
    pauseAfterDelete?: number
  } = $props()

  let display = $state('')

  onMount(() => {
    let cancelled = false
    let wordIdx = 0
    let charIdx = 0
    let isDeleting = false

    function tick() {
      if (cancelled) return
      const current = words[wordIdx % words.length]

      if (!isDeleting) {
        if (charIdx < current.length) {
          charIdx++
          display = current.slice(0, charIdx)
          setTimeout(tick, typeSpeed)
        } else {
          isDeleting = true
          setTimeout(tick, pauseAfterType)
        }
      } else {
        if (charIdx > 0) {
          charIdx--
          display = current.slice(0, charIdx)
          setTimeout(tick, deleteSpeed)
        } else {
          isDeleting = false
          wordIdx++
          setTimeout(tick, pauseAfterDelete)
        }
      }
    }

    const timer = setTimeout(tick, pauseAfterDelete)
    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  })
</script>

<span class="typing">
  {display}<span class="cursor"></span>
</span>

<style>
  .cursor {
    display: inline-block;
    width: 1px;
    height: 1em;
    background: var(--text-muted);
    vertical-align: middle;
    margin-left: 0.05em;
    animation: blink 0.6s step-end infinite;
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
</style>
