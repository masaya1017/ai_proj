import sys
import os
import time
import datetime
from google.cloud import pubsub_v1

# コマンド実行時の引数をsys.argvによって取得することができる。
# 今回指定するのは、GCPのプロジェクトID、トピック名、サービスアカウントキーのJSONファイル
project_id, topic_name = sys.argv[1], sys.argv[2]
cred_file = sys.argv[3]
# サービスアカウントキーのJSONファイルを読み込む
publisher = pubsub_v1.publisher.Client.from_service_account_file(cred_file)
# プロジェクトIDとトピック名より、トピックを探索する。
topic_path = publisher.topic_path(project_id, topic_name)

cnt = 0
while True:
    data = u"Message from test publisher {}".format(
        cnt) + datetime.datetime.now().isoformat(" ")
    # データを送信するときは、unicode-8によってエンコードしておく。
    data = data.encode("utf-8")
    print("Publish: " + data.decode("utf-8", "ignore"))
    future = publisher.publish(topic_path, data=data)
    print("return ", future.result())
    # publishは0.25秒おきに実行する。
    time.sleep(0.25)
    cnt = cnt + 1
