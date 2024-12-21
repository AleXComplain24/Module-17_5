from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем объект Engine для подключения к базе данных
DATABASE_URL = "sqlite:///./test.db"  # Пример для SQLite базы данных

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей
Base = declarative_base()

# Создание таблиц в базе данных
def create_db():
    Base.metadata.create_all(bind=engine)
