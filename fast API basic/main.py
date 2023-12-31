from typing import List

from fastapi import FastAPI,HTTPException

from models import User,Gender,Role,UserUpdateRequest

from uuid import UUID

app = FastAPI()

db: List[User] = [
    User(id = UUID("867548df-cb11-4b79-96ca-03eb7ab497de"), 
         first_name = "Jamila",
         last_name="Ahmed",
         gender=Gender.female,
         roles=[Role.student]),
    
    User(id = UUID("7da92197-2e92-4c02-bb39-d8b3a15cebe1"), 
         first_name = "Alex",
         last_name="Jones",
         gender=Gender.male,
         roles=[Role.admin, Role.user]),
]


@app.get("/")
async def read_root():
    return {"Hello": "Along"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user:User):
    db.append(user)
    return {"id":user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return 
    raise HTTPException(
        status_code= 404,
        detail=f"user with id: {user_id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id:UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code= 404,
        detail=f"user with id: {user_id} does not exists"
    )