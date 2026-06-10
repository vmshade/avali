<script lang="ts">
  import { ChevronDown } from '@lucide/svelte'

  let {
    targetId = '',
    ...rest
  }: {
    targetId?: string
    [key: string]: any
  } = $props()

  function scrollTo() {
    if (targetId) {
      document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' })
    }
  }
</script>

<button type="button" class="scroll-hint" aria-label="Scroll to next section" onclick={scrollTo} {...rest}>
  <ChevronDown size={16} />
</button>

<style>
  .scroll-hint {
    all: unset;
    position: absolute;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    color: var(--text-muted);
    cursor: pointer;
    animation: scroll-bounce 2s ease-in-out infinite;
    transition: color 0.15s;
  }
  .scroll-hint:hover {
    color: var(--text);
  }
  .scroll-hint:focus-visible {
    outline: 1px solid var(--text);
    outline-offset: 2px;
  }
  @keyframes scroll-bounce {
    0%, 100% { transform: translateX(-50%) translateY(0); }
    50% { transform: translateX(-50%) translateY(0.4rem); }
  }
</style>
