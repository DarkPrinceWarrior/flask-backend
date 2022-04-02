from flask import jsonify
from flask_restful import reqparse, Resource
from sqlalchemy.orm import sessionmaker

from DAO.Models.UsersAnswers_entity import UsersAnswersModel
from DAO.database_setup import engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

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
        user_answer = session.query(UsersAnswersModel).all()
        session.close()
        return jsonify(list(x.dictionarize() for x in user_answer))
        # return jsonify({'Users': list(x.dictionarize() for x in users)})

    def post(self):
        args = user_answer_post_args.parse_args()

        choiceId = args['choiceId']
        attemptId = args['attemptId']

        print(choiceId,attemptId)

        user_answer = UsersAnswersModel(choiceId=choiceId,
                                        attemptId=attemptId)
        session.add(user_answer)
        session.commit()
        session.close()
        return {"status": "OK"}


class UserAnswer(Resource):

    def get(self, id):
        user_answer = session.query(UsersAnswersModel).filter_by(id=id).one()
        session.close()
        return jsonify(user_answer.dictionarize())

    def patch(self, new_choice):
        print("Patch"+str(new_choice))
        args = user_answer_put_args.parse_args()
        editedAnswer = session.query(UsersAnswersModel).filter_by(attemptId=args["attemptId"],
                                                                  choiceId=args["choiceId"]).one()
        editedAnswer.choiceId = new_choice
        session.add(editedAnswer)
        session.commit()
        session.close()
        return {"Status": "User answer was updated"}

    def delete(self, id):
        deletedAnswer = session.query(UsersAnswersModel).filter_by(id=id).one()
        session.delete(deletedAnswer)
        session.commit()
        session.close()
        return "User answer deleted OK"
