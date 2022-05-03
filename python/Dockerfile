#ベースイメージのインポート
FROM python:3.6
#環境変数の設定
ARG work_dir=/flask/
#ワーキングディレクトリの設定
WORKDIR $work_dir/src
#フォルダをコンテナ内に移動
ADD src $work_dir/src
#text内に定義されているものをインストール
RUN pip install -r requirements.txt
CMD ["python", "/flask/src/app.py"]