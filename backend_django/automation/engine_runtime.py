# backend_django\automation\engine_runtime.py
# Note: This module runs on the machine that will control keyboard/mouse.
from automation.engine.logger import EngineLogger
import subprocess
import time
import pyautogui
import pyperclip
import psutil
import os
import json
from django.conf import settings
import os
import uuid
from automation.models import ProgramElement
from pywinauto import Desktop
from rich.console import Console
from automation.services.screenshot import capture_screen

console = Console()

# =========================================
# 🔹 فتح البرنامج حسب النوع (OBS / VSCode / أي برنامج)
# =========================================


def _open_program(program_obj, timeout=20):
    try:
        path = program_obj.executable_path
        project_path = program_obj.project_path

        if not path or not os.path.exists(path):
            return {"status": "error", "error": "invalid_path"}

        exe_name = os.path.basename(path).lower()

        # ===============================
        # VS CODE (الطريقة الصح 100%)
        # ===============================
        if "code.exe" in exe_name:

            if project_path and os.path.exists(project_path):
                # يفتح فولدر محدد
                subprocess.Popen(
                    ["cmd", "/c", "start", "", path, project_path],
                    shell=True
                )
            else:
                os.startfile(path)

        # ===============================
        # OBS (يفتح طبيعي زي الدبل كليك)
        # ===============================
        elif "obs" in exe_name:
            # تأكد من المسار التنفيذي والدليل
            args = [path]
            # لو فيه project_path أو folder معين
            if project_path and os.path.exists(project_path):
                args.append(project_path)

            # مثال: لو عايز يبدأ التسجيل تلقائيًا
            args.append("--startrecording")

            # cwd لازم يكون مسار تثبيت البرنامج
            cwd_dir = os.path.dirname(path)

            # تشغيل OBS بنفس الطريقة اللي بيشتغل بيها double-click
            subprocess.Popen(args, cwd=cwd_dir, shell=False)

        # ===============================
        # أي برنامج تاني
        # ===============================
        else:
            if project_path and os.path.exists(project_path):
                subprocess.Popen(
                    [path, project_path],
                    shell=True
                )
            else:
                os.startfile(path)

        # ===============================
        # تأكيد إن البرنامج اشتغل
        # ===============================
        start = time.time()
        while time.time() - start < timeout:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and exe_name in proc.info['name'].lower():
                    return {"status": "ok"}
            time.sleep(0.5)

        return {"status": "error", "error": "program_not_started"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def _close_program(path):
    """
    يغلق البرنامج المفتوح حسب المسار
    """
    try:
        # البحث عن كل العمليات المفتوحة بنفس path
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if proc.info['exe'] == path:
                proc.terminate()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _get_program_status(path):
    try:
        target_name = os.path.basename(path).lower()

        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == target_name:
                return {"status": "ok", "is_running": True}

        return {"status": "ok", "is_running": False}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def _click_element(element_id, program_obj=None):
    try:
        element = ProgramElement.objects.get(id=element_id)

        # 🔥 دايمًا ركّز البرنامج قبل أي Click
        if program_obj:
            _focus_program_window(program_obj=program_obj)
            time.sleep(0.5)

        if element.selector_type == "image":
            location = pyautogui.locateCenterOnScreen(
                element.image.path,
                confidence=element.confidence,
                grayscale=True
            )

            if not location:
                return {"status": "error", "error": "element_not_found"}

            pyautogui.click(location)
            return {"status": "ok"}

        elif element.selector_type == "coords":
            pyautogui.click(element.x, element.y)
            return {"status": "ok"}

        elif element.shortcut:
            keys = [k.strip() for k in element.shortcut.split(",")]
            pyautogui.hotkey(*keys)
            return {"status": "ok"}

        return {"status": "error", "error": "unsupported_selector"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def _focus_program_window(program_obj=None, title=None):
    try:
        if program_obj and not title:
            title = program_obj.window_title

        if not title:
            return {"status": "error", "error": "no_title"}

        windows = Desktop(backend="uia").windows(title_re=f".*{title}.*")

        if not windows:
            return {"status": "error", "error": "window_not_found"}

        win = windows[0]

        try:
            win.restore()
        except:
            pass

        win.set_focus()
        win.maximize()

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def _press(key):
    try:
        pyautogui.press(key)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _hotkey(keys_str):
    try:
        # expects comma separated keys like "ctrl,shift,`"
        keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        pyautogui.hotkey(*keys)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _typewrite(text, program_obj=None, typing_delay=0.01):
    try:
        if program_obj:
            _focus_program_window(program_obj=program_obj)
            time.sleep(0.5)

        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")

        return {"status": "ok"}

    except Exception:
        try:
            for ch in text:
                pyautogui.typewrite(ch)
                time.sleep(typing_delay)
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


def _run_cmd(cmd):
    try:
        subprocess.Popen(cmd, shell=True)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _wait(seconds):
    try:
        time.sleep(float(seconds))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _print(message):
    console.print(message)
    return {"status": "ok"}


ACTION_EXECUTORS = {
    "open_program": lambda a, program_obj=None: _open_program(program_obj),
    "press": lambda a, program_obj=None: _press(a.value),
    "hotkey": lambda a, program_obj=None: _hotkey(a.value),
    "typewrite": lambda a, program_obj=None: _typewrite(a.value, program_obj),
    "run": lambda a, program_obj=None: _run_cmd(a.value),
    "wait": lambda a, program_obj=None: _wait(a.value),
    "print": lambda a, program_obj=None: _print(a.value),
    "click_element": lambda a, program_obj=None: _click_element(a.value, program_obj),
    "focus_program_window": lambda a, program_obj=None: _focus_program_window(program_obj=program_obj),
}


def run_action_instance(action, program_obj=None, task_run=None):
    logger = EngineLogger(task_run)

    start_time = time.time()

    logger.info(
        f"start action: {action.action_type}",
        data={"payload": action.payload},
    )
    if program_obj and action.action_type not in ["open_program", "close_program"]:
        _focus_program_window(program_obj=program_obj)
        time.sleep(0.3)

    try:
        payload = action.payload or {}

        if action.action_type == "open_program":

            result = _open_program(program_obj)

            time.sleep(2)

            check = _get_program_status(program_obj.executable_path)

            if not check.get("is_running"):
                result = {"status": "error", "error": "program_not_started"}
                if task_run:
                    try:
                        capture_screen(
                            task_run, user=task_run.created_by, program_obj=program_obj)
                    except Exception as e:
                        logger.error("Failed to capture screen",
                                     data={"error": str(e)})

        elif action.action_type == "close_program":
            result = _close_program(program_obj.executable_path)

        elif action.action_type == "click_element":
            result = _click_element(payload.get("element_id"))

        elif action.action_type == "focus_program_window":
            result = _focus_program_window(payload.get("title"))

        elif action.action_type == "wait":
            if isinstance(payload, str):
                payload = json.loads(payload)
            result = _wait(payload.get("seconds", 2))

        elif action.action_type == "press":
            result = _press(payload.get("key"))

        elif action.action_type == "hotkey":
            result = _hotkey(payload.get("keys"))

        else:
            raise Exception("unknown_action")

        # ----------------------------------
        # handle result
        # ----------------------------------
        if result["status"] == "ok":

            logger.info(
                f"action success: {action.action_type}",
                data=result,
                started_at=start_time,
            )

        else:
            # ناخد screenshot في الفشل
            shot_path = f"/media/runs/{task_run.id}_{time.time()}.png"
            pyautogui.screenshot(shot_path)

            logger.error(
                f"action failed: {action.action_type}",
                data=result,
                screenshot=shot_path,
                started_at=start_time,
            )

        return result

    except Exception as e:
        shot_path = os.path.join(
            settings.MEDIA_ROOT, "runs", f"{uuid.uuid4()}.png")
        os.makedirs(os.path.dirname(shot_path), exist_ok=True)
        pyautogui.screenshot(shot_path)

        logger.error(
            f"crash in action: {action.action_type}",
            data={"error": str(e)},
            screenshot=shot_path,
            started_at=start_time,
        )

        return {"status": "error", "error": str(e)}
