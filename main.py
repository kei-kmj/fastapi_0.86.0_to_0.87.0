from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from models import UserModel
from schemas import User, UserCreate, UserDelete

app = FastAPI()


@app.get("/users", response_model=List[User])
def get_users():
    return UserModel.get_users()


@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    created_user = UserModel.create_user(name=user.name, email=user.email)
    return created_user


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    success = UserModel.delete_user(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@app.delete("/users", response_model=dict)
def delete_user_by_body(user_delete: UserDelete):
    success = UserModel.delete_user(user_id=user_delete.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}