import uuid
import os
import pathlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
from hyperdb import HyperDB
from datetime import datetime

app = FastAPI()

# Define the data models


class DB_Input(BaseModel):
    name: str
    key: str
    metadata: Any


class DB_Meta(BaseModel):
    id: str
    name: str
    key: str
    metadata: Any
    created_at: datetime
    last_sync: datetime
    updated_at: datetime


# Define the database
databases: dict[str, HyperDB] = {

}

databases_meta: dict[str, DB_Meta] = {

}

# Create data folder
pathlib.Path('data').mkdir(parents=True, exist_ok=True)

# Create endpoints for CRUD operations


@app.get("/db")
async def get_all_dbs() -> List[DB_Meta]:
    return list(databases_meta.values())


@app.post("/db")
async def create_db(db: DB_Input) -> DB_Meta:
    # generate random ID lol
    db_id = str(uuid.uuid4())
    now = datetime.now()
    new_db_meta: DB_Meta = DB_Meta(id=db_id, name=db.name, key=db.key,
                                   metadata=db.metadata, created_at=now, updated_at=now, last_sync=now)
    databases_meta[db_id] = new_db_meta

    new_db = HyperDB(None, db.key)
    new_db.save("data/" + db_id + ".pickle.gz")
    databases[db_id] = new_db

    return new_db_meta


# @app.get("/db/{user_id}", response_model=DB_Meta)
# async def read_user(user_id: int):
#     for user in database["users"]:
#         if user.id == user_id:
#             return user
#     raise HTTPException(status_code=404, detail="User not found")


# @app.put("/db/{user_id}", response_model=DB_Meta)
# async def update_user(user_id: int, user: Dict):
#     for i, user_data in enumerate(database["users"]):
#         if user_data["id"] == user_id:
#             database["users"][i] = user
#             return user
#     raise HTTPException(status_code=404, detail="User not found")


# @app.delete("/db/{user_id}")
# async def delete_user(user_id: int):
#     for i, user_data in enumerate(database["users"]):
#         if user_data["id"] == user_id:
#             database["users"].pop(i)
#             return {"message": "User deleted successfully"}
#     raise HTTPException(status_code=404, detail="User not found")
