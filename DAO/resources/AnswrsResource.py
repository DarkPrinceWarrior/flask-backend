from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.orm import sessionmaker

from DAO.Models.database_setup import db_session
from DAO.Models.models import AnswerModel

answer_get_args = reqparse.RequestParser()
answer_get_args.add_argument("id", type=int, required=True)


answer_delete_args = reqparse.RequestParser()
answer_delete_args.add_argument("id", type=int, required=True)

answer_post_args = reqparse.RequestParser()
answer_post_args.add_argument("answer_text", type=str, required=True)


answer_put_args = reqparse.RequestParser()
answer_put_args.add_argument("answer_text", type=str)


class AnswersList(Resource):
    def get(self):
        answers = db_session.query(AnswerModel).all()
        return jsonify(list(x.dictionarize() for x in answers))


class Answer(Resource):

    def get(self, id):
        answer = db_session.query(AnswerModel).filter_by(id=id).one()
        return jsonify(answer.dictionarize())


    def post(self, id):
        args = answer_post_args.parse_args()
        answer = AnswerModel(answer_text=args["answer_text"])
        db_session.add(answer)
        db_session.commit()
        return "Answer added OK"


    def put(self, id):
        args = answer_put_args.parse_args()
        editedAnswer = db_session.query(AnswerModel).filter_by(id=id).one()
        editedAnswer.answer_text = args["answer_text"]
        db_session.add(editedAnswer)
        db_session.commit()
        return "Answer updated OK"

    def delete(self, id):
        deletedAnswer = db_session.query(AnswerModel).filter_by(id=id).one()
        db_session.delete(deletedAnswer)
        db_session.commit()
        return "Answer deleted OK"
