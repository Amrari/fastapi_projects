from pydantic import BaseModel, HttpUrl
from typing import Sequence


class Learning_path(BaseModel):
    id: int
    label: str
    source: str
    URL: HttpUrl

class learning_path_list(BaseModel):
    learning_path: Sequence[Learning_path]

class learning_path_create(BaseModel):
    id: int
    label: str
    URL: HttpUrl
    submitter: str