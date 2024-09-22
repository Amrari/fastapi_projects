from typing import Union
from pytest import Session
from app.crud.base import CRUDBase
from app.models.learning_path import Learning_Path
from app.schemas.learning_path import LPupdate, learning_path_create, learning_path_Update


class CRUDLearning_Path(CRUDBase[Learning_Path, learning_path_create, learning_path_Update]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Learning_Path,
        obj_in: Union[learning_path_Update, LPupdate]
    ) -> Learning_Path:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


learning_path = CRUDLearning_Path(Learning_Path)
