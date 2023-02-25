import datetime

from flask import Flask, request, render_template, redirect
import al_db
import email_lib
import mongo_lib
from bson.objectid import ObjectId

from models import Vacancy, Event, User, EmailCredentials

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main_proc():
    al_db.init_db()
    mongo_obj = mongo_lib.MongoLib('vacancy_crm', 'contacts')
    mongo_obj.check_create_db()
    return redirect('/vacancy/')


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancy():
    mongo_obj = mongo_lib.MongoLib('vacancy_crm', 'contacts')
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        comment = request.form.get('comment')

        contact_id = mongo_obj.m_insert_one({"name": contact_name, "email": contact_email, "phone": contact_phone})

        current_vacancy = Vacancy(position_name, company, description, str(contact_id), comment, status=1, user_id=1)
        al_db.db_session.add(current_vacancy)
        al_db.db_session.commit()

    result = al_db.db_session.query(Vacancy.id, Vacancy.position_name, Vacancy.company, Vacancy.description,
                                    Vacancy.comment, Vacancy.contact_ids).all()
    contact_result = []
    for item in result:
        contacts = item[5].split(',')
        for one_contact in contacts:
            data = mongo_obj.m_find_one({'_id': ObjectId(one_contact)})
            contact_result.append(data)
    return render_template('vacancy_add.html', vacancies=result, contact_result=contact_result)


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
        al_db.db_session.query(Event).filter(Event.id == event_id, Event.vacancy_id == vacancy_id). \
            update({Event.title: title, Event.description: description, Event.due_to_date: due_to_date})
        al_db.db_session.commit()
    event = al_db.db_session.query(Event.id, Event.title, Event.description, Event.due_to_date). \
        where(Event.id == event_id, Event.vacancy_id == vacancy_id).first()
    return render_template('event_update.html', vacancy_id=vacancy_id, event_id=event_id, event=event)


@app.route("/vacancy/<vacancy_id>/history/", methods=['GET'])
def vacancy_history():
    return 'vacancy history'


@app.route("/user/", methods=['GET', 'POST'])
def user_main_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        login = request.form.get('login')
        password = request.form.get('password')
        add_user = User(name, email, login, password)
        al_db.db_session.add(add_user)
        al_db.db_session.commit()
    result = al_db.db_session.query(User.id, User.name, User.email, User.login, User.password).all()
    return render_template('user_add.html', users=result)


@app.route("/user/calendar/", methods=['GET'])
def user_calendar():
    return 'user calendar'


@app.route("/user/mail/", methods=['GET', 'POST'])
def user_mail():
    user_settings = al_db.db_session.query(EmailCredentials).filter_by(user_id=1).first()
    email_obj = email_lib.EmailWrapper(
        user_settings.email,
        user_settings.login,
        user_settings.password,
        user_settings.smtp_server,
        user_settings.imap_server,
        user_settings.pop_server,
        user_settings.smtp_port,
        user_settings.imap_port,
        user_settings.pop_port
    )
    emails = []
    protocol = 'none'
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = 'Subject: ' + request.form.get('subject') + '\n\n'
        message = request.form.get('message')
        protocol = request.form.get('protocol')
        if recipient and message:
            message = subject + message
            email_obj.send_email(recipient, message)
            return render_template('sent_email_success.html')
        if protocol == 'none':
            pass
        else:
            emails = email_obj.get_emails([1, 3], protocol)
    return render_template('send_email.html', emails=emails, protocol=protocol)


@app.route("/user/settings/", methods=['GET', 'PUT'])
def user_settings_page():
    return 'user settings'


@app.route("/user/documents/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_documents():
    return 'user documents'


@app.route("/user/templates/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_templates():
    return 'user templates'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
