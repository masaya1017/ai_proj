import streamlit as st
import random
import requests
import json
import datetime
import pandas as pd
# streamlitにおけるサイドバー機能を持つ。ユーザを指定して、切り替えることができる。
page = st.sidebar.selectbox('ユーザを指定してください', ['users', 'rooms', 'bookings'])
# usersを選択したとき、以下の処理を行う。
if page == 'users':
    st.title(('ユーザ登録画面'))
    # フォームの作成
    with st.form(key='user'):
        # ユーザIDについては自動で生成する。
        # user_id: int = random.randint(0, 10)
        # 入力できる最大文字数は12文字とする。
        username: str = st.text_input('ユーザー名', max_chars=12)
        # json形式で取得したデータを変数に保存する。
        # jsonの構造はkeyとvalue形式とする。今回は、usernameをFastAPIサーバに送信する。
        user_data = {
            # 'user_id': user_id,
            'username': username
        }
        # 送信ボタンの定義
        submit_button = st.form_submit_button(label='ユーザ登録')

    # 送信ボタンが押されたとき
    if submit_button:
        # urlを指定して、先ほどの送信データをPOSTする。
        url_user = 'http://127.0.0.1:8000/users'
        #requestsのPostメソッドでは、URLを指定し、jsonファイルを変換し、送信する。
        user_res = requests.post(
            url_user,
            data=json.dumps(user_data)
        )
        #ステータスコード=200のときは、問題なく、fastapiサーバにデータを送信し、登録できている。
        #ステータスコードとは、FastAPIサーバより返ってくるメッセージコードみたいなものである。
        if user_res.status_code == 200:
            st.success('ユーザ登録完了')
        #とりあえず、FastAPIより返ってくるデータ（ステータスコードとJSON）を確認できるようにしておく。
        st.write(user_res.status_code)
        st.json(user_res.json())

elif page == 'rooms':
    st.title(('会議室登録画面'))
    # フォームの作成
    with st.form(key='room'):
        # ルームIDについては自動で生成する。
        # room_id: int = random.randint(0, 10)
        # 入力できる最大文字数は12文字とする。
        room_name: str = st.text_input('会議室名', max_chars=12)
        # 定員の定義
        capacity: int = st.number_input('定員', step=1)
        # json形式で取得したデータを変数に保存する。
        # jsonの構造はkeyとvalue形式とする。
        room_data = {
            # 'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        # 送信ボタンの定義
        submit_button = st.form_submit_button(label='会議室登録')

    # 送信ボタンが押されたとき
    if submit_button:
        # urlを指定して、先ほどの送信データをPOSTする。
        url_room = 'http://127.0.0.1:8000/rooms'
        room_res = requests.post(
            url_room,
            data=json.dumps(room_data)
        )
        if room_res.status_code == 200:
            st.success('会議室登録完了')
        st.write(room_res.status_code)
        st.json(room_res.json())

if page == 'bookings':
    st.title(('会議室予約画面'))
    # ユーザ一覧の取得を行う。
    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users = res.json()
    # st.json(users) 中身確認用
    # ユーザ名（キー）：ユーザID（バリュー）
    users_name = {}
    for user in users:
        users_name[user['username']] = user['user_id']
    # st.write(users_name) 中身確認用

    # 会議室一覧の取得
    url_rooms = 'http://127.0.0.1:8000/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }
    # st.write(rooms_dict) 中身確認用

    st.write('### 会議室一覧')
    # pandasを用いて表形式で表示
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    url_bookings = 'http://127.0.0.1:8000/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    users_id = {}
    rooms_id = {}
    for user in users:
        users_id[user['user_id']] = user['username']

    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity']
        }

    # IDを各値に変更する。
    def to_username(x): return users_id[x]
    def to_room_name(x): return rooms_id[x]['room_name']

    def to_datetime(x): return datetime.datetime.fromisoformat(x)\
        .strftime('%Y/%m/%d %H:%M')

    # 特定の列に適用
    if bookings == {}:
        df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
        df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
        df_bookings['start_datetime'] = df_bookings['start_datetime'].map(
            to_datetime)
        df_bookings['end_datetime'] = df_bookings['end_datetime'].map(
            to_datetime)

    df_bookings = df_bookings.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'booked_num': '予約人数',
        'start_datetime': '開始時刻',
        'end_datetime': '終了時刻',
        'booking_id': '予約番号'
    })

    st.write('### 予約一覧')
    st.table(df_bookings)

    # フォームの作成
    with st.form(key='booking'):
        # 選択ボタンにデータを格納
        username: str = st.selectbox('予約者名', users_name.keys())
        room_name: str = st.selectbox('会議室名', rooms_name.keys())
        # 入力できる最大文字数は12文字とする。
        booked_num: str = st.number_input('予約人数', step=1, min_value=1)
        # 日付
        date = st.date_input('日付:', min_value=datetime.date.today())
        start_time = st.time_input(
            '開始時刻:', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input(
            '終了時刻:', value=datetime.time(hour=20, minute=0))
        # json形式で取得したデータを変数に保存する。
        # jsonの構造はkeyとvalue形式とする。

        # 送信ボタンの定義
        submit_button = st.form_submit_button(label='予約登録')

    # 送信ボタンが押されたとき
    if submit_button:
        st.write('## 送信データ')
        user_id: int = users_name[username]
        room_id: int = rooms_name[room_name]['room_id']
        capacity: int = rooms_name[room_name]['capacity']

        booking_data = {
            'user_id': user_id,
            'room_id': room_id,
            'booked_num': booked_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        # validation機能を追加
        # 定員より大きい予約人数の場合
        if booked_num > capacity:
            st.error(
                f'{room_name}の定員は、{capacity}名です。{capacity}名以下の予約人数のみを受付けております。')
        # 開始時間は終了時間よりも早いはずである。
        elif start_time >= end_time:
            st.error('開始時刻が終了時刻を超えています。')
        # 開始時間と終了時間が9～20時の間にあるかを確認している。
        elif start_time < datetime.time(hour=9, minute=0, second=0) or \
                end_time > datetime.time(hour=20, minute=0, second=0):
            st.error('利用時間は9時から20時になります')
        else:
           # urlを指定して、先ほどの送信データをPOSTする。
            url_booking = 'http://127.0.0.1:8000/bookings'
            booking_res = requests.post(
                url_booking,
                data=json.dumps(booking_data)
            )
            if booking_res.status_code == 200:
                st.success('予約完了しました')
            if booking_res.status_code == 404 \
                    and booking_res.json()['detail'] == 'already_booked':
                st.success('指定時間は既に予約が入っています。')
            st.write(booking_res.status_code)  # データの中身確認用
            st.json(booking_res.json())  # データの中身確認用
