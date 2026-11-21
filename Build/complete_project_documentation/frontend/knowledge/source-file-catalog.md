# knowledge source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/knowledge/knowledgeView.vue
- Type: .vue
- Declarations: L22: const knowledgeStore = useKnowledgeStore(); L24: const saving = ref(false); L25: const extractingMetadata = ref(false); L27: const error = ref(''); L28: const successMessage = ref(''); L30: const searchQuery = ref(''); L31: const selectedType = ref('all'); L33: const showForm = ref(false); L34: const editingKnowledge = ref(null); L37: const viewDialogVisible = ref(false); L38: const selectedKnowledge = ref(null); L40: const knowledgeTypes = [; L52: const loadKnowledge = async () => {; L62: const filteredKnowledge = computed(() => {; L63: const query = searchQuery.value.trim().toLowerCase(); L66: const matchesType = selectedType.value === 'all' || item.knowledge_type === selectedType.value; L72: const searchableText = [; L86: const totalKnowledge = computed(() => knowledgeItems.value.length); L88: const openCreateForm = () => {; L95: const openEditForm = (knowledge) => {; L103: const openViewDialog = (knowledge) => {; L108: const extractSelectedMetadata = async () => {; L113: const result = await knowledgeStore.extractItemMetadata(selectedKnowledge.value.id); L123: const closeForm = () => {; L128: const saveKnowledge = async (data) => {; L142: const report = knowledgeStore.lastUploadReport; L160: const archiveKnowledge = async (knowledge) => {; L161: const confirmed = window.confirm(`Archive "${knowledge.title}"?`); L178: const clearFilters = () => {
- Imports (first five): import { computed, onMounted, ref } from 'vue'; import {; import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'; import { storeToRefs } from 'pinia'; import { useKnowledgeStore } from '@/stores/knowledge/knowledgeStore'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Knowledge/Knowledge.js
- Type: .js
- Declarations: L8: export const knowledgeService = {; L13: const response = await api.get(endpoints.knowledge.items, {; L24: const response = await api.get(endpoints.knowledge.item(id)); L32: const response = await api.post(endpoints.knowledge.items, data); L40: const response = await api.patch(endpoints.knowledge.item(id), data); L49: const response = await api.post(endpoints.knowledge.extractMetadata(id)); L57: const response = await api.post(endpoints.knowledge.archive(id)); L62: const response = await api.post(endpoints.knowledge.restore(id)); L75: const response = await api.get(endpoints.knowledge.itemFiles(knowledgeId)); L84: const formData = new FormData(); L89: const response = await api.post(endpoints.knowledge.uploadFile(knowledgeId), formData, {; L101: const uploaded = []; L104: const result = await this.uploadFile(knowledgeId, file); L121: const response = await api.post(endpoints.knowledge.connectTopic(knowledgeId), { topic_id: topicId }); L126: const response = await api.post(endpoints.knowledge.disconnectTopic(knowledgeId), { topic_id: topicId }); L131: const response = await api.post(endpoints.knowledge.archiveAll, null, { params }); L139: const response = await api.get(endpoints.knowledge.items, {
- Imports (first five): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/knowledge/knowledgeStore.js
- Type: .js
- Declarations: L5: function unwrapList(payload) {; L13: function splitFiles(data = {}) {; L15: const pending = Array.isArray(files) ? files.filter((f) => typeof File !== 'undefined' && f instanceof File) : []; L19: export const useKnowledgeStore = defineStore('knowledge', () => {; L20: const items = ref([]); L21: const count = ref(0); L22: const next = ref(null); L23: const previous = ref(null); L24: const filesByKnowledgeId = ref({}); L25: const loading = ref(false); L26: const saving = ref(false); L27: const error = ref(null); L29: const lastUploadReport = ref({ uploaded: [], failed: [] }); L31: async function uploadPending(knowledgeId, pending) {; L32: const report = { uploaded: [], failed: [] }; L36: const saved = await uploadFile(knowledgeId, file); L39: const data = cause?.response?.data; L40: const message = data?.file?.[0] || data?.file || data?.detail || cause?.message || 'Upload failed'; L48: async function fetchItems(params = {}) {; L52: const payload = await knowledgeService.getAll(params); L66: async function fetchItem(id) {; L70: async function createItem(data) {; L75: const created = await knowledgeService.create(payload); L88: async function updateItem(id, data) {; L93: const updated = await knowledgeService.update(id, payload); L105: async function archiveItem(id) {; L106: const archived = await knowledgeService.archive(id); L112: async function restoreItem(id) {; L113: const restored = await knowledgeService.restore(id); L119: async function deleteItem(id) {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import { knowledgeService } from '@/services/Knowledge/Knowledge'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/knowledge/KnowledgeCard.vue
- Type: .vue
- Declarations: L21: const emit = defineEmits(['edit', 'archive']); L23: const typeIcons = {; L35: const getIcon = (type) => {; L39: const getTypeLabel = (type) => {; L40: const labels = {; L55: const formatDate = (date) => {
- Imports (first five): import {; import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/knowledge/KnowledgeEmptyState.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/knowledge/KnowledgeForm.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L16: const emit = defineEmits(['submit', 'cancel']); L22: const form = reactive({; L37: const tagsInput = ref(''); L43: const selectedFiles = ref([]); L45: const fileInput = ref(null); L47: const isDragging = ref(false); L50: const acceptedFileTypes = [; L88: const acceptedFileTypesString = acceptedFileTypes.join(','); L94: const knowledgeTypes = [; L110: const existingFiles = computed(() => {; L122: const resetForm = () => {; L144: const fillForm = (knowledge) => {; L180: const openFilePicker = () => {; L188: const isValidFile = (file) => {; L189: const extension = `.${file.name.split('.').pop()?.toLowerCase()}`; L197: const addFiles = (files) => {; L202: const incomingFiles = Array.from(files); L209: const alreadyExists = selectedFiles.value.some(; L228: const handleFileChange = (event) => {; L237: const handleDragOver = (event) => {; L242: const handleDragLeave = (event) => {; L247: const handleDrop = (event) => {; L257: const removeSelectedFile = (index) => {; L265: const formatFileSize = (size) => {; L270: const units = ['B', 'KB', 'MB', 'GB']; L271: const unitIndex = Math.floor(Math.log(size) / Math.log(1024)); L272: const safeIndex = Math.min(unitIndex, units.length - 1); L273: const value = size / Math.pow(1024, safeIndex); L282: const getFileIcon = (file) => {
- Imports (first five): import { reactive, ref, watch, computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.

