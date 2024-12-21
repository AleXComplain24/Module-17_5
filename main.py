from fastapi import FastAPI
from routers import category, products
from routers import task, user
import uvicorn


app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "My shop"}

# Подключение маршрутов
app.include_router(category.router)
app.include_router(products.router)
app.include_router(task.router)
app.include_router(user.router)


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)