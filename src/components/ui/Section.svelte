<script lang="ts">
  let {
    heading,
    description,
    headingLevel = 2,
    children,
    ...rest
  }: {
    heading?: string
    description?: string
    headingLevel?: number
    children?: () => any
    [key: string]: any
  } = $props()
</script>

<section class="section" {...rest}>
  {#if heading}
    <h2 class="section-heading" style="font-size: {headingLevel === 1 ? '1.5rem' : headingLevel === 2 ? '1.25rem' : '1rem'}; font-weight: 600;">{heading}</h2>
  {/if}
  {#if description}
    <p class="section-desc">{description}</p>
  {/if}
  <div class="section-body">
    {@render children?.()}
  </div>
</section>

<style>
  .section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .section-heading {
    color: var(--text);
    line-height: 1.3;
    margin: 0;
  }
  .section-desc {
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin: 0;
  }
  .section-body {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
</style>
