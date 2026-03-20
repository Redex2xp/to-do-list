# crud.py
from sqlalchemy.orm import Session
import models

def get_task(db: Session, task_id: int):
    """Получение задачи по ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка всех задач."""
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, title: str, description: str):
    """Создание новой задачи."""
    db_task = models.Task(title=title, description=description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, title: str, description: str, is_done: bool):
    """Обновление существующей задачи."""
    db_task = get_task(db, task_id)
    if db_task:
        db_task.title = title
        db_task.description = description
        db_task.is_done = is_done
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """Удаление задачи."""
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
