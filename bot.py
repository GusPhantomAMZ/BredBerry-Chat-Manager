import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = int(os.getenv("VK_GROUP_ID"))

if not TOKEN:
    raise RuntimeError("VK_TOKEN не найден")

if not GROUP_ID:
    raise RuntimeError("VK_GROUP_ID не найден")


# Простой HTTP-сервер для Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BredBerry Chat Manager is running!")

    def log_message(self, format, *args):
        pass


def start_web_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"HTTP-сервер запущен на порту {port}")
    server.serve_forever()


# Запускаем HTTP-сервер в отдельном потоке
threading.Thread(target=start_web_server, daemon=True).start()


# Подключение к VK
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

print("🍓 BredBerry Chat Manager запущен!")


# Получение сообщений VK
for event in longpoll.listen():

    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.message
        text = message.get("text", "")
        peer_id = message["peer_id"]

        print(f"Получено сообщение: {text}")

        vk.messages.send(
            peer_id=peer_id,
            message="🍓 BredBerry Chat Manager работает!",
            random_id=0
        )
