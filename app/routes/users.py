from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas, util
from ..database import get_db

router = APIRouter(
    tags=['Users']
)


@router.post("/create/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_password = util.hashed_password(user.password)
    user.password = hashed_password

    user_dict = user.model_dump()
    new_user = models.User(**user_dict)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as e:
        # Rollback the changes to maintain data consistency
        db.rollback()

        if "unique constraint" in str(e.orig).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with the same email already exists.")
        else:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="An error occurred while processing your request")

    db.refresh(new_user)
    return new_user


@router.get("/user/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User doesn't exists.")

    return user
