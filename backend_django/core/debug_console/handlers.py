# import logging

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


# class WebSocketLogHandler(logging.Handler):

#     def emit(self, record):
#         """
#         إرسال أي Django Log إلى Live Debug Console
#         """

#         try:

#             channel_layer = get_channel_layer()

#             if channel_layer is None:
#                 return

#             data = {
#                 "type": "log",
#                 "level": self.get_level(record.levelname),
#                 "message": self.format(record),
#                 "logger": record.name,
#                 "timestamp": record.created,
#             }

#             async_to_sync(
#                 channel_layer.group_send
#             )(
#                 "debug_console",
#                 {
#                     "type": "send_log",
#                     "data": data,
#                 },
#             )

#         except Exception:
#             self.handleError(record)

#     @staticmethod
#     def get_level(level_name):

#         mapping = {
#             "DEBUG": "debug",
#             "INFO": "info",
#             "WARNING": "warn",
#             "ERROR": "error",
#             "CRITICAL": "error",
#         }

#         return mapping.get(
#             level_name,
#             "info",
#         )


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import asyncio


class WebSocketLogHandler(logging.Handler):

    def emit(self, record):
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

            message = {
                "type": "send_log",
                "data": data,
            }

            # --------------------------------------------------
            # الحالة 1:
            # نحن بالفعل داخل asyncio event loop
            # مثل Daphne / Channels
            # --------------------------------------------------
            try:
                loop = asyncio.get_running_loop()

                loop.create_task(
                    channel_layer.group_send(
                        "debug_console",
                        message,
                    )
                )

            # --------------------------------------------------
            # الحالة 2:
            # نحن داخل thread عادي / synchronous code
            # --------------------------------------------------
            except RuntimeError:
                async_to_sync(
                    channel_layer.group_send
                )(
                    "debug_console",
                    message,
                )

        except Exception:
            # لا تجعل نظام الـ logging نفسه يسبب crash للتطبيق
            pass

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
