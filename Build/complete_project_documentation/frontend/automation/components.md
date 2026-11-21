# automation components

Component files under the matching components/automation directory are inventoried below. Props, emits, and slots are listed only when explicit declarations are found.


## components/automation/AIPrompt.vue
No explicit props/emits/slot declaration matched this static scan.

## components/automation/ApiFlowPanel.vue
L102: const props = defineProps({

## components/automation/ProgramsView.vue
L221: const emit = defineEmits(['program-selected'])

## components/automation/Action/ActionPanel.vue
L6: const props = defineProps({
L12: const emit = defineEmits([
L256: const props = defineProps({
L262: const emit = defineEmits([

## components/automation/Edge/CustomEdge.vue
L4: defineProps({
L21: <slot />

## components/automation/Execution/LiveConsole.vue
L25: const props = defineProps({
L33: const emit = defineEmits(['close', 'done', 'error'])

## components/automation/Execution/RealtimeGraph.vue
L22: const props = defineProps({
L29: const emit = defineEmits(['close', 'update:visible'])

## components/automation/Node/CustomNode.vue
L460: const props = defineProps({
L464: const emit = defineEmits([

## components/automation/Node/NodeMarketplace.vue
L30: const props = defineProps({
L41: const emit = defineEmits([

## components/automation/Node/NodePluginCard.vue
L20: const props = defineProps({
L32: const emit = defineEmits([

## components/automation/Node/NodeVisualBuilder.vue
L24: const props = defineProps({
L29: const emit = defineEmits(['confirm', 'cancel', 'update:visible'])

## components/automation/nodes/DelayNode.vue
L18: const props = defineProps(['id', 'data'])

## components/automation/Program/CreateProgram.vue
L5: const props = defineProps({
L10: const emit = defineEmits(['update:visible', 'image-change', 'submit'])

## components/automation/Program/EditProgram.vue
L4: const props = defineProps({
L9: const emit = defineEmits(['update:visible', 'save'])

## components/automation/Workflow/WorkflowCanvas.vue
L33: const props = defineProps({
L39: console.log('props: ', props)
L43: const emit = defineEmits([
L115: <slot name="toolbar" />

## components/automation/Workflow/WorkflowToolbar.vue
L26: defineProps({
L34: const emit = defineEmits([

## components/automation/Workflow/WorkflowVersions.vue
L26: const props = defineProps({
L31: const emit = defineEmits(['restore', 'close', 'update:visible'])
