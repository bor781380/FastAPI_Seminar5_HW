# задача 3-6, джинжа должна вернуть шаблон в гет т.е. НТМЛ страницу
# Задание №3
# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Реализуйте валидацию данных запроса и ответа.

# Задание №4
# Создать API для обновления информации о пользователе в базе данных.
# Приложение должно иметь возможность принимать PUT запросы с данными
# пользователей и обновлять их в базе данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для обновления информации о пользователе (метод PUT).
# Реализуйте валидацию данных запроса и ответа.

# Задание №5
# Создать API для удаления информации о пользователе из базы данных.
# Приложение должно иметь возможность принимать DELETE запросы и
# удалять информацию о пользователе из базы данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для удаления информации о пользователе (метод DELETE).
# Реализуйте проверку наличия пользователя в списке и удаление его из
# списка.

# Задание №6
# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.


import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = [
    User(id=1, name="Андрей", email="andrey@mail.ru", password="123"),
    User(id=2, name="Сергей", email="sergey@mail.ru", password="111"),
    User(id=3, name="Иван", email="ivan@mail.ru", password="000"),
    User(id=4, name="Василий", email="vasay@mail.ru", password="123456"),
]


@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post("/users", response_model=User)
async def create_user(user: User):
    users.append(user)
    print(users)
    return user


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    for index, u in enumerate(users):
        if u.id == user_id:
            users[index] = user
            return user
    #return {"user_id": user_id, "user": user}
    return HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, u in enumerate(users):
        if u.id == user_id:
            del users[index]
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/")
async def user_list(request: Request):
    print(request)
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})


if __name__ == "__main__":
    uvicorn.run("hw1:app", host="127.0.0.1", port=8000)