# automation/engine/runner.py

import time
from automation.models import TaskRun
from .executor import ActionExecutor
from .router import get_next_node
from .logger import EngineLogger


class WorkflowRunner:

    MAX_STEPS = 500  # حماية من اللوب اللانهائي

    def __init__(self, task_run: TaskRun):
        self.task_run = task_run
        self.workflow = task_run.workflow
        self.executor = ActionExecutor()
        self.logger = EngineLogger(task_run)
        self.step_counter = 0

    def get_start_node(self):
        return self.workflow.nodes.filter(is_start=True).first()

    def run(self):
        try:
            node = self.get_start_node()

            if not node:
                raise Exception("No start node defined")

            self.logger.start()

            while node:
                self.step_counter += 1

                if self.step_counter > self.MAX_STEPS:
                    raise Exception("Max steps exceeded")

                start_time = time.time()

                self.logger.log_step(
                    step=self.step_counter,
                    message=f"Running node: {node.label}"
                )

                result = True

                for action in node.actions.all():
                    action_result = self.executor.execute(action)

                    self.logger.log_action(action, action_result)

                    if not action_result:
                        result = False
                        break  # وقف هنا

                execution_time = time.time() - start_time

                self.logger.log_step(
                    step=self.step_counter,
                    message=f"Node finished in {execution_time:.2f}s"
                )

                node = get_next_node(node, result)

            self.logger.success()

        except Exception as e:
            self.logger.fail(str(e))
