##サーバ起動方法\
今回のアプリは、サーバを二つ起動します。\
一つ目はStreamlit、もう一つはFastapiによるものです。\
まず、Fastapiを起動した後に、Streamlitを起動させる必要があります。\
・app.pyがあるところにcdで移動。その後、以下の二つの操作を行う。\
＊Fastapiの起動方法\
ターミナル上で[uvicorn sql_app.main:app --reload]を実行してください。\
＊Streamlitの起動方法\
ターミナル上で[streamlit run app.py]を実行してください。

##sqlite.dbについて\
デプロイ済みのapp.pyと同じ階層にsql_app.dbがあります。\
そこにはデータが入っているので初期状態でアプリを動かしたいときは、削除したのちにサーバを起動してください。

##サーバを動かす方法\
・pip install fastapi[all]　を実行\
・pip install streamlit　を実行\
・sqliteのインストール（現段階では、windows環境を使用）



