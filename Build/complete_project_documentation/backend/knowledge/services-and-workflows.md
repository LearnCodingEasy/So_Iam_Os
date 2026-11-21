# knowledge services and workflows

## Service/task/signal source


### knowledge/services/file_service.py
L11: class KnowledgeFileService:
L22: def add_file(
L88: def delete_file(

### knowledge/services/knowledge_service.py
L12: class KnowledgeService:
L22: def get_user_knowledge(
L69: def create_knowledge(
L85: def update_knowledge(
L113: def archive_knowledge(
L140: def restore_knowledge(
L167: def connect_to_topic(
L213: def disconnect_from_topic(
L239: def search(

### knowledge/services/__init__.py
No class/function declaration matched the static inventory pattern.

### knowledge/tasks/knowledge_file_tasks.py
L13: def process_knowledge_file(self, file_id):

### knowledge/tasks/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
