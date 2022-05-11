import os
import sys
import time
import datetime
from google.cloud import pubsub_v1


def callback(message):
    now = datetime.datetime.now()
    print("msg = \"" + message.data.decode("utf-8") +
          "\"" + "  [" + now.isoformat(" ") + "]")
    message.ack()


# コマンド実行時の引数をsys.argvによって取得することができる。
# 今回指定するのは、GCPのプロジェクトID、トピック名、サービスアカウントキーのJSONファイル
project_id, sub_name, cred_file = sys.argv[1],  sys.argv[2], sys.argv[3]
# サービスアカウントキーのJSONファイルを読み込む
subscriber = pubsub_v1.subscriber.Client.from_service_account_file(cred_file)
# プロジェクトIDとトピック名より、トピックを探索する。
subpath = subscriber.subscription_path(project_id, sub_name)
flow_control = pubsub_v1.types.FlowControl(max_messages=2)
# データを取得する。
subscriber.subscribe(subpath, callback=callback, flow_control=flow_control)
input()
