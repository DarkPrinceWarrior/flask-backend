from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.orm import relationship, sessionmaker

from DAO.Models.Role_entity import RoleModel
from DAO.database_setup import Base, engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class RolesList(Resource):

    def get(self):
        role = session.query(RoleModel).all()
        session.close()
        return jsonify(list(x.dictionarize() for x in role))




    def post(self):
        name = request.args.get('name')

        role = RoleModel(name=name)
        session.add(role)
        session.commit()
        session.close()
        return "Role added OK"

    def put(self):

        id = request.args.get('id')
        new_name = request.args.get('name')
        editedRole = session.query(RoleModel).filter_by(id=id).one()
        editedRole.name = new_name
        session.add(editedRole)
        session.commit()
        session.close()
        return "Role updated OK"

    def delete(self):
        id = request.args.get('id')
        deletedRole = session.query(RoleModel).filter_by(id=id).one()
        session.delete(deletedRole)
        session.commit()
        session.close()
        return "Role deleted OK"


