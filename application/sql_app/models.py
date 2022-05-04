from pydantic import IntegerError
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .database import Base


# userモデルの作成
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

# roomモデルの作成


class Room(Base):
    __tablename__ = 'rooms'
    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, unique=True, index=True)
    capacity = Column(Integer)

# 予約モデルの作成


class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        'users.user_id', ondelete='SET NULL'), nullable=False)
    room_id = Column(Integer, ForeignKey(
        'rooms.room_id', ondelete='SET NULL'), nullable=False)
    booked_num = Column(Integer)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
