from operator import and_
import os
from typing import Dict, List
from sqlalchemy.orm import Session
from db.database import get_session
import uuid
from db.model.api_inventory import APIInventory
from db.model.api_spec import APISpec
from db.model.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def add_user(name: str, email: str, password: str):
    """
    Create and insert user object given input params
    """
    user = User(
        user_id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=generate_password_hash(password),
    )
    # insert user
    session: Session = get_session()
    session.add(user)
    session.commit()


def get_user(email: str = None, user_id: str = None):
    """
    Retrieve user object given email id or user_id
    """
    session: Session = get_session()
    user = None
    if email:
        user = session.query(User).filter_by(email=email).first()
    elif user_id:
        user = session.query(User).filter_by(user_id=user_id).first()
    else:
        # TODO: Make this a DBException class
        raise Exception("Missing required parameters to get user from db")
    return user


def add_api_to_inventory(api_path: str, api_details: Dict):
    """
    Insert or Update api path in inventory table based on whether it exists
    """
    session: Session = get_session()
    api_path_obj = session.query(APIInventory).filter_by(api_path=api_path).first()
    # http_method
    http_method = api_details.get("http_method")
    session: Session = get_session()
    if not api_path_obj:
        spec_id = api_details.get("spec_id")
        user_id = api_details.get("user_id")
        added_by = api_details.get("added_by")
        found_in_file = api_details.get("found_in_file")
        # Store additional info if any
        message = api_details.get("message")
        api_inventory_object = APIInventory(
            spec_id=spec_id,
            user_id=user_id,
            added_by=added_by,
            api_path=api_path,
            http_method=http_method,
            found_in_file=found_in_file,
            message=message,
        )
        session.add(api_inventory_object)
        session.commit()
    else:
        # TODO: Chance of a bug: As per below logic, we are extending http methods for existing APIs
        # However, in case a http method for existing endpoint is deleted/deprecated from code.
        # It may still linger here as per method extension logic
        temp: List = api_path_obj.http_method.split(",")
        # Extend http methods if incoming method isn't part of existing list
        if http_method and temp and http_method not in temp:
            temp.append(http_method)
            temp.sort()
            methoD = ",".join(temp)
            api_path_obj.method = methoD
            session.commit()


def get_discovered_apis(user_id):
    """
    Get discovered APIs given user id
    """
    session: Session = get_session()
    inventory = session.query(APIInventory).filter_by(user_id=user_id).first()
    return inventory


def get_spec(spec_id, api_path=None):
    """
    Retrieve spec object given spec_id & api path
    """
    session: Session = get_session()
    # spec = None
    # if api_path:
    # spec = (
    # session.query(APISpec)
    # .filter(and_(spec_id == spec_id, api_path == api_path))
    # .first()
    # )
    # else:
    spec = session.query(APISpec).filter_by(spec_id=spec_id).first()
    return spec


def add_spec(
    spec_id: str, user_id: str, collection_name: str, file_name: str, data_dir: str
):
    """
    Add following records to db
    1. openapi spec to specs table
    2. api to inventory table
    """
    session: Session = get_session()
    spec = APISpec(spec_id, user_id, collection_name, file_name, data_dir)
    session.add(spec)
    session.commit()
