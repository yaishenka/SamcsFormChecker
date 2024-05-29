import vk_api
import random
from vk_settings import common_token

vk_session = vk_api.VkApi(token=common_token)
vk = vk_session.get_api()


i = 1
while True:
    peer_id = 2000000000 + i
    try:
        result = vk.messages.getConversationsById(peer_ids=[peer_id])
    except Exception as e:
        print(e)
        print(f"Sending hello to {peer_id}")
        try:
            vk.messages.send(
                message="Hi! Я бот, буду помогать с заполнением формы",
                peer_id=peer_id,
                random_id=random.randint(0, 2 ** 30)
            )
        except:
            i += 1
        continue
    item = result['items'][0]
    print(f"{peer_id}:\t{item['chat_settings']['title']}")

    i += 1
