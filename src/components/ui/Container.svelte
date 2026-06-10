<script lang="ts">
  let {
    maxWidth = '64rem',
    padding = true,
    children,
    ...rest
  }: {
    maxWidth?: string
    padding?: boolean
    children?: () => any
    [key: string]: any
  } = $props()
</script>

<div class="container" class:pad={padding} style="max-width: {maxWidth}" {...rest}>
  {@render children?.()}
</div>

<style>
  .container {
    width: 100%;
    margin: 0 auto;
  }
  .pad {
    padding: 0 1.25rem;
  }
</style>
