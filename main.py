import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from hyperdb import HyperDB

app = FastAPI()

# Define the data models


class DB_Input(BaseModel):
    name: str
    key: str
    metadata: str

    # class Config:
    #     frozen = True


class DB(BaseModel):
    id: str
    name: str
    key: str
    metadata: str


# Define the database
databases = {

}

databases_meta = {

}

# Create endpoints for CRUD operations


@app.post("/db")
async def create_db(db: DB_Input) -> DB:
    # generate random ID lol
    db_id = str(uuid.uuid4())
    new_db: DB = {'id': db_id, 'name': db.name,
                  'metadata': db.metadata, 'key': db.key}
    databases[db_id] = {'id': db_id,
                        'metadata': db.metadata, db: HyperDB(None, db.key)}
    databases_meta[db_id] = new_db
    return new_db


@app.get("/db")
async def read_users() -> List[DB]:
    print(list(databases_meta.values()))
    return list(databases_meta.values())


@app.get("/db/{user_id}", response_model=DB)
async def read_user(user_id: int):
    for user in database["users"]:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/db/{user_id}", response_model=DB)
async def update_user(user_id: int, user: Dict):
    for i, user_data in enumerate(database["users"]):
        if user_data["id"] == user_id:
            database["users"][i] = user
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/db/{user_id}")
async def delete_user(user_id: int):
    for i, user_data in enumerate(database["users"]):
        if user_data["id"] == user_id:
            database["users"].pop(i)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
