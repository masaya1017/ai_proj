from flask import Flask, jsonify, request
import os
import MySQLdb

app = Flask(__name__)
# 読み込み先のファイルパスを指定する。
conf_file = os.path.join(os.getcwd(), 'conf', 'conf.cfg')
mail_file = os.path.join(os.getcwd(), 'data', 'info.csv')

# 初期設定
app.config.from_pyfile(conf_file)

# データ取得


@app.route('/', methods=['GET'])
def hello():
    result_dict = {}
    address_list = []
    # リクエストデータより、データを抽出
    target_pref = request.args.get('pref')
    '''csvを利用する場合
    # csvデータを一行ずつ読み込み
    with open(mail_file, 'r') as inf:
        for row, line in enumerate(inf):
            # ヘッダー部は無視
            if row == 0:
                continue
            line = line.rstrip()
            # データの分割
            vals = line.split(',')
            mail, sex, age, name, pref = vals

            # リクエストしたデータとＣＳＶデータが一致している場合
            if target_pref == pref:
                address_list.append(mail)

        # key='mail_address_list' value=address_list
        result_dict['mail_address_list'] = address_list
        # json化
        return jsonify(result_dict)
    '''

    # MYSQLを利用する場合
    conn = MySQLdb.connect(user='root', passwd='pass',
                           host='db_server', db='testdb')
    cur = conn.cursor()
    sql = "select * from personal_info;"
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        mail_add, sex, age, name, prefecture, insert_date, update_date = row
        if target_pref:
            if prefecture == target_pref:
                address_list.append(mail_add)
        else:
            address_list.append(mail_add)

    result_dict['mail_address_list'] = address_list
    return jsonify(result_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
