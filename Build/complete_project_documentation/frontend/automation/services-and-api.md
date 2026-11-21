# automation services and API

Service files found under services/Automation. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Automation/AutomationService.js
L60: const q = programId ? `?program=${programId}` : ''
L121: const q = workflowId ? `?workflow=${workflowId}` : ''
L152: const q = workflowId ? `?workflow=${workflowId}` : ''
L172: const q = nodeId ? `?node=${nodeId}` : ''
L233: const q = taskRunId ? `?task_run=${taskRunId}` : ''

## services/Automation/nodeStorageService.js
L3: const STORAGE_KEY = 'vueflow_graph'
L10: function read() {
L11: const raw = localStorage.getItem(STORAGE_KEY)
L16: const parsed = JSON.parse(raw)
L27: function write(graph) {
L36: export function getGraph() {
L41: export function getOne(id) {
L42: const graph = read()
L46: export function getEdge(id) {
L47: const graph = read()
L51: export function createNode(node) {
L52: const graph = read()
L58: export function updateNode(id, newData) {
L59: const graph = read()
L60: const index = graph.nodes.findIndex((n) => n.id === id)
L71: export function removeNode(id) {
L72: const graph = read()
L78: export function removeEdge(id) {
L79: const graph = read()
L85: export function saveGraph(nodes, edges) {

## services/Automation/taskService.js
No exported definition matched the static scan.

## services/Automation/workflowService.js
No exported definition matched the static scan.


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
