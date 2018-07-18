from flask import g, Blueprint
from flask_restful import (Resource, Api, reqparse, inputs,
                           fields, marshal, marshal_with, url_for)

from auth import auth
import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'completed': fields.Boolean,
    'edited': fields.Boolean,
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            # required=True,
            help='No completed field provided',
            location=['form', 'json'],
            type=inputs.boolean
        )
        self.reqparse.add_argument(
            'edited',
            required=True,
            help='No edited field provided',
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    @auth.login_required
    def get(self):
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select().where(models.Todo.user == g.user.id)]
        return {'todos': todos}

    @auth.login_required
    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        # import pdb;pdb.set_trace()
        todo = models.Todo.create(
            completed=args['completed'],
            edited=args['edited'],
            name=args['name'],
            user=g.user.id
        )
        return todo, 201, {'Location': url_for('resources.todos.todos')}


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=True,
            help='No completed field provided',
            location=['form', 'json'],
            type=inputs.boolean
        )
        self.reqparse.add_argument(
            'edited',
            required=True,
            help='No edited field provided',
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    @auth.login_required
    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        # import pdb;pdb.set_trace()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        return (models.Todo.get(models.Todo.id == id), 200,
                {'Location': url_for('resources.todos.todos')})

    @auth.login_required
    def delete(self, id):
        query = models.Todo.delete().where(models.Todo.id == id)
        query.execute()
        return '', 204, {'Location': url_for('resources.todos.todos')}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)
