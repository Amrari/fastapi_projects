from pydantic import BaseModel, HttpUrl
from typing import Sequence


class Learning_path(BaseModel):
    label: str
    source: str
    URL: HttpUrl


class learning_path_create(BaseModel):  
    course: str
    label: str
    URL: HttpUrl
    submitter: str

class learning_path_Update(Learning_path):
    label: str


# Properties shared by models stored in DB
class LPInDBBase(Learning_path):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


class LPupdate(BaseModel):
    id: int
    label: str

# Properties to return to client
class LP(LPInDBBase):
    pass


# Properties properties stored in DB
class LPInDB(LPInDBBase):
    pass


class LPSearchResults(BaseModel):
    results: Sequence[LP]
