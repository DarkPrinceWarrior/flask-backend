from firebase_admin import auth
from flask import Flask
from flask_restful import Api

import DAO.database_setup
from DAO.resources.AnswrsResource import AnswersList, AnswersList, Answer
from DAO.resources.AttemptResource import AttemptList, Attempt
from DAO.resources.QuestsResource import QuestsList, Quest
from DAO.resources.RolesResource import RolesList
from DAO.resources.UserResultsResource import ResultsList, Result
from DAO.resources.UsersAnswersResource import UserAnswerList, UserAnswer
from DAO.resources.UsersResource import UsersList, User
from DAO.resources.AnswerQuestionResource import ChoiceList, Choice

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

# return list of objects
api.add_resource(RolesList, '/Roles')
api.add_resource(UsersList, '/Users')
api.add_resource(QuestsList, '/Quests')
api.add_resource(AnswersList, '/Answers')
api.add_resource(ChoiceList, '/Choices')
api.add_resource(UserAnswerList, '/Users/Answers')
api.add_resource(ResultsList, '/Users/Results')
api.add_resource(AttemptList, '/Users/Attempts')


# return single object
api.add_resource(User, '/User/<string:email>')
api.add_resource(Quest, '/Quest/<int:id>')
api.add_resource(Answer, '/Answer/<int:id>')
api.add_resource(Choice, '/Choice/<int:id>')
api.add_resource(Attempt, '/User/Attempt/<int:user_id>')
api.add_resource(Result, '/User/Result/<int:id>')
api.add_resource(UserAnswer, '/User/Answer/<int:new_choice>')


if __name__ == '__main__':
    DAO.database_setup.create_db()
    app.run(host="0.0.0.0", debug=True)

