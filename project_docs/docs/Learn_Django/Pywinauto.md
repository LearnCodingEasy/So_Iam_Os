# 🕸️ Automation

## Intro

<div dir="rtl" >
PyAutoGUI يعني إيه؟
<br/>
مكتبة Python تقدر من خلالها:
<br/>

✅ تحرك الماوس
<br/>
✅ تضغط
<br/>
✅ تكتب
<br/>
✅ تاخد Screenshot
<br/>
✅ تدور على صورة جوة الشاشة
<br/>
✅ تنتظر حدث يحصل
<br/>

يعني بتديك القدرة تخلي الكود يتصرف كإنه بني آدم.

</div>

## Install

```cmd
pip install pywinauto
```

## Import

```python
from pywinauto.application import Application
```

## Open

<div dir="rtl" >
  <h2>
    🚀 فتح VS Code
  </h2>
</div>

```python
# 🚀 فتح VS Code
from pywinauto.application import Application

vs_code_path = r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"

Application(backend="uia").start(vs_code_path)

"""
# Run
python path\file.py
"""
```

<div dir="rtl" >
  <h2>
    🚀 فتح VS Code وكمان مشروع معين
  </h2>
</div>

```python
# 🚀 فتح VS Code
from pywinauto.application import Application

vs_code_path = r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"
project_path = r"D:\Python_Libraries\automation\Pyautogui\automation_examples"

cmd = f'"{vs_code_path}" "{project_path}"'

Application(backend="uia").start(cmd)

"""
# Run
python path\file.py
"""
```

<div dir="rtl" >
  <h2>
    🚀 فتح VS Code وكمان مشروع معين
  </h2>
</div>

```python
# 🚀 فتح VS Code
from pywinauto.application import Application

vs_code_path = r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"
project_path = r"D:\Python_Libraries\automation\Pyautogui\automation_examples"

cmd = f'"{vs_code_path}" "{project_path}"'

Application(backend="uia").start(cmd)

"""
# Run
python path\file.py
"""
```

<div dir="rtl" >
  <h2>
    🚀 فتح VS Code وكمان مشروع معين وكمان ملف معين
  </h2>
</div>

```python
# 🚀 فتح VS Code
from pywinauto.application import Application

vs_code_path = r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"
project_path = r"D:\Python_Libraries\automation\Pyautogui\automation_examples"
file_path = r"D:\Python_Libraries\automation\Pyautogui\automation_examples\example_12.py"

cmd = f'"{vs_code_path}" "{project_path}" "{file_path}"'

app = Application(backend="uia").start(cmd)

"""
# Run
python path\file.py
"""
```
