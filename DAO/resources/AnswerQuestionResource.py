from flask_restful import Resource

from flask import jsonify
from sqlalchemy.orm import sessionmaker



# aq_get_args = reqparse.RequestParser()
# aq_get_args.add_argument("id", type=int, required=True)
#
# aq_delete_args = reqparse.RequestParser()
# aq_delete_args.add_argument("id", type=int, required=True)
#
# aq_post_args = reqparse.RequestParser()
# aq_post_args.add_argument("attempt_number", type=int, required=True)
# aq_post_args.add_argument("userId", type=int, required=True)
# aq_post_args.add_argument("passing_time", type=datetime, required=True)
#
# aq_put_args = reqparse.RequestParser()
# aq_put_args.add_argument("id", type=int)
# aq_put_args.add_argument("attempt_number", type=int)
# aq_put_args.add_argument("userId", type=int)
from DAO.Models.database_setup import db_session
from DAO.Models.models import AnswerQuestionModel


class ChoiceList(Resource):

    def get(self):
        questions = db_session.query(AnswerQuestionModel).all()
        return jsonify(list(x.dictionarize() for x in questions))

    # def post(self):
    #
    #     question_text = request.args.get('question_text')
    #
    #     question = QuestModel(question_text=question_text)
    #     session.add(question)
    #     session.commit()
    #     session.close()
    #     return "Question added OK"


class Choice(Resource):

    def get(self, id):
        question = db_session.query(AnswerQuestionModel).filter_by(id=id).one()
        return jsonify(question.dictionarize())



    # def put(self):
    #
    #     id = request.args.get('id')
    #     question_text = request.args.get('question_text')
    #
    #     editedQuestion = session.query(QuestModel).filter_by(id=id).one()
    #     editedQuestion.question_text = question_text
    #     session.add(editedQuestion)
    #     session.commit()
    #     session.close()
    #     return "Question updated OK"
    #
    #
    # def delete(self, id):
    #     deletedChoice = session.query(AnswerQuestionModel).filter_by(id=id).one()
    #     session.delete(deletedChoice)
    #     session.commit()
    #     session.close()
    #     return "Choice deleted OK"

