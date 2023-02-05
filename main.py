from flask import Flask, request, render_template
import db_processing

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index_page():
    return 'index page'


@app.route("/vacancy/", methods=['GET', 'POST', 'PUT'])
def vacancy():
    if request.method == 'POST':
        vacancy_data = {
            "user_id": 1,
            "position_name": request.form.get('position_name'),
            "company": request.form.get('company'),
            "description": request.form.get('description'),
            "contact_ids": request.form.get('contact_ids'),
            "comment": request.form.get('comment')
        }
        db_processing.insert_info("vacancy", vacancy_data)
    elif request.method == 'PUT':
        pass
    result = db_processing.select_info("SELECT * FROM vacancy;")
    return render_template('vacancy_add.html', vacancies=result)


@app.route("/vacancy/<vacancy_id>/", methods=['GET', 'PUT'])
def show_vacancy_content(vacancy_id):
    result = db_processing.select_info("SELECT * FROM vacancy where id='%s';" % vacancy_id)
    return result


@app.route("/vacancy/<vacancy_id>/events/", methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    if request.method == 'POST':
        event_data = {
            "vacancy_id": vacancy_id,
            "description": request.form.get('description'),
            "title": request.form.get('title'),
            "due_to_date": request.form.get('due_to_date'),
        }
        db_processing.insert_info("event", event_data)
    result = db_processing.select_info("SELECT * FROM event where vacancy_id='%s'" % vacancy_id)
    return render_template('event_add.html', vacancy_id=vacancy_id, events=result)


@app.route("/vacancy/<vacancy_id>/events/<event_id>/", methods=['GET', 'PUT'])
def show_event_content(vacancy_id, event_id):
    result = db_processing.select_info("SELECT * FROM event where vacancy_id='%s' and id='%s';" % (vacancy_id, event_id))
    return result


@app.route("/vacancy/<vacancy_id>/history/", methods=['GET'])
def vacancy_history():
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
