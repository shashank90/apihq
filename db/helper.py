from operator import and_
import os
from typing import Dict, List
from sqlalchemy import desc
from sqlalchemy.orm import Session
from db.database import get_session
import uuid
from db.model.api_inventory import ApiInventory
from db.model.api_spec import ApiSpec
from db.model.user_login import Login
from db.model.user_api_run_limit import UserApiRunLimit
from db.model.api_run import ApiRun, RunStatusEnum
from db.model.user import User
from db.model.api_validate import ApiValidate, ValidateStatusEnum
from werkzeug.security import generate_password_hash, check_password_hash


def add_user(name: str, email: str, password: str, company_name: str):
    """
    Create user object in db given input params
    """
    user = User(
        user_id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=generate_password_hash(password),
        company_name=company_name,
    )
    # insert user
    session: Session = get_session()
    session.add(user)
    session.commit()
    return user


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


def update_validation_status(spec_id: str, user_id: str, status: ValidateStatusEnum):
    """
    Update spec validation status
    """
    session: Session = get_session()
    api_validate = (
        session.query(ApiValidate).filter(ApiValidate.spec_id == spec_id).first()
    )
    # Update status
    if api_validate:
        api_validate.status = status
    # Or insert fresh record
    else:
        api_validate = ApiValidate(spec_id, user_id, status)
        session.add(api_validate)
    session.commit()


def get_api_status(spec_id: str) -> str:
    """
    Given spec id, get validation status
    """
    spec: ApiSpec = get_spec(spec_id)
    return spec.validate_result.status.name


def get_validation_status(spec_id: str) -> str:
    """
    Get validation status given spec_id
    """
    session: Session = get_session()
    api_validate = session.query(ApiValidate).filter_by(spec_id=spec_id).first()
    return api_validate.status.name


def get_run_records(user_id: str) -> List[ApiRun]:
    """
    Get api run records for a given user
    """
    session: Session = get_session()
    api_runs = (
        session.query(ApiRun)
        .filter_by(user_id=user_id)
        .order_by(desc(ApiRun.time_updated))
    )
    return api_runs


def get_api_details(api_id: str) -> ApiInventory:
    """
    Get api record given api_id
    """
    session: Session = get_session()
    api_run = session.query(ApiInventory).filter_by(api_id=api_id).first()
    return api_run


def add_login_details(user_id: str, ip_addr: str = None):
    session: Session = get_session()
    login_details: Login = Login(user_id, ip_addr)
    session.add(login_details)
    session.commit()


def add_api_run_limit(user_id: str, limit: int):
    session: Session = get_session()
    user_api_run_limit: UserApiRunLimit = UserApiRunLimit(user_id, limit)
    session.add(user_api_run_limit)
    session.commit()


def get_run_details(run_id: str) -> ApiRun:
    """
    Get run record given run_id
    """
    session: Session = get_session()
    api = session.query(ApiRun).filter_by(run_id=run_id).first()
    return api


def add_run_details(run_id: str, api_id: str, user_id: str, run_status: RunStatusEnum):
    """
    Add run record
    """
    session: Session = get_session()
    api_run = ApiRun(run_id, api_id, user_id, run_status)
    session.add(api_run)
    session.commit()


def update_run_details(run_id: str, run_status: RunStatusEnum, message=None):
    session: Session = get_session()
    api_run = session.query(ApiRun).filter_by(run_id=run_id).first()
    api_run.status = run_status
    if message:
        api_run.message = message
    session.commit()


def add_api_to_inventory(user_id: str, api_path: str, api_details: Dict):
    """
    Insert or Update api path in inventory table based on whether it exists
    """
    session: Session = get_session()
    api_path_obj = (
        session.query(ApiInventory)
        .filter(
            and_(ApiInventory.user_id == user_id, ApiInventory.api_path == api_path)
        )
        .first()
    )
    # http_method
    http_method = api_details.get("http_method")
    session: Session = get_session()

    api_endpoint_url = api_details.get("api_endpoint_url")
    spec_id = api_details.get("spec_id")

    if not api_path_obj:
        api_id = api_details.get("api_id")
        user_id = api_details.get("user_id")
        added_by = api_details.get("added_by")
        found_in_file = api_details.get("found_in_file")
        # Store additional info if any
        message = api_details.get("message")
        api_inventory_object = ApiInventory(
            api_id=api_id,
            spec_id=spec_id,
            user_id=user_id,
            added_by=added_by,
            api_path=api_path,
            api_endpoint_url=api_endpoint_url,
            http_method=http_method,
            found_in_file=found_in_file,
            message=message,
        )
        session.add(api_inventory_object)
        session.commit()
    else:
        # Overwrite api path and endpoint url
        api_path_obj.api_path = api_path
        api_path_obj.api_endpoint_url = api_endpoint_url
        api_path_obj.spec_id = spec_id
        # TODO: Chance of a bug: As per below logic, we are extending http methods for existing APIs
        # However, in case a http method for existing endpoint is deleted/deprecated from code.
        # It may still linger here as per method extension logic
        # Extend http methods if incoming method isn't part of existing list
        if http_method:
            temp: List = api_path_obj.http_method.split(",")
            if temp and http_method not in temp:
                temp.append(http_method)
                temp.sort()
                methoD = ",".join(temp)
                api_path_obj.http_method = methoD
                session.commit()
            else:
                api_path_obj.http_method = http_method
                session.commit()


def get_api_inventory(user_id):
    """
    Get discovered APIs given user id
    """
    session: Session = get_session()
    inventory = (
        session.query(ApiInventory)
        .filter_by(user_id=user_id)
        .order_by(desc(ApiInventory.time_updated))
    )
    return inventory


def update_spec(spec_id, collection_name=None):
    session: Session = get_session()
    spec: ApiSpec = get_spec(spec_id)
    spec.collection_name = collection_name
    session.commit()


def get_spec(spec_id):
    """
    Retrieve spec object given spec_id & api path
    """
    session: Session = get_session()
    spec = session.query(ApiSpec).filter_by(spec_id=spec_id).first()
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
    spec = ApiSpec(spec_id, user_id, collection_name, file_name, data_dir)
    session.add(spec)
    session.commit()
