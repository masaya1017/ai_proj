import datetime
from pydantic import BaseModel, Field

# スキーマでは、FastAPIのデータ構造（dict型)を定義している。
# Stremlitから送信されたデータの整合性を確認できる。

# クラス名については、先頭大文字とするのが基本
# Bookingクラスは継承によって、BaseModelのメソッドの使用や機能の拡張が可能になる。

# 予約モデルの作成
# 予約登録モデル(BaseModelを継承）
class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    booked_num: int  # 予約者数を定義
    start_datetime: datetime.datetime  # 予約開始日時を定義
    end_datetime: datetime.datetime  # 予約終了日時を定義
# 予約一覧表示モデル(予約登録モデルを継承）
class Booking(BookingCreate):
    booking_id: int
    # dict型だけでなく、ORMマッパーにも対応が可能である。
    class Config:
        orm_mode = True

# ユーザモデルの作成
# ユーザ登録モデル
class UserCreate(BaseModel):
    # ユーザ名の長さは12文字として制限する
    username: str = Field(max_length=12)

# ユーザ一覧表示モデル
class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True

# 部屋モデルの作成
# 部屋登録モデル
class RoomCreate(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int  # 部屋の最大人数
# 部屋一覧表示モデル
class Room(RoomCreate):
    room_id: int

    class Config:
        orm_mode = True
