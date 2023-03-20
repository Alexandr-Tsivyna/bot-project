from tables import *
from sqlalchemy.orm import Session
from database import engine


# read user in database
def is_user_in_db(user_id):
    session = Session(bind=engine)
    exists = session.query(Client).filter_by(telegram_id=str(user_id)).first() is not None
    return exists


# create user in database
def create_user_in_db(user_id):
    session = Session(bind=engine)
    new_client = Client(telegram_id=user_id)
    session.add(new_client)
    session.commit()


# read diet in database
def show_diets():
    session = Session(bind=engine)
    all_diets = session.query(Diet.description).all()
    descriptions = '\n '.join([d[0] for d in all_diets])
    return descriptions


def show_diets_for_buttons():
    session = Session(bind=engine)
    diets = session.query(Diet).all()
    buttons = []

    for diet in diets:
        buttons.append({"text": diet.description, "callback_data": str(diet.id)})
    return buttons


def edit_buttons():
    session = Session(bind=engine)
    diets = session.query(Diet).all()
    deleted_buttons = []

    for diet in diets:
        deleted_buttons.append({"text": "", "callback_data": str(diet.id)})
    return deleted_buttons


# read user details in database
def is_user_details_in_db(user_id):
    session = Session(bind=engine)
    exists = session.query(ClientsDetails).filter_by(user_id=str(user_id)).first() is not None
    return exists


# create user details in database
def create_user_details_in_db(user_id, diet):
    session = Session(bind=engine)
    user_details = ClientsDetails(user_id=user_id, diet=diet)
    session.add(user_details)
    session.commit()


def update_diet_in_user_details(user_id, diet):
    session = Session(bind=engine)
    update_user_details = session.query(ClientsDetails).filter_by(user_id=str(user_id)).first()
    new_diet = diet
    update_user_details.diet = new_diet
    session.commit()


def delete_user(user_id):
    session = Session(bind=engine)
    user_details = session.query(ClientsDetails).filter_by(user_id=str(user_id)).first()
    user = session.query(Client).filter_by(telegram_id=str(user_id)).first()
    session.delete(user_details)
    session.delete(user)
    session.commit()


def show_products_in_message(user_id):
    session = Session(bind=engine)
    user_diet_id = session.query(ClientsDetails.diet).filter_by(user_id=str(user_id)).scalar()
    user_diet = session.query(Diet).filter_by(id=user_diet_id).one()
    product_ids = [p[0] for p in session.query(DietDetails.product).filter_by(diet=user_diet.id).all()]
    products_list_for_message = session.query(Food.name, Food.kal).filter(Food.id.in_(product_ids)).all()
    message = '\n '.join([f"{p[0]} ({p[1]} )" for p in products_list_for_message])
    return message
