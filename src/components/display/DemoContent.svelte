<script lang="ts">
  import { Plus, Minus, RotateCcw, User, Bell } from '@lucide/svelte'
  import Heading from '../ui/Heading.svelte'
  import Text from '../ui/Text.svelte'
  import Button from '../ui/Button.svelte'
  import Badge from '../ui/Badge.svelte'
  import Card from '../ui/Card.svelte'
  import Container from '../ui/Container.svelte'
  import Spacer from '../ui/Spacer.svelte'
  import CodeBlock from './CodeBlock.svelte'
  import ReactiveCard from './ReactiveCard.svelte'
  import ScrollView from './ScrollView.svelte'
  import ContextMenu from '../navigation/ContextMenu.svelte'
  import ContextItem from '../navigation/ContextItem.svelte'
  import Input from '../form/Input.svelte'
  import Toggle from '../form/Toggle.svelte'
  import Select from '../form/Select.svelte'
  import Progress from '../ui/Progress.svelte'
  import Tabs from '../navigation/Tabs.svelte'
  import Kbd from '../ui/Kbd.svelte'
  import Divider from '../ui/Divider.svelte'

  const codeText = `<Navbar>
  <NavbarLink href="/">Home</NavbarLink>
  <NavbarLink href="/docs">Docs</NavbarLink>
  <Button variant="primary" size="sm">
    Get started
  </Button>
</Navbar>`

  const codeHtml = `  <span class="hl-punct">&lt;</span><span class="hl-tag">Navbar</span><span class="hl-punct">&gt;</span>
    <span class="hl-punct">&lt;</span><span class="hl-tag">NavbarLink</span> <span class="hl-attr">href</span><span class="hl-punct">=</span><span class="hl-string">"/"</span><span class="hl-punct">&gt;</span>Home<span class="hl-punct">&lt;/</span><span class="hl-tag">NavbarLink</span><span class="hl-punct">&gt;</span>
    <span class="hl-punct">&lt;</span><span class="hl-tag">NavbarLink</span> <span class="hl-attr">href</span><span class="hl-punct">=</span><span class="hl-string">"/docs"</span><span class="hl-punct">&gt;</span>Docs<span class="hl-punct">&lt;/</span><span class="hl-tag">NavbarLink</span><span class="hl-punct">&gt;</span>
    <span class="hl-punct">&lt;</span><span class="hl-tag">Button</span> <span class="hl-attr">variant</span><span class="hl-punct">=</span><span class="hl-string">"primary"</span> <span class="hl-attr">size</span><span class="hl-punct">=</span><span class="hl-string">"sm"</span><span class="hl-punct">&gt;</span>
      Get started
    <span class="hl-punct">&lt;/</span><span class="hl-tag">Button</span><span class="hl-punct">&gt;</span>
  <span class="hl-punct">&lt;/</span><span class="hl-tag">Navbar</span><span class="hl-punct">&gt;</span>`

  let count = $state(0)
  let inputVal = $state('')
  let toggleChecked = $state(false)
  let selectVal = $state('option-1')
  let progressVal = $state(0)

  $effect(() => {
    const id = setInterval(() => {
      progressVal = (progressVal + 2) % 101
    }, 50)
    return () => clearInterval(id)
  })
</script>

<div class="content-overlay">
  <Container maxWidth="64rem">
  <Spacer size="xl" />

  <section id="implement" style="scroll-margin-top: calc(3rem + 1px + 2rem);">
    <Heading level={2}>Implement with ease</Heading>
    <Text muted>Import what you need. Compose freely.</Text>
    <Spacer size="md" />
    <CodeBlock code={codeText} codeHtml={codeHtml} />
  </section>

  <Spacer size="xl" />

  <section id="demos" style="scroll-margin-top: calc(3rem + 1px + 2rem);">
    <Heading level={2}>Interactive demos</Heading>
    <Text muted>Components that respond. State that reacts.</Text>
    <Spacer size="md" />

    <Card>
      <Heading level={4}>Reactive state</Heading>
      <Text size="sm" muted>A counter built with $state, click to see Svelte 5 reactivity in action.</Text>
      <Spacer size="sm" />
      <div class="demo-counter">
        <Button variant="outline" size="sm" onclick={() => count--}>
          <Minus size={12} />
        </Button>
        <span class="demo-count">{count}</span>
        <Button variant="outline" size="sm" onclick={() => count++}>
          <Plus size={12} />
        </Button>
        <Button variant="ghost" size="sm" onclick={() => count = 0}>
          <RotateCcw size={12} /> Reset
        </Button>
      </div>
    </Card>

    <Spacer size="md" />

    <div class="demo-grid">
      <ScrollView>
        <ReactiveCard>
          <Heading level={4}>Cursor follows</Heading>
          <Text size="sm" muted>Move your mouse over this card, the border highlight tracks your pointer in real time using CSS custom properties.</Text>
        </ReactiveCard>
      </ScrollView>
      <ScrollView animation="slide-up">
        <ReactiveCard>
          <Heading level={4}>Zero overhead</Heading>
          <Text size="sm" muted>Powered entirely by pointer events and radial gradients. No runtime, no dependencies, no framework overhead.</Text>
        </ReactiveCard>
      </ScrollView>
      <ScrollView animation="fade-in">
        <ReactiveCard>
          <Heading level={4}>Compose freely</Heading>
          <Text size="sm" muted>ReactiveCard wraps any content, drop in headings, text, buttons. The border effect just works.</Text>
        </ReactiveCard>
      </ScrollView>
    </div>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Component variants</Heading>
      <Text size="sm" muted>Buttons and badges in every variant. Click around.</Text>
      <Spacer size="sm" />
      <div class="demo-variants">
        <Button variant="primary" size="sm">Primary</Button>
        <Button variant="secondary" size="sm">Secondary</Button>
        <Button variant="outline" size="sm">Outline</Button>
        <Button variant="ghost" size="sm">Ghost</Button>
        <Badge>Default</Badge>
        <Badge variant="primary">Primary</Badge>
        <Badge variant="outline">Outline</Badge>
      </div>
    </Card>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Context actions</Heading>
      <Text size="sm" muted>Right-click the button to open a context menu with actions.</Text>
      <Spacer size="sm" />
      <ContextMenu>
        {#snippet trigger()}
          <Button variant="outline" size="sm">Right-click me</Button>
        {/snippet}
        <ContextItem onclick={() => alert('Viewing profile')}><User size={12} /> View profile</ContextItem>
        <ContextItem onclick={() => alert('Opening settings')}><User size={12} /> Preferences</ContextItem>
        <ContextItem onclick={() => alert('Not available')} disabled><Bell size={12} /> Notifications</ContextItem>
      </ContextMenu>
    </Card>
  </section>

  <Spacer size="xl" />

  <section id="forms" style="scroll-margin-top: calc(3rem + 1px + 2rem);">
    <Heading level={2}>Form components</Heading>
    <Text muted>Inputs, toggles, selects, all with the same zinc aesthetic.</Text>
    <Spacer size="md" />

    <Card>
      <Heading level={4}>Input</Heading>
      <Text size="sm" muted>Text input with optional label and placeholder.</Text>
      <Spacer size="sm" />
      <Input
        label="Name"
        placeholder="Enter your name"
        bind:value={inputVal}
      />
    </Card>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Toggle</Heading>
      <Text size="sm" muted>Switch for boolean state.</Text>
      <Spacer size="sm" />
      <div class="demo-row">
        <Toggle bind:checked={toggleChecked} label="Enable notifications" />
        <Toggle label="Dark mode" disabled />
      </div>
    </Card>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Select</Heading>
      <Text size="sm" muted>Dropdown with labelled options.</Text>
      <Spacer size="sm" />
      <Select
        label="Framework"
        bind:value={selectVal}
        options={[
          { value: 'option-1', label: 'Svelte' },
          { value: 'option-2', label: 'React' },
          { value: 'option-3', label: 'Vue' },
        ]}
      />
    </Card>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Progress</Heading>
      <Text size="sm" muted>Determinate progress bar for loading states.</Text>
      <Spacer size="sm" />
      <div class="demo-progress">
        <Progress value={progressVal} size="sm" />
        <Progress value={progressVal} size="md" />
        <Progress value={progressVal} size="lg" />
      </div>
    </Card>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Tabs</Heading>
      <Text size="sm" muted>Switchable tab interface.</Text>
      <Spacer size="sm" />
      <Tabs
        tabs={[
          { id: 'tab1', label: 'Code' },
          { id: 'tab2', label: 'Preview' },
          { id: 'tab3', label: 'Settings' },
        ]}
      >
        <Text size="sm" muted>Tab content area, render anything here.</Text>
      </Tabs>
    </Card>

    <Spacer size="md" />

    <Card>
      <Heading level={4}>Kbd & Divider</Heading>
      <Text size="sm" muted>Utility components for keyboard shortcuts and visual separation.</Text>
      <Spacer size="sm" />
      <Text size="sm" muted>Press <Kbd>Ctrl</Kbd> + <Kbd>K</Kbd> to search</Text>
      <Spacer size="sm" />
      <Divider label="Section break" />
      <Spacer size="sm" />
      <div class="demo-row">
        <Text size="sm">Left</Text>
        <Divider axis="vertical" />
        <Text size="sm">Center</Text>
        <Divider axis="vertical" />
        <Text size="sm">Right</Text>
      </div>
    </Card>
  </section>

  <Spacer size="xl" />
  </Container>
</div>

<style>
  .content-overlay {
    position: relative;
    background: var(--surface-raised);
    z-index: 1;
  }
  .demo-counter {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .demo-count {
    font-family: 'Geist Mono', monospace;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    min-width: 2.5rem;
    text-align: center;
  }
  .demo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
    gap: 1rem;
  }
  .demo-variants {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
  }
  .demo-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }
  .demo-progress {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
</style>
