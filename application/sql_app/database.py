from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# ローカル上に作成されるDBの出力先
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
# sqliteの操作に必要な基盤のインスタンス化
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)
# session（DBの一連の操作）と先ほどの基盤をバインドする。
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
