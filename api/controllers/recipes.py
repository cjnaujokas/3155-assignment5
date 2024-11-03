from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        amount=recipe.amount,
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def update(db: Session, recipe_id, recipe):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    update_data = recipe.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recipe, field, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def delete(db: Session, recipe_id):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)