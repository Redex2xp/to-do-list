import time
import sqlalchemy.exc
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
import models
from database import SessionLocal, engine, init_db

time.sleep(5) 

try:
    init_db()
except sqlalchemy.exc.OperationalError as e:
    print(
        f"Ошибка подключения к БД. Убедитесь, что Docker-контейнер с PostgreSQL запущен.\n{e}"
    )
    exit()


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Зависимости ---

def get_db():
    """Создает сессию БД для каждого запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Роуты ---

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    """Главная страница - отображение всех задач."""
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/tasks")
def create_new_task(
    title: str = Form(...), 
    description: str = Form(""), 
    db: Session = Depends(get_db)
):
    """Создание новой задачи из формы."""
    crud.create_task(db=db, title=title, description=description)
    return RedirectResponse(url="/", status_code=303)

@app.get("/tasks/{task_id}/toggle")
def toggle_task_done(task_id: int, db: Session = Depends(get_db)):
    """Изменение статуса выполнения задачи."""
    task = crud.get_task(db, task_id)
    if task:
        crud.update_task(db, task.id, task.title, task.description, not task.is_done)
    return RedirectResponse(url="/", status_code=303)

@app.get("/tasks/{task_id}/delete")
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    """Удаление задачи."""
    crud.delete_task(db, task_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
def health_check():
    """Эндпоинт для проверки работоспособности (для Docker HEALTHCHECK)."""
    return {"status": "ok"}
