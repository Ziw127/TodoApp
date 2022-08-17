from flask import Flask, render_template, request, session
from flask import redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import sys
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)

# Auth0 Config
app.secret_key = '!secret'
app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://newuser:postgres@localhost:5432/list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# from backend.src.models import *
from models import *


# db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, complete=False, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['complete'] = todo.complete
        body['description'] = todo.description
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-complete', methods=['POST'])
def update_todo(todo_id):
    error = False
    try:
        complete = request.get_json()['complete']
        todo = Todo.query.get(todo_id)
        print('Todo: ', todo)
        todo.complete = complete
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('get_list_todos', list_id=1))

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    try:
        #Todo.query.filter_by(id=todo_id).delete()
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    error = False

    try:
        completed = request.get_json()['completed']

        todo = Todo.query.get(todo_id)
        todo.completed = completed

        db.session.commit()
    except:
        db.session.rollback()

        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return '', 200

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id)
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()

    return render_template('index.html', todos=todos, lists=lists, active_list=active_list)

@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)

@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)
        
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})

        
@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    error = False

    try:
        list = TodoList.query.get(list_id)

        for todo in list.todos:
            todo.completed = True

        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return '', 200

#Create error handlers for all expected errors including 404 and 422.
@app.errorhandler(404)
def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
    }), 400

@app.errorhandler(422)
def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
    }), 422


if __name__ == '__main__':
    app.run(debug=True)
