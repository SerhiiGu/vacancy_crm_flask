from flask import Flask
from flask import request
from lists_of_dicts import *

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index_page():
    return 'index page'


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancy():
    return vacancy_data


@app.route("/vacancy/<vacancy_id>/", methods=['GET', 'PUT'])
def show_vacancy_content(vacancy_id):
    vacancy_id = int(vacancy_id)
    for vacancy in vacancy_data:
        if vacancy['id'] == vacancy_id:
            return vacancy
    return f'No vacancies with vacancy_id {vacancy_id} found!'


@app.route("/vacancy/<vacancy_id>/events/", methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    event_list = []
    vacancy_id = int(vacancy_id)
    for event in event_data:
        if event['vacancy_id'] == vacancy_id:
            event_list.append(event)
    return event_list


@app.route("/vacancy/<vacancy_id>/events/<event_id>/", methods=['GET', 'PUT'])
def show_event_content(vacancy_id, event_id):
    vacancy_id = int(vacancy_id)
    event_id = int(event_id)
    for event in event_data:
        if event['vacancy_id'] == vacancy_id and event['id'] == event_id:
            return event
    return f'No events with vacancy_id {vacancy_id} and event_id {event_id} found!'


@app.route("/vacancy/<vacancy_id>/history/", methods=['GET'])
def vacancy_history(vacancy_id):
    return 'vacancy history'


@app.route("/user/", methods=['GET', 'POST'])
def user_main_page():
    return 'user main page, dashboard'


@app.route("/user/calendar/", methods=['GET'])
def user_calendar():
    return 'user calendar'


@app.route("/user/mail/", methods=['GET'])
def user_mail():
    return 'user mail'


@app.route("/user/settings/", methods=['GET', 'PUT'])
def user_settings():
    return 'user settings'


@app.route("/user/documents/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_documents():
    return 'user documents'


@app.route("/user/templates/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_templates():
    return 'user templates'


if __name__ == '__main__':
    app.run(debug=True)
