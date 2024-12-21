from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.backend.db import Base  # Import Base from db module
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = 'tasks'

    # Это добавлено для разрешения ошибки
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    priority = Column(Integer, default=0, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)

    # Relationship with the User table
    user = relationship('User', back_populates='tasks')

# Pydantic Schemas
from pydantic import BaseModel

# User schemas
class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(BaseModel):
    firstname: str = None
    lastname: str = None
    age: int = None

class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int

    class Config:
        orm_mode = True

# Task schemas
class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    user_id: int
    
class UpdateTask(BaseModel):
    title: str = None
    content: str = None
    priority: int = None
    completed: bool = None

class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    completed: bool
    slug: str
    user_id: int

    class Config:
        orm_mode = True
