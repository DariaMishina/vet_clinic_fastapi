from enum import Enum
from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10),
]

@app.get("/")
async def root():
    return {"message": "WELCOME TO VET CLINIC!"}

@app.post("/post", response_model=Timestamp)
async def get_post():
    new_timestamp = Timestamp(id=len(post_db), timestamp=int(round(datetime.now().timestamp())))
    post_db.append(new_timestamp)
    return new_timestamp

@app.get("/dog", response_model=list[Dog])
async def get_dogs(kind: DogType = Query(None, description="Filter dogs by kind")):
    if kind:
        filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return filtered_dogs
    else:
        return list(dogs_db.values())

@app.post("/dog", response_model=Dog)
async def create_dog(dog: Dog):
    # Генерировать уникальный pk для новой собаки
    new_pk = max(dogs_db.keys()) + 1
    dog.pk = new_pk
    dogs_db[new_pk] = dog
    return dog

# отправлять json в тело запроса в таком формате
# {
#     "name": "Sharik",
#     "pk": 7,
#     "kind": "terrier"
# }

@app.get("/dog/{pk}", response_model=Dog)
async def get_dog_by_pk(pk: int = Path(..., description="Primary key of the dog")):
    if pk in dogs_db:
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=404, detail="Dog not found")

@app.patch("/dog/{pk}", response_model=Dog)
async def update_dog(pk: int = Path(..., description="Primary key of the dog"), updated_dog: Dog = Body(..., description="Updated dog data")):
    if pk in dogs_db:
        dogs_db[pk] = updated_dog
        return updated_dog
    else:
        raise HTTPException(status_code=404, detail="Dog not found")

# отправлять json в тело запроса в таком формате
# {
#     "name": "Tuzik",
#     "pk": 2,
#     "kind": "dalmatian"
# }