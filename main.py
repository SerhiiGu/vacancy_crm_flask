from flask import Flask, request, render_template, redirect
import al_db

from models import Vacancy, Event


app = Flask(__name__)


@app.route("/", methods=['GET'])
def main_proc():
    al_db.init_db()
    return redirect('/vacancy/')


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancy():
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        contact_ids = request.form.get('contact_ids')
        comment = request.form.get('comment')
        current_vacancy = Vacancy(position_name, company, description, contact_ids, comment, status=1, user_id=1)
        al_db.db_session.add(current_vacancy)
        al_db.db_session.commit()
    result = al_db.db_session.query(Vacancy.id, Vacancy.position_name,
                                    Vacancy.company, Vacancy.description, Vacancy.comment).all()
    return render_template('vacancy_add.html', vacancies=result)


@app.route("/vacancy/<int:vacancy_id>/", methods=['GET', 'POST'])
def show_vacancy_content(vacancy_id):
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        contact_ids = request.form.get('contact_ids')
        comment = request.form.get('comment')
        al_db.db_session.query(Vacancy).filter(Vacancy.id == vacancy_id).update({
            Vacancy.position_name: position_name, Vacancy.company: company, Vacancy.description: description,
            Vacancy.contact_ids: contact_ids, Vacancy.comment: comment})
        al_db.db_session.commit()
    vacancy_desc = al_db.db_session.query(Vacancy.id, Vacancy.position_name, Vacancy.company, Vacancy.description,
                    Vacancy.comment, Vacancy.contact_ids).where(Vacancy.id == vacancy_id).first()
    events = al_db.db_session.query(Event.id, Event.title, Event.description,
                                    Event.due_to_date).where(Event.vacancy_id == vacancy_id)
    return render_template('vacancy_update.html', vacancy_id=vacancy_id, vacancy_desc=vacancy_desc, events=events)


@app.route("/vacancy/<int:vacancy_id>/events/", methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    if request.method == 'POST':
        description = request.form.get('description')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')
        add_event = Event(vacancy_id, title, description, due_to_date, status=1)
        al_db.db_session.add(add_event)
        al_db.db_session.commit()
    result = al_db.db_session.query(Event.id, Event.title, Event.description,
                                    Event.due_to_date).where(Event.vacancy_id == vacancy_id)
    return render_template('event_add.html', vacancy_id=vacancy_id, events=result)


@app.route("/vacancy/<int:vacancy_id>/events/<int:event_id>/", methods=['GET', 'POST'])
def show_event_content(vacancy_id, event_id):
    if request.method == 'POST':
        description = request.form.get('description')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')
        al_db.db_session.query(Event).filter(Event.id == event_id, Event.vacancy_id == vacancy_id).\
            update({Event.title: title, Event.description: description, Event.due_to_date: due_to_date})
        al_db.db_session.commit()
    event = al_db.db_session.query(Event.id, Event.title, Event.description, Event.due_to_date).\
        where(Event.id == event_id, Event.vacancy_id == vacancy_id).first()
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
    app.run(host='0.0.0.0', port=5005, debug=True)
