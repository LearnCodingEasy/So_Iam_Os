# shared services and API

Service files found under services/Shared. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Shared/api.js
L5: const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
L9: const safeLogUrl = (baseURL, requestURL) => {
L10: const raw = `${baseURL || ''}${requestURL || ''}`
L14: const api = axios.create({
L20: const getAccessToken = () => localStorage.getItem('user.access')
L21: const getRefreshToken = () => localStorage.getItem('user.refresh')
L23: const clearAuthStorage = () => {
L30: const notifyAuthExpired = () => {
L37: async function refreshAccessToken() {
L38: const refreshToken = getRefreshToken()
L52: const accessToken = response.data?.access
L53: const rotatedRefreshToken = response.data?.refresh
L91: export async function getValidAccessToken() {
L92: const token = getAccessToken()
L95: const refreshed = await refreshAccessToken()
L104: const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
L105: const decoded = JSON.parse(atob(payload.padEnd(Math.ceil(payload.length / 4) * 4, '=')))
L112: const refreshed = await refreshAccessToken()
L123: const accessToken = getAccessToken()
L160: const duration = response.config?.metadata?.startedAt
L188: const status = error.response?.status
L189: const originalRequest = error.config
L190: const duration = originalRequest?.metadata?.startedAt
L215: const requestPath = String(originalRequest?.url || '').replace(/^\/+/, '')
L216: const isRefreshRequest = requestPath === 'users/refresh/' || requestPath.endsWith('/users/refresh/')
L224: const accessToken = await refreshAccessToken()

## services/Shared/axiosInstance.js
L6: const api = axios.create({
L21: const token = localStorage.getItem('auth_token');
L39: const errorMessage = getErrorMessage(error);
L51: function getErrorMessage(error) {
L78: function formatDjangoErrors(data) {
L80: const errors = [];
L94: function triggerGlobalToast(severity, summary, detail) {

## services/Shared/ecosystemApi.js
L10: const normalizeBase = (base) => `/${String(base).replace(/^\/+|\/+$/g, '')}/`
L11: const withId = (base, id) => `${normalizeBase(base)}${encodeURIComponent(id)}/`
L13: function resource(base) {
L14: const root = normalizeBase(base)
L29: export const coreApi = {
L35: export const socialApi = {
L44: export const memoryApi = { items: resource('memory/items') }
L45: export const projectsApi = {
L50: export const challengesApi = {
L56: export const financeApi = {
L82: export const appApi = {

## services/Shared/endpoints.js
L8: export const endpoints = {
L345: export const domainEndpoints = {

## services/Shared/explainsService.js
L4: const explainService = {
L16: const res = await api.get('/explain/explains/')
L42: const res = await api.get('/explain/explains_category/')

## services/Shared/mcpService.js
L10: const api = axios.create({
L17: export const mcpService = {

## services/Shared/product_services.js
No exported definition matched the static scan.


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
