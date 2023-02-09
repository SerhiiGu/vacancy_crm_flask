from flask import Flask, request, render_template
import db_processing

app = Flask(__name__)


@app.route("/", methods=['GET'])
@app.route("/vacancy/", methods=['GET', 'POST'])
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
        with db_processing.DB() as db:
            db.insert("vacancy", vacancy_data)
    with db_processing.DB() as db:
        result = db.query("SELECT * FROM vacancy;")
    return render_template('vacancy_add.html', vacancies=result)


@app.route("/vacancy/<vacancy_id>/", methods=['GET', 'POST'])
def show_vacancy_content(vacancy_id):
    if request.method == 'POST':
        qry = "UPDATE vacancy SET "
        x = 0
        for value in request.form:
            if request.form.get(value) != '':
                if x == 1:
                    qry += ", "
                qry += f"{value}='{request.form.get(value)}'"
                x = 1
        qry += f" WHERE id='{vacancy_id}';"
        with db_processing.DB() as db:
            db.update(qry)
    with db_processing.DB() as db:
        vacancy_desc = db.query("SELECT * FROM vacancy where id='%s';" % vacancy_id)
        events = db.query("SELECT * FROM event where vacancy_id='%s'" % vacancy_id)
    return render_template('vacancy_update.html', vacancy_id=vacancy_id, vacancy_desc=vacancy_desc, events=events)


@app.route("/vacancy/<vacancy_id>/events/", methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    if request.method == 'POST':
        event_data = {
            "vacancy_id": vacancy_id,
            "description": request.form.get('description'),
            "title": request.form.get('title'),
            "due_to_date": request.form.get('due_to_date'),
        }
        with db_processing.DB() as db:
            db.insert("event", event_data)
    with db_processing.DB() as db:
        result = db.query("SELECT * FROM event where vacancy_id='%s'" % vacancy_id)
    return render_template('event_add.html', vacancy_id=vacancy_id, events=result)


@app.route("/vacancy/<vacancy_id>/events/<event_id>/", methods=['GET', 'POST'])
def show_event_content(vacancy_id, event_id):
    if request.method == 'POST':
        qry = "UPDATE event SET "
        x = 0
        for value in request.form:
            if request.form.get(value) != '':
                if x == 1:
                    qry += ", "
                qry += f"{value}='{request.form.get(value)}'"
                x = 1
        qry += f" WHERE id='{event_id}';"
        with db_processing.DB() as db:
            db.update(qry)
    with db_processing.DB() as db:
        event = db.query("SELECT * FROM event where vacancy_id='%s' and id='%s';" % (vacancy_id, event_id))
    return render_template('event_update.html', vacancy_id=vacancy_id, event_id=event_id, event=event)


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
