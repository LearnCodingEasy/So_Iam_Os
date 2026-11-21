# Frontend Source-File Catalog

Static inventory of JavaScript, Vue, TypeScript, SCSS, and CSS files under frontend_vue/src. Tests are included and labeled; binary assets are excluded from symbol extraction. Imported dependencies are excerpts, and global callers are not exhaustively resolved.

**Files indexed:** 286. Source evidence: frontend_vue/src/.

## src/App.vue
- Type/category: VUE
- Declarations: L7: const userStore = useUserStore()
- Imports/style dependencies (first six): import { RouterView } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import AppLayout from '@/components/ai/layout/AppLayout.vue'; import LiveDebugConsole from '@/components/shared/LiveDebugConsole.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/main.js
- Type/category: JS
- Declarations: L172: const app = createApp(App)
- Imports/style dependencies (first six): import './assets/Tailwind/tailwind.css'; import 'tailwindcss/tailwind.css'; import 'animate.css'; import './assets/scss/style.scss'; import VueMarkdownIt from 'vue3-markdown-it'; import 'github-markdown-css/github-markdown.css'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/Images/Finance/_Finance.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/style.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use 'AI/AI.scss';; @use 'AI/AIChat';; @use 'Automation/Automation';; @use 'Codex/Codex';; @use 'Dashboard/Dashboard';; @use 'Finance/Finance';
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/abstracts/_tokens.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/AI/AI.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/AI/AIOperationsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/AI/_AIChat.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Automation/_Automation.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/base/_base.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Codex/CodexView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Codex/_Codex.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use './CodexCapabilities';
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Codex/_CodexCapabilities.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Codex/_CodexView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/components/_states.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Dashboard/_Dashboard.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Finance/_Finance.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Framework/_Border.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Framework/_flex.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Framework/_Framework.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use 'Border';; @use 'Media_Queries';; @use 'Grid';; @use 'flex';; @use 'Display/Display';
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Framework/_Grid.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use 'Media_Queries' as *; // ðŸ“‚ Ø§Ø³ØªÙŠØ±Ø§Ø¯ Ø§Ù„ÙˆØ³Ø§Ø¦Ø·
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Framework/_Media_Queries.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Framework/Display/_Display.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use '../Media_Queries' as *; // ðŸ“‚ Ø§Ø³ØªÙŠØ±Ø§Ø¯ Ø§Ù„ÙˆØ³Ø§Ø¦Ø·
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Goals/GoalsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Header/_Header.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Jobs/JobsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Jobs/_Jobs.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Learn/Learn.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Learn/_LearningTopic.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Learn/_LearnView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Library/Vue_Flow/_useVueFlow.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Library/Vue_Flow/_vueflow-controls.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Library/Vue_Flow/_vueflow-controls_aside.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Library/Vue_Flow/_vueflow-minimap.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Library/Vue_Flow/_vueflow_node.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Library/Vue_Flow/_vue_flow.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use './vueflow-controls';; @use './vueflow-minimap';; @use './useVueFlow';; @use './vueflow_node';; @use './vueflow-controls_aside';
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/LiveDebugConsole/_LiveDebugConsole.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Login/_Login.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): @use '../Framework/Media_Queries' as *;
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Profile/_Profile.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Scraper/ScraperView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/Settings/_Settings.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AboutView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Account_ProfileView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AIControl.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AI_AgentPlanner.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AI_AI.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AI_AIChat.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AI_AIControl.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/AI_AIOperationsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Authentication_AuthCallback.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Authentication_auth_callback.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Authentication_LoginView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_AutomationView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_AutomationView_NEW.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_DashboardAutomationView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_icon.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_ProgramCreate.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_ProgramEdit.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_ProgramList.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_TaskCreate.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Automation_TaskEditor.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Challenges_ChallengesView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Codex_CodexBuildWorkspace.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Codex_CodexCapabilities.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Codex_CodexView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Dashboard_DashboardView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Finance_FinanceView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Goals_Goals.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/HomeView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/jobs_JobsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/knowledge_KnowledgeView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/learning_LearningTopic.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/learning_LearningView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Memory_MemoryView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Notifications_NotificationsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Page_Not_Found_Page_Not_Found.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Progress_MyProgress.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Projects_ProjectsView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Scraper_ScraperView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Settings_Settings.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Social_SocialView.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Tasks_TasksCalendar.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Tasks_TasksCalendar_copy.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/scss/views/Tasks_TodayTasks.scss
- Type/category: SCSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/assets/Tailwind/tailwind.css
- Type/category: CSS asset/style source
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/accounts/ImageCropperDialog.vue
- Type/category: VUE
- Declarations: L15: const props = defineProps({ file: { type: [File, Object], default: null }, aspectRatio: { type: Number, default: 1 } }); L16: const emit = defineEmits(['cropped', 'cancel']); L17: const visible = ref(false), previewUrl = ref(''), imageRef = ref(null), cropper = ref(null); L20: function crop() { const canvas = cropper.value?.getCroppedCanvas({ maxWidth: 1200, maxHeight: 1200 }); if (!canvas) return; canvas.toBlob((blob) => { if (!blob) return; emit('cropped', new File([blob], props.file?.name || 'cropped-image.jpg', { type: blob.type || 'image/jpeg' })); visible.value = false }, 'image/jpeg', 0.9) }; L21: function cleanup(emitCancel = true) { cropper.value?.destroy(); cropper.value = null; if (objectUrl) URL.revokeObjectURL(objectUrl); objectUrl = ''; previewUrl.value = ''; if (emitCancel && visible.value) emit('cancel') }
- Imports/style dependencies (first six): import { nextTick, onBeforeUnmount, ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import Cropper from 'cropperjs'; import 'cropperjs/dist/cropper.css'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/accounts/LoginForm.vue
- Type/category: VUE
- Declarations: L63: const router = useRouter(); L64: const userStore = useUserStore(); L70: const loading = ref(false); L71: const error = ref(null); L73: const formLogin = ref({; L82: const submitFormLogin = async () => {; L88: const response = await usersAccountsAPI.login({; L97: const userResponse = await usersAccountsAPI.me(); L118: const loginWithGoogle = () => {; L126: const loginWithFacebook = () => {
- Imports/style dependencies (first six): import { ref } from 'vue'; import { useRouter } from 'vue-router'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'; import { useUserStore } from '@/stores/accounts/user'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/accounts/SignupForm.vue
- Type/category: VUE
- Declarations: L102: const formSignup = ref({; L116: const day = ref(''); L117: const month = ref(''); L118: const year = ref(''); L124: const errorsSignup = ref([]); L125: const loading = ref(false); L131: const submitFormSignup = async () => {; L177: const response = await usersAccountsAPI.signup({; L219: const data = err.response.data
- Imports/style dependencies (first six): import { ref } from 'vue'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/AIActivityLog.vue
- Type/category: VUE
- Declarations: L21: const events = ref([]); L25: function addEvent(detail = {}) {; L26: const phase = detail.phase; L39: function formatTime(value) {
- Imports/style dependencies (first six): import { onBeforeUnmount, onMounted, ref } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/AIChat.vue
- Type/category: VUE
- Declarations: L249: const HelpButton = defineComponent({; L263: const helpCopy = {; L280: const sidebarCollapsed = ref(false); L281: const settingsOpen = ref(false); L282: const settingsTab = ref('general'); L283: const settingsTabs = [; L289: const conversations = ref([]); L290: const activeConversationId = ref(null); L291: const messages = ref([]); L292: const draft = ref(''); L293: const sending = ref(false); L294: const loadingConversations = ref(false)
- Imports/style dependencies (first six): import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'; import api from '@/services/Shared/api'; import aiControl from '@/services/AI/aiControl'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/AIProviderUsageChart.vue
- Type/category: VUE
- Declarations: L7: const props = defineProps({ rows: { type: Array, default: () => [] } }); L8: const data = computed(() => ({ labels: props.rows.map((row) => row.provider), datasets: [{ label: 'Messages', data: props.rows.map((row) => row.count || 0), borderWidth: 1 }] })); L9: const options = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
- Imports/style dependencies (first six): import { computed } from 'vue'; import { Bar } from 'vue-chartjs'; import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/AIStatusIndicator.vue
- Type/category: VUE
- Declarations: L13: defineProps({; L18: const status = ref('checking'); L21: const label = computed(() => ({; L29: async function check() {
- Imports/style dependencies (first six): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import api from '@/services/Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/MarkdownRenderer.vue
- Type/category: VUE
- Declarations: L17: const props = defineProps({ content: { type: String, default: '' } }); L20: const safeHtml = computed(() => {; L21: const html = marked.parse(props.content || ''); L22: const sanitized = DOMPurify.sanitize(html, {; L26: const wrapper = document.createElement('div'); L29: const language = [...block.classList].find((name) => name.startsWith('language-'))?.slice(9)
- Imports/style dependencies (first six): import { computed } from 'vue'; import { marked } from 'marked'; import DOMPurify from 'dompurify'; import Prism from 'prismjs'; import 'prismjs/components/prism-markup'; import 'prismjs/components/prism-javascript'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/dashboard/OpportunityRow.vue
- Type/category: VUE
- Declarations: L16: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/dashboard/Recommendation.vue
- Type/category: VUE
- Declarations: L15: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/dashboard/SkillBar.vue
- Type/category: VUE
- Declarations: L14: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/dashboard/StatCard.vue
- Type/category: VUE
- Declarations: L16: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/layout/AppLayout.vue
- Type/category: VUE
- Declarations: L25: const sidebarCollapsed = ref(false); L26: const mobileMenuOpen = ref(false)
- Imports/style dependencies (first six): import { ref } from 'vue'; import Sidebar from './Sidebar.vue'; import Topbar from './Topbar.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/layout/Sidebar.vue
- Type/category: VUE
- Declarations: L58: defineProps({ collapsed: Boolean }); L59: defineEmits(['toggle', 'navigate']); L61: const mainItems = [; L79: const secondaryItems = [
- Imports/style dependencies (first six): import { RouterLink } from 'vue-router'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/ai/layout/Topbar.vue
- Type/category: VUE
- Declarations: L24: defineEmits(['toggle-sidebar']); L25: const route = useRoute(); L26: const isDark = ref(false); L27: const pageTitle = computed(() => route.meta?.title || ({; L33: const pageDescription = computed(() => route.meta?.description || 'Ù…Ø³Ø§Ø­Ø© Ø§Ù„Ø¹Ù…Ù„ Ø§Ù„Ø´Ø®ØµÙŠØ©'); L35: function applyTheme(value) {; L41: function toggleTheme() { applyTheme(!isDark.value) }
- Imports/style dependencies (first six): import { computed, onMounted, ref, watch } from 'vue'; import { RouterLink, useRoute } from 'vue-router'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/AIPrompt.vue
- Type/category: VUE
- Declarations: L6: const prompt = ref(''); L7: const result = ref(null); L8: const loading = ref(false); L9: const error = ref(''); L11: async function runPrompt() {; L17: const response = await api.post(endpoints.ai.agentPlan, { request: prompt.value.trim() })
- Imports/style dependencies (first six): import { ref } from 'vue'; import api from '@/services/Shared/api'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/ApiFlowPanel.vue
- Type/category: VUE
- Declarations: L102: const props = defineProps({; L110: const openIdx = ref(null); L112: function toggleDetail(i) {; L116: function getConnectorClass(i) {; L117: const cur = props.stages[i]?.status; L119: const next = props.stages[i + 1]?.status; L126: const overallClass = computed(() => {; L127: const hasFail = props.stages.some((s) => s.status === 'fail'); L128: const hasActive = props.stages.some((s) => s.status === 'active'); L129: const allDone = props.stages.find((s) => s.id === 'done')?.status === 'pass'; L136: const overallLabel = computed(() => {; L137: const hasFail = props.stages.some((s) => s.status === 'fail')
- Imports/style dependencies (first six): import { ref, computed } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/ProgramsView.vue
- Type/category: VUE
- Declarations: L216: const toast = useToast(); L218: const confirm = useConfirm(); L221: const emit = defineEmits(['program-selected']); L223: const selectProgram = async (id) => {; L234: const programs = ref([]); L235: const loadingPrograms = ref(false); L236: const currentProgramId = ref(null); L237: const ceateProgramVisible = ref(false); L238: const editProgramVisible = ref(false); L239: const formProgram = ref({; L260: const loadPrograms = async () => {; L274: const loadProgram = async (id) => {
- Imports/style dependencies (first six): import { ref,  } from 'vue'; import automationService from '@/services/Automation/AutomationService'; import { useToast } from 'primevue/usetoast'; import { useConfirm } from 'primevue/useconfirm'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Action/ActionPanel.vue
- Type/category: VUE
- Declarations: L6: const props = defineProps({; L12: const emit = defineEmits([; L23: const actionOptions = [; L36: const getNodeId = () => props.selectedNode?.data?.node?.backend_id ?? props.selectedNode?.id; L256: const props = defineProps({; L262: const emit = defineEmits([; L273: const nodeType = computed(() => props.selectedNode?.data?.node?.node_type?.toLowerCase() ?? ''); L274: const isProgramNode = computed(() => nodeType.value === 'program'); L275: const isProgramElementNode = computed(() => nodeType.value === 'program-element'); L276: const isDelayNode = computed(() => ['delay', 'timing', 'wait'].includes(nodeType.value)); L281: const ACTION_OPTIONS = {; L311: const currentOptions = computed(() => {
- Imports/style dependencies (first six): import { computed } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Edge/CustomEdge.vue
- Type/category: VUE
- Declarations: L4: defineProps({
- Imports/style dependencies (first six): import { Handle, Position } from '@vue-flow/core'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Execution/LiveConsole.vue
- Type/category: VUE
- Declarations: L25: const props = defineProps({; L33: const emit = defineEmits(['close', 'done', 'error']); L36: const logs = ref([]); L37: const status = ref('connecting') // connecting | running | success | failed | closed; L38: const ws = ref(null); L39: const consoleEl = ref(null); L40: const isMinimized = ref(false); L44: const connect = () => {; L47: const url = `${props.wsBaseUrl}/ws/workflow/${props.taskRunId}/`; L63: const msg = JSON.parse(data); L83: const handleMessage = (msg) => {; L108: const addLog = (level, message, nodeId = null) => {
- Imports/style dependencies (first six): import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Execution/RealtimeGraph.vue
- Type/category: VUE
- Declarations: L22: const props = defineProps({; L29: const emit = defineEmits(['close', 'update:visible']); L33: const nodeStats = ref(new Map()) // node_id â†’ { label, status, duration_ms }; L34: const startTime = ref(null); L35: const elapsed = ref(0); L40: const totalNodes = computed(() => props.nodes.length); L41: const executedCount = computed(; L44: const successCount = computed(; L47: const failedCount = computed(; L50: const successRate = computed(() => {; L51: const done = successCount.value + failedCount.value; L55: const progressPercent = computed(() =>
- Imports/style dependencies (first six): import { ref, computed, watch, onBeforeUnmount } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Node/CustomNode.vue
- Type/category: VUE
- Declarations: L44: const localAction = ref(props.data?.action?.action_type ?? 'open_program') // âš™ Ù†ÙˆØ¹ Ø§Ù„Ø£ÙƒØ´Ù†; L46: const localDelay = ref(props.data?.config?.delay ?? 0) // â± Ù‚ÙŠÙ…Ø© Ø§Ù„ØªØ£Ø®ÙŠØ±; L48: const localTypingText = ref(props.data?.config?.text ?? '') // âŒ¨ Ø§Ù„Ù†Øµ Ø§Ù„Ù…ÙƒØªÙˆØ¨; L59: const nodeTypeClass = computed(() => {; L60: const type = node.value.node_type?.toLowerCase(); L74: const dynamicIcon = computed(() => {; L75: const type = node.value.node_type; L89: const isProgramNode = computed(() => node.value.node_type?.toLowerCase() === 'program'); L96: const isProgramElementNode = computed(; L105: const isDelayNode = computed(() => {; L106: const type = node.value.node_type?.toLowerCase(); L116: const actionColor = computed(() => {
- Imports/style dependencies (first six): import { ref, watch, computed } from 'vue'; import { Handle, Position } from '@vue-flow/core'; import { ref, watch, computed } from 'vue'; import { Handle, Position } from '@vue-flow/core'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Node/NodeMarketplace.vue
- Type/category: VUE
- Declarations: L30: const props = defineProps({; L41: const emit = defineEmits([; L57: const activeTab = ref(0) // 0=Programs, 1=Elements, 2=Plugins, 3=Tasks, 4=Workflows; L58: const searchText = ref(''); L59: const activeCategory = ref('all') // all | programs | input | timing | ai; L62: const allPlugins = computed(() => registry.getMarketplaceItems()); L64: const filteredPlugins = computed(() => {; L70: const q = searchText.value.toLowerCase(); L82: const filteredPrograms = computed(() => {; L84: const q = searchText.value.toLowerCase(); L88: const filteredElements = computed(() => {; L90: const q = searchText.value.toLowerCase()
- Imports/style dependencies (first six): import { ref, computed } from 'vue'; import registry, { PLUGIN_CATEGORIES } from '@/plugins/PluginRegistry'; import NodePluginCard from './NodePluginCard.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Node/NodePluginCard.vue
- Type/category: VUE
- Declarations: L20: const props = defineProps({; L32: const emit = defineEmits([; L37: const onDragStart = (e) => {
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Node/NodeVisualBuilder.vue
- Type/category: VUE
- Declarations: L24: const props = defineProps({; L29: const emit = defineEmits(['confirm', 'cancel', 'update:visible']); L32: const label = ref(''); L33: const customColor = ref(''); L34: const formData = ref({}); L35: const error = ref(null); L51: const nodeColor = computed(() => customColor.value || props.plugin?.color || '#334155'); L54: const handleConfirm = () => {; L57: const validErr = registry.validate(props.plugin.id, formData.value); L64: const payload = props.plugin ? registry.buildPayload(props.plugin.id, formData.value) : {}
- Imports/style dependencies (first six): import { ref, watch, computed } from 'vue'; import registry from '@/plugins/PluginRegistry'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/nodes/DelayNode.vue
- Type/category: VUE
- Declarations: L18: const props = defineProps(['id', 'data']); L21: const updateDelay = () => {; L22: const node = findNode(props.id)
- Imports/style dependencies (first six): import { useVueFlow } from '@vue-flow/core'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Program/CreateProgram.vue
- Type/category: VUE
- Declarations: L5: const props = defineProps({; L10: const emit = defineEmits(['update:visible', 'image-change', 'submit'])
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Program/EditProgram.vue
- Type/category: VUE
- Declarations: L4: const props = defineProps({; L9: const emit = defineEmits(['update:visible', 'save']); L11: const editProgramVisible = ref(false); L13: const formProgram = ref({; L40: const onImageChangeProgram = (e) => {; L44: const saveProgram = () => {
- Imports/style dependencies (first six): import { ref, watch } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Workflow/WorkflowCanvas.vue
- Type/category: VUE
- Declarations: L33: const props = defineProps({; L43: const emit = defineEmits([; L57: const nodeTypes = computed(() => ({ custom: CustomNode })); L58: const edgeTypes = computed(() => ({ custom: CustomEdge })); L61: const onNodeDragStop = ({ node }) => emit('node-drag-stop', node); L62: const onNodeClick = (event) => emit('node-click', event); L63: const onConnect = (params) => emit('connect', params); L64: const onDrop = (e) => emit('drop', e); L65: const onDragOver = (e) => {
- Imports/style dependencies (first six): import { computed } from 'vue'; import { VueFlow, Panel } from '@vue-flow/core'; import { Background } from '@vue-flow/background'; import { Controls } from '@vue-flow/controls'; import { MiniMap } from '@vue-flow/minimap'; import CustomNode from '@/components/automation/Node/CustomNode.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Workflow/WorkflowToolbar.vue
- Type/category: VUE
- Declarations: L26: defineProps({; L34: const emit = defineEmits([; L44: const layoutOptions = [; L52: const statusOptions = [
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/automation/Workflow/WorkflowVersions.vue
- Type/category: VUE
- Declarations: L26: const props = defineProps({; L31: const emit = defineEmits(['restore', 'close', 'update:visible']); L33: const toast = useToast(); L34: const versions = ref([]); L35: const loading = ref(false); L36: const restoring = ref(null) // id of version being restored; L46: const loadVersions = async () => {; L90: const restoreVersion = async (version) => {; L110: const formatDate = (iso) => {; L111: const d = new Date(iso)
- Imports/style dependencies (first six): import { ref, watch } from 'vue'; import automationService from '@/services/Automation/AutomationService'; import { useToast } from 'primevue/usetoast'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/Build/WorkspaceView.vue
- Type/category: VUE
- Declarations: L7: const buildSteps = ref([
- Imports/style dependencies (first six): import { ref } from 'vue'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/Capabilities/CapabilitiesView.vue
- Type/category: VUE
- Declarations: L11: const activeTab = ref('features'); L13: const mockFeatures = ref([; L19: const mockTools = ref([
- Imports/style dependencies (first six): import { ref } from 'vue'; import Card from 'primevue/card'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tabs from 'primevue/tabs'; import TabList from 'primevue/tablist'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/dialogs/CodexInfoDialog.vue
- Type/category: VUE
- Declarations: L4: defineProps({; L9: defineEmits(['update:visible'])
- Imports/style dependencies (first six): import Dialog from 'primevue/dialog'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/dialogs/CodexPromptDialog.vue
- Type/category: VUE
- Declarations: L8: const props = defineProps({; L13: const emit = defineEmits(['update:visible', 'update:promptType']); L16: const promptCopyState = ref(''); L18: async function copyPrompt() {
- Imports/style dependencies (first six): import { ref } from 'vue'; import Dialog from 'primevue/dialog'; import SelectButton from 'primevue/selectbutton'; import Textarea from 'primevue/textarea'; import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/dialogs/CodexResultDialog.vue
- Type/category: VUE
- Declarations: L5: defineProps({; L10: defineEmits(['update:visible'])
- Imports/style dependencies (first six): import Dialog from 'primevue/dialog'; import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/Layout/CodexRightSidebar.vue
- Type/category: VUE
- Declarations: L4: defineProps({ chatInput: String, healthScores: Object }); L5: defineEmits(['update:chatInput', 'analyze', 'prompt', 'send', 'navigate'])
- Imports/style dependencies (first six): import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/Layout/CodexSidebar.vue
- Type/category: VUE
- Declarations: L2: defineProps({ navItems: Array, activePanel: String, projectName: String }); L3: defineEmits(['update:activePanel'])
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/Layout/CodexTopbar.vue
- Type/category: VUE
- Declarations: L6: defineProps({ query: String, activePanel: String, navItems: Array }); L7: defineEmits(['update:query', 'update:activePanel'])
- Imports/style dependencies (first six): import Tabs from 'primevue/tabs'; import TabList from 'primevue/tablist'; import Tab from 'primevue/tab'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/panels/CodexAnalysisPanel.vue
- Type/category: VUE
- Declarations: L6: defineProps({; L10: defineEmits(['rebuild'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/panels/CodexChatPanel.vue
- Type/category: VUE
- Declarations: L5: defineProps({; L10: defineEmits(['update:chatInput', 'send'])
- Imports/style dependencies (first six): import Button from 'primevue/button'; import InputText from 'primevue/inputtext'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/panels/CodexGovernancePanel.vue
- Type/category: VUE
- Declarations: L8: defineProps({; L12: defineEmits(['manifest'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/panels/CodexPipelinePanel.vue
- Type/category: VUE
- Declarations: L6: defineProps({; L9: defineEmits(['refresh'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/panels/CodexRegistryPanel.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/workspace/CodexCodeEditor.vue
- Type/category: VUE
- Declarations: L4: defineProps({ selectedFile: Object, selectedFiles: Array, fileContent: String }); L5: defineEmits(['close', 'freeze', 'summary', 'openLocal', 'analyzeSelected'])
- Imports/style dependencies (first six): import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/workspace/CodexFileActions.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/workspace/CodexInspectorWorkspace.vue
- Type/category: VUE
- Declarations: L4: const props = defineProps({; L11: const emit = defineEmits(['openFile', 'askAI', 'scan']); L13: const activeApp = ref(null); L14: const activeRoute = ref(''); L15: const inspectEnabled = ref(false); L16: const viewport = ref('desktop'); L17: const selectedElement = ref(null); L18: const resourcePaths = ref([]); L19: const previewError = ref(''); L20: const frame = ref(null); L23: const appFeatures = computed(() => [...props.features].sort((a, b) => (a.name || '').localeCompare(b.name || ''))); L24: const activeRoutes = computed(() => {
- Imports/style dependencies (first six): import { computed, onBeforeUnmount, ref, watch } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/workspace/CodexProjectExplorer.vue
- Type/category: VUE
- Declarations: L4: const props = defineProps({; L11: defineEmits(['update:fileQuery', 'openFile', 'toggleFile']); L13: const filteredFiles = computed(() => {; L14: const q = (props.fileQuery || '').trim().toLowerCase()
- Imports/style dependencies (first six): import { computed } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/codex/workspace/CodexTerminal.vue
- Type/category: VUE
- Declarations: L2: defineProps({ command: String, result: [Object, Array, String] }); L3: defineEmits(['update:command', 'run'])
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/core/FrontendEnhancementCenter.vue
- Type/category: VUE
- Declarations: L116: const isDark = useDark({ selector: 'html', attribute: 'class', valueDark: 'p-dark', valueLight: '' }); L117: const prefersReducedMotion = computed(() => usePreferredReducedMotion().value === 'reduce'); L119: const query = useQuery({; L122: const response = await api.get('/ai/health/'); L129: const editor = useEditor({; L134: const cards = ref([; L141: const activity = Array.from({ length: 250 }, (_, index) => ({; L146: const fileInput = ref(null); L164: function toggleLocale() {; L169: function notify() {
- Imports/style dependencies (first six): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import { useDark, usePreferredReducedMotion } from '@vueuse/core'; import { useQuery } from '@tanstack/vue-query'; import { EditorContent, useEditor } from '@tiptap/vue-3'; import StarterKit from '@tiptap/starter-kit'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceApiTest.vue
- Type/category: VUE
- Declarations: L41: defineProps({
- Imports/style dependencies (first six): import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceBudgets.vue
- Type/category: VUE
- Declarations: L55: defineProps({; L67: defineEmits(['add', 'edit', 'remove'])
- Imports/style dependencies (first six): import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceCoach.vue
- Type/category: VUE
- Declarations: L47: defineProps({; L64: defineEmits(['update:question', 'ask'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import Textarea from 'primevue/textarea'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceCrudDialog.vue
- Type/category: VUE
- Declarations: L407: const props = defineProps({; L439: const emit = defineEmits(['update:visible', 'update:form', 'cancel', 'save']); L441: const localForm = ref({}); L468: const formTitle = computed(() => {; L469: const labels = {
- Imports/style dependencies (first six): import { computed, ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import InputText from 'primevue/inputtext'; import InputNumber from 'primevue/inputnumber'; import Select from 'primevue/select'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceDebts.vue
- Type/category: VUE
- Declarations: L75: defineProps({; L97: defineEmits(['add', 'payment', 'edit', 'remove'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceForecast.vue
- Type/category: VUE
- Declarations: L110: defineProps({; L137: defineEmits(['refresh', 'scenario'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import InputNumber from 'primevue/inputnumber'; import Select from 'primevue/select'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceHabits.vue
- Type/category: VUE
- Declarations: L51: defineProps({; L58: defineEmits(['add', 'edit', 'remove'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceHealthAlerts.vue
- Type/category: VUE
- Declarations: L69: defineProps({; L99: defineEmits(['mark-alert'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Tag from 'primevue/tag'; import Badge from 'primevue/badge'; import ProgressBar from 'primevue/progressbar'; import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceHero.vue
- Type/category: VUE
- Declarations: L46: defineProps({; L57: defineEmits([
- Imports/style dependencies (first six): import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceIntegrations.vue
- Type/category: VUE
- Declarations: L48: defineProps({
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceKpiGrid.vue
- Type/category: VUE
- Declarations: L21: defineProps({
- Imports/style dependencies (first six): import Card from 'primevue/card'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceLoans.vue
- Type/category: VUE
- Declarations: L85: defineProps({; L110: defineEmits(['add', 'payment', 'edit', 'remove'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceOverview.vue
- Type/category: VUE
- Declarations: L131: defineProps({; L200: defineEmits(['ask-ai', 'go-transactions'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Tag from 'primevue/tag'; import Button from 'primevue/button'; import ProgressBar from 'primevue/progressbar'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinancePaymentDialog.vue
- Type/category: VUE
- Declarations: L46: const props = defineProps({; L67: const emit = defineEmits(['update:visible', 'update:paymentForm', 'cancel', 'save']); L69: const localForm = ref({
- Imports/style dependencies (first six): import { ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import InputNumber from 'primevue/inputnumber'; import InputText from 'primevue/inputtext'; import DatePicker from 'primevue/datepicker'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceRecurring.vue
- Type/category: VUE
- Declarations: L68: defineProps({; L95: defineEmits(['add', 'edit', 'remove'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceReports.vue
- Type/category: VUE
- Declarations: L24: defineProps({
- Imports/style dependencies (first six): import Card from 'primevue/card'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceSavings.vue
- Type/category: VUE
- Declarations: L87: defineProps({; L114: defineEmits(['add', 'plan', 'edit', 'remove'])
- Imports/style dependencies (first six): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'; import ProgressBar from 'primevue/progressbar'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceSectionNav.vue
- Type/category: VUE
- Declarations: L15: defineProps({; L27: defineEmits(['update:modelValue'])
- Imports/style dependencies (first six): import SelectButton from 'primevue/selectbutton'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/finance/FinanceTransactions.vue
- Type/category: VUE
- Declarations: L58: defineProps({; L85: defineEmits(['add', 'edit', 'remove'])
- Imports/style dependencies (first six): import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/goals/GoalCard.vue
- Type/category: VUE
- Declarations: L113: defineProps({; L124: defineEmits(['details', 'edit', 'action', 'duplicate', 'remove'])
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/goals/GoalStats.vue
- Type/category: VUE
- Declarations: L28: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/goals/GoalsToolbar.vue
- Type/category: VUE
- Declarations: L40: defineProps({; L50: defineEmits(['update:search', 'update:statusFilter', 'update:categoryFilter', 'update:sortBy'])
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/knowledge/KnowledgeCard.vue
- Type/category: VUE
- Declarations: L14: defineProps({; L21: const emit = defineEmits(['edit', 'archive']); L23: const typeIcons = {; L35: const getIcon = (type) => {; L39: const getTypeLabel = (type) => {; L40: const labels = {; L55: const formatDate = (date) => {
- Imports/style dependencies (first six): import {; import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/knowledge/KnowledgeEmptyState.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/knowledge/KnowledgeForm.vue
- Type/category: VUE
- Declarations: L4: const props = defineProps({; L16: const emit = defineEmits(['submit', 'cancel']); L22: const form = reactive({; L37: const tagsInput = ref(''); L43: const selectedFiles = ref([]); L45: const fileInput = ref(null); L47: const isDragging = ref(false); L50: const acceptedFileTypes = [; L88: const acceptedFileTypesString = acceptedFileTypes.join(','); L94: const knowledgeTypes = [; L110: const existingFiles = computed(() => {; L122: const resetForm = () => {
- Imports/style dependencies (first six): import { reactive, ref, watch, computed } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/learning/AIReviewPanel.vue
- Type/category: VUE
- Declarations: L4: const props = defineProps({; L11: const score = computed(() => {; L15: const scoreClass = computed(() => {; L31: const list = (value) => {
- Imports/style dependencies (first six): import { computed } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/learning/ApplicationComposer.vue
- Type/category: VUE
- Declarations: L11: const props = defineProps({; L23: const emit = defineEmits(['updated']); L25: const title = ref(props.application?.title || ''); L27: const content = ref(props.application?.content || ''); L29: const saving = ref(false); L31: const submitting = ref(false); L33: const reviewing = ref(false); L35: const error = ref(''); L37: const currentApplication = ref(props.application); L39: const isReviewed = computed(() => {; L44: const saveApplication = async () => {; L90: const submitApplication = async () => {
- Imports/style dependencies (first six): import { computed, ref } from 'vue'; import {
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/learning/LearningPathEditor.vue
- Type/category: VUE
- Declarations: L17: const props = defineProps({; L34: const emit = defineEmits(['refresh']); L36: const selectedPathId = ref(props.paths[0]?.id || null); L38: const savingOrder = ref(false); L40: const savingTopic = ref(false); L42: const deletingTopic = ref(false); L44: const error = ref(''); L46: const showTopicModal = ref(false); L48: const editingTopic = ref(null); L50: const topicForm = ref({; L58: const selectedPath = computed(() => {; L62: const pathTopics = computed(() => {
- Imports/style dependencies (first six): import { computed, ref } from 'vue'; import { RouterLink } from 'vue-router'; import draggable from 'vuedraggable'; import LearningTopicCard from './LearningTopicCard.vue'; import {
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/learning/LearningTopicCard.vue
- Type/category: VUE
- Declarations: L2: defineProps({; L14: const statusLabel = (status) => {; L15: const labels = {
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/GlobalToastNotification.vue
- Type/category: VUE
- Declarations: L9: const toast = useToast();; L12: const showNotification = (severity, summary, detail) => {
- Imports/style dependencies (first six): import { useToast } from 'primevue/usetoast';; import { provide } from 'vue';
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/HeaderView.vue
- Type/category: VUE
- Declarations: L14: const router = useRouter(); L15: const route = useRoute(); L16: const userStore = useUserStore(); L18: const sidebarOpen = ref(true); L19: const mobileMenuOpen = ref(false); L20: const profileMenu = ref(null); L21: const searchQuery = ref(''); L23: const menuItems = [; L66: const secondaryItems = [; L72: const userName = computed(() => {; L76: const userEmail = computed(() => userStore.user?.email || ''); L78: const userInitials = computed(() => {
- Imports/style dependencies (first six): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import { RouterLink, useRoute, useRouter } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import Avatar from 'primevue/avatar'; import Badge from 'primevue/badge'; import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/HelloWorld.spec.js
- Type/category: JS test source
- Declarations: L8: const wrapper = mount(HelloWorld, { props: { msg: 'Hello Vitest' } })
- Imports/style dependencies (first six): import { describe, it, expect } from 'vitest'; import { mount } from '@vue/test-utils'; import HelloWorld from './HelloWorld.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/HelloWorld.vue
- Type/category: VUE
- Declarations: L2: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/IconCommunity.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/IconDocumentation.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/IconEcosystem.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/IconSupport.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/IconTooling.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/LiveDebugConsole.vue
- Type/category: VUE
- Declarations: L10: const enabled = import.meta.env.DEV || import.meta.env.VITE_DEBUG_CONSOLE === 'true'; L11: const wsEnabled = import.meta.env.VITE_DEBUG_CONSOLE === 'true'; L12: const WS_URL = import.meta.env.VITE_DEBUG_WS_URL || 'ws://127.0.0.1:8000/ws/debug/'; L13: const MAX_LOGS = 500; L16: const open = ref(false); L17: const minimized = ref(false); L18: const paused = ref(false); L19: const autoScroll = ref(true); L20: const searchQuery = ref(''); L21: const activeFilter = ref('all') // 'all' | 'error' | 'warn' | 'network' | 'pinia'; L24: const logs = ref([]); L25: const status = ref('closed') // 'connecting' | 'connected' | 'closed' | 'error'
- Imports/style dependencies (first six): import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'; import Button from 'primevue/button'; import InputText from 'primevue/inputtext'; import IconField from 'primevue/iconfield'; import InputIcon from 'primevue/inputicon'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/ThemeSwitcher.vue
- Type/category: VUE
- Declarations: L19: const THEME_KEY = 'so_iam_os.theme'; L30: const saved = localStorage.getItem(THEME_KEY); L31: const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches; L32: const isDark = saved ? saved === 'dark' : prefersDark; L33: const root = document.documentElement; L40: const root = document.getElementsByTagName('html')[0]; L41: const isDark = !root.classList.contains('p-dark')
- Imports/style dependencies (first six): import { updatePreset, updateSurfacePalette } from '@primevue/themes'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/TheWelcome.vue
- Type/category: VUE
- Declarations: L9: const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
- Imports/style dependencies (first six): import WelcomeItem from './WelcomeItem.vue'; import DocumentationIcon from './IconDocumentation.vue'; import ToolingIcon from './IconTooling.vue'; import EcosystemIcon from './IconEcosystem.vue'; import CommunityIcon from './IconCommunity.vue'; import SupportIcon from './IconSupport.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/components/shared/WelcomeItem.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useAI.js
- Type/category: JS
- Declarations: L4: export function useAI() {; L5: const response = ref(''); L6: const isLoading = ref(false); L7: const error = ref(null); L8: const conversationId = ref(null); L11: async function chatStream(messages, model = '', options = {}) {; L17: const result = await AIService.chatStream(messages, model, (chunk) => { response.value += chunk }, {; L38: function stopStream() {; L42: function resetConversation() {
- Imports/style dependencies (first six): import { ref } from 'vue'; import AIService from '@/services/AI/AIService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useApiTracker.js
- Type/category: JS
- Declarations: L312: const STAGES_TEMPLATE = [; L322: function freshStages() {; L331: export function useApiTracker() {; L332: const stages = reactive(freshStages()); L333: const isLoading = ref(false); L334: const result = ref(null); L335: const error = ref(null); L336: const meta = reactive({; L346: function setStage(id, status, detail = null) {; L347: const s = stages.find((x) => x.id === id); L357: function resetAll() {; L372: async function execute(options = {}) {
- Imports/style dependencies (first six): import { ref, reactive } from 'vue'; import axios from 'axios'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useAppToast.js
- Type/category: JS
- Declarations: L4: export function useAppToast() {; L5: const toast = useToast(); L7: const success = (detail, summary = 'Success') =>; L10: const info = (detail, summary = 'Info') =>; L13: const warn = (detail, summary = 'Attention') =>; L16: const error = (value, summary = 'Error') =>
- Imports/style dependencies (first six): import { useToast } from 'primevue/usetoast'; import { getApiErrorMessage } from '@/utils/apiError'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useAsyncAction.js
- Type/category: JS
- Declarations: L32: export function useAsyncAction() {; L33: const loading = ref(false); L34: const toast   = useToast(); L35: const tracker = useApiTracker(); L40: const run = async (apiFn, options = {}) => {; L54: const validErr = validate(); L65: const result = await tracker.execute({ serviceFn: apiFn }); L75: const status = err?.response?.status; L76: const body   = err?.response?.data
- Imports/style dependencies (first six): import { ref } from 'vue'; import { useToast } from 'primevue/usetoast'; import { useApiTracker } from '@/composables/useApiTracker'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useNodeDragDrop.js
- Type/category: JS
- Declarations: L27: export function useNodeDragDrop({ workflowStore, programStore, tracker, project, showToast }) {; L32: const draggedItem = ref(null)   // Ø§Ù„Ù€ item Ø§Ù„Ù„ÙŠ Ø¨ÙŠØªØ³Ø­Ø¨ Ù…Ù† Ø§Ù„Ù€ sidebar; L34: const syncState = reactive({; L44: const startDrag = (item) => {; L49: const onDragOver = (e) => {; L55: const onDrop = async (e) => {; L72: const createNodeOnCanvas = async (item, dropEvent) => {; L83: const position = project({ x: dropEvent.clientX, y: dropEvent.clientY }); L86: const ACTION_TYPE_MAP = {; L91: const actionType = ACTION_TYPE_MAP[item.type] ?? 'custom'; L94: const programData = programStore.programById(item.id); L95: const nodeLabel   = programData?.name ?? item.name ?? actionType
- Imports/style dependencies (first six): import { ref, reactive } from 'vue'; import { debounce }       from 'lodash'; import automationService  from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/usePrograms.js
- Type/category: JS
- Declarations: L25: export function usePrograms() {; L26: const confirm       = useConfirm(); L28: const programAction = useAsyncAction(); L29: const programStore  = useProgramStore(); L32: const createProgramVisible = ref(false); L33: const editProgramVisible   = ref(false); L36: const onImageChange = (e) => {; L37: const err = programStore.onImageChange(e); L42: const createProgram = () =>; L55: const openEditProgram = async (id) => {; L65: const editProgram = () =>; L77: const confirmDeleteProgram = (program) => {
- Imports/style dependencies (first six): import { ref }              from 'vue'; import { useConfirm }       from 'primevue/useconfirm'; import { useToastHelper }   from '@/composables/useToastHelper'; import { useAsyncAction }   from '@/composables/useAsyncAction'; import { useProgramStore }  from '@/stores/automation/useProgramStore'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useTheme.js
- Type/category: JS
- Declarations: L3: const THEME_KEY = 'so_iam_os.theme'; L5: export function useTheme() {; L6: const isDark = ref(false); L8: const apply = (dark) => {; L15: const toggle = () => apply(!isDark.value); L18: const saved = localStorage.getItem(THEME_KEY)
- Imports/style dependencies (first six): import { onMounted, ref } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/composables/useToastHelper.js
- Type/category: JS
- Declarations: L12: export function useToastHelper() {; L13: const toast = useToast(); L19: const success = (summary, detail, life = 3000) =>; L22: const error = (summary, detail, life = 5000) =>; L25: const warn = (summary, detail, life = 4000) =>; L28: const info = (summary, detail, life = 3000) =>; L31: const cancelled = (detail = 'Ù„Ù… ÙŠØªÙ… ØªÙ†ÙÙŠØ° Ø§Ù„Ø¥Ø¬Ø±Ø§Ø¡') =>; L38: const apiError = (err, fallbackSummary = 'Ø­ØµÙ„ Ø®Ø·Ø£') => {; L39: const status = err?.response?.status; L40: const data   = err?.response?.data; L44: const entries = Object.entries(data).slice(0, 3); L45: const detail = entries
- Imports/style dependencies (first six): import { useToast } from 'primevue/usetoast'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/i18n.js
- Type/category: JS
- Declarations: L3: const messages = {; L32: export const i18n = createI18n({
- Imports/style dependencies (first six): import { createI18n } from 'vue-i18n'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/PluginRegistry.js
- Type/category: JS
- Declarations: L29: export const PLUGIN_CATEGORIES = {; L43: const PressPlugin = definePlugin({; L56: const HotkeyPlugin = definePlugin({; L76: const CloseProgram = definePlugin({; L91: class PluginRegistry {; L168: const plugin = this.get(actionType); L183: const plugin = this.get(actionType); L225: const registry = new PluginRegistry()
- Imports/style dependencies (first six): import { definePlugin } from './PluginSDK'; import OpenProgramPlugin from './builtin/OpenProgramPlugin'; import ClickElementPlugin from './builtin/ClickElementPlugin'; import WaitPlugin from './builtin/WaitPlugin'; import AIActionPlugin from './builtin/AIActionPlugin'; import SendEmailPlugin from './custom/SendEmailPlugin'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/PluginSDK.js
- Type/category: JS
- Declarations: L36: export function definePlugin(config) {; L38: const required = ['id', 'label', 'icon', 'color', 'category', 'buildPayload']; L93: export const PLUGIN_CATEGORIES = {
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/builtin/AIActionPlugin.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import { definePlugin } from '../PluginSDK'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/builtin/ClickElementPlugin.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import { definePlugin } from '../PluginSDK'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/builtin/OpenProgramPlugin.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import { definePlugin } from '../PluginSDK'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/builtin/WaitPlugin.js
- Type/category: JS
- Declarations: L46: const sec = Number(formData.seconds)
- Imports/style dependencies (first six): import { definePlugin } from '../PluginSDK'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/plugins/custom/SendEmailPlugin.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import { definePlugin } from '@/plugins/PluginSDK'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/presets/Noir.js
- Type/category: JS
- Declarations: L4: const Noir = definePreset(Aura, {
- Imports/style dependencies (first six): import { definePreset } from '@primevue/themes'; import Aura from '@primevue/themes/aura'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/router/index.js
- Type/category: JS
- Declarations: L5: const HomeView = () => import('../views/shared/HomeView.vue'); L6: const AboutView = () => import('../views/shared/AboutView.vue'); L8: const LoginView = () => import('../views/accounts/LoginView.vue'); L9: const ProfileView = () => import('../views/accounts/ProfileView.vue'); L10: const AuthCallback = () => import('../views/accounts/AuthCallback.vue'); L13: const LearningView = () => import('../views/learning/LearningView.vue'); L15: const Dashboard = () => import('../views/core/DashboardView.vue'); L17: const ScraperView = () => import('@/views/scraper/ScraperView.vue'); L19: const AIChat = () => import('@/views/ai/AIChat.vue'); L20: const AIControl = () => import('@/views/ai/AIControl.vue'); L21: const SettingsView = () => import('@/views/core/Settings.vue'); L22: const GoalsView = () => import('@/views/goals/Goals.vue')
- Imports/style dependencies (first six): import { createRouter, createWebHistory } from 'vue-router'; import NProgress from 'nprogress'; import 'nprogress/nprogress.css'; import { useUserStore } from '@/stores/accounts/user'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Accounts/usersAccounts.js
- Type/category: JS
- Declarations: L4: const API_URL = 'http://127.0.0.1:8000/api'; L6: export const usersAccountsAPI = {
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/AI/Ai.js
- Type/category: JS
- Declarations: L5: export const sendMessage = async ({ message, conversation_id = null, provider = null, model = '', ...options }) => {; L13: export const streamMessage = async ({ message, conversation_id = null, provider = null, model = '', onChunk, signal, ...options }) => {; L22: export const getConversations = async () => (await api.get(endpoints.ai.conversations)).data; L23: export const getConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data; L24: export const createConversation = async (payload = {}) => (await api.post(endpoints.ai.conversations, payload)).data; L25: export const deleteConversation = async (id) => { await api.delete(endpoints.ai.conversation(id)); return true }; L26: export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data; L27: export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data
- Imports/style dependencies (first six): import AIService from './AIService'; import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/AI/aiControl.js
- Type/category: JS
- Declarations: L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || []); L6: export const getAISettings = async () => (await api.get(endpoints.ai.settings)).data; L7: export const updateAISettings = async (payload) =>; L10: export const getCredentials = async () => unwrap((await api.get(endpoints.ai.credentials)).data); L11: export const saveCredential = async (payload) =>; L13: export const deleteCredential = async (provider) => {; L18: export const getProviderModels = async (provider, force = false) =>; L20: export const testProviderConnection = async (provider, model = '') =>; L22: export const listAIProviders = async () => (await api.get(endpoints.ai.providers)).data; L23: export const getAIUsage = async () => (await api.get(endpoints.ai.usage)).data; L24: export const listAIExecutions = async () => (await api.get(endpoints.ai.executions)).data; L25: export const listAIBudgets = async () => unwrap((await api.get(endpoints.ai.budgets)).data)
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/AI/aiPlatformService.js
- Type/category: JS
- Declarations: L4: export const getSettings = aiControl.getAISettings; L5: export const saveSettings = aiControl.updateAISettings; L6: export const listCredentials = aiControl.getCredentials; L7: export const saveCredential = aiControl.saveCredential; L8: export const deleteCredential = aiControl.deleteCredential; L9: export const testProvider = aiControl.testProviderConnection; L10: export const listProviders = aiControl.listAIProviders; L11: export const listProviderModels = aiControl.getProviderModels; L12: export const getHealth = aiControl.getAIHealth; L13: export const getCapabilities = aiControl.getAICapabilities; L14: export const getUsage = aiControl.getAIUsage; L15: export const listExecutions = aiControl.listAIExecutions
- Imports/style dependencies (first six): import aiControl from './aiControl'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/AI/AIService.js
- Type/category: JS
- Declarations: L6: function buildPayload(messages, model = '', options = {}) {; L7: const history = Array.isArray(messages) ? messages : []; L8: const latestUser = [...history].reverse().find((item) => item?.role === 'user' && item?.content?.trim()); L10: const payload = { message: latestUser.content.trim() }; L14: const systemMessage = history.find((item) => item?.role === 'system' && item?.content?.trim()); L27: const error = new Error(data.error || 'AI request failed.'); L34: const body = error?.response?.data; L42: const payload = buildPayload(messages, model, options); L43: const accessToken = await getValidAccessToken(); L46: const baseURL = String(api.defaults.baseURL || '').replace(/\/+$/, ''); L47: const streamPath = endpoints.ai.chatStream.startsWith('/'); L50: const response = await fetch(`${baseURL}${streamPath}`, {
- Imports/style dependencies (first six): import api, { getValidAccessToken } from '../Shared/api'; import { endpoints } from '../Shared/endpoints'; import { consumeSSEStream } from './sse'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/AI/sse.js
- Type/category: JS
- Declarations: L2: export function parseSSEEvent(block) {; L4: const data = []; L7: const separator = rawLine.indexOf(':'); L8: const field = separator < 0 ? rawLine : rawLine.slice(0, separator); L15: const raw = data.join('\n'); L23: export async function consumeSSEStream(stream, onEvent) {; L24: const reader = stream.getReader(); L25: const decoder = new TextDecoder(); L27: const dispatch = (block) => {; L28: const event = parseSSEEvent(block)
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/AI/__tests__/AIService.spec.js
- Type/category: JS test source
- Declarations: L6: function streamFrom(parts) {; L7: const encoder = new TextEncoder(); L19: const events = []; L20: const stream = streamFrom([; L34: const callback = vi.fn()
- Imports/style dependencies (first six): import { describe, expect, it, vi } from 'vitest'; import { ReadableStream } from 'node:stream/web'; import { TextEncoder } from 'node:util'; import { consumeSSEStream, parseSSEEvent } from '../sse'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Automation/AutomationService.js
- Type/category: JS
- Declarations: L60: const q = programId ? `?program=${programId}` : ''; L121: const q = workflowId ? `?workflow=${workflowId}` : ''; L152: const q = workflowId ? `?workflow=${workflowId}` : ''; L172: const q = nodeId ? `?node=${nodeId}` : ''; L233: const q = taskRunId ? `?task_run=${taskRunId}` : ''
- Imports/style dependencies (first six): import api from '../Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Automation/nodeStorageService.js
- Type/category: JS
- Declarations: L3: const STORAGE_KEY = 'vueflow_graph'; L10: function read() {; L11: const raw = localStorage.getItem(STORAGE_KEY); L16: const parsed = JSON.parse(raw); L27: function write(graph) {; L36: export function getGraph() {; L41: export function getOne(id) {; L42: const graph = read(); L46: export function getEdge(id) {; L47: const graph = read(); L51: export function createNode(node) {; L52: const graph = read()
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Automation/taskService.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import api from '../Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Automation/workflowService.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import api from '../Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Challenges/challenges.js
- Type/category: JS
- Declarations: L3: const data = r => r?.data ?? r; L4: const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || []); L5: export const challengesApi = { list:()=>api.get(e.challenges).then(list), create:p=>api.post(e.challenges,p).then(data), update:(id,p)=>api.patch(`${e.challenges}${id}/`,p).then(data), remove:id=>api.delete(`${e.challenges}${id}/`) }
- Imports/style dependencies (first six): import api from '@/services/Shared/api'; import { domainEndpoints as e } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Codex/codex.js
- Type/category: JS
- Declarations: L4: const list = (data) =>; L7: const data = async (request) => (await request).data
- Imports/style dependencies (first six): import api from '@/services/Shared/api'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Core/dashboard.js
- Type/category: JS
- Declarations: L4: export const dashboardService = {; L6: const response = await api.get(endpoints.core.dashboard)
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Core/settings.js
- Type/category: JS
- Declarations: L2: export const getLearningSettings = async () => (await api.get('/core/learning-settings/')).data; L3: export const updateLearningSettings = async (payload) => (await api.patch('/core/learning-settings/', payload)).data
- Imports/style dependencies (first six): import api from '../Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Finance/finance.js
- Type/category: JS
- Declarations: L3: const data = r => r?.data ?? r; L4: const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || []); L5: export const financeApi = {
- Imports/style dependencies (first six): import api from '@/services/Shared/api'; import { domainEndpoints as e } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Goals/goals.js
- Type/category: JS
- Declarations: L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || []); L6: export const listGoalsPage = async (params = {}) => (await api.get(endpoints.goals.list, { params })).data; L7: export const listGoals = async (params = {}) => unwrap(await listGoalsPage(params)); L8: export const getGoal = async (id) => (await api.get(endpoints.goals.detail(id))).data; L9: export const getGoalAnalytics = async () => (await api.get(endpoints.goals.analytics)).data; L10: export const createGoal = async (payload) => (await api.post(endpoints.goals.list, payload)).data; L11: export const updateGoal = async (id, payload) => (await api.patch(endpoints.goals.detail(id), payload)).data; L12: export const deleteGoal = async (id) => { await api.delete(endpoints.goals.detail(id)); return true }; L13: export const completeGoal = async (id, notes = '') => (await api.post(endpoints.goals.complete(id), { notes })).data; L14: export const pauseGoal = async (id) => (await api.post(endpoints.goals.pause(id))).data; L15: export const resumeGoal = async (id) => (await api.post(endpoints.goals.resume(id))).data; L16: export const archiveGoal = async (id) => (await api.post(endpoints.goals.archive(id))).data
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Jobs/jobs.js
- Type/category: JS
- Declarations: L4: const list = (data) => (Array.isArray(data) ? data : data?.results || []); L5: const dataOf = async (request) => (await request).data; L7: export const listJobs = async (params = {}) =>; L9: export const getJob = async (id) => dataOf(api.get(endpoints.jobs.opportunity(id))); L10: export const createJob = async (payload) => dataOf(api.post(endpoints.jobs.opportunities, payload)); L11: export const updateJob = async (id, payload) =>; L13: export const deleteJob = async (id) => {; L17: export const refreshJobMatch = async (id) => dataOf(api.post(endpoints.jobs.refreshMatch(id))); L18: export const analyzeJob = async (id) => dataOf(api.post(endpoints.jobs.analyze(id))); L19: export const getReadiness = async (id) => dataOf(api.get(endpoints.jobs.opportunityReadiness(id))); L20: export const listSimilarJobs = async (id) => list(await dataOf(api.get(endpoints.jobs.similar(id)))); L21: export const compareJobs = async (ids) =>
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Knowledge/Knowledge.js
- Type/category: JS
- Declarations: L8: export const knowledgeService = {; L13: const response = await api.get(endpoints.knowledge.items, {; L24: const response = await api.get(endpoints.knowledge.item(id)); L32: const response = await api.post(endpoints.knowledge.items, data); L40: const response = await api.patch(endpoints.knowledge.item(id), data); L49: const response = await api.post(endpoints.knowledge.extractMetadata(id)); L57: const response = await api.post(endpoints.knowledge.archive(id)); L62: const response = await api.post(endpoints.knowledge.restore(id)); L75: const response = await api.get(endpoints.knowledge.itemFiles(knowledgeId)); L84: const formData = new FormData(); L89: const response = await api.post(endpoints.knowledge.uploadFile(knowledgeId), formData, {; L101: const uploaded = []
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Learning/learning.js
- Type/category: JS
- Declarations: L8: const normalizeList = (data) => {; L20: const getErrorMessage = (error, fallback = 'Something went wrong.') => {; L33: export async function getLearningDashboard() {; L73: export async function getLearningTopic(topicId) {; L74: const response = await api.get(endpoints.learning.topic(topicId)); L79: export async function createLearningTopic(payload) {; L80: const response = await api.post(endpoints.learning.topics, payload); L85: export async function updateLearningTopic(topicId, payload) {; L86: const response = await api.patch(endpoints.learning.topic(topicId), payload); L91: export async function deleteLearningTopic(topicId) {; L95: export async function startLearningTopic(topicId) {; L96: const response = await api.post(endpoints.learning.topicStart(topicId))
- Imports/style dependencies (first six): import api from '@/services/Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Memory/memory.js
- Type/category: JS
- Declarations: L3: const data = r => r?.data ?? r; L4: const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || []); L5: export const memoryApi = { list:()=>api.get(e.memory).then(list), create:p=>api.post(e.memory,p).then(data), update:(id,p)=>api.patch(`${e.memory}${id}/`,p).then(data), remove:id=>api.delete(`${e.memory}${id}/`) }
- Imports/style dependencies (first six): import api from '@/services/Shared/api'; import { domainEndpoints as e } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Notifications/notifications.js
- Type/category: JS
- Declarations: L4: const listOf = (response) => response?.data?.results ?? response?.data ?? []; L5: const dataOf = (response) => response?.data; L7: export const listNotifications = async (params = {}) => listOf(await api.get(endpoints.notifications.list, { params })); L8: export const unreadCount = async () => dataOf(await api.get(endpoints.notifications.unreadCount)); L9: export const markRead = async (id) => dataOf(await api.post(endpoints.notifications.read(id))); L10: export const markAllRead = async () => dataOf(await api.post(endpoints.notifications.readAll)); L11: export const archiveNotification = async (id) => {; L15: export const updateNotification = async (id, payload) => dataOf(await api.patch(endpoints.notifications.detail(id), payload)); L16: export const deleteNotification = async (id) => {
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Projects/projects.js
- Type/category: JS
- Declarations: L4: const unwrap = (payload) => (Array.isArray(payload) ? payload : payload?.results || []); L6: export const listProjectsPage = async (params = {}) =>; L8: export const listProjects = async (params = {}) => unwrap(await listProjectsPage(params)); L9: export const getProject = async (id) => (await api.get(`${domainEndpoints.projects}${id}/`)).data; L10: export const createProject = async (payload) =>; L12: export const updateProject = async (id, payload) =>; L14: export const deleteProject = async (id) => {
- Imports/style dependencies (first six): import api from '../Shared/api'; import { domainEndpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Scraper/scraperApi.js
- Type/category: JS
- Declarations: L4: const unwrap = (response) => response.data; L5: const list = (response) => {; L6: const data = response.data; L10: export const scraperApi = {
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/api.js
- Type/category: JS
- Declarations: L5: const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'; L9: const safeLogUrl = (baseURL, requestURL) => {; L10: const raw = `${baseURL || ''}${requestURL || ''}`; L14: const api = axios.create({; L20: const getAccessToken = () => localStorage.getItem('user.access'); L21: const getRefreshToken = () => localStorage.getItem('user.refresh'); L23: const clearAuthStorage = () => {; L30: const notifyAuthExpired = () => {; L37: async function refreshAccessToken() {; L38: const refreshToken = getRefreshToken(); L52: const accessToken = response.data?.access; L53: const rotatedRefreshToken = response.data?.refresh
- Imports/style dependencies (first six): import axios from 'axios'; import NProgress from 'nprogress'; import 'nprogress/nprogress.css'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/axiosInstance.js
- Type/category: JS
- Declarations: L6: const api = axios.create({; L21: const token = localStorage.getItem('auth_token');; L39: const errorMessage = getErrorMessage(error);; L51: function getErrorMessage(error) {; L78: function formatDjangoErrors(data) {; L80: const errors = [];; L94: function triggerGlobalToast(severity, summary, detail) {
- Imports/style dependencies (first six): import axios from 'axios';; import NProgress from 'nprogress';; import 'nprogress/nprogress.css';
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/ecosystemApi.js
- Type/category: JS
- Declarations: L10: const normalizeBase = (base) => `/${String(base).replace(/^\/+|\/+$/g, '')}/`; L11: const withId = (base, id) => `${normalizeBase(base)}${encodeURIComponent(id)}/`; L13: function resource(base) {; L14: const root = normalizeBase(base); L29: export const coreApi = {; L35: export const socialApi = {; L44: export const memoryApi = { items: resource('memory/items') }; L45: export const projectsApi = {; L50: export const challengesApi = {; L56: export const financeApi = {; L82: export const appApi = {
- Imports/style dependencies (first six): import api from './api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/endpoints.js
- Type/category: JS
- Declarations: L8: export const endpoints = {; L345: export const domainEndpoints = {
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/explainsService.js
- Type/category: JS
- Declarations: L4: const explainService = {; L16: const res = await api.get('/explain/explains/'); L42: const res = await api.get('/explain/explains_category/')
- Imports/style dependencies (first six): import api from './api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/mcpService.js
- Type/category: JS
- Declarations: L10: const api = axios.create({; L17: export const mcpService = {
- Imports/style dependencies (first six): import axios from 'axios'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Shared/product_services.js
- Type/category: JS
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import api from './api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Social/social.js
- Type/category: JS
- Declarations: L3: const dataOf = (r) => r?.data?.results ?? r?.data ?? []; L4: export const getSocialProfile = async () => dataOf(await api.get(endpoints.social.profile)); L5: export const updateSocialProfile = async (payload) => dataOf(await api.patch(endpoints.social.profile, payload)); L6: export const getRecommendations = async (params = {}) => dataOf(await api.get(endpoints.social.recommendations, { params })); L7: export const sendFriendRequest = async (id) => dataOf(await api.post(endpoints.social.request(id)))
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/services/Tasks/tasks.js
- Type/category: JS
- Declarations: L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || []); L6: export const listTasks = async (params = {}) => unwrap((await api.get(endpoints.tasks.list, { params })).data); L7: export const listTodayTasks = async () => unwrap((await api.get(endpoints.tasks.today)).data); L8: export const getTask = async (id) => (await api.get(endpoints.tasks.detail(id))).data; L9: export const createTask = async (payload) => (await api.post(endpoints.tasks.list, payload)).data; L10: export const updateTask = async (id, payload) => (await api.patch(endpoints.tasks.detail(id), payload)).data; L11: export const deleteTask = async (id) => { await api.delete(endpoints.tasks.detail(id)); return true }; L12: export const completeTask = async (id, actual_minutes) => (await api.post(endpoints.tasks.complete(id), { actual_minutes })).data; L13: export const postponeTask = async (id, until) => (await api.post(endpoints.tasks.postpone(id), { until })).data; L14: export const generateTodayTasks = async (payload={}) => (await api.post(endpoints.tasks.generate, payload)).data; L15: export const startTask = async (id) => (await api.post(endpoints.tasks.start(id))).data; L16: export const cancelTask = async (id) => (await api.post(endpoints.tasks.cancel(id))).data
- Imports/style dependencies (first six): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/accounts/user.js
- Type/category: JS
- Declarations: L9: const ACCESS_TOKEN_KEY = 'user.access'; L10: const REFRESH_TOKEN_KEY = 'user.refresh'; L11: const USER_KEY = 'user.info'; L16: const defaultUser = () => ({; L48: export const useUserStore = defineStore('user', {; L127: const accessToken = event.detail?.access; L128: const refreshToken = event.detail?.refresh; L140: const access = localStorage.getItem(ACCESS_TOKEN_KEY); L142: const refresh = localStorage.getItem(REFRESH_TOKEN_KEY); L144: const storedUser = localStorage.getItem(USER_KEY); L172: const parsedUser = JSON.parse(storedUser); L199: const response = await api.get('/users/me/')
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import api from '@/services/Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/ai/useAIStore.js
- Type/category: JS
- Declarations: L5: const asArray = (value) => Array.isArray(value) ? value : value?.results || []; L7: export const useAIStore = defineStore('ai-management', () => {; L8: const providers = ref([]); L9: const credentials = ref([]); L10: const settings = ref(null); L11: const conversations = ref([]); L12: const executions = ref([]); L13: const usage = ref({}); L14: const budgets = ref([]); L15: const audit = ref([]); L16: const workflows = ref([]); L17: const health = ref(null)
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref } from 'vue'; import aiControl from '@/services/AI/aiControl'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/automation/useProgramElementStore.js
- Type/category: JS
- Declarations: L15: export const useProgramElementStore = defineStore('programElement', () => {; L19: const elements = ref([]); L20: const currentElement = ref(null); L21: const isLoading = ref(false); L23: const form = ref({; L42: const SELECTOR_TYPES = [; L52: const currentElementId = computed(() => currentElement.value?.id ?? null); L54: const elementById = (id) => elements.value.find((e) => e.id === id) ?? null; L57: const elementsByProgram = (programId) => elements.value.filter((e) => e.program === programId); L62: function validateForm(f = form.value) {; L69: function validateImageSize(file, maxMB = 5) {; L79: function buildFormData(f = form.value) {
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import automationService from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/automation/useProgramStore.js
- Type/category: JS
- Declarations: L15: export const useProgramStore = defineStore('program', () => {; L19: const programs = ref([]); L20: const currentProgram = ref(null); L21: const isLoading = ref(false); L22: const isScanning = ref(false); L24: const form = ref({; L37: const currentProgramId = computed(() => currentProgram.value?.id ?? null); L39: const programById = (id) => programs.value.find((p) => p.id === id) ?? null; L44: function validateForm(f = form.value) {; L50: function validateImageSize(file, maxMB = 5) {; L60: function buildFormData(f = form.value) {; L61: const fd = new FormData()
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import automationService from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/automation/useTaskStore.js
- Type/category: JS
- Declarations: L16: export const useTaskStore = defineStore('task', () => {; L20: const tasks = ref([]); L21: const currentTask = ref(null); L23: const currentTaskRunId = ref(null); L24: const isLoading = ref(false); L26: const form = ref({; L35: const currentTaskId = computed(() => currentTask.value?.id ?? null); L37: const taskById = (id) => tasks.value.find((t) => t.id === id) ?? null; L40: const tasksByProgram = (programId) => tasks.value.filter((t) => t.program === programId); L45: function validateForm(f = form.value) {; L54: function buildFormData(f = form.value) {; L55: const fd = new FormData()
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import automationService from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/automation/useWorkflowStore.js
- Type/category: JS
- Declarations: L18: export const useWorkflowStore = defineStore('workflow', () => {; L22: const workflows = ref([]); L23: const currentWorkflow = ref(null); L24: const nodes = ref([]); L25: const edges = ref([]); L27: const isLoading = ref(false); L28: const isSaving = ref(false); L29: const isInitialized = ref(false); L31: const formWorkflow = ref({ name: '', description: '', status: 'draft' }); L36: const currentWorkflowId = computed(() => currentWorkflow.value?.id ?? null); L38: const workflowById = (id) => workflows.value.find((w) => w.id === id) ?? null; L43: function mapNode(n) {
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import { debounce } from 'lodash'; import dagre from 'dagre'; import automationService from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/codex/codex.js
- Type/category: JS
- Declarations: L4: export const useCodexStore = defineStore('codex', {; L83: const result = await codex.bootstrap(); L106: const result = await codex.registry.bootstrap(); L111: const result = await codex.scan()
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import codex from '@/services/Codex/codex'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/goals/goalsStore.js
- Type/category: JS
- Declarations: L5: export const useGoalsStore = defineStore('goals', () => {; L6: const items = ref([]); L7: const analytics = ref(null); L8: const count = ref(0); L9: const next = ref(null); L10: const previous = ref(null); L11: const loading = ref(false); L12: const analyticsLoading = ref(false); L13: const error = ref(null); L15: async function fetchGoals(params = {}) {; L19: const pageData = await goalApi.listGoalsPage(params); L33: async function fetchAnalytics() {
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref } from 'vue'; import * as goalApi from '@/services/Goals/goals'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/goals/__tests__/goalsStore.spec.js
- Type/category: JS test source
- Declarations: L20: const store = useGoalsStore(); L30: const failure = new Error('API unavailable'); L32: const store = useGoalsStore()
- Imports/style dependencies (first six): import { beforeEach, describe, expect, it, vi } from 'vitest'; import { createPinia, setActivePinia } from 'pinia'; import { useGoalsStore } from '../goalsStore'; import * as goalApi from '@/services/Goals/goals'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/knowledge/knowledgeStore.js
- Type/category: JS
- Declarations: L5: function unwrapList(payload) {; L13: function splitFiles(data = {}) {; L15: const pending = Array.isArray(files) ? files.filter((f) => typeof File !== 'undefined' && f instanceof File) : []; L19: export const useKnowledgeStore = defineStore('knowledge', () => {; L20: const items = ref([]); L21: const count = ref(0); L22: const next = ref(null); L23: const previous = ref(null); L24: const filesByKnowledgeId = ref({}); L25: const loading = ref(false); L26: const saving = ref(false); L27: const error = ref(null)
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref } from 'vue'; import { knowledgeService } from '@/services/Knowledge/Knowledge'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/knowledge/__tests__/knowledgeStore.spec.js
- Type/category: JS test source
- Declarations: L33: const store = useKnowledgeStore(); L42: const store = useKnowledgeStore(); L53: const store = useKnowledgeStore(); L63: const store = useKnowledgeStore(); L69: const store = useKnowledgeStore(); L70: const file = new File(['content'], 'guide.pdf'); L81: const store = useKnowledgeStore()
- Imports/style dependencies (first six): import { beforeEach, describe, expect, it, vi } from 'vitest'; import { createPinia, setActivePinia } from 'pinia'; import { useKnowledgeStore } from '../knowledgeStore'; import { knowledgeService } from '@/services/Knowledge/Knowledge'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/projects/projects.js
- Type/category: JS
- Declarations: L5: export const useProjectsStore = defineStore('projects', () => {; L6: const items = ref([]); L7: const count = ref(0); L8: const next = ref(null); L9: const previous = ref(null); L10: const loading = ref(false); L11: const saving = ref(false); L12: const error = ref(null); L14: async function fetchProjects(params = {}) {; L18: const page = await projectsApi.listProjectsPage(params); L32: async function getProject(id) {; L36: async function createProject(payload) {
- Imports/style dependencies (first six): import { defineStore } from 'pinia'; import { ref } from 'vue'; import * as projectsApi from '@/services/Projects/projects'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/shared/counter.js
- Type/category: JS
- Declarations: L4: export const useCounterStore = defineStore('counter', () => {; L5: const count = ref(0); L6: const doubleCount = computed(() => count.value * 2); L7: function increment() {
- Imports/style dependencies (first six): import { ref, computed } from 'vue'; import { defineStore } from 'pinia'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/stores/shared/primeTheme.js
- Type/category: JS
- Declarations: L4: const _appState = reactive({ theme: 'Aura', darkTheme: false })
- Imports/style dependencies (first six): import { reactive } from 'vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/utils/apiError.js
- Type/category: JS
- Declarations: L1: export function getApiErrorMessage(error, fallback = 'Something went wrong.') {; L2: const data = error?.response?.data; L8: const first = Object.values(data).flat?.()[0]; L15: export function isAuthError(error) {
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/accounts/auth-callback.vue
- Type/category: VUE
- Declarations: L14: const response = await api.get('/users/me/')
- Imports/style dependencies (first six): import api from '@/services/Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/accounts/AuthCallback.vue
- Type/category: VUE
- Declarations: L13: const route = useRoute(); L14: const router = useRouter(); L15: const userStore = useUserStore(); L18: const access = route.query.access; L19: const refresh = route.query.refresh; L25: const userData = {
- Imports/style dependencies (first six): import { onMounted } from 'vue'; import { useRoute, useRouter } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import axios from 'axios'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/accounts/LoginView.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): import LoginForm from '@/components/accounts/LoginForm.vue'; import SignupForm from '@/components/accounts/SignupForm.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/accounts/ProfileView.vue
- Type/category: VUE
- Declarations: L10: const route = useRoute(); L11: const userStore = useUserStore(); L17: const user = ref(null); L18: const storeReady = ref(false); L19: const loadingProfile = ref(false); L20: const savingProfile = ref(false); L26: const sidebar_open = ref(false); L27: const activeTab = ref('1'); L33: const can_send_friendship_request = ref(false); L39: const formInfo = ref({; L54: const selectedImageAvatarFile = ref(null); L55: const selectedImageCoverFile = ref(null)
- Imports/style dependencies (first six): import { ref, computed, watch, onMounted } from 'vue'; import { useRoute } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'; import ImageCropperDialog from '@/components/accounts/ImageCropperDialog.vue'; import fallbackImage from '@/assets/Images/Page_Not_Found/404.jpg'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/ai/AgentPlanner.vue
- Type/category: VUE
- Declarations: L52: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L53: const request = ref(''); L54: const planning = ref(false), selecting = ref(false), proposing = ref(false); L55: const error = ref(''), proposalError = ref(''); L56: const result = ref(null), selection = ref(null), proposal = ref(null); L57: const task = reactive({ title: '', description: '', priority: 'medium' }); L58: const stepsText = ref(''); L59: const priorityOptions = [{ label: 'Ù…Ù†Ø®ÙØ¶Ø©', value: 'low' }, { label: 'Ù…ØªÙˆØ³Ø·Ø©', value: 'medium' }, { label: 'Ø¹Ø§Ù„ÙŠØ©', value: 'high' }, { label: 'Ø¹Ø§Ø¬Ù„Ø©', value: 'urgent' }]; L61: async function plan() {; L68: async function selectAgent() {; L75: async function createProposal() {
- Imports/style dependencies (first six): import { computed, reactive, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Textarea from 'primevue/textarea'; import InputText from 'primevue/inputtext'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/ai/AI.vue
- Type/category: VUE
- Declarations: L125: const providerOptions = [; L132: const settings = ref({ preferred_provider: 'ollama', preferred_model: '' }); L133: const selectedProvider = ref('ollama'); L134: const selectedModel = ref(''); L135: const apiKey = ref(''); L136: const credentials = ref([]); L137: const providerRows = ref([]); L138: const modelOptions = ref([]); L139: const providerMessage = ref(null); L140: const chatError = ref(''); L141: const planError = ref(''); L142: const messages = ref([])
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Message from 'primevue/message'; import Password from 'primevue/password'; import Select from 'primevue/select'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/ai/AIChat.vue
- Type/category: VUE
- Declarations: L547: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L549: const HelpButton = defineComponent({; L572: const helpCopy = {; L631: const sidebarCollapsed = ref(false); L632: const settingsOpen = ref(false); L633: const contextDialog = ref(false); L634: const contextLoading = ref(false); L635: const conversationContext = ref(null); L636: const contextError = ref(''); L637: const settingsTab = ref('general'); L638: const settingsTabs = [; L644: const conversations = ref([])
- Imports/style dependencies (first six): import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'; import aiControl from '@/services/AI/aiControl'; import { sendMessage as sendNonStreamingMessage, streamMessage } from '@/services/AI/Ai'; import MarkdownRenderer from '@/components/ai/MarkdownRenderer.vue'; import { useI18n } from 'vue-i18n'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/ai/AIControl.vue
- Type/category: VUE
- Declarations: L144: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L146: const providerOptions = [; L153: const settings = ref({ preferred_provider: 'ollama', preferred_model: '' }); L154: const selectedProvider = ref('ollama'); L155: const selectedModel = ref(''); L157: const credentials = ref([]); L158: const providerRows = ref([]); L159: const modelOptions = ref([]); L160: const providerMessage = ref(null); L161: const chatError = ref(''); L162: const planError = ref(''); L163: const messages = ref([])
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import { gsap } from 'gsap'; import { useForm } from 'vee-validate'; import { toTypedSchema } from '@vee-validate/zod'; import { z } from 'zod'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/ai/AIOperationsView.vue
- Type/category: VUE
- Declarations: L196: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L197: const store = useAIStore(); L199: const activeTab = ref('executions'); L200: const errorMessage = ref(''); L201: const budgetDialog = ref(false), workflowDialog = ref(false), runsDialog = ref(false), auditDialog = ref(false); L202: const savingBudget = ref(false), savingWorkflow = ref(false), validatingWorkflow = ref(false), diagnosticsLoading = ref(false), sendingFeedback = ref(false); L203: const workflowRuns = ref([]), selectedRun = ref(null), selectedAudit = ref(null), workflowValidation = ref(null); L204: const feedbackMessage = ref(null); L205: const workflowJson = ref('{\n  "nodes": [],\n  "edges": []\n}'); L206: const workflowForm = reactive({ id: null, name: '', description: '' }); L207: const budgetForm = reactive({ id: null, scope: 'user', scope_key: '', daily_cost_limit: null, monthly_cost_limit: null, daily_token_limit: null, monthly_token_limit: null, enabled: true }); L208: const feedback = reactive({ message_id: null, sentiment: 'like', reason: '', comment: '', feedback_category: '', rating: null })
- Imports/style dependencies (first six): import { onMounted, reactive, ref } from 'vue'; import { computed } from 'vue'; import { useI18n } from 'vue-i18n'; import { storeToRefs } from 'pinia'; import Button from 'primevue/button'; import Card from 'primevue/card'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/AutomationView.vue
- Type/category: VUE
- Declarations: L56: const toast = useToast(); L57: const confirm = useConfirm(); L59: const tracker = useApiTracker(); L60: const programStore = useProgramStore(); L61: const elementStore = useProgramElementStore(); L62: const workflowStore = useWorkflowStore(); L63: const taskStore = useTaskStore(); L69: function useAsyncAction() {; L70: const loading = ref(false); L71: const run = async (apiFn, options = {}) => {; L83: const validErr = validate(); L97: const result = await tracker.execute({ serviceFn: apiFn })
- Imports/style dependencies (first six): import { ref, reactive, watch, onMounted, onUnmounted } from 'vue'; import { useVueFlow } from '@vue-flow/core'; import { debounce } from 'lodash'; import { useToast } from 'primevue/usetoast'; import { useConfirm } from 'primevue/useconfirm'; import { useProgramStore } from '@/stores/automation/useProgramStore'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/DashboardAutomationView.vue
- Type/category: VUE
- Declarations: L24: const tasks = ref([]); L25: const load = async () => {; L26: const res = await taskService.list(); L30: const run = async (id) => {; L31: const res = await taskService.run(id)
- Imports/style dependencies (first six): import { ref, onMounted } from 'vue'; import taskService from '../../services/Automation/taskService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/icon.vue
- Type/category: VUE
- Declarations: L2: defineProps({
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/ProgramCreate.vue
- Type/category: VUE
- Declarations: L136: const form = ref({; L161: const onImageChange = (e) => {; L183: const createProgram = async () => {; L185: const formData = new FormData(); L223: const res = await programService.createProgram(formData)
- Imports/style dependencies (first six): import { ref } from 'vue'; import programService from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/ProgramEdit.vue
- Type/category: VUE
- Declarations: L139: const route = useRoute(); L145: const currentId = ref(null); L150: const form = ref({; L175: const onImageChange = (e) => {; L197: const createProgram = async () => {; L199: const formData = new FormData(); L237: const res = await programService.createProgram(formData); L249: const getExplain = async () => {; L252: const res = await programService.get(currentId.value)
- Imports/style dependencies (first six): import { ref, onMounted } from 'vue'; import { useRoute } from 'vue-router'; import programService from '@/services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/ProgramList.vue
- Type/category: VUE
- Declarations: L21: const programs = ref([]); L22: const load = async () => {; L23: const res = await programService.list(); L26: const open = async (id) => {
- Imports/style dependencies (first six): import { ref, onMounted } from 'vue'; import programService from '../../services/Automation/AutomationService'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/TaskCreate.vue
- Type/category: VUE
- Declarations: L27: const programs = ref([]); L28: const name = ref(''); L29: const programId = ref(''); L30: const actionsJson = ref('[]'); L33: const r = await api.get('automation/programs/'); L37: const create = async () => {; L44: const payload = {; L50: const res = await api.post('automation/tasks/', payload); L51: const taskId = res.data.id; L54: const actions = JSON.parse(actionsJson.value || '[]')
- Imports/style dependencies (first six): import { ref, onMounted } from 'vue'; import api from '../../services/Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/automation/TaskEditor.vue
- Type/category: VUE
- Declarations: L22: const route = useRoute(); L23: const taskId = route.params.id; L24: const task = ref(null); L25: const actions = ref([]); L26: const runs = ref([]); L28: const load = async ()=>{; L29: const t = await api.get(`/tasks/${taskId}/`); L31: const a = await api.get(`/tasks/${taskId}/actions/`); L33: const tr = await api.get(`/taskruns/?task=${taskId}`); L36: const runTask = async ()=>{; L37: const res = await api.post(`/tasks/${taskId}/run/`); L45: const pollLogs = async (run_id) => {
- Imports/style dependencies (first six): import { ref, onMounted } from 'vue'; import api from '../../services/Shared/api'; import { useRoute } from 'vue-router'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/challenges/ChallengesView.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/codex/CodexBuildWorkspace.vue
- Type/category: VUE
- Declarations: L14: const loading = ref(false); L15: const error = ref(''); L16: const payload = ref(null); L17: const selectedNode = ref(null); L18: const nodes = computed(() => payload.value?.graph?.nodes || []); L19: const edges = computed(() => payload.value?.graph?.edges || []); L21: async function refresh() {; L32: function statusSeverity(status) {
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import { VueFlow } from '@vue-flow/core'; import { Background } from '@vue-flow/background'; import { Controls } from '@vue-flow/controls'; import { MiniMap } from '@vue-flow/minimap'; import Button from 'primevue/button'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/codex/CodexCapabilities.spec.js
- Type/category: JS test source
- Declarations: L8: const store = useCodexStore()
- Imports/style dependencies (first six): import { beforeEach, describe, expect, it } from 'vitest'; import { createPinia, setActivePinia } from 'pinia'; import { useCodexStore } from '@/stores/codex/codex'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/codex/CodexCapabilities.vue
- Type/category: VUE
- Declarations: L15: const store = useCodexStore(); L16: const query = ref(''); L17: const busy = ref(false); L18: const validating = ref(false); L19: const selected = ref(null); L20: const result = ref(null); L21: const registryTab = ref('features'); L22: const infoVisible = ref(false); L23: const infoItem = ref(null); L25: function showInfo(item) {; L30: const features = computed(() => filter(store.capabilityFeatures.value || store.capabilityFeatures)); L31: const tools = computed(() => filter(store.capabilityTools.value || store.capabilityTools))
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/codex/CodexView.vue
- Type/category: VUE
- Declarations: L35: const store = useCodexStore(); L36: const router = useRouter(); L38: const activePanel = ref('workspace'); L39: const query = ref(''); L40: const fileQuery = ref(''); L41: const chatInput = ref(''); L42: const busy = ref(false); L43: const loading = ref(true); L44: const errorMessage = ref(''); L45: const successMessage = ref(''); L46: const selectedFile = ref(null); L47: const selectedFiles = ref([])
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import { useRouter } from 'vue-router'; import { useCodexStore } from '@/stores/codex/codex'; import codex from '@/services/Codex/codex'; import CodexSidebar from '@/components/codex/Layout/CodexSidebar.vue'; import CodexRightSidebar from '@/components/codex/Layout/CodexRightSidebar.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/core/DashboardView.vue
- Type/category: VUE
- Declarations: L388: const isOnline = useOnline(); L390: const isDark = useDark(); L393: const dashboard = ref(null); L394: const loading = ref(true); L395: const error = ref(null); L397: const loadDashboard = async () => {; L401: const data = await dashboardService.get(); L420: const selectedRange = ref('Ø´Ù‡Ø±ÙŠ'); L421: const isModalOpen = ref(false); L423: const newItemForm = ref({; L428: const serviceOptions = [; L436: const userName = computed(() => dashboard.value?.user?.name || 'Ù…. Ø­Ø³Ø§Ù… Ø±Ø´Ø§Ø¯ Ø¹Ø¨ÙˆØ¯')
- Imports/style dependencies (first six): import { ref, computed, onMounted } from 'vue'; import { RouterLink } from 'vue-router'; import { useOnline, useDark } from '@vueuse/core'; import { toast } from 'vue-sonner'; import { dashboardService } from '@/services/Core/dashboard'; import {
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/core/MyProgress.vue
- Type/category: VUE
- Declarations: L8: const toast = useAppToast(); L9: const summary=ref({overall_progress:0,topics_total:0,topics_completed:0,goals:[]}),loading=ref(true),error=ref(''); L10: async function load(){loading.value=true;error.value='';try{summary.value=(await api.get('/learning/progress/summary/')).data}catch(e){error.value = getApiErrorMessage(e, 'ØªØ¹Ø°Ø± ØªØ­Ù…ÙŠÙ„ Ø§Ù„ØªÙ‚Ø¯Ù….')}finally { loading.value = false }}
- Imports/style dependencies (first six): import { onMounted, ref } from 'vue'; import { useAppToast } from '@/composables/useAppToast'; import { getApiErrorMessage } from '@/utils/apiError'; import api from '@/services/Shared/api'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/core/Settings.vue
- Type/category: VUE
- Declarations: L145: const providers = ['ollama', 'openai', 'openrouter'],; L169: async function load() {; L173: const g = await api.get('/learning/goals/'); L182: async function loadModels() {; L185: const r = await getProviderModels(settings.preferred_provider); L194: async function save() {; L204: async function saveLearning() {; L214: async function addCredential() {; L224: async function removeCredential(p) {; L232: async function createPrompt() {; L243: async function deletePromptProfile(id) {
- Imports/style dependencies (first six): import { onMounted, reactive, ref, watch } from 'vue'; import api from '@/services/Shared/api'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Select from 'primevue/select'; import Checkbox from 'primevue/checkbox'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/finance/FinanceView.vue
- Type/category: VUE
- Declarations: L243: const toast = useToast(); L244: const confirm = useConfirm(); L246: const loading = ref(false); L247: const saving = ref(false); L248: const aiLoading = ref(false); L249: const coachLoading = ref(false); L250: const apiChecking = ref(false); L252: const pageError = ref(''); L254: const section = ref('overview'); L256: const sections = [; L272: const summary = ref({}); L273: const dashboard = ref({})
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import { useConfirm } from 'primevue/useconfirm'; import { useToast } from 'primevue/usetoast'; import api from '@/services/Shared/api'; import { financeApi } from '@/services/Finance/finance'; import FinanceHero from '@/components/finance/FinanceHero.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/goals/Goals.vue
- Type/category: VUE
- Declarations: L128: const store = useGoalsStore(); L129: const toast = useAppToast(); L130: const search = ref(''); L131: const statusFilter = ref(null); L132: const categoryFilter = ref(null); L133: const sortBy = ref('-created_at'); L134: const page = ref(1); L135: const pageSize = 20; L136: const editorVisible = ref(false); L137: const detailsVisible = ref(false); L138: const milestoneVisible = ref(false); L139: const proposalVisible = ref(false)
- Imports/style dependencies (first six): import { computed, onMounted, reactive, ref, watch } from 'vue'; import { useGoalsStore } from '@/stores/goals/goalsStore'; import { useAppToast } from '@/composables/useAppToast'; import * as goalApi from '@/services/Goals/goals'; import { createTask, listTasks } from '@/services/Tasks/tasks'; import { getLearningGoals } from '@/services/Learning/learning'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/jobs/JobsView.vue
- Type/category: VUE
- Declarations: L582: const activeTab = ref('jobs'); L583: const busy = ref(false); L584: const loading = ref(false); L585: const saving = ref(false); L586: const error = ref(''); L587: const notice = ref(''); L588: const dialog = ref(false); L589: const sourceDialog = ref(false); L590: const timelineDialog = ref(false); L591: const letterDialog = ref(false); L592: const helpDialog = ref(false); L593: const generatedLetter = ref('')
- Imports/style dependencies (first six): import { computed, onMounted, reactive, ref } from 'vue'; import '@/assets/scss/Jobs/JobsView.scss'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Message from 'primevue/message'; import InputText from 'primevue/inputtext'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/knowledge/knowledgeView.vue
- Type/category: VUE
- Declarations: L22: const knowledgeStore = useKnowledgeStore(); L24: const saving = ref(false); L25: const extractingMetadata = ref(false); L27: const error = ref(''); L28: const successMessage = ref(''); L30: const searchQuery = ref(''); L31: const selectedType = ref('all'); L33: const showForm = ref(false); L34: const editingKnowledge = ref(null); L37: const viewDialogVisible = ref(false); L38: const selectedKnowledge = ref(null); L40: const knowledgeTypes = [
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import {; import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'; import { storeToRefs } from 'pinia'; import { useKnowledgeStore } from '@/stores/knowledge/knowledgeStore'; import KnowledgeCard from '@/components/knowledge/KnowledgeCard.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/learning/LearningTopic.vue
- Type/category: VUE
- Declarations: L28: const route = useRoute(); L34: const loading = ref(true); L35: const error = ref(''); L37: const topic = ref(null); L39: const activeApplication = ref(null); L40: const activeReference = ref(null); L42: const lessonCompleted = ref(false); L43: const quickCheckStarted = ref(false); L44: const quickCheckCompleted = ref(false); L45: const finalAssessmentCompleted = ref(false); L47: const personalNote = ref(''); L48: const personalNoteId = ref(null)
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import api from '@/services/Shared/api'; import { endpoints } from '@/services/Shared/endpoints'; import { RouterLink, useRoute } from 'vue-router'; import {; import ApplicationComposer from '@/components/learning/ApplicationComposer.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/learning/LearningView.vue
- Type/category: VUE
- Declarations: L10: const loading = ref(true); L11: const refreshing = ref(false); L12: const error = ref(''); L14: const skills = ref([]); L15: const goals = ref([]); L16: const paths = ref([]); L17: const topics = ref([]); L18: const progress = ref([]); L19: const assessments = ref([]); L20: const attempts = ref([]); L21: const applications = ref([]); L22: const revisions = ref([])
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import { RouterLink } from 'vue-router'; import { getLearningDashboard, updateLearningProgress, pauseLearningGoal, resumeLearningGoal } from '@/services/Learning/learning'; import LearningPathEditor from '@/components/learning/LearningPathEditor.vue'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/memory/MemoryView.vue
- Type/category: VUE
- Declarations: L43: const items = ref([]),; L48: const load = async () => {; L56: const create = async () => {; L63: const remove = async (id) => {
- Imports/style dependencies (first six): import { onMounted, ref } from 'vue'; import Card from 'primevue/card'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Button from 'primevue/button'; import Dialog from 'primevue/dialog'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/notifications/NotificationsView.vue
- Type/category: VUE
- Declarations: L4: const items = ref([]); const loading = ref(true); L5: const load = async () => { loading.value = true; try { items.value = await listNotifications() } finally { loading.value = false } }; L6: const read = async (item) => { if (!item.read_at) { await markRead(item.id); item.read_at = new Date().toISOString() } }; L7: const readAll = async () => { await markAllRead(); items.value.forEach(x => x.read_at = new Date().toISOString()) }; L8: const archive = async (item) => { await archiveNotification(item.id); items.value = items.value.filter(x => x.id !== item.id) }
- Imports/style dependencies (first six): import { onMounted, ref } from 'vue'; import { listNotifications, markAllRead, markRead, archiveNotification } from '@/services/Notifications/notifications'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/projects/ProjectsView.vue
- Type/category: VUE
- Declarations: L135: const store = useProjectsStore(); L136: const toast = useToast(); L137: const search = ref(''); L138: const statusFilter = ref(null); L139: const sortBy = ref('-updated_at'); L140: const dialogVisible = ref(false); L141: const detailsVisible = ref(false); L142: const detailsLoading = ref(false); L143: const selectedProject = ref(null); L144: const editing = ref(null); L145: const deletingId = ref(null); L146: const formError = ref('')
- Imports/style dependencies (first six): import { computed, onMounted, reactive, ref, watch } from 'vue'; import { useProjectsStore } from '@/stores/projects/projects'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Column from 'primevue/column'; import DataTable from 'primevue/datatable'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/scraper/ScraperView.vue
- Type/category: VUE
- Declarations: L99: const sources = ref([]); L100: const runs = ref([]); L101: const stats = ref({}); L102: const loading = ref(false); L103: const saving = ref(false); L104: const busyId = ref(null); L105: const error = ref(''); L106: const message = ref(''); L107: const dialogOpen = ref(false); L108: const editingId = ref(null); L109: const form = reactive({ name: '', base_url: '', description: '', source_type: 'json', is_active: true, config: { items_path: '', item_selector: '', fields_json: '{}', ai_analyze_on_import: false, terms_confirmed: false } }); L110: const resultsDialogOpen = ref(false)
- Imports/style dependencies (first six): import { onMounted, onUnmounted, reactive, ref } from 'vue'; import { scraperApi } from '@/services/Scraper/scraperApi'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/shared/AboutView.vue
- Type/category: VUE
- Declarations: L5: const activeTab = ref('vue'); L6: const isInspectMode = ref(true); L7: const currentTarget = ref('HeaderBar Component'); L8: const toastMessage = ref(''); L9: const showToast = ref(false); L12: const codeSnippets = {; L18: const route = useRoute(); L19: const username = ref('Eng. Ahmed'); L20: const systemStatus = ref('Operational'); L22: function refreshTelemetry() {; L39: class TelemetryStreamView(APIView):; L59: const frame = JSON.parse(event.data)
- Imports/style dependencies (first six): import { ref, onMounted } from 'vue'; import { ref } from 'vue'; import { useRoute } from 'vue-router'; import { useWebSocket } from '@vueuse/core'; import { z } from 'zod'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/shared/HomeView.vue
- Type/category: VUE
- Declarations: L13: const sidebarOpen = ref(true); L15: const toggleSidebar = () => {; L19: const closeSidebarOnMobile = () => {; L31: const menuItems = [; L105: const dashboard = ref(null); L106: const loading = ref(true); L107: const error = ref(null); L115: const loadDashboard = async () => {; L120: const data = await dashboardService.get(); L144: const userName = computed(() => {; L148: const userEmail = computed(() => {; L152: const userInitials = computed(() => {
- Imports/style dependencies (first six): import { ref, computed, onMounted, onBeforeUnmount } from 'vue'; import { RouterLink } from 'vue-router'; import { dashboardService } from '@/services/Core/dashboard'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/shared/Page_Not_Found.vue
- Type/category: VUE
- Declarations: no matched top-level declaration
- Imports/style dependencies (first six): none matched
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/social/SocialView.vue
- Type/category: VUE
- Declarations: L4: const recommendations = ref([]); const profile = ref({ learning_interests: [], professional_interests: [], topics: [], looking_for: [], bio: '', discoverable: true }); const saving = ref(false); L5: const text = (v) => Array.isArray(v) ? v.join(', ') : v; L6: const parse = (v) => v.split(',').map(x => x.trim()).filter(Boolean); L7: const load = async () => { const p = await getSocialProfile(); profile.value = {...p, learning_interests: text(p.learning_interests), professional_interests: text(p.professional_interests), topics: text(p.topics), looking_for: text(p.looking_for)}; recommendations.value = await getRecommendations() }; L8: const save = async () => { saving.value = true; try { profile.value = await updateSocialProfile({...profile.value, learning_interests: parse(text(profile.value.learning_interests)), professional_interests: parse(text(profile.value.professional_interests)), topics: parse(text(profile.value.topics)), looking_for: parse(text(profile.value.looking_for))}); recommendations.value = await getRecommendations() } finally { saving.value = false } }; L9: const connect = async (id) => { await sendFriendRequest(id); recommendations.value = recommendations.value.filter(x => x.candidate.id !== id) }
- Imports/style dependencies (first six): import { onMounted, ref } from 'vue'; import { getRecommendations, getSocialProfile, updateSocialProfile, sendFriendRequest } from '@/services/Social/social'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/tasks/TasksCalendar copy.vue
- Type/category: VUE
- Declarations: L6: const cursor = ref(new Date()); L7: const view = ref('week'); L8: const tasks = ref([]); L9: const loading = ref(false); L10: const startOfWeek = (date) => {; L11: const d = new Date(date); L12: const day = d.getDay(); L17: const rangeStart = computed(() =>; L22: const rangeEnd = computed(() =>; L27: const days = computed(() => {; L28: const arr = []; L29: const count = view.value === 'month' ? rangeEnd.value.getDate() : 7
- Imports/style dependencies (first six): import { computed, onMounted, ref } from 'vue'; import { listTasks, createTask, updateTask, completeTask } from '@/services/Tasks/tasks'; import api from '@/services/Shared/api'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/tasks/TasksCalendar.vue
- Type/category: VUE
- Declarations: L14: const cursor = ref(new Date()); L15: const view = ref('week'); L17: const tasks = ref([]); L18: const loading = ref(false); L19: const generating = ref(false); L20: const errorMessage = ref(''); L21: const successMessage = ref(''); L23: const busyTaskIds = ref(new Set()); L24: const requestId = ref(0); L32: const pad = (value) => String(value).padStart(2, '0'); L34: const formatDateKey = (date) => {; L35: const d = new Date(date)
- Imports/style dependencies (first six): import { ref, computed, onMounted, watch } from 'vue'; import {
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## src/views/tasks/TodayTasks.vue
- Type/category: VUE
- Declarations: L138: const tasks = ref([]),; L150: const form = reactive({; L159: const completed = computed(() => tasks.value.filter((t) => t.status === 'completed').length),; L167: const generate = async () => {; L179: const load = async () => {; L190: const reset = () =>; L200: const openCreate = () => {; L205: const editTask = (t) => {; L218: const save = async () => {; L221: const payload = { ...form, scheduled_start: form.scheduled_start || null }; L230: const finish = async (t) => {; L242: const reopen = async (task) => {
- Imports/style dependencies (first six): import { computed, onMounted, reactive, ref } from 'vue'; import {
- Consumers/callers: direct imports are partially discoverable; no complete call graph is claimed.

## Frontend root configuration files
Also relevant: frontend_vue/package.json, package-lock.json, vite.config.js, vitest.config.js, eslint.config.js, postcss.config.js, tailwind.config.js, jsconfig.json, index.html. These are configuration/manifests, not included in the src file count.

## Exclusions
Binary image assets have no source declarations; node_modules and generated distribution/cache output are excluded. Test files are indexed but were not executed.

## Non-code resources not included in the 286 code/style rows

- Two HTML resources: frontend_vue/src/composables/api-flow-demo.html; frontend_vue/src/views/finance/test.html.
- Two Markdown resources (contents not used as architecture evidence): frontend_vue/src/views/automation/Project_Context_Analysis.md; Project_Context_Profile.md.
- Seventeen binary image assets under frontend_vue/src/assets/Images/ (including one .jpg in a SCSS-named directory); binary contents are not parsed.

These resources are tracked separately from the 286 JS/Vue/TS/SCSS/CSS files indexed above.
