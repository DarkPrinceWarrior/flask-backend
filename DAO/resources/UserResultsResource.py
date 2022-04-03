from flask import jsonify
from flask_restful import reqparse, Resource

from DAO.Models.database_setup import db_session
from DAO.Models.models import UsersResultsModel

result_get_args = reqparse.RequestParser()
result_get_args.add_argument("id", type=int, required=True)

result_delete_args = reqparse.RequestParser()
result_delete_args.add_argument("id", type=int, required=True)

result_post_args = reqparse.RequestParser()
result_post_args.add_argument("involvement", type=int, required=True)
result_post_args.add_argument("control", type=int, required=True)
result_post_args.add_argument("risk_taking", type=int, required=True)
result_post_args.add_argument("attemptId", type=int, required=True)

result_put_args = reqparse.RequestParser()
result_put_args.add_argument("involvement", type=int)
result_put_args.add_argument("control", type=int)
result_put_args.add_argument("risk_taking", type=int)
result_put_args.add_argument("attemptId", type=int)


class ResultsList(Resource):

    def get(self):
        results = db_session.query(UsersResultsModel).all()
        return jsonify(list(x.dictionarize() for x in results))

    def post(self):
        args = result_post_args.parse_args()
        involvement = args['involvement']
        control = args['control']
        risk_taking = args['risk_taking']
        attemptId = args['attemptId']

        results = UsersResultsModel(involvement=involvement,
                                    control=control,
                                    risk_taking=risk_taking,
                                    attemptId=attemptId)

        db_session.add(results)
        db_session.commit()
        return {"status": "OK"}


class Result(Resource):

    def get(self, id):
        result = db_session.query(UsersResultsModel).filter_by(attemptId=id).one()
        return jsonify(result.dictionarize())

    def put(self, id):
        args = result_put_args.parse_args()
        involvement = args['involvement']
        control = args['control']
        risk_taking = args['risk_taking']
        attemptId = args["attemptId"]

        # new_role_id = request.args.get('role_id')

        editedResult = db_session.query(UsersResultsModel).filter_by(id=id).one()

        editedResult.involvement = involvement
        editedResult.control = control
        editedResult.risk_taking = risk_taking
        editedResult.attemptId = attemptId

        db_session.add(editedResult)
        db_session.commit()
        return "Result updated OK"

    def delete(self, id):
        deletedResult = db_session.query(UsersResultsModel).filter_by(id=id).one()
        db_session.delete(deletedResult)
        db_session.commit()
        return "Result deleted OK"
