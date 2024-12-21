from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask, TaskResponse
from app.backend.db_depends import get_db
from sqlalchemy import select, update, delete
from slugify import slugify

router = APIRouter()

# Получение всех заданий
@router.get("/", response_model=List[TaskResponse])
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task)
    tasks = db.scalars(stmt).all()
    return tasks

# Получение задания по ID
@router.get("/{task_id}", response_model=TaskResponse)
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.id == task_id)
    task = db.scalar(stmt)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

# Создание задания
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(task: CreateTask, db: Annotated[Session, Depends(get_db)]):
    # Проверка существования пользователя
    user_stmt = select(User).where(User.id == task.user_id)
    user = db.scalar(user_stmt)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Генерация уникального slug для задания
    task_slug = slugify(task.title)

    # Создание нового задания
    new_task = Task(
        title=task.title,
        content=task.content,
        priority=task.priority,
        slug=task_slug,
        completed=False,  # По умолчанию задание не завершено
        user_id=task.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Обновление задания
@router.put("/update/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.id == task_id)
    existing_task = db.scalar(stmt)
    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Обновляем задание, обновляем только те поля, которые были переданы
    updated_values = {
        "title": task.title if task.title is not None else existing_task.title,
        "content": task.content if task.content is not None else existing_task.content,
        "priority": task.priority if task.priority is not None else existing_task.priority,
        "completed": task.completed if task.completed is not None else existing_task.completed
    }

    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(updated_values)
        .execution_options(synchronize_session="fetch")
    )
    db.execute(stmt)
    db.commit()

    # Обновленный task
    db.refresh(existing_task)
    return existing_task

# Удаление задания
@router.delete("/delete/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Task).where(Task.id == task_id)
    existing_task = db.scalar(stmt)
    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Удаляем задание
    stmt = delete(Task).where(Task.id == task_id)
    db.execute(stmt)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deleted successfully!"}


