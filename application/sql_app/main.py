from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import cruds, models, schemas
from .database import session_local, engine
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# dbのセッション情報を取得する。
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


'''
@app.get("/")
async def index():
    return {"message": "Success"}
'''

# 一覧表示用URL


@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db)):
    users = cruds.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/rooms", response_model=List[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db)):
    rooms = cruds.get_rooms(db, skip=skip, limit=limit)
    return rooms


@app.get("/bookings", response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100,
                        db: Session = Depends(get_db)):
    bookings = cruds.get_bookings(db, skip=skip, limit=limit)
    return bookings

# 登録用URL


@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return cruds.create_user(db=db, user=user)


@app.post("/rooms", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return cruds.create_room(db=db, room=room)


@app.post("/bookings", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate,
                         db: Session = Depends(get_db)):
    return cruds.create_booking(db=db, booking=booking)
