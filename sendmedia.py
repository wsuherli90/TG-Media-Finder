"""
此脚本用于获取链接。要使用它，只需向您的“已保存的消息”发送一个视频。
然后，它将在 data.json 中返回文件链接。
"""

from telethon import TelegramClient, events
from credential import getPathEnv
import sqlite3
import json
import os

API_KEY, API_HASH, SESSION, DATABASE = getPathEnv()

_CLIENT = TelegramClient(SESSION, API_KEY, API_HASH)

@_CLIENT.on(events.NewMessage(from_users='me'))  # 使用 from_users='me' 更精确地限定消息来源
async def getLink(event):
    """
    此函数允许等待事件。
    """
    media_id = ''
    message_id = event.message.id
    if event.photo:
        media_id = event.photo.id
    elif event.video:
        media_id = event.video.id
    elif event.document:
        media_id = event.document.id

    if media_id:
        await getMediaId(media_id, message_id)

async def getMediaId(media_id, message_id):
    """
    根据 media_id 在数据库中查找对应的链接，并将结果保存到 data.json 文件中。

    Args:
        media_id (int): 媒体 ID。
        message_id (int): 触发此操作的消息 ID。
    """
    min_limit = media_id - 1000
    max_limit = media_id + 1000  # 您可以调整 min_limit 和 max_limit 的范围
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        query = '''SELECT media_id, group_id, message_id
                   FROM media
                   WHERE media_id BETWEEN (?) AND (?)
                   ORDER BY media_id ASC
                   LIMIT 1000'''
        response = cursor.execute(query, (min_limit, max_limit))
        result = response.fetchall()
        if result:
            links = []
            for data in result:
                # 修正：从 group_id 中去除 100 前缀
                group_id_str = str(data[1])
                if group_id_str.startswith('100'):
                  group_id = group_id_str[3:]
                else:
                  group_id = group_id_str
                link = f"https://t.me/c/{group_id}/{data[2]}"
                links.append(link)
            data = {'file': links}
            await toTxt(data, message_id)
        else:
            await _CLIENT.send_message('me', message='未找到', reply_to=message_id)

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if conn:
            conn.close()

async def toTxt(data, message_id):
    """
    将数据写入 data.json 文件。

    Args:
        data (dict): 要写入的数据。
        message_id (int): 触发此操作的消息 ID。
    """
    with open('data.json', 'w') as path:
        json.dump(data, path, indent=2)

    await sendMessage(message_id)

async def sendMessage(message_id):
    """
    发送 data.json 文件到“已保存的消息”。

    Args:
        message_id (int): 触发此操作的消息 ID。
    """
    await _CLIENT.send_file('me', file='data.json', reply_to=message_id)
    os.remove('data.json')

if __name__ == '__main__':
    _CLIENT.start()
    _CLIENT.run_until_disconnected()