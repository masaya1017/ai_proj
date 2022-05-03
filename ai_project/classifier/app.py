import os
import shutil
from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from PIL import Image
import numpy as np

UPLOAD_FOLDER = "./classifier/static/images/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

labels = ["飛行機", "自動車", "鳥", "猫", "鹿", "犬", "カエル", "馬", "船", "トラック"]
n_class = len(labels)
img_size = 32
n_result = 3  # 上位3つの結果を表示

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config['DEBUG'] = True  # デバッグモードをTrueにする


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
# 初期表示時はGETによって、「index.html」が返される。
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    # 判定ボタンを押す(SUBMIT)とPOST処理が行われる。
    if request.method == "POST":
        # ファイルの存在と形式を確認
        if "file" not in request.files:
            print("File doesn't exist!")
            return redirect(url_for("index"))
        file = request.files["file"]
        if not allowed_file(file.filename):
            print(file.filename + ": File not allowed!")
            return redirect(url_for("index"))

        # アップロードしたファイルをローカルのフォルダに落として保存する。
        if os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)
        # ファイル名を安全なものにする。
        #filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 画像の読み込み
        image = Image.open(filepath)
        # 色の変換
        image = image.convert("RGB")
        # サイズの変換
        image = image.resize((img_size, img_size))
        # numpy配列化
        x = np.array(image, dtype=float)
        # 配列のサイズの変更後に、正規化
        x = x.reshape(1, img_size, img_size, 3) / 255

        # モデルの読み込み
        model = load_model("./image_classifier.h5")
        # モデルにデータを渡し、推測させる。
        y = model.predict(x)[0]
        sorted_idx = np.argsort(y)[::-1]  # 降順でソート
        result = ""
        for i in range(n_result):
            idx = sorted_idx[i]
            ratio = y[idx]
            label = labels[idx]
            result += "<p>" + str(round(ratio*100, 1)) + \
                "%の確率で" + label + "です。</p>"
        return render_template("result.html",
                               result=Markup(result),
                               filepath=f"../../static/images/{file.filename}")
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
