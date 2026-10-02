خطاء حين الضغط على زورار ال

warn
2026-09-27 20:47:30,482 | WARNING | daphne.server | Application instance <Task pending name='Task-394' coro=<ASGIStaticFilesHandler.**call**() running at D:\So_Iam_Os\venv\Lib\site-packages\django\contrib\staticfiles\handlers.py:101> wait_for=<\_GatheringFuture pending cb=[Task.task_wakeup()]>> for connection <WebRequest at 0x1538919e210 method=POST uri=/api/tasks/generate/ clientproto=HTTP/1.1> took too long to shut down and was killed.
٢٠:٤٧:٣١
warn
2026-09-27 20:47:31,491 | WARNING | daphne.server | Application instance <Task cancelling name='Task-394' coro=<ASGIStaticFilesHandler.**call**() running at D:\So_Iam_Os\venv\Lib\site-packages\django\contrib\staticfiles\handlers.py:101> wait_for=<Future pending cb=[_chain_future.<locals>._call_check_cancel() at C:\Python314\Lib\asyncio\futures.py:393, Task.task_wakeup()]>> for connection <WebRequest at 0x1538919e210 method=POST uri=/api/tasks/generate/ clientproto=HTTP/1.1> took too long to shut down and was killed.
٢٠:٤٧:٣١
warn
2026-09-27 20:47:31,493 | WARNING | daphne.server | Application instance <Task pending name='Task-398' coro=<ASGIStaticFilesHandler.**call**() running at D:\So_Iam_Os\venv\Lib\site-packages\django\contrib\staticfiles\handlers.py:101> wait_for=<\_GatheringFuture pending cb=[Task.task_wakeup()]>> for connection <WebRequest at 0x1538919ead0 method=POST uri=/api/tasks/generate/ clientproto=HTTP/1.1> took too long to shut down and was killed.
٢٠:٤٧:٣٢
warn
2026-09-27 20:47:32,496 | WARNING | daphne.server | Application instance <Task cancelling name='Task-398' coro=<ASGIStaticFilesHandler.**call**() running at D:\So_Iam_Os\venv\Lib\site-packages\django\contrib\staticfiles\handlers.py:101> wait_for=<Future pending cb=[_chain_future.<locals>._call_check_cancel() at C:\Python314\Lib\asyncio\futures.py:393, Task.task_wakeup()]>> for connection <WebRequest at 0x1538919ead0 method=POST uri=/api/tasks/generate/ clientproto=HTTP/1.1> took too long to shut down and was killed.

---

---

---

---

---

الخطاء ده بيظهر ساعت ما بدوس على تاجيل المعمة

2026-09-27 20:56:28,329 | INFO | django.channels.server | HTTP GET /api/tasks/today/ 200 [0.04, 127.0.0.1:14168]  
HTTP OPTIONS /api/tasks/9/postpone/ 200 [0.00, 127.0.0.1:14168]
2026-09-27 20:56:38,582 | INFO | django.channels.server | HTTP OPTIONS /api/tasks/9/postpone/ 200 [0.00, 127.0.0.1:14168]
Internal Server Error: /api/tasks/9/postpone/
Traceback (most recent call last):
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\exception.py", line 42, in inner
response = await get_response(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\base.py", line 254, in \_get_response_async
response = await wrapped_callback(
^^^^^^^^^^^^^^^^^^^^^^^
request, *callback_args, \*\*callback_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 526, in **call**
ret = await asyncio.shield(exec_coro)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Python314\Lib\concurrent\futures\thread.py", line 86, in run
result = ctx.run(self.task)
File "C:\Python314\Lib\concurrent\futures\thread.py", line 73, in run
return fn(*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 581, in thread_handler
return func(\*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 508, in func
return context.run(run_child)
~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 506, in run_child
return child()
File "D:\So_Iam_Os\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in \_view_wrapper
return view_func(request, *args, \*\*kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\viewsets.py", line 124, in view
return self.dispatch(request, *args, \*\*kwargs)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 526, in dispatch
response = self.handle_exception(exc)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 474, in handle_exception
self.raise_uncaught_exception(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 485, in raise_uncaught_exception
raise exc
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 523, in dispatch
response = handler(request, \*args, \*\*kwargs)
File "D:\So_Iam_Os\backend_django\tasks\views.py", line 66, in postpone
return Response(self.get_serializer(task).data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 583, in data
ret = super().data
^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 249, in data
self.\_data = self.to_representation(self.instance)  
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^  
 File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 550, in to_representation
ret[field.field_name] = field.to_representation(attribute)
~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\fields.py", line 1938, in to_representation
return method(value)
File "D:\So_Iam_Os\backend_django\tasks\serializers.py", line 27, in get_overdue
and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and
'datetime.date'
2026-09-27 20:56:50,132 | ERROR | django.request | Internal
Server Error: /api/tasks/9/postpone/
Traceback (most recent call last):
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\exception.py", line 42, in inner
response = await get_response(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\base.py", line 254, in \_get_response_async
response = await wrapped_callback(
^^^^^^^^^^^^^^^^^^^^^^^
request, *callback_args, \*\*callback_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 526, in **call**
ret = await asyncio.shield(exec_coro)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Python314\Lib\concurrent\futures\thread.py", line 86, in run
result = ctx.run(self.task)
File "C:\Python314\Lib\concurrent\futures\thread.py", line 73, in run
return fn(*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 581, in thread_handler
return func(\*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 508, in func
return context.run(run_child)
~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 506, in run_child
return child()
File "D:\So_Iam_Os\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in \_view_wrapper
return view_func(request, *args, \*\*kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\viewsets.py", line 124, in view
return self.dispatch(request, *args, \*\*kwargs)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 526, in dispatch
response = self.handle_exception(exc)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 474, in handle_exception
self.raise_uncaught_exception(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 485, in raise_uncaught_exception
raise exc
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 523, in dispatch
response = handler(request, \*args, \*\*kwargs)
File "D:\So_Iam_Os\backend_django\tasks\views.py", line 66, in postpone
return Response(self.get_serializer(task).data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 583, in data
ret = super().data
^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 249, in data
self.\_data = self.to_representation(self.instance)  
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^  
 File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 550, in to_representation
ret[field.field_name] = field.to_representation(attribute)
~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\fields.py", line 1938, in to_representation
return method(value)
File "D:\So_Iam_Os\backend_django\tasks\serializers.py", line 27, in get_overdue
and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and
'datetime.date'
Internal Server Error: /api/tasks/9/postpone/
Traceback (most recent call last):
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\exception.py", line 42, in inner
response = await get_response(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\base.py", line 254, in \_get_response_async
response = await wrapped_callback(
^^^^^^^^^^^^^^^^^^^^^^^
request, *callback_args, \*\*callback_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 526, in **call**
ret = await asyncio.shield(exec_coro)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Python314\Lib\concurrent\futures\thread.py", line 86, in run
result = ctx.run(self.task)
File "C:\Python314\Lib\concurrent\futures\thread.py", line 73, in run
return fn(*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 581, in thread_handler
return func(\*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 508, in func
return context.run(run_child)
~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 506, in run_child
return child()
File "D:\So_Iam_Os\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in \_view_wrapper
return view_func(request, *args, \*\*kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\viewsets.py", line 124, in view
return self.dispatch(request, *args, \*\*kwargs)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 526, in dispatch
response = self.handle_exception(exc)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 474, in handle_exception
self.raise_uncaught_exception(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 485, in raise_uncaught_exception
raise exc
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 523, in dispatch
response = handler(request, \*args, \*\*kwargs)
File "D:\So_Iam_Os\backend_django\tasks\views.py", line 66, in postpone
return Response(self.get_serializer(task).data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 583, in data
ret = super().data
^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 249, in data
self.\_data = self.to_representation(self.instance)  
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^  
 File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 550, in to_representation
ret[field.field_name] = field.to_representation(attribute)
~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\fields.py", line 1938, in to_representation
return method(value)
File "D:\So_Iam_Os\backend_django\tasks\serializers.py", line 27, in get_overdue
and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and
'datetime.date'
2026-09-27 20:56:50,140 | ERROR | django.request | Internal
Server Error: /api/tasks/9/postpone/
Traceback (most recent call last):
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\exception.py", line 42, in inner
response = await get_response(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\base.py", line 254, in \_get_response_async
response = await wrapped_callback(
^^^^^^^^^^^^^^^^^^^^^^^
request, *callback_args, \*\*callback_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 526, in **call**
ret = await asyncio.shield(exec_coro)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Python314\Lib\concurrent\futures\thread.py", line 86, in run
result = ctx.run(self.task)
File "C:\Python314\Lib\concurrent\futures\thread.py", line 73, in run
return fn(*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 581, in thread_handler
return func(\*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 508, in func
return context.run(run_child)
~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 506, in run_child
return child()
File "D:\So_Iam_Os\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in \_view_wrapper
return view_func(request, *args, \*\*kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\viewsets.py", line 124, in view
return self.dispatch(request, *args, \*\*kwargs)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 526, in dispatch
response = self.handle_exception(exc)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 474, in handle_exception
self.raise_uncaught_exception(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 485, in raise_uncaught_exception
raise exc
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 523, in dispatch
response = handler(request, \*args, \*\*kwargs)
File "D:\So_Iam_Os\backend_django\tasks\views.py", line 66, in postpone
return Response(self.get_serializer(task).data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 583, in data
ret = super().data
^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 249, in data
self.\_data = self.to_representation(self.instance)  
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^  
 File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 550, in to_representation
ret[field.field_name] = field.to_representation(attribute)
~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\fields.py", line 1938, in to_representation
return method(value)
File "D:\So_Iam_Os\backend_django\tasks\serializers.py", line 27, in get_overdue
and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and
'datetime.date'
Internal Server Error: /api/tasks/9/postpone/
Traceback (most recent call last):
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\exception.py", line 42, in inner
response = await get_response(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\base.py", line 254, in \_get_response_async
response = await wrapped_callback(
^^^^^^^^^^^^^^^^^^^^^^^
request, *callback_args, \*\*callback_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 526, in **call**
ret = await asyncio.shield(exec_coro)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Python314\Lib\concurrent\futures\thread.py", line 86, in run
result = ctx.run(self.task)
File "C:\Python314\Lib\concurrent\futures\thread.py", line 73, in run
return fn(*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 581, in thread_handler
return func(\*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 508, in func
return context.run(run_child)
~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 506, in run_child
return child()
File "D:\So_Iam_Os\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in \_view_wrapper
return view_func(request, *args, \*\*kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\viewsets.py", line 124, in view
return self.dispatch(request, *args, \*\*kwargs)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 526, in dispatch
response = self.handle_exception(exc)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 474, in handle_exception
self.raise_uncaught_exception(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 485, in raise_uncaught_exception
raise exc
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 523, in dispatch
response = handler(request, \*args, \*\*kwargs)
File "D:\So_Iam_Os\backend_django\tasks\views.py", line 66, in postpone
return Response(self.get_serializer(task).data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 583, in data
ret = super().data
^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 249, in data
self.\_data = self.to_representation(self.instance)  
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^  
 File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 550, in to_representation
ret[field.field_name] = field.to_representation(attribute)
~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\fields.py", line 1938, in to_representation
return method(value)
File "D:\So_Iam_Os\backend_django\tasks\serializers.py", line 27, in get_overdue
and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and
'datetime.date'
2026-09-27 20:56:50,161 | ERROR | django.request | Internal
Server Error: /api/tasks/9/postpone/
Traceback (most recent call last):
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\exception.py", line 42, in inner
response = await get_response(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 577, in thread_handler
raise exc_info[1]
File "D:\So_Iam_Os\venv\Lib\site-packages\django\core\handlers\base.py", line 254, in \_get_response_async
response = await wrapped_callback(
^^^^^^^^^^^^^^^^^^^^^^^
request, *callback_args, \*\*callback_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 526, in **call**
ret = await asyncio.shield(exec_coro)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Python314\Lib\concurrent\futures\thread.py", line 86, in run
result = ctx.run(self.task)
File "C:\Python314\Lib\concurrent\futures\thread.py", line 73, in run
return fn(*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 581, in thread_handler
return func(\*args, **kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 508, in func
return context.run(run_child)
~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\asgiref\sync.py", line 506, in run_child
return child()
File "D:\So_Iam_Os\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in \_view_wrapper
return view_func(request, *args, \*\*kwargs)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\viewsets.py", line 124, in view
return self.dispatch(request, *args, \*\*kwargs)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 526, in dispatch
response = self.handle_exception(exc)
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 474, in handle_exception
self.raise_uncaught_exception(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 485, in raise_uncaught_exception
raise exc
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\views.py", line 523, in dispatch
response = handler(request, \*args, \*\*kwargs)
File "D:\So_Iam_Os\backend_django\tasks\views.py", line 66, in postpone
return Response(self.get_serializer(task).data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 583, in data
ret = super().data
^^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 249, in data
self.\_data = self.to_representation(self.instance)  
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^  
 File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\serializers.py", line 550, in to_representation
ret[field.field_name] = field.to_representation(attribute)
~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
File "D:\So_Iam_Os\venv\Lib\site-packages\rest_framework\fields.py", line 1938, in to_representation
return method(value)
File "D:\So_Iam_Os\backend_django\tasks\serializers.py", line 27, in get_overdue
and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and
'datetime.date'
HTTP POST /api/tasks/9/postpone/ 500 [11.98, 127.0.0.1:14254]
2026-09-27 20:56:50,595 | ERROR | django.channels.server | HTTP POST /api/tasks/9/postpone/ 500 [11.98, 127.0.0.1:14254]

---

---

---

---

---

خطاء فى صفحة ال ai.vue اثناء الضغط على المحادثة 


HTTP GET /api/ai/conversations/ 200 [0.04, 127.0.0.1:13371]
2026-09-27 22:54:42,492 | INFO | django.channels.server | HTTP GET /api/ai/conversations/ 200 [0.04, 127.0.0.1:13371]   
HTTP OPTIONS /api/ai/chat/ 200 [0.01, 127.0.0.1:13371]
2026-09-27 22:54:48,347 | INFO | django.channels.server | HTTP OPTIONS /api/ai/chat/ 200 [0.01, 127.0.0.1:13371]        
2026-09-27 22:55:29,790 | WARNING | daphne.server | Application instance <Task pending name='Task-39' coro=<ASGIStaticFilesHandler.__call__() running at D:\So_Iam_Os\venv\Lib\site-packages\django\contrib\staticfiles\handlers.py:101> wait_for=<_GatheringFuture pending cb=[Task.task_wakeup()]>> for connection <WebRequest at 0x20d97b6b390 method=POST uri=/api/ai/chat/ clientproto=HTTP/1.1> took too long to shut down and was killed.
2026-09-27 22:55:30,799 | WARNING | daphne.server | Application instance <Task cancelling name='Task-39' coro=<ASGIStaticFilesHandler.__call__() running at D:\So_Iam_Os\venv\Lib\site-packages\django\contrib\staticfiles\handlers.py:101> wait_for=<Future pending cb=[_chain_future.<locals>._call_check_cancel() at C:\Python314\Lib\asyncio\futures.py:393, Task.task_wakeup()]>> for connection <WebRequest at 0x20d97b6b390 method=POST uri=/api/ai/chat/ clientproto=HTTP/1.1> took too 
long to shut down and was killed.


______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
______________________________
بيظهار فى صفجة الشات الخاص بى ال ai و ساعت ما اختار claud 

OpenRouter API key is not configured.

Bad Gateway: /api/ai/chat/
2026-09-29 06:50:23,371 | ERROR | django.request | Bad Gateway: /api/ai/chat/
HTTP POST /api/ai/chat/ 502 [0.16, 127.0.0.1:7378]
2026-09-29 06:50:23,372 | ERROR | django.channels.server | HTTP POST /api/ai/chat/ 502 [0.16, 127.0.0.1:7378]
