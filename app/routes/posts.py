from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db

router = APIRouter(
    tags=['Posts']
)
# prefix=/post then remove it with /


@router.get("/get/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/add/post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def add_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    post_dict = post.model_dump()
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/get/post/{post_id}", response_model=schemas.Post)
def get_one_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{post_id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id:{post_id} not found"}
    return post


@router.delete("/delete/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{post_id} not found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/post/{post_id}", response_model=schemas.Post)
def update_one_post(post_id: int, post_model: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    print(post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{post_id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id:{post_id} not found"}

    post_query.update(post_model.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


#
# @router.get("/posts")
# async def get_all_post():
#     cursor.execute("""SELECT * FROM post""")
#     posts = cursor.fetchall()
#     return {"data": posts}
#
#
# @router.post("/post", status_code=status.HTTP_201_CREATED)
# async def create_post(post: schemas.CreatePost):
#     cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}
#
#
# @router.get("/post/{post_id}")
# def get_post(post_id: int, response: Response):
#     cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(post_id)))
#     post = cursor.fetchone()
#     # print(post_id)
#     # post = find_post(post_id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{post_id} not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id:{post_id} not found"}
#     return {"data": post}
#
#
# @router.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(post_id: int):
#     cursor.execute("""DELETE FROM post where id = %s RETURNING * """, (str(post_id)))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{post_id} not found")
#
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#
# @router.put("/post/{post_id}")
# def update_post(post_id: int, post: schemas.PostBase):
#     cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
#                    (post.title, post.content, post.published, str(post_id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{post_id} not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id:{post_id} not found"}
#
#     return {"data": updated_post}
