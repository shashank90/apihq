from sqlalchemy.orm import Session

from db.database import get_session
from db.model.api_validate import ApiValidate, ValidateStatusEnum
from db.model.api_run import ApiRun, RunStatusEnum
from db.model.api_spec import ApiSpec
from db.model.company import Company
from db.model.user import User
from log.factory import Logger

logger = Logger(__name__)


def insert_customer():
    session: Session = get_session()
    customer = Company("usefulsecurity")
    session.add(customer)
    session.commit()
    print(f"Added customer: {customer.id}!")


def insert_user():
    session: Session = get_session()
    user1 = User("arjun@usefulsecurity.com", "password123", 1)
    user2 = User("nanna@usefulsecurity.com", "password456", 1)
    session.add(user1)
    session.add(user2)
    session.commit()
    # print(user1.customer)


def insert_spec():
    session: Session = get_session()
    user_id = 2
    spec_id = "spec1234566777"
    collection_name = "import_api"
    data_dir = "/abc/dir"
    spec = ApiSpec(spec_id, user_id, collection_name, data_dir)
    # session.add(spec)
    # session.commit()

    # print(f"APP ID: {app.id} ORG : {app.organisation.name}")


def insert_audit():
    session: Session = get_session()
    spec_id = "spec1234566777"
    user_id = 2
    score = 25
    status = ValidateStatusEnum.INITIATIED
    audit = ApiValidate(spec_id, user_id, score, status)
    session.add(audit)
    session.commit()


def insert_scan():
    session: Session = get_session()
    spec_id = "spec1234566777"
    user_id = 2
    score = 25
    status = RunStatusEnum.INITIATIED
    audit = ApiRun(spec_id, user_id, score, status)
    session.add(audit)
    session.commit()


def get_user_customer(username):
    session: Session = get_session()
    user: User = session.query(User).filter(User.email == username).first()
    print(f"FOUND MY FIRST User {user} ")


def get_api_spec(collection_name):
    session: Session = get_session()
    spec: ApiSpec = (
        session.query(ApiSpec)
        .filter(ApiSpec.collection_name == collection_name)
        .first()
    )
    print(f"FOUND MY FIRST API Spec {spec.scan_result.status} ")


def test():
    # insert_customer()
    insert_user()
    # get_user_customer("arjun@usefulsecurity.com")
    # insert_audit()
    # get_api_spec("import_api")


# insert_org()
# insert_user()
# get_user("nanna@usefulsecurity.com")
# insert_app()
# insert_txn()
# insert_zap_detail()
# session: Session = get_session()
# session.commit()
