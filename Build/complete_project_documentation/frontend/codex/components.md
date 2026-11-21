# codex components

Component files under the matching components/codex directory are inventoried below. Props, emits, and slots are listed only when explicit declarations are found.


## components/codex/Build/WorkspaceView.vue
No explicit props/emits/slot declaration matched this static scan.

## components/codex/Capabilities/CapabilitiesView.vue
No explicit props/emits/slot declaration matched this static scan.

## components/codex/dialogs/CodexInfoDialog.vue
L4: defineProps({
L9: defineEmits(['update:visible'])

## components/codex/dialogs/CodexPromptDialog.vue
L8: const props = defineProps({
L13: const emit = defineEmits(['update:visible', 'update:promptType'])

## components/codex/dialogs/CodexResultDialog.vue
L5: defineProps({
L10: defineEmits(['update:visible'])

## components/codex/Layout/CodexRightSidebar.vue
L4: defineProps({ chatInput: String, healthScores: Object })
L5: defineEmits(['update:chatInput', 'analyze', 'prompt', 'send', 'navigate'])

## components/codex/Layout/CodexSidebar.vue
L2: defineProps({ navItems: Array, activePanel: String, projectName: String })
L3: defineEmits(['update:activePanel'])

## components/codex/Layout/CodexTopbar.vue
L6: defineProps({ query: String, activePanel: String, navItems: Array })
L7: defineEmits(['update:query', 'update:activePanel'])

## components/codex/panels/CodexAnalysisPanel.vue
L6: defineProps({
L10: defineEmits(['rebuild'])

## components/codex/panels/CodexChatPanel.vue
L5: defineProps({
L10: defineEmits(['update:chatInput', 'send'])

## components/codex/panels/CodexGovernancePanel.vue
L8: defineProps({
L12: defineEmits(['manifest'])

## components/codex/panels/CodexPipelinePanel.vue
L6: defineProps({
L9: defineEmits(['refresh'])

## components/codex/panels/CodexRegistryPanel.vue
L7: <slot />

## components/codex/workspace/CodexCodeEditor.vue
L4: defineProps({ selectedFile: Object, selectedFiles: Array, fileContent: String })
L5: defineEmits(['close', 'freeze', 'summary', 'openLocal', 'analyzeSelected'])

## components/codex/workspace/CodexFileActions.vue
No explicit props/emits/slot declaration matched this static scan.

## components/codex/workspace/CodexInspectorWorkspace.vue
L4: const props = defineProps({
L11: const emit = defineEmits(['openFile', 'askAI', 'scan'])

## components/codex/workspace/CodexProjectExplorer.vue
L4: const props = defineProps({
L11: defineEmits(['update:fileQuery', 'openFile', 'toggleFile'])

## components/codex/workspace/CodexTerminal.vue
L2: defineProps({ command: String, result: [Object, Array, String] })
L3: defineEmits(['update:command', 'run'])
