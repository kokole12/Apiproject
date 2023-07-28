from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from pprint import pprint
from typing import List, Optional
from ..database import engine, get_db
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get('/', response_model=List[schemas.PostRespone])
@router.get('/')
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search.capitalize())).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id)
    pprint(results)
    return posts


@router.get('/mine', response_model=List[schemas.PostRespone])
def get_my_Posts(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED,
            response_model=schemas.PostRespone)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *''',
    #                 (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    # post_dict = new_post.model_dump()
    # post_dict['id'] = randrange(0, 100)
    # my_posts.append(post_dict)
    # print(post_dict)
    # print(new_post.model_dump())
    print(current_user.id)
    newPost = models.Post(user_id=current_user.id,**post.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@router.get('/{id}', response_model=schemas.PostRespone)
def get_post(id: int, response: Response, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute('''SELECT * FROM post where id = %s''', str(id))
    # post = cursor.fetchone()
    if post is not None:
        return post
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post with id {id}")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute('''DELETE FROM post WHERE id = %s RETURNING *''', (str(id),))
    # conn.commit()
    # post = cursor.fetchone()
    print(post.first().user_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post woth id: {id}")
    
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not epermitted to perform this action")
    
    post.delete(synchronize_session=False)
    db.commit()
    return post


@router.put('/{id}', response_model=schemas.PostRespone)
def update_post(id: int, posts: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    # cursor.execute('''UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''',
    #                (post.title, post.content, post.published, str(id),))
    # conn.commit()
    # post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not epermitted to perform this action")
    
    post_query.update(posts.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()