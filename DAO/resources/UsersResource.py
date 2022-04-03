from flask import jsonify, request
from flask_restful import Resource, reqparse
from sqlalchemy.orm import sessionmaker
import time
from DAO.Models.Role_entity import RoleModel
from DAO.Models.User_entity import UserModel
from DAO.database_setup import engine
from firestore_connection import db
from firebase_admin import auth

DBSession = sessionmaker(bind=engine)
session = DBSession()


user_get_args = reqparse.RequestParser()
user_get_args.add_argument("id", type=int, required=True)

user_delete_args = reqparse.RequestParser()
user_delete_args.add_argument("id", type=int, required=True)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("login", type=str, required=True)
user_post_args.add_argument("email", type=str, required=True)
user_post_args.add_argument("gender", type=str, required=True)
user_post_args.add_argument("age", type=int, required=True)
user_post_args.add_argument("role_id", type=int, required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("login", type=str)
user_put_args.add_argument("current_email", type=str)
user_put_args.add_argument("gender", type=str)
user_put_args.add_argument("age", type=str)
user_put_args.add_argument("role_id", type=str)


class UsersList(Resource):

    def get(self):
        users = session.query(UserModel).all()
        session.close()
        return jsonify(list(x.dictionarize() for x in users))


    def post(self):
        args = user_post_args.parse_args()

        login = args['login']
        email = args['email']
        role_id = args['role_id']
        gender = args["gender"]
        age = args["age"]

        user = UserModel(login=login,
                         email=email.lower(),
                         gender=gender,
                         age=age,
                         role_id=role_id)
        session.add(user)
        session.commit()
        session.close()
        return {"status": "OK"}



class User(Resource):

    def get(self, email):
        user = session.query(UserModel).filter_by(email=email).first()
        session.close()
        if user is None:
            return {"Status": "No user was found"}
        else:
            return jsonify(user.dictionarize())


    def put(self, email):
        args = user_put_args.parse_args()
        new_login = args['login']
        new_email = email
        new_gender = args["gender"]
        new_age = args["age"]
        print(email,new_login,args["current_email"],new_gender,new_age)
        editedUser = session.query(UserModel).filter_by(email=args["current_email"]).one()
        editedUser.id = editedUser.id
        editedUser.login = new_login
        editedUser.email = new_email.lower()
        editedUser.gender = new_gender
        editedUser.age = new_age
        editedUser.role_id = editedUser.role_id
        session.add(editedUser)
        session.commit()
        session.close()

        serializerObject = {
            "email": new_email,
            "login": new_login,
            "gender": new_gender,
            "age": new_age,
            "role_id": editedUser.role_id
        }

        return serializerObject

    def delete(self, email):
        try:
            auth.get_user_by_email(email)
        except:
            user = session.query(UserModel).filter_by(email=email).first()
            session.close()
            if user is None:
                return {"Status": "User wasn't created"}
            else:
                deletedUser = session.query(UserModel).filter_by(email=email).one()
                session.delete(deletedUser)
                session.commit()
                session.close()
                return {"Status": "User was deleted"}




