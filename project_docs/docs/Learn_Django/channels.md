## Install

```
pip install channels

```

```
pip show django-celery-results
```

```
pip show django-celery-beat
```

## Setting

```python
INSTALLED_APPS = [
    ...
    "channels",
]

ASGI_APPLICATION = "backend_django.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

## Consumers

- 2️⃣ Create File إنشاء مجلد Debug Console

```text
consumers.py
```

```
backend_django/
│
├── manage.py
│
├── backend_django/
│   ├── settings.py
│   ├── asgi.py
│   ├── urls.py
│   └── ...
│
├── core/
│   ├── __init__.py
│   │
│   └── debug/
│       ├── __init__.py
│       ├── consumers.py
│       ├── routing.py
│       └── handlers.py
│
├── users_accounts/
│   ├── api.py
│   └── ...
│
└── ...
```

```python
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class DebugConsoleConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        الاتصال بالـ Live Debug Console
        """

        self.group_name = "debug_console"

        # إضافة المتصفح إلى مجموعة Debug Console
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        # قبول WebSocket connection
        await self.accept()

        # رسالة اتصال أولية
        await self.send(
            text_data=json.dumps({
                "type": "system",
                "level": "success",
                "message": "🔌 Debug Console connected",
            })
        )

    async def disconnect(self, close_code):
        """
        إزالة المتصفح من Debug Console
        """

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def send_log(self, event):
        """
        استقبال Log من Django Logging Handler
        وإرساله للمتصفح
        """

        await self.send(
            text_data=json.dumps(
                event["data"]
            )
        )
```

## Routing

```text
routing.py
```

```python
from django.urls import re_path

from .consumers import DebugConsoleConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/debug/$",
        DebugConsoleConsumer.as_asgi(),
    ),
]
```

- إذن عنوان WebSocket أصبح:

```text
ws://127.0.0.1:8000/ws/debug/
```

## Handlers

- 5️⃣ أهم جزء — تحويل Django Logs إلى WebSocket 🔥

- ده قلب النظام.

```text
handlers.py
```

```python
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebSocketLogHandler(logging.Handler):

    def emit(self, record):
        """
        إرسال أي Django Log إلى Live Debug Console
        """

        try:

            channel_layer = get_channel_layer()

            if channel_layer is None:
                return

            data = {
                "type": "log",
                "level": self.get_level(record.levelname),
                "message": self.format(record),
                "logger": record.name,
                "timestamp": record.created,
            }

            async_to_sync(
                channel_layer.group_send
            )(
                "debug_console",
                {
                    "type": "send_log",
                    "data": data,
                },
            )

        except Exception:
            self.handleError(record)

    @staticmethod
    def get_level(level_name):

        mapping = {
            "DEBUG": "debug",
            "INFO": "info",
            "WARNING": "warn",
            "ERROR": "error",
            "CRITICAL": "error",
        }

        return mapping.get(
            level_name,
            "info",
        )
```

## settings

- 7️⃣ تعديل settings.py

```python

# 0️⃣ channels

ASGI_APPLICATION = "backend_django.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

SO_IAM_OS_DEBUG_CONSOLE = config(
    "SO_IAM_OS_DEBUG_CONSOLE",
    default=False,
    cast=bool,
)
LOGGING = {
    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {
        "debug_console": {
            "format": (
                "{asctime} | "
                "{levelname} | "
                "{name} | "
                "{message}"
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "debug_console",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


if SO_IAM_OS_DEBUG_CONSOLE:

    LOGGING["handlers"]["websocket"] = {
        "class": "core.debug_console.handlers.WebSocketLogHandler",
        "formatter": "debug_console",
    }

    LOGGING["root"]["handlers"].append(
        "websocket"
    )


# Application definition
INSTALLED_APPS = [

    # 📚 Libraries
    # 0️⃣ channels
    "channels",
    "django_celery_results",
    "django_celery_beat",


    # So_Iam_OS
    "users_accounts",  # ✅
    # ...
]
```

## ASGI

- 🔟 تعديل ASGI

```python
"""
ASGI config for backend_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

from core.debug_console.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": URLRouter(
        websocket_urlpatterns
    ),

})

```

## Frontend

- 1️⃣1️⃣ LiveDebugConsole vue

```javascript
<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount,
  nextTick,
} from 'vue'

const logs = ref([])

const status = ref('connecting')

const consoleEl = ref(null)

const isMinimized = ref(false)

const ws = ref(null)

const maxLines = 500

const DEBUG_ENABLED =
  import.meta.env.VITE_DEBUG_CONSOLE === 'true'

const WS_URL =
  import.meta.env.VITE_DEBUG_WS_URL ||
  'ws://127.0.0.1:8000/ws/debug/'


// ============================================================
// Add Log
// ============================================================

const addLog = (
  level,
  message,
  logger = null,
  timestamp = null,
) => {

  logs.value.push({

    id:
      Date.now() +
      Math.random(),

    level,

    message,

    logger,

    timestamp:
      timestamp ||
      Date.now(),

    time:
      new Date(
        timestamp
          ? timestamp * 1000
          : Date.now()
      ).toLocaleTimeString(
        'ar-EG',
        {
          hour12: false,
        }
      ),
  })


  if (
    logs.value.length >
    maxLines
  ) {

    logs.value =
      logs.value.slice(
        -maxLines
      )
  }


  nextTick(() => {

    if (consoleEl.value) {

      consoleEl.value.scrollTop =
        consoleEl.value.scrollHeight
    }

  })
}


// ============================================================
// Connect WebSocket
// ============================================================

const connect = () => {

  if (!DEBUG_ENABLED) {

    status.value = 'disabled'

    return
  }


  ws.value =
    new WebSocket(
      WS_URL
    )


  ws.value.onopen = () => {

    status.value =
      'connected'

    addLog(
      'success',
      '🔌 Debug Console connected'
    )
  }


  ws.value.onmessage =
    (event) => {

      try {

        const data =
          JSON.parse(
            event.data
          )


        addLog(

          data.level ||
            'info',

          data.message ||
            '',

          data.logger ||
            null,

          data.timestamp ||
            null,

        )

      } catch {

        addLog(
          'info',
          event.data
        )
      }

    }


  ws.value.onerror = () => {

    status.value =
      'error'

    addLog(
      'error',
      '❌ WebSocket connection error'
    )
  }


  ws.value.onclose = () => {

    status.value =
      'closed'

    addLog(
      'warn',
      '🔌 Debug Console disconnected'
    )
  }
}


// ============================================================
// Close
// ============================================================

const closeConsole = () => {

  ws.value?.close()

}


// ============================================================
// Clear
// ============================================================

const clearLogs = () => {

  logs.value = []

}


// ============================================================
// Level Class
// ============================================================

const levelClass = (
  level
) => {

  return {

    debug:
      'log-debug',

    info:
      'log-info',

    warn:
      'log-warn',

    error:
      'log-error',

    success:
      'log-success',

  }[level] ||
    'log-info'
}


// ============================================================
// Lifecycle
// ============================================================

onMounted(() => {

  connect()

})


onBeforeUnmount(() => {

  ws.value?.close()

})
</script>

```

```html
<template>
  <div
    v-if="DEBUG_ENABLED"
    class="live-debug-console"
    :class="{
      minimized:
        isMinimized
    }"
  >
    <!-- Header -->

    <div class="console-header">
      <div>
        <span class="console-title">
          <i class="pi pi-terminal" />

          Live Debug Console
        </span>

        <span class="console-status" :class="status"> ● {{ status }} </span>
      </div>

      <div class="console-actions">
        <button @click="clearLogs">Clear</button>

        <button
          @click="
            isMinimized =
              !isMinimized
          "
        >
          {{ isMinimized ? '▲' : '▼' }}
        </button>

        <button @click="closeConsole">×</button>
      </div>
    </div>

    <!-- Logs -->

    <div v-if="!isMinimized" ref="consoleEl" class="console-body">
      <div v-if="!logs.length" class="console-empty">
        Waiting for Django logs...
      </div>

      <div
        v-for="log in logs"
        :key="log.id"
        class="log-line"
        :class="
          levelClass(
            log.level
          )
        "
      >
        <span class="log-time"> {{ log.time }} </span>

        <span class="log-level"> {{ log.level .toUpperCase() }} </span>

        <span v-if="log.logger" class="log-logger"> [{{ log.logger }}] </span>

        <span class="log-message"> {{ log.message }} </span>
      </div>
    </div>
  </div>
</template>
```

```css

<style scoped>
.live-debug-console {

  position: fixed;

  left: 20px;

  right: 20px;

  bottom: 20px;

  z-index: 99999;

  background:
    #07111f;

  border:
    1px solid #1e5eff;

  border-radius:
    10px;

  color:
    #e5e7eb;

  font-family:
    monospace;

  box-shadow:
    0 10px 40px
    rgba(0, 0, 0, .5);

}


.console-header {

  display:
    flex;

  justify-content:
    space-between;

  align-items:
    center;

  padding:
    12px 16px;

  background:
    #0b1728;

  border-bottom:
    1px solid #1e293b;

}


.console-title {

  font-weight:
    700;

  margin-right:
    15px;

}


.console-status {

  font-size:
    12px;

}


.console-status.connected {

  color:
    #22c55e;

}


.console-status.error {

  color:
    #ef4444;

}


.console-status.closed {

  color:
    #f59e0b;

}


.console-actions {

  display:
    flex;

  gap:
    6px;

}


.console-actions button {

  border:
    0;

  background:
    #17243a;

  color:
    white;

  padding:
    5px 10px;

  border-radius:
    5px;

  cursor:
    pointer;

}


.console-body {

  height:
    300px;

  overflow-y:
    auto;

  padding:
    12px;

}


.console-empty {

  color:
    #64748b;

  text-align:
    center;

  padding:
    50px;

}


.log-line {

  display:
    flex;

  gap:
    10px;

  padding:
    4px 0;

  font-size:
    13px;

  line-height:
    1.5;

}


.log-time {

  color:
    #64748b;

  min-width:
    75px;

}


.log-level {

  min-width:
    65px;

  font-weight:
    bold;

}


.log-logger {

  color:
    #38bdf8;

}


.log-message {

  white-space:
    pre-wrap;

}


.log-info {

  color:
    #60a5fa;

}


.log-debug {

  color:
    #a78bfa;

}


.log-warn {

  color:
    #fbbf24;

}


.log-error {

  color:
    #f87171;

}


.log-success {

  color:
    #4ade80;

}


.minimized
.console-body {

  display:
    none;

}

</style>
```

-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-

# SO_IAM_OS — Live Debug Console

## 1. تعريف المعرفة

**اسم النظام:** Live Debug Console
**المشروع:** SO_IAM_OS
**التقنية:** Django Channels + WebSocket + Vue.js
**الغرض:** عرض Django Logs مباشرة داخل واجهة Vue أثناء تشغيل المشروع.

---

# 2. الهدف من النظام

Live Debug Console هو نظام Debug داخلي يسمح للمطور بمشاهدة Logs الخاصة بـ Django مباشرة داخل المتصفح.

التدفق الأساسي:

```text
Django Logger
      ↓
WebSocketLogHandler
      ↓
Django Channels
      ↓
WebSocket Group
      ↓
Vue LiveDebugConsole
      ↓
عرض الـ Logs مباشرة
```

وبذلك لا يحتاج المطور إلى الاعتماد فقط على Terminal لمتابعة Logs.

---

# 3. Django Channels

يتم استخدام مكتبة:

```bash
pip install channels
```

ويمكن فحص بعض حزم المشروع باستخدام:

```bash
pip show django-celery-results
```

```bash
pip show django-celery-beat
```

---

# 4. إعداد Django

إضافة Channels إلى:

```python
INSTALLED_APPS = [
    ...
    "channels",
]
```

وتحديد ASGI:

```python
ASGI_APPLICATION = "backend_django.asgi.application"
```

ثم إعداد Channel Layer:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

في الوضع الحالي يتم استخدام:

```text
InMemoryChannelLayer
```

---

# 5. هيكل ملفات Debug Console

الهيكل المقترح داخل المشروع:

```text
backend_django/
│
├── manage.py
│
├── backend_django/
│   ├── settings.py
│   ├── asgi.py
│   ├── urls.py
│   └── ...
│
├── core/
│   ├── __init__.py
│   │
│   └── debug/
│       ├── __init__.py
│       ├── consumers.py
│       ├── routing.py
│       └── handlers.py
│
├── users_accounts/
│   ├── api.py
│   └── ...
│
└── ...
```

> **ملاحظة:** ملف الإعدادات الوارد في المصدر يشير لاحقًا إلى المسار `core.debug_console.handlers.WebSocketLogHandler`، بينما الهيكل المعروض يستخدم `core/debug/`. هذه نقطة يجب الحفاظ عليها كقرار يحتاج للمراجعة قبل التنفيذ النهائي، وليس تغييرها تلقائيًا.

---

# 6. Consumer

الـ Consumer مسؤول عن إدارة اتصال WebSocket.

## `consumers.py`

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DebugConsoleConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        الاتصال بالـ Live Debug Console
        """

        self.group_name = "debug_console"

        # إضافة المتصفح إلى مجموعة Debug Console
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        # قبول WebSocket connection
        await self.accept()

        # رسالة اتصال أولية
        await self.send(
            text_data=json.dumps({
                "type": "system",
                "level": "success",
                "message": "🔌 Debug Console connected",
            })
        )

    async def disconnect(self, close_code):
        """
        إزالة المتصفح من Debug Console
        """

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def send_log(self, event):
        """
        استقبال Log من Django Logging Handler
        وإرساله للمتصفح
        """

        await self.send(
            text_data=json.dumps(
                event["data"]
            )
        )
```

---

# 7. Debug Group

جميع اتصالات Debug Console تستخدم المجموعة:

```text
debug_console
```

عند اتصال المتصفح:

```python
await self.channel_layer.group_add(
    self.group_name,
    self.channel_name,
)
```

وعند إغلاق الاتصال:

```python
await self.channel_layer.group_discard(
    self.group_name,
    self.channel_name,
)
```

وبالتالي يمكن إرسال Log واحد إلى جميع متصفحات Debug Console المتصلة بالمجموعة.

---

# 8. WebSocket Routing

## `routing.py`

```python
from django.urls import re_path
from .consumers import DebugConsoleConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/debug/$",
        DebugConsoleConsumer.as_asgi(),
    ),
]
```

عنوان WebSocket المستخدم في النظام:

```text
ws://127.0.0.1:8000/ws/debug/
```

---

# 9. WebSocketLogHandler

هذا هو الجزء الأساسي الذي يربط Django Logging مع WebSocket.

الفكرة:

```text
logging.LogRecord
       ↓
WebSocketLogHandler
       ↓
Channel Layer
       ↓
debug_console
       ↓
WebSocket
```

## `handlers.py`

```python
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebSocketLogHandler(logging.Handler):

    def emit(self, record):
        """
        إرسال أي Django Log إلى Live Debug Console
        """

        try:
            channel_layer = get_channel_layer()

            if channel_layer is None:
                return

            data = {
                "type": "log",
                "level": self.get_level(record.levelname),
                "message": self.format(record),
                "logger": record.name,
                "timestamp": record.created,
            }

            async_to_sync(
                channel_layer.group_send
            )(
                "debug_console",
                {
                    "type": "send_log",
                    "data": data,
                },
            )

        except Exception:
            self.handleError(record)

    @staticmethod
    def get_level(level_name):

        mapping = {
            "DEBUG": "debug",
            "INFO": "info",
            "WARNING": "warn",
            "ERROR": "error",
            "CRITICAL": "error",
        }

        return mapping.get(
            level_name,
            "info",
        )
```

---

# 10. تحويل مستويات Logging

النظام يحول مستويات Django Logging إلى مستويات مناسبة للواجهة:

| Django   | Vue Console |
| -------- | ----------- |
| DEBUG    | debug       |
| INFO     | info        |
| WARNING  | warn        |
| ERROR    | error       |
| CRITICAL | error       |

---

# 11. البيانات المرسلة إلى Vue

كل Log يتم تحويله إلى Object يحتوي على:

```python
{
    "type": "log",
    "level": "...",
    "message": "...",
    "logger": "...",
    "timestamp": ...
}
```

حيث:

- `type`: نوع الرسالة.
- `level`: مستوى الـ Log.
- `message`: نص الرسالة.
- `logger`: اسم الـ Logger.
- `timestamp`: وقت إنشاء الـ Log.

---

# 12. إعداد Logging في settings.py

يتم تشغيل Debug Console بناءً على متغير:

```python
SO_IAM_OS_DEBUG_CONSOLE
```

ويتم قراءته من إعدادات المشروع:

```python
SO_IAM_OS_DEBUG_CONSOLE = config(
    "SO_IAM_OS_DEBUG_CONSOLE",
    default=False,
    cast=bool,
)
```

وهذا يجعل تشغيل Live Debug Console قابلًا للتحكم من إعدادات البيئة.

---

# 13. Logging Configuration

الإعداد الأساسي:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "debug_console": {
            "format": (
                "{asctime} | "
                "{levelname} | "
                "{name} | "
                "{message}"
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "debug_console",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

---

# 14. تفعيل WebSocket Logging

إذا كان:

```python
SO_IAM_OS_DEBUG_CONSOLE = True
```

يتم إضافة WebSocket Handler:

```python
if SO_IAM_OS_DEBUG_CONSOLE:

    LOGGING["handlers"]["websocket"] = {
        "class": "core.debug_console.handlers.WebSocketLogHandler",
        "formatter": "debug_console",
    }

    LOGGING["root"]["handlers"].append(
        "websocket"
    )
```

وبالتالي يصبح الـ Root Logger مرتبطًا أيضًا بـ WebSocket.

> **ملاحظة:** المسار `core.debug_console.handlers.WebSocketLogHandler` يجب أن يتطابق فعليًا مع مكان `handlers.py` في المشروع.

---

# 15. Installed Apps

إضافة Channels:

```python
INSTALLED_APPS = [
    # Libraries

    "channels",
    "django_celery_results",
    "django_celery_beat",

    # SO_IAM_OS

    "users_accounts",

    # ...
]
```

---

# 16. ASGI

ملف:

```text
backend_django/asgi.py
```

هو نقطة الدخول التي تجمع HTTP وWebSocket.

الكود المستخدم:

```python
from core.debug_console.routing import websocket_urlpatterns

from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)

import os

from django.core.asgi import (
    get_asgi_application,
)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend_django.settings",
)


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": URLRouter(
        websocket_urlpatterns
    ),

})
```

---

# 17. وظيفة ProtocolTypeRouter

النظام يفرق بين نوعين من الاتصالات:

```text
HTTP
 ↓
Django ASGI Application
```

و:

```text
WebSocket
 ↓
URLRouter
 ↓
websocket_urlpatterns
 ↓
DebugConsoleConsumer
```

---

# 18. Frontend — LiveDebugConsole

واجهة Vue مسؤولة عن:

- إنشاء WebSocket connection.
- استقبال Logs.
- تخزين Logs.
- عرض Logs.
- تحديد حالة الاتصال.
- مسح Logs.
- تصغير Console.
- إغلاق الاتصال.
- الاحتفاظ بحد أقصى 500 Log.

---

# 19. إعدادات Frontend

يتم التحكم في تشغيل Debug Console من:

```javascript
import.meta.env.VITE_DEBUG_CONSOLE;
```

ويتم التحقق من:

```javascript
const DEBUG_ENABLED = import.meta.env.VITE_DEBUG_CONSOLE === "true";
```

عنوان WebSocket:

```javascript
const WS_URL =
  import.meta.env.VITE_DEBUG_WS_URL || "ws://127.0.0.1:8000/ws/debug/";
```

وبالتالي يمكن تغيير WebSocket URL من Environment Variable.

---

# 20. تخزين Logs

يتم استخدام:

```javascript
const logs = ref([]);
```

والحد الأقصى:

```javascript
const maxLines = 500;
```

عند تجاوز 500 Log يتم الاحتفاظ بآخر 500 فقط:

```javascript
if (logs.value.length > maxLines) {
  logs.value = logs.value.slice(-maxLines);
}
```

---

# 21. إضافة Log

الدالة:

```javascript
const addLog = (
  level,
  message,
  logger = null,
  timestamp = null,
) => {
```

تقوم بإضافة:

```text
id
level
message
logger
timestamp
time
```

إلى Array الخاصة بالـ Logs.

ويتم تحويل Timestamp إلى وقت محلي باستخدام:

```javascript
new Date(...).toLocaleTimeString(
    'ar-EG',
    {
        hour12: false,
    }
)
```

---

# 22. الاتصال بـ WebSocket

يتم الاتصال باستخدام:

```javascript
ws.value = new WebSocket(WS_URL);
```

وعند نجاح الاتصال:

```javascript
ws.value.onopen = () => {
  status.value = "connected";

  addLog("success", "🔌 Debug Console connected");
};
```

---

# 23. استقبال الرسائل

عند استقبال Message:

```javascript
ws.value.onmessage =
  (event) => {
```

يتم تحويل البيانات من JSON:

```javascript
const data = JSON.parse(event.data);
```

ثم إضافتها إلى Console:

```javascript
addLog(
  data.level || "info",
  data.message || "",
  data.logger || null,
  data.timestamp || null
);
```

وفي حالة عدم كون البيانات JSON:

```javascript
catch {
    addLog(
        'info',
        event.data
    )
}
```

---

# 24. حالات الاتصال

النظام يستخدم الحالات:

```text
connecting
connected
error
closed
disabled
```

إذا كان Debug Console غير مفعّل:

```javascript
if (!DEBUG_ENABLED) {
  status.value = "disabled";
  return;
}
```

---

# 25. WebSocket Error

عند حدوث خطأ:

```javascript
ws.value.onerror = () => {
  status.value = "error";

  addLog("error", "❌ WebSocket connection error");
};
```

---

# 26. WebSocket Close

عند إغلاق الاتصال:

```javascript
ws.value.onclose = () => {
  status.value = "closed";

  addLog("warn", "🔌 Debug Console disconnected");
};
```

---

# 27. إغلاق Console

الدالة:

```javascript
const closeConsole = () => {
  ws.value?.close();
};
```

---

# 28. مسح Logs

```javascript
const clearLogs = () => {
  logs.value = [];
};
```

---

# 29. تصنيف مستوى Log

الدالة:

```javascript
const levelClass = (level) => {
  return (
    {
      debug: "log-debug",
      info: "log-info",
      warn: "log-warn",
      error: "log-error",
      success: "log-success",
    }[level] || "log-info"
  );
};
```

وتستخدم لتحديد CSS class حسب مستوى الرسالة.

---

# 30. Lifecycle

عند تحميل Component:

```javascript
onMounted(() => {
  connect();
});
```

وعند إزالة Component:

```javascript
onBeforeUnmount(() => {
  ws.value?.close();
});
```

وبالتالي يتم فتح WebSocket عند تشغيل الواجهة وإغلاقه عند إزالة Component.

---

# 31. واجهة Console

الـ Template يحتوي على:

```text
Live Debug Console
        ↓
Connection Status
        ↓
Clear
Minimize
Close
        ↓
Logs
```

العنصر الرئيسي:

```html
<div v-if="DEBUG_ENABLED" class="live-debug-console"></div>
```

وبالتالي لا تظهر الواجهة إذا كان:

```javascript
DEBUG_ENABLED === false;
```

---

# 32. Header

يحتوي Header على:

```text
Terminal Icon
Live Debug Console
Status
Clear
Minimize
Close
```

مثال:

```html
<span class="console-title">
  <i class="pi pi-terminal" />
  Live Debug Console
</span>
```

---

# 33. عرض Logs

يتم عرض كل Log باستخدام:

```html
<div v-for="log in logs" :key="log.id" class="log-line"></div>
```

ويتم عرض:

```text
Time
Level
Logger
Message
```

---

# 34. Empty State

عندما لا توجد Logs:

```html
<div v-if="!logs.length" class="console-empty">Waiting for Django logs...</div>
```

---

# 35. Console UI

خصائص الواجهة:

```text
position: fixed
left: 20px
right: 20px
bottom: 20px
z-index: 99999
```

وارتفاع منطقة Logs:

```text
300px
```

مع:

```text
overflow-y: auto
```

---

# 36. مستويات العرض

CSS classes المستخدمة:

```text
.log-debug
.log-info
.log-warn
.log-error
.log-success
```

والغرض منها إعطاء كل مستوى Log مظهرًا مختلفًا داخل Console.

---

# 37. تصغير Console

يتم التحكم باستخدام:

```javascript
const isMinimized = ref(false);
```

والزر:

```javascript
isMinimized = !isMinimized;
```

وعند التصغير يتم إخفاء:

```text
.console-body
```

---

# 38. التكامل الكامل

النظام بالكامل يعمل بهذا التسلسل:

```text
1. Django يقوم بإنشاء Log
          ↓
2. Python Logging
          ↓
3. WebSocketLogHandler
          ↓
4. get_channel_layer()
          ↓
5. group_send()
          ↓
6. debug_console group
          ↓
7. DebugConsoleConsumer
          ↓
8. WebSocket
          ↓
9. Vue LiveDebugConsole
          ↓
10. JSON.parse()
          ↓
11. addLog()
          ↓
12. عرض Log للمطور
```

---

# 39. Environment Variables

النظام يعتمد على متغيرين أساسيين للـ Debug Console:

### Django

```text
SO_IAM_OS_DEBUG_CONSOLE
```

### Vue

```text
VITE_DEBUG_CONSOLE
VITE_DEBUG_WS_URL
```

المبدأ:

```text
Backend
SO_IAM_OS_DEBUG_CONSOLE
        ↓
تشغيل/إيقاف إرسال Logs عبر WebSocket


Frontend
VITE_DEBUG_CONSOLE
        ↓
إظهار/إخفاء Live Debug Console
```

---

# 40. الحالة الحالية للمعرفة

تم تعريف المكونات التالية:

```text
[Django]
├── Channels
├── Channel Layer
├── Consumer
├── Routing
├── Logging Handler
├── LOGGING
└── ASGI

[Vue]
├── WebSocket
├── Logs State
├── Connection Status
├── Log Renderer
├── Clear
├── Minimize
└── Close
```

---

# 41. قرارات المشروع

## القرار 1

استخدام:

```text
Django Channels
```

للتعامل مع WebSocket.

## القرار 2

استخدام:

```text
WebSocketLogHandler
```

لتحويل Django Logs إلى WebSocket.

## القرار 3

استخدام Group باسم:

```text
debug_console
```

## القرار 4

عنوان WebSocket المحلي:

```text
ws://127.0.0.1:8000/ws/debug/
```

## القرار 5

Vue هو الطرف الذي يعرض Live Debug Console.

## القرار 6

الحد الأقصى للـ Logs داخل الواجهة:

```text
500
```

## القرار 7

تفعيل Debug Console يتم التحكم فيه من Environment Variables.

---

# 42. نقاط تحتاج مراجعة قبل التنفيذ النهائي

المحتوى الحالي يحتوي على نقطة مسار تحتاج توحيدًا:

### الهيكل المعروض

```text
core/debug/
    consumers.py
    routing.py
    handlers.py
```

### بينما settings.py يستخدم

```python
core.debug_console.handlers.WebSocketLogHandler
```

### وASGI يستخدم

```python
from core.debug_console.routing import websocket_urlpatterns
```

لذلك يجب اختيار مسار واحد فعليًا قبل التشغيل.

---

# 43. قاعدة مهمة

لا يتم تغيير المعمارية الأساسية للنظام لمجرد وجود اختلاف في المسارات.

يجب أولًا تحديد:

```text
هل المجلد هو:

core/debug/

أم:

core/debug_console/
```

ثم جعل:

```text
consumers.py
routing.py
handlers.py
settings.py
asgi.py
```

كلها تستخدم نفس المسار.

---

# 44. تعريف مختصر للميزة

**Live Debug Console** في SO_IAM_OS هي طبقة Debug داخلية تقوم بتحويل Django Logs إلى WebSocket Messages ثم عرضها لحظيًا في Vue.

```text
Django Logs
    ↓
Logging Handler
    ↓
Channels
    ↓
WebSocket
    ↓
Vue
    ↓
Live Debug Console
```

هذه الميزة جزء من أدوات التطوير والمراقبة داخل مشروع **SO_IAM_OS** وليست جزءًا من منطق المستخدم الأساسي.
