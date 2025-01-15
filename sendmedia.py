""" Path: /sendmedia.py

此函数用于以 .JSON 格式发送频道链接数据。
"""

import sqlite3
import time
from telethon import TelegramClient, events
from telethon.tl import types
from credential import getPathEnv

API_KEY, API_HASH, SESSION, DATABASE = getPathEnv()

client = TelegramClient(SESSION, API_KEY, API_HASH)
DATA = []

def connection():
    """
    建立与 SQLite 数据库的连接。

    Returns:
        sqlite3.Connection: 数据库连接对象。

    Raises:
        sqlite3.DatabaseError: 如果连接数据库失败，则抛出此异常。
    """
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.DatabaseError as e:
        raise e

async def sending_media(row):
    """
    发送媒体消息。

    Args:
        row (int): 当前处理的行号。
    """
    rows = row
    global DATA
    for item in DATA:
        for items in item:
            group_id = items[2]
            message_id = items[3]

            async for items in client.iter_messages(group_id, min_id=message_id):
                await client.send_message(entity=-1002483750921, message=items)
                await insert_data_db(rows)
                rows += 1
                print('消息发送成功')
                time.sleep(3)

async def insert_data_db(row_id):
    """
    将数据插入数据库或更新数据库中的现有数据。

    Args:
        row_id (int): 要插入或更新的行号。
    """
    rows = row_id - 1
    conn = connection()
    cursor = conn.cursor()
    _check_query = 'SELECT row_id FROM last_sending WHERE row_id = (?)'
    response = cursor.execute(_check_query, (row_id,))
    result = response.fetchall()
    if result:
        _update_query = f'''UPDATE last_sending SET row_id = {row_id} WHERE row_id = (?)'''
        cursor.execute(_update_query, (rows,))
        conn.commit()
        conn.close()
    else:
        _insert_query = '''INSERT INTO last_sending (row_id) VALUES (?)'''
        cursor.execute(_insert_query, (row_id,))
        conn.commit()
        conn.close()

async def get_data_from_db():
    """
    从数据库中获取数据并调用 sending_media 函数发送消息。
    """
    global DATA

    conn = connection()
    cursor = conn.cursor()
    query_row = ''' SELECT row_id FROM last_sending'''
    response = cursor.execute(query_row)
    result = response.fetchall()
    if result:
        for item in result:
            lst_row = item[0]
    else:
        lst_row = 0

    query = f'''SELECT * FROM media WHERE row_id LIMIT -1 OFFSET {lst_row}'''
    response = cursor.execute(query)
    result = response.fetchall()
    DATA.append(result)

    await sending_media(lst_row)

if __name__ == "__main__":
    client.start()
    client.loop.run_until_complete(get_data_from_db())