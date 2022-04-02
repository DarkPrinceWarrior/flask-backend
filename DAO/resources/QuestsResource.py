from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_restful.representations import json
from sqlalchemy.orm import sessionmaker

from DAO.Models.Question_entity import QuestionModel
from DAO.Models.Role_entity import RoleModel
from DAO.Models.User_entity import UserModel
from DAO.database_setup import engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

quest_post_args = reqparse.RequestParser()
quest_post_args.add_argument("question_text", type=str, required=True)
quest_post_args.add_argument("question_type", type=str, required=True)
quest_post_args.add_argument("statement_type", type=str, required=True)

quest_put_args = reqparse.RequestParser()
quest_put_args.add_argument("question_text", type=str)
quest_put_args.add_argument("question_type", type=str)
quest_put_args.add_argument("statement_type", type=str)


class QuestsList(Resource):

    def get(self):
        questions = session.query(QuestionModel).all()
        session.close()
        return jsonify(list(x.dictionarize() for x in questions))


class Quest(Resource):

    def get(self, id):
        question = session.query(QuestionModel).filter_by(id=id).one()
        session.close()
        return jsonify(question.dictionarize())

    def post(self, id):
        args = quest_post_args.parse_args()
        question = QuestionModel(question_text=args["question_text"],
                                 question_type=args["question_type"],
                                 statement_type=args["statement_type"])
        session.add(question)
        session.commit()
        session.close()
        return "Question added OK"

    def put(self, id):
        args = quest_put_args.parse_args()
        editedQuestion = session.query(QuestionModel).filter_by(id=id).one()
        editedQuestion.question_text = args["question_text"]
        editedQuestion.question_type = args["question_type"]
        editedQuestion.statement_type = args["statement_type"]
        session.add(editedQuestion)
        session.commit()
        session.close()
        return "Question updated OK"

    def delete(self, id):
        id = request.args.get('id')
        deletedQuestion = session.query(QuestionModel).filter_by(id=id).one()
        session.delete(deletedQuestion)
        session.commit()
        session.close()
        return "Question deleted OK"
