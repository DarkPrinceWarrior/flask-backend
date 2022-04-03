from flask import jsonify
from flask_restful import Resource, reqparse

from DAO.Models.database_setup import db_session
from DAO.Models.models import UsersAttemptsModel

attempt_get_args = reqparse.RequestParser()
attempt_get_args.add_argument("id", type=int, required=True)

attempt_delete_args = reqparse.RequestParser()
attempt_delete_args.add_argument("id", type=int, required=True)

attempt_post_args = reqparse.RequestParser()
attempt_post_args.add_argument("attempt_number", type=int, required=True)
attempt_post_args.add_argument("userId", type=int, required=True)
attempt_post_args.add_argument("passing_time", type=str, required=True)

attempt_put_args = reqparse.RequestParser()
attempt_put_args.add_argument("id", type=int)
attempt_put_args.add_argument("attempt_number", type=int)
attempt_put_args.add_argument("userId", type=int)
attempt_put_args.add_argument("passing_time", type=str)


class AttemptList(Resource):

    def get(self):

        numberOfElements = db_session.query(UsersAttemptsModel).count()

        if numberOfElements == 0:
            return {
                "id": 0,
                "attempt_number": 0,
                "userId": 0,
                "passing_time": "0:0"
            }
        else:
            attempt = db_session.query(UsersAttemptsModel).all()
            return jsonify(list(x.dictionarize() for x in attempt))



    def post(self):
        args = attempt_post_args.parse_args()

        attempt_number = args['attempt_number']
        userId = args['userId']
        passing_time = args["passing_time"]
        user_attempt = UsersAttemptsModel(attempt_number=attempt_number,
                                          userId=userId,
                                          passing_time=passing_time)
        db_session.add(user_attempt)
        db_session.commit()
        return {"Status": "OK"}


class Attempt(Resource):

    def get(self, user_id):
        index = self.get_attemptId(user_id)
        user_attempts = db_session.query(UsersAttemptsModel).filter_by(id=index).one()
        return jsonify(list(x.dictionarize() for x in user_attempts))

    # Обновление записи
    def patch(self, user_id):
        args = attempt_put_args.parse_args()
        Id = self.get_attemptId(user_id)
        editedAttempt = db_session.query(UsersAttemptsModel).filter_by(id=Id).one()
        editedAttempt.attempt_number = editedAttempt.attempt_number
        editedAttempt.userId = editedAttempt.userId
        editedAttempt.passing_time = args["passing_time"]
        db_session.add(editedAttempt)
        db_session.commit()
        return {"Status": "Attempt was updated"}

    def delete(self, user_id):
        index = self.get_attemptId(user_id)
        deletedAttempt = db_session.query(UsersAttemptsModel).filter_by(id=index).one()
        db_session.delete(deletedAttempt)
        db_session.commit()
        return {"Status": "Attempt was deleted"}

    # Ищем id попытки по id юзера и его последней попытке
    def get_attemptId(self, user_id):

        user_attempts = db_session.query(UsersAttemptsModel).count()
        if user_attempts != 1:
            user_attempts = db_session.query(UsersAttemptsModel).filter_by(userId=user_id).all()
            attempt_list = list(x.dictionarize() for x in user_attempts)
            max_attempt = 0
            index = 0
            for i in attempt_list:
                if i["attempt_number"] > max_attempt:
                    max_attempt = i["attempt_number"]
                    index = i["id"]
            return index
        else:
            user_attempts = db_session.query(UsersAttemptsModel).filter_by(userId=user_id).one()
            return user_attempts.id
