随机媒体搜索脚本
概述

此脚本用于从多个频道中搜索随机的视频、图片或文档。

使用方法：

    获取 API 凭证：

        首先，您需要在 https://my.telegram.org/apps 注册并获取您的 API ID 和 API 哈希。

    创建 .env 文件：

        创建一个名为 .env 的文件，并将您的凭证信息填入其中。此脚本使用 SQLite 数据库，因此 .env 文件的格式应如下所示：

          
    api-key = '您的 API 密钥'
    api-hash = '您的 API 哈希'
    SESSION = '您的会话名称'
    DATABASE = '您的数据库名称.db'

        

Use code with caution.

配置目标频道：

    在 getmediaid.py 脚本中，找到 FROM_GROUP_IDS 变量，并将您要从中获取媒体的频道的 ID 添加到列表中。

安装依赖项：

    使用以下命令安装所需的库：

          
    pip3 install -r requirements.txt

        

        Use code with caution.Bash

    运行 getmediaid.py：

        运行 python getmediaid.py 脚本开始获取媒体 ID。请耐心等待，直到抓取过程完成。在抓取过程中，请勿终止终端。

    运行 sendmediaid.py：

        抓取过程完成后，您可以运行 sendmediaid.py 脚本。

    使用方法：

        将您想要搜索的视频发送到您的“已保存的消息”中。

        脚本将会用包含相关信息的 JSON 文件回复您的消息。

重要说明：

    您需要拥有包含视频、图片或文档对象的频道。

    脚本会将媒体信息存储在 SQLite 数据库中。

    getmediaid.py 脚本负责从频道抓取媒体信息并将其存储到数据库中。

    sendmediaid.py 脚本负责根据用户发送的消息搜索并返回相关的媒体信息。

文件说明：

    getmediaid.py：用于从指定频道获取媒体 ID 并存储到数据库。

    sendmediaid.py：用于根据用户的消息搜索并发送相应的媒体信息。

    credential.py：用于从 .env 文件中读取配置信息。

    requirements.txt：列出了脚本所需的 Python 库。

希望此 README 文件对您有所帮助！