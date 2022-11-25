from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="FastAPI with PostgreSQL",
    description="This a REST API with FastAPI library, with PostgreSQL and SqlAlchemy ORM",
    version="1.0.0",
    openapi_tags=[{
        "name":"Users",
        "description":"Basic CRUD for Users"
    }]
)

app.include_router(user)