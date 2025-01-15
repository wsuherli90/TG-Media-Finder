"""
此脚本允许从频道获取 File_id。

路径：/getmediaid.py
"""

from telethon import TelegramClient
from credential import getPathEnv
import sqlite3

API_KEY, API_HASH, SESSION, DATABASE = getPathEnv()

# 认证状态
client = TelegramClient(SESSION, API_KEY, API_HASH)
FROM_GROUP_IDS = [
    -1009293939393  # 在这里，您必须定义群组的 ID
]
TEMP_DB = []

# 定义连接
def Connection():
    """
    建立与 SQLite 数据库的连接。

    Returns:
        sqlite3.Connection: 数据库连接对象，如果连接成功；否则返回 None。
    """
    connect = sqlite3.connect(DATABASE)
    if connect:
        return connect
    else:
        print('数据库不存在')

# 创建数据库
def createDatabase():
    """
    创建数据库表（如果它们不存在）。
    """
    cursor = Connection().cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS media (
                     row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     media_id INTEGER,
                     group_id INTEGER,
                     message_id INTEGER,
                     message_type TEXT)''')

    cursor.execute(''' CREATE TABLE IF NOT EXISTS last_sending (
                    row_id INTEGER
                    )
                    ''')

    cursor.execute(''' CREATE TABLE IF NOT EXISTS last_id (
                    group_id INTEGER,
                    max_id INTEGER)''')

    cursor.close()

async def getMediaId():
    """
    此函数不是异步的，它从频道获取媒体 ID。
    """
    for group_id in FROM_GROUP_IDS:
        get_max_id = await client.get_messages(group_id)
        min_id = get_max_ids(group_id)
        async for message in client.iter_messages(group_id, min_id=min_id, reverse=True):
            print(f"正在处理来自 {group_id} 的消息")
            if message.photo:
                data = message.photo.id, message.peer_id.channel_id, message.id, 'photo'
                TEMP_DB.append(data)
            elif message.video:
                data = message.video.id, message.peer_id.channel_id, message.id, 'video'
                TEMP_DB.append(data)
            elif message.document:
                data = message.document.id, message.peer_id.channel_id, message.id, 'document'
                TEMP_DB.append(data)
        save_last_message_group_toDB(group_id, get_max_id[0].id)

    save_message_id_toDB()

def get_max_ids(group_id):
    """
    从数据库中获取给定群组的最后一条消息的 ID。

    Args:
        group_id (int): 群组 ID。

    Returns:
        int: 最后一条消息的 ID，如果数据库中没有记录，则返回 1。
    """
    conn = Connection()
    cursor = conn.cursor()
    query = ''' SELECT max_id FROM last_id WHERE group_id = ?'''
    response = cursor.execute(query, (group_id,))
    result = response.fetchone()
    if result:
        for ids in result:
            return ids
    else:
        return 1

def save_last_message_group_toDB(group_id, max_id):
    """
    将给定群组的最后一条消息的 ID 保存到数据库。

    Args:
        group_id (int): 群组 ID。
        max_id (int): 最后一条消息的 ID。
    """
    conn = Connection()
    cursor = conn.cursor()
    query = ''' SELECT group_id FROM last_id WHERE group_id = (?)'''
    response = cursor.execute(query, (group_id,))
    result = response.fetchone()
    if result:
        try:
            query = ''' UPDATE last_id SET max_Id= ? WHERE group_id = ?'''
            cursor.execute(query, (max_id, group_id,))
            conn.commit()
        except sqlite3.Error as e:
            print("错误")
    else:
        try:
            query = ''' INSERT INTO last_id (group_id, max_id) VALUES (?,?)'''
            cursor.execute(query, (group_id, max_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"错误，原因：{e}")

def save_message_id_toDB():
    """
    将媒体 ID、群组 ID、消息 ID 和消息类型保存到数据库。
    """
    global TEMP_DB
    TEMP_DB.sort()
    conn = Connection()
    for data in TEMP_DB:
        media_id = data[0]
        group_id = data[1]
        message_id = data[2]
        message_type = data[3]
        cursor = conn.cursor()
        _query_check = 'SELECT media_id FROM media WHERE media_id = (?) '
        response = cursor.execute(_query_check, (media_id,))
        result = response.fetchall()
        if result:
            print(f"媒体 ID {media_id} 已存在")
        else:
            _inert_query = 'INSERT INTO media (media_id, group_id, message_id, message_type) VALUES (?,?,?,?)'
            cursor.execute(_inert_query, (media_id, group_id, message_id, message_type,))
            conn.commit()

    conn.close()

def start():
    """
    启动脚本。
    """
    try:
        client.loop.run_until_complete(getMediaId())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    createDatabase()
    client.start()
    start()