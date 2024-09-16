from app.crud.base import CRUDBase
from app.models.learning_path import Learning_Path
from app.schemas.learning_path import learning_path_create, learning_path_Update


class CRUDLearning_Path(CRUDBase[Learning_Path, learning_path_create, learning_path_Update]):
    ...


learning_path = CRUDLearning_Path(Learning_Path)
