from fastapi import FastAPI

app = FastAPI()
# ルーティング(entory point)

# デコレータ⇒直下の関数の処理を受け取り、appにおいてget処理を行わせる。
# async⇒非同期処理を行うことができる。（複数の処理を同時に行う）
# レスポンスはjson形式のデータとする。


@app.get("/")
async def index():
    return {"message": "Hello World"}
