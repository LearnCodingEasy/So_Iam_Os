# knowledge services and API

Service files found under services/Knowledge. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Knowledge/Knowledge.js
L8: export const knowledgeService = {
L13: const response = await api.get(endpoints.knowledge.items, {
L24: const response = await api.get(endpoints.knowledge.item(id))
L32: const response = await api.post(endpoints.knowledge.items, data)
L40: const response = await api.patch(endpoints.knowledge.item(id), data)
L49: const response = await api.post(endpoints.knowledge.extractMetadata(id))
L57: const response = await api.post(endpoints.knowledge.archive(id))
L62: const response = await api.post(endpoints.knowledge.restore(id))
L75: const response = await api.get(endpoints.knowledge.itemFiles(knowledgeId))
L84: const formData = new FormData()
L89: const response = await api.post(endpoints.knowledge.uploadFile(knowledgeId), formData, {
L101: const uploaded = []
L104: const result = await this.uploadFile(knowledgeId, file)
L121: const response = await api.post(endpoints.knowledge.connectTopic(knowledgeId), { topic_id: topicId })
L126: const response = await api.post(endpoints.knowledge.disconnectTopic(knowledgeId), { topic_id: topicId })
L131: const response = await api.post(endpoints.knowledge.archiveAll, null, { params })
L139: const response = await api.get(endpoints.knowledge.items, {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
