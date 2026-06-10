<script lang="ts">
  let {
    size = 'md',
    axis = 'vertical',
    flex = false,
  }: {
    size?: 'sm' | 'md' | 'lg' | 'xl'
    axis?: 'vertical' | 'horizontal'
    flex?: boolean
  } = $props()
</script>

<div
  class="spacer spacer-{size} spacer-{axis}"
  class:spacer-flex={flex}
  role="presentation"
></div>

<style>
  .spacer-vertical.spacer-sm { height: 0.5rem; }
  .spacer-vertical.spacer-md { height: 1rem; }
  .spacer-vertical.spacer-lg { height: 2rem; }
  .spacer-vertical.spacer-xl { height: 4rem; }

  .spacer-horizontal.spacer-sm { width: 0.5rem; }
  .spacer-horizontal.spacer-md { width: 1rem; }
  .spacer-horizontal.spacer-lg { width: 2rem; }
  .spacer-horizontal.spacer-xl { width: 4rem; }

  .spacer-flex {
    flex: 1;
  }
  .spacer-flex.spacer-vertical {
    height: auto;
  }
  .spacer-flex.spacer-horizontal {
    width: auto;
  }
</style>
