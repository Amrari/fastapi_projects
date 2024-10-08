import logging
from app import schemas
from app.schemas import learning_path
from sqlalchemy.orm import Session

from app import crud
from app.db import base  # noqa: F401
from app.learning_path_data import LEARNING_PATH

logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@LPeapi.com"



def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            user_in = learning_path.UserCreate(
                full_name="Initial Super User",
                email=FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.LP:
            for learning_path in LEARNING_PATH:
                learning_path_in = schemas.learning_path_create(
                    label=learning_path["label"],
                    source=learning_path["source"],
                    url=learning_path["url"],
                    submitter_id=user.id,
                )
                crud.crud_learning_path.create(db, obj_in=learning_path_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
