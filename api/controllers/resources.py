from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, resource):
    # Create a new instance of the Order model with the provided data
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )
    # Add the newly created Order object to the database session
    db.add(db_resource)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_resource)
    # Return the newly created Order object
    return db_resource

def update(db: Session, resource_id, resource):
    # Query the database for the specific order to update
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Extract the update data from the provided 'order' object
    update_data = resource.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_resource.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_resource.first()

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

def delete(db: Session, resource_id):
    # Query the database for the specific order to delete
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Delete the database record without synchronizing the session
    db_resource.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
