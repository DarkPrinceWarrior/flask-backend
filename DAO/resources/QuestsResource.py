from flask import jsonify, request
from flask_restful import Resource, reqparse

from DAO.Models.database_setup import db_session
from DAO.Models.models import QuestionModel

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
        questions = db_session.query(QuestionModel).all()
        return jsonify(list(x.dictionarize() for x in questions))


class Quest(Resource):

    def get(self, id):
        question = db_session.query(QuestionModel).filter_by(id=id).one()
        return jsonify(question.dictionarize())

    def post(self, id):
        args = quest_post_args.parse_args()
        question = QuestionModel(question_text=args["question_text"],
                                 question_type=args["question_type"],
                                 statement_type=args["statement_type"])
        db_session.add(question)
        db_session.commit()
        return "Question added OK"

    def put(self, id):
        args = quest_put_args.parse_args()
        editedQuestion = db_session.query(QuestionModel).filter_by(id=id).one()
        editedQuestion.question_text = args["question_text"]
        editedQuestion.question_type = args["question_type"]
        editedQuestion.statement_type = args["statement_type"]
        db_session.add(editedQuestion)
        db_session.commit()
        return "Question updated OK"

    def delete(self, id):
        id = request.args.get('id')
        deletedQuestion = db_session.query(QuestionModel).filter_by(id=id).one()
        db_session.delete(deletedQuestion)
        db_session.commit()
        return "Question deleted OK"
