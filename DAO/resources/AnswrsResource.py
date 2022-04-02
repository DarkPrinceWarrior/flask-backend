from flask import jsonify, request
from flask_restful import Resource, reqparse, fields, marshal_with
from sqlalchemy.orm import sessionmaker

from DAO.Models.Answer_entity import AnswerModel

from DAO.database_setup import engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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
        answers = session.query(AnswerModel).all()
        session.close()
        return jsonify(list(x.dictionarize() for x in answers))


class Answer(Resource):

    def get(self, id):
        answer = session.query(AnswerModel).filter_by(id=id).one()
        session.close()
        return jsonify(answer.dictionarize())


    def post(self, id):
        args = answer_post_args.parse_args()
        answer = AnswerModel(answer_text=args["answer_text"])
        session.add(answer)
        session.commit()
        session.close()
        return "Answer added OK"


    def put(self, id):
        args = answer_put_args.parse_args()
        editedAnswer = session.query(AnswerModel).filter_by(id=id).one()
        editedAnswer.answer_text = args["answer_text"]
        session.add(editedAnswer)
        session.commit()
        session.close()
        return "Answer updated OK"

    def delete(self, id):
        deletedAnswer = session.query(AnswerModel).filter_by(id=id).one()
        session.delete(deletedAnswer)
        session.commit()
        session.close()
        return "Answer deleted OK"
