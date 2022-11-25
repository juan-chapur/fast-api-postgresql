from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet_function = Fernet(key)

user = APIRouter()

@user.get("/users", response_model=list[User], tags=["Users"])
def get_users():
    sql_query=users.select()
    return conn.execute(sql_query).fetchall()

@user.post("/users", response_model=User, tags=["Users"])
def get_users(user: User):
    new_user = {"name":user.name, "email":user.email}
    new_user["password"] = fernet_function.encrypt(user.password.encode("utf-8"))
    sql_query = users.insert().values(new_user)
    conn.execute(sql_query)
    print(sql_query)
    return conn.execute(users.select().where(users.c.email == user.email)).first()

@user.get("/users/{id}", response_model=User, tags=["Users"])
def get_user(id:str):
    sql_query=users.select().where(users.c.id == id)
    return conn.execute(sql_query).first()

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id:str):
    sql_query=users.delete().where(users.c.id == id)
    conn.execute(sql_query)
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}", response_model=User, tags=["Users"])
def update_user(id:str, user:User):
    password_encrypt = fernet_function.encrypt(user.password.encode("utf-8"))
    sql_query=users.update().values(
        name=user.name, 
        email=user.email,
        password=password_encrypt).where(users.c.id == id)
    conn.execute(sql_query)
    return conn.execute(users.select().where(users.c.email == user.email)).first()