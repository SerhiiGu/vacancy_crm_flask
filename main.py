from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    return 'index page'


@app.route('/vacancy/', methods=['GET', 'POST'])
def vacancy():
    return 'all vacancies'


@app.route('/vacancy/<id>/', methods=['GET', 'PUT'])
def vacancy_content():
    return 'vacancy with id'


@app.route('/vacancy/<id>/events/', methods=['GET', 'POST'])
def vacancy_events():
    return 'vacancy events'


@app.route('/vacancy/<id>/events/<event_id>/', methods=['GET', 'PUT'])
def show_event_content():
    return 'inside event with id'


@app.route('/vacancy/history/', methods=['GET'])
def vacancy_history():
    return 'vacancy history'


@app.route('/user/', methods=['GET'])
def user_main_page():
    return 'user main page, dashboard'


@app.route('/user/calendar', methods=['GET'])
def user_calendar():
    return 'user calendar'


@app.route('/user/mail/', methods=['GET'])
def user_mail():
    return 'user mail'


@app.route('/user/settings/', methods=['GET', 'PUT'])
def user_settings():
    return 'user settings'


@app.route('/user/documents/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_documents():
    return 'user documents'


@app.route('/user/templates/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_templates():
    return 'user templates'


if __name__ == '__main__':
    app.run()
