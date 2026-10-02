import pyautogui
import tempfile
from django.core.files import File
from automation.models import ScreenState
import uuid


def capture_screen(task_run, user, program_obj=None, action_id=None, status="ok"):
    import pyautogui
    import tempfile
    from django.core.files import File
    from automation.models import ScreenState

    screenshot = pyautogui.screenshot()
    temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    screenshot.save(temp.name)

    screen_state = ScreenState.objects.create(
        task_run=task_run,
        created_by=user,
        active_program=program_obj.name if program_obj else "unknown",
        detected_elements={},
        action_id=action_id or uuid.uuid4(),
        status=status
    )

    with open(temp.name, "rb") as f:
        screen_state.screenshot.save("screen.png", File(f), save=True)

    return screen_state
