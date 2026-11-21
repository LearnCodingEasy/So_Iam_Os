# shared source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/shared/AboutView.vue
- Type: .vue
- Declarations: L5: const activeTab = ref('vue'); L6: const isInspectMode = ref(true); L7: const currentTarget = ref('HeaderBar Component'); L8: const toastMessage = ref(''); L9: const showToast = ref(false); L12: const codeSnippets = {; L18: const route = useRoute(); L19: const username = ref('Eng. Ahmed'); L20: const systemStatus = ref('Operational'); L22: function refreshTelemetry() {; L39: class TelemetryStreamView(APIView):; L59: const frame = JSON.parse(event.data); L67: export const TelemetryFrameSchema = z.object({; L77: const filePathDisplayMap = {; L84: const activeComponentTagMap = {; L92: function switchCodeTab(tab) {; L96: function toggleInspectMode() {; L103: function selectComponent(componentName) {; L104: const mapNames = {; L115: function triggerActionLog(msg) {; L123: function copyCurrentCode() {; L124: const code = codeSnippets[activeTab.value]
- Imports (first five): import { ref, onMounted } from 'vue'; import { ref } from 'vue'; import { useRoute } from 'vue-router'; import { useWebSocket } from '@vueuse/core'; import { z } from 'zod'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/shared/HomeView.vue
- Type: .vue
- Declarations: L13: const sidebarOpen = ref(true); L15: const toggleSidebar = () => {; L19: const closeSidebarOnMobile = () => {; L31: const menuItems = [; L105: const dashboard = ref(null); L106: const loading = ref(true); L107: const error = ref(null); L115: const loadDashboard = async () => {; L120: const data = await dashboardService.get(); L144: const userName = computed(() => {; L148: const userEmail = computed(() => {; L152: const userInitials = computed(() => {; L153: const name = userName.value.trim(); L159: const parts = name.split(/\s+/); L174: const greeting = computed(() => {; L175: const hour = new Date().getHours(); L198: const currentDate = ref(new Date()); L202: const updateClock = () => {; L206: const formattedDate = computed(() => {; L215: const formattedTime = computed(() => {; L228: const stats = computed(() => {; L229: const data = dashboard.value?.stats || {}; L280: const recentKnowledge = computed(() => {; L290: const tasks = computed(() => {; L300: const quickActions = [; L344: const openAI = () => {
- Imports (first five): import { ref, computed, onMounted, onBeforeUnmount } from 'vue'; import { RouterLink } from 'vue-router'; import { dashboardService } from '@/services/Core/dashboard'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/shared/Page_Not_Found.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/api.js
- Type: .js
- Declarations: L5: const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'; L9: const safeLogUrl = (baseURL, requestURL) => {; L10: const raw = `${baseURL || ''}${requestURL || ''}`; L14: const api = axios.create({; L20: const getAccessToken = () => localStorage.getItem('user.access'); L21: const getRefreshToken = () => localStorage.getItem('user.refresh'); L23: const clearAuthStorage = () => {; L30: const notifyAuthExpired = () => {; L37: async function refreshAccessToken() {; L38: const refreshToken = getRefreshToken(); L52: const accessToken = response.data?.access; L53: const rotatedRefreshToken = response.data?.refresh; L91: export async function getValidAccessToken() {; L92: const token = getAccessToken(); L95: const refreshed = await refreshAccessToken(); L104: const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'); L105: const decoded = JSON.parse(atob(payload.padEnd(Math.ceil(payload.length / 4) * 4, '='))); L112: const refreshed = await refreshAccessToken(); L123: const accessToken = getAccessToken(); L160: const duration = response.config?.metadata?.startedAt; L188: const status = error.response?.status; L189: const originalRequest = error.config; L190: const duration = originalRequest?.metadata?.startedAt; L215: const requestPath = String(originalRequest?.url || '').replace(/^\/+/, ''); L216: const isRefreshRequest = requestPath === 'users/refresh/' || requestPath.endsWith('/users/refresh/'); L224: const accessToken = await refreshAccessToken()
- Imports (first five): import axios from 'axios'; import NProgress from 'nprogress'; import 'nprogress/nprogress.css'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/axiosInstance.js
- Type: .js
- Declarations: L6: const api = axios.create({; L21: const token = localStorage.getItem('auth_token');; L39: const errorMessage = getErrorMessage(error);; L51: function getErrorMessage(error) {; L78: function formatDjangoErrors(data) {; L80: const errors = [];; L94: function triggerGlobalToast(severity, summary, detail) {
- Imports (first five): import axios from 'axios';; import NProgress from 'nprogress';; import 'nprogress/nprogress.css';
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/ecosystemApi.js
- Type: .js
- Declarations: L10: const normalizeBase = (base) => `/${String(base).replace(/^\/+|\/+$/g, '')}/`; L11: const withId = (base, id) => `${normalizeBase(base)}${encodeURIComponent(id)}/`; L13: function resource(base) {; L14: const root = normalizeBase(base); L29: export const coreApi = {; L35: export const socialApi = {; L44: export const memoryApi = { items: resource('memory/items') }; L45: export const projectsApi = {; L50: export const challengesApi = {; L56: export const financeApi = {; L82: export const appApi = {
- Imports (first five): import api from './api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/endpoints.js
- Type: .js
- Declarations: L8: export const endpoints = {; L345: export const domainEndpoints = {
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/explainsService.js
- Type: .js
- Declarations: L4: const explainService = {; L16: const res = await api.get('/explain/explains/'); L42: const res = await api.get('/explain/explains_category/')
- Imports (first five): import api from './api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/mcpService.js
- Type: .js
- Declarations: L10: const api = axios.create({; L17: export const mcpService = {
- Imports (first five): import axios from 'axios'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Shared/product_services.js
- Type: .js
- Declarations: none matched
- Imports (first five): import api from './api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/shared/counter.js
- Type: .js
- Declarations: L4: export const useCounterStore = defineStore('counter', () => {; L5: const count = ref(0); L6: const doubleCount = computed(() => count.value * 2); L7: function increment() {
- Imports (first five): import { ref, computed } from 'vue'; import { defineStore } from 'pinia'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/shared/primeTheme.js
- Type: .js
- Declarations: L4: const _appState = reactive({ theme: 'Aura', darkTheme: false })
- Imports (first five): import { reactive } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/GlobalToastNotification.vue
- Type: .vue
- Declarations: L9: const toast = useToast();; L12: const showNotification = (severity, summary, detail) => {
- Imports (first five): import { useToast } from 'primevue/usetoast';; import { provide } from 'vue';
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/HeaderView.vue
- Type: .vue
- Declarations: L14: const router = useRouter(); L15: const route = useRoute(); L16: const userStore = useUserStore(); L18: const sidebarOpen = ref(true); L19: const mobileMenuOpen = ref(false); L20: const profileMenu = ref(null); L21: const searchQuery = ref(''); L23: const menuItems = [; L66: const secondaryItems = [; L72: const userName = computed(() => {; L76: const userEmail = computed(() => userStore.user?.email || ''); L78: const userInitials = computed(() => {; L79: const name = userName.value.trim(); L89: const avatarUrl = computed(() => userStore.user?.avatar_url || null); L91: const currentRouteLabel = computed(() => {; L92: const item = [...menuItems, ...secondaryItems].find((entry) => {; L100: const profileRoute = computed(() => {; L101: const id = userStore.user?.id; L105: const profileMenuItems = computed(() => [; L124: function userProfileRoute() {; L128: function toggleSidebar() {; L132: function closeSidebarOnMobile() {; L139: function toggleProfileMenu(event) {; L143: function submitSearch() {; L144: const query = searchQuery.value.trim(); L153: function logout() {; L159: function handleKeydown(event) {
- Imports (first five): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import { RouterLink, useRoute, useRouter } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import Avatar from 'primevue/avatar'; import Badge from 'primevue/badge'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/HelloWorld.spec.js
- Type: .js
- Declarations: L8: const wrapper = mount(HelloWorld, { props: { msg: 'Hello Vitest' } })
- Imports (first five): import { describe, it, expect } from 'vitest'; import { mount } from '@vue/test-utils'; import HelloWorld from './HelloWorld.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/HelloWorld.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconCommunity.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconDocumentation.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconEcosystem.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconSupport.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconTooling.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/LiveDebugConsole.vue
- Type: .vue
- Declarations: L10: const enabled = import.meta.env.DEV || import.meta.env.VITE_DEBUG_CONSOLE === 'true'; L11: const wsEnabled = import.meta.env.VITE_DEBUG_CONSOLE === 'true'; L12: const WS_URL = import.meta.env.VITE_DEBUG_WS_URL || 'ws://127.0.0.1:8000/ws/debug/'; L13: const MAX_LOGS = 500; L16: const open = ref(false); L17: const minimized = ref(false); L18: const paused = ref(false); L19: const autoScroll = ref(true); L20: const searchQuery = ref(''); L21: const activeFilter = ref('all') // 'all' | 'error' | 'warn' | 'network' | 'pinia'; L24: const logs = ref([]); L25: const status = ref('closed') // 'connecting' | 'connected' | 'closed' | 'error'; L30: const frontendConsoleEl = ref(null); L31: const backendConsoleEl = ref(null); L32: const toastMessage = ref(''); L33: const showToastFlag = ref(false); L36: const filterTabs = [; L45: function showToast(msg) {; L55: async function copyToClipboard(text, successMsg = 'ØªÙ… Ø§Ù„Ù†Ø³Ø® Ø¥Ù„Ù‰ Ø§Ù„Ø­Ø§ÙØ¸Ø© Ø¨Ù†Ø¬Ø§Ø­') {; L65: const addLog = (entry) => {; L68: const normalizedSource = (entry.source || 'APP').toUpperCase(); L69: const normalizedLevel = (entry.level || 'info').toLowerCase(); L70: const formattedPayload = entry.payload ? JSON.stringify(entry.payload, null, 2) : null; L72: const newEntry = {; L96: const targetEl = newEntry.isBackend ? backendConsoleEl.value : frontendConsoleEl.value; L105: function connect() {; L125: const d = JSON.parse(e.data); L154: function disconnect() {; L164: function toggle() {; L172: function onApi(e) {
- Imports (first five): import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'; import Button from 'primevue/button'; import InputText from 'primevue/inputtext'; import IconField from 'primevue/iconfield'; import InputIcon from 'primevue/inputicon'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/ThemeSwitcher.vue
- Type: .vue
- Declarations: L19: const THEME_KEY = 'so_iam_os.theme'; L30: const saved = localStorage.getItem(THEME_KEY); L31: const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches; L32: const isDark = saved ? saved === 'dark' : prefersDark; L33: const root = document.documentElement; L40: const root = document.getElementsByTagName('html')[0]; L41: const isDark = !root.classList.contains('p-dark')
- Imports (first five): import { updatePreset, updateSurfacePalette } from '@primevue/themes'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/TheWelcome.vue
- Type: .vue
- Declarations: L9: const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
- Imports (first five): import WelcomeItem from './WelcomeItem.vue'; import DocumentationIcon from './IconDocumentation.vue'; import ToolingIcon from './IconTooling.vue'; import EcosystemIcon from './IconEcosystem.vue'; import CommunityIcon from './IconCommunity.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/WelcomeItem.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.

