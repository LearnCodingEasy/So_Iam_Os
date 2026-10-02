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
pip install pyautogui
```

```python
import pyautogui, time
```

## Mouse

<div dir="rtl" >  
  🖱️ تحريك الماوس
</div>

```python
# 🖱️ تحريك الماوس
import pyautogui
pyautogui.moveTo(500, 300)
```

<div dir="rtl" >  
الحركة تكون ناعمة؟
</div>

```python
# 🖱️ تحريك الماوس
import pyautogui
pyautogui.moveTo(100,100,duration=1)
```

<div dir="rtl" >  
  🖱️ مكان الماوس الحالي؟
</div>

```python
# 🖱️ مكان الماوس الحالي؟
import pyautogui
print(pyautogui.position())
```

<div dir="rtl" >  
  الضغط بالماوس
  <br/>
كليك عادي 👆 نقرة واحدة
</div>

```python
# 👆 نقرة واحدة
import pyautogui
pyautogui.click(100,100)
```

<div dir="rtl" >  
  دبل كليك
</div>

```python
import pyautogui

pyautogui.doubleClick(500, 300)

```

<div dir="rtl" >  
  كليك يمين
</div>

```python
import pyautogui
pyautogui.rightClick(500, 300)

```

<div dir="rtl" >  
  ↔️ سحب الماوس
</div>

```python
# ↔️ سحب الماوس
import pyautogui
pyautogui.dragTo(400,400,duration=1)
```

## keypord

<div dir="rtl" >
  الكتابة بالكيبورد
</div>

```python
import pyautogui

pyautogui.write("Hello World")
# ✍️ كتابة النص
import pyautogui
pyautogui.write('Hello VS Code!', interval=0.1)
```

<div dir="rtl" >
  ضغط زر
</div>

```python
# ⏎ الضغط على Enter
import pyautogui
pyautogui.press('enter')
```

<div dir="rtl" >
  الشورت كات 
</div>

```python
# 💾 حفظ الملف
import pyautogui
pyautogui.hotkey('ctrl','s')
```

```python
# 🔍 فتح Command Palette
import pyautogui
pyautogui.hotkey('ctrl','shift','p')
```

## screenshot

<div dir="rtl" >
  📸 أخذ سكرين شوت
</div>

```python
# 📸 أخذ سكرين شوت
import pyautogui
screenshot = pyautogui.screenshot()
# 💾 حفظ الصورة
screenshot.save('screenshot.png')
```

<div dir="rtl" >
  🔍 البحث عن أيقونة
</div>

```python
# 🔍 البحث عن أيقونة
import pyautogui
location = pyautogui.locateOnScreen('TogglePanel.png')
print(location)
```

<div dir="rtl" >
<h2>👆 النقر على الصورة</h2>
  <h2>
    
  </h2>
</div>

```python
# 👆 النقر على الصورة
import pyautogui
pyautogui.click(pyautogui.locateCenterOnScreen(
    'TogglePanel.png'))

```
<div dir="rtl" >
  <h2>
    
  </h2>
</div>

```python
import pyautogui
```

<div dir="rtl" >
  <h2>
    
  </h2>
</div>

```python
import pyautogui
```
