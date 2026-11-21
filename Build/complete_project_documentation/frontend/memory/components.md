# memory components

Component files under the matching components/memory directory are inventoried below. Props, emits, and slots are listed only when explicit declarations are found.


## components/accounts/ImageCropperDialog.vue
L15: const props = defineProps({ file: { type: [File, Object], default: null }, aspectRatio: { type: Number, default: 1 } })
L16: const emit = defineEmits(['cropped', 'cancel'])

## components/accounts/LoginForm.vue
No explicit props/emits/slot declaration matched this static scan.

## components/accounts/SignupForm.vue
No explicit props/emits/slot declaration matched this static scan.

## components/ai/AIActivityLog.vue
No explicit props/emits/slot declaration matched this static scan.

## components/ai/AIChat.vue
L251: emits: ['click'],

## components/ai/AIProviderUsageChart.vue
L7: const props = defineProps({ rows: { type: Array, default: () => [] } })

## components/ai/AIStatusIndicator.vue
L13: defineProps({

## components/ai/MarkdownRenderer.vue
L17: const props = defineProps({ content: { type: String, default: '' } })

## components/ai/dashboard/OpportunityRow.vue
L16: defineProps({

## components/ai/dashboard/Recommendation.vue
L15: defineProps({

## components/ai/dashboard/SkillBar.vue
L14: defineProps({

## components/ai/dashboard/StatCard.vue
L16: defineProps({

## components/ai/layout/AppLayout.vue
L14: <slot />

## components/ai/layout/Sidebar.vue
L58: defineProps({ collapsed: Boolean })
L59: defineEmits(['toggle', 'navigate'])

## components/ai/layout/Topbar.vue
L24: defineEmits(['toggle-sidebar'])

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

## components/core/FrontendEnhancementCenter.vue
No explicit props/emits/slot declaration matched this static scan.

## components/finance/FinanceApiTest.vue
L41: defineProps({

## components/finance/FinanceBudgets.vue
L55: defineProps({
L67: defineEmits(['add', 'edit', 'remove'])

## components/finance/FinanceCoach.vue
L47: defineProps({
L64: defineEmits(['update:question', 'ask'])

## components/finance/FinanceCrudDialog.vue
L407: const props = defineProps({
L439: const emit = defineEmits(['update:visible', 'update:form', 'cancel', 'save'])

## components/finance/FinanceDebts.vue
L75: defineProps({
L97: defineEmits(['add', 'payment', 'edit', 'remove'])

## components/finance/FinanceForecast.vue
L110: defineProps({
L137: defineEmits(['refresh', 'scenario'])

## components/finance/FinanceHabits.vue
L51: defineProps({
L58: defineEmits(['add', 'edit', 'remove'])

## components/finance/FinanceHealthAlerts.vue
L69: defineProps({
L99: defineEmits(['mark-alert'])

## components/finance/FinanceHero.vue
L46: defineProps({
L57: defineEmits([

## components/finance/FinanceIntegrations.vue
L48: defineProps({

## components/finance/FinanceKpiGrid.vue
L21: defineProps({

## components/finance/FinanceLoans.vue
L85: defineProps({
L110: defineEmits(['add', 'payment', 'edit', 'remove'])

## components/finance/FinanceOverview.vue
L131: defineProps({
L200: defineEmits(['ask-ai', 'go-transactions'])

## components/finance/FinancePaymentDialog.vue
L46: const props = defineProps({
L67: const emit = defineEmits(['update:visible', 'update:paymentForm', 'cancel', 'save'])

## components/finance/FinanceRecurring.vue
L68: defineProps({
L95: defineEmits(['add', 'edit', 'remove'])

## components/finance/FinanceReports.vue
L24: defineProps({

## components/finance/FinanceSavings.vue
L87: defineProps({
L114: defineEmits(['add', 'plan', 'edit', 'remove'])

## components/finance/FinanceSectionNav.vue
L15: defineProps({
L27: defineEmits(['update:modelValue'])

## components/finance/FinanceTransactions.vue
L58: defineProps({
L85: defineEmits(['add', 'edit', 'remove'])

## components/goals/GoalCard.vue
L113: defineProps({
L124: defineEmits(['details', 'edit', 'action', 'duplicate', 'remove'])

## components/goals/GoalStats.vue
L28: defineProps({

## components/goals/GoalsToolbar.vue
L40: defineProps({
L50: defineEmits(['update:search', 'update:statusFilter', 'update:categoryFilter', 'update:sortBy'])

## components/knowledge/KnowledgeCard.vue
L14: defineProps({
L21: const emit = defineEmits(['edit', 'archive'])

## components/knowledge/KnowledgeEmptyState.vue
No explicit props/emits/slot declaration matched this static scan.

## components/knowledge/KnowledgeForm.vue
L4: const props = defineProps({
L16: const emit = defineEmits(['submit', 'cancel'])

## components/learning/AIReviewPanel.vue
L4: const props = defineProps({

## components/learning/ApplicationComposer.vue
L11: const props = defineProps({
L23: const emit = defineEmits(['updated'])

## components/learning/LearningPathEditor.vue
L17: const props = defineProps({
L34: const emit = defineEmits(['refresh'])

## components/learning/LearningTopicCard.vue
L2: defineProps({

## components/shared/GlobalToastNotification.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/HeaderView.vue
L339: <slot />

## components/shared/HelloWorld.spec.js
L8: const wrapper = mount(HelloWorld, { props: { msg: 'Hello Vitest' } })

## components/shared/HelloWorld.vue
L2: defineProps({

## components/shared/IconCommunity.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/IconDocumentation.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/IconEcosystem.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/IconSupport.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/IconTooling.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/LiveDebugConsole.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/ThemeSwitcher.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/TheWelcome.vue
No explicit props/emits/slot declaration matched this static scan.

## components/shared/WelcomeItem.vue
L4: <slot name="icon"></slot>
L8: <slot name="heading"></slot>
L10: <slot></slot>
