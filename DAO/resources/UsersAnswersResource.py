from flask import jsonify
from flask_restful import reqparse, Resource

from DAO.Models.database_setup import db_session
from DAO.Models.models import UsersAnswersModel

user_answer_get_args = reqparse.RequestParser()
user_answer_get_args.add_argument("id", type=int, required=True)

user_answer_delete_args = reqparse.RequestParser()
user_answer_delete_args.add_argument("id", type=int, required=True)

user_answer_post_args = reqparse.RequestParser()
user_answer_post_args.add_argument("choiceId", type=int, required=True)
user_answer_post_args.add_argument("attemptId", type=int, required=True)

user_answer_put_args = reqparse.RequestParser()
user_answer_put_args.add_argument("id", type=int)
user_answer_put_args.add_argument("choiceId", type=int)
user_answer_put_args.add_argument("attemptId", type=int)


class UserAnswerList(Resource):

    def get(self):
        user_answer = db_session.query(UsersAnswersModel).all()
        return jsonify(list(x.dictionarize() for x in user_answer))
        # return jsonify({'Users': list(x.dictionarize() for x in users)})

    def post(self):
        args = user_answer_post_args.parse_args()

        choiceId = args['choiceId']
        attemptId = args['attemptId']

        print(choiceId,attemptId)

        user_answer = UsersAnswersModel(choiceId=choiceId,
                                        attemptId=attemptId)
        db_session.add(user_answer)
        db_session.commit()
        return {"status": "OK"}


class UserAnswer(Resource):

    def get(self, id):
        user_answer = db_session.query(UsersAnswersModel).filter_by(id=id).one()
        return jsonify(user_answer.dictionarize())

    def patch(self, new_choice):
        print("Patch"+str(new_choice))
        args = user_answer_put_args.parse_args()
        editedAnswer = db_session.query(UsersAnswersModel).filter_by(attemptId=args["attemptId"],
                                                                  choiceId=args["choiceId"]).one()
        editedAnswer.choiceId = new_choice
        db_session.add(editedAnswer)
        db_session.commit()
        return {"Status": "User answer was updated"}

    def delete(self, id):
        deletedAnswer = db_session.query(UsersAnswersModel).filter_by(id=id).one()
        db_session.delete(deletedAnswer)
        db_session.commit()
        return "User answer deleted OK"
