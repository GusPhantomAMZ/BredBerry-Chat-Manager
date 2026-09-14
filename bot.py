import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "ТВОЙ_ТОКЕН"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

print("BredBerry Chat Manager запущен!")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        vk.messages.send(
            user_id=event.user_id,
            message="🍓 BredBerry Chat Manager работает!",
            random_id=0
        )
