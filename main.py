import datetime

from flask import Flask, request, render_template, redirect, session, url_for
import al_db
import email_lib
import mongo_lib
from bson.objectid import ObjectId
import re

from celery_worker import send_mail
from models import Vacancy, Event, User, EmailCredentials

app = Flask(__name__)
app.secret_key = 'f5d24c22ee66171979a78155d54b656fcea6a51b0ad49b3892393a08ebac7795'


@app.route("/", methods=['GET'])
def main_proc():
    al_db.init_db()
    return redirect('/vacancy/')


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancy():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    mongo_obj = mongo_lib.MongoLib()
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        comment = request.form.get('comment')

        contact_id = mongo_obj.m_insert_one({"name": contact_name, "email": contact_email, "phone": contact_phone})

        current_vacancy = Vacancy(position_name, company, description, str(contact_id), comment,
                                  status=1, user_id=session.get('user_id'))
        al_db.db_session.add(current_vacancy)
        al_db.db_session.commit()

    result = al_db.db_session.query(Vacancy.id, Vacancy.position_name, Vacancy.company, Vacancy.description,
                                    Vacancy.comment, Vacancy.contact_ids).\
        filter_by(user_id=session.get('user_id')).all()
    result_data = []
    for item in result:
        contacts = item[5].split(',')
        contact_result = []
        for one_contact in contacts:
            data = mongo_obj.m_find_one({'_id': ObjectId(one_contact)})
            contact_result.append(data)
        result_data.append({'id': item[0], 'position_name': item[1], 'company': item[2], 'description': item[3],
                            'comment': item[4], 'contacts': contact_result})
    return render_template('vacancy_add.html', vacancies=result_data)


@app.route("/vacancy/<int:vacancy_id>/", methods=['GET', 'POST'])
def show_vacancy_content(vacancy_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    mongo_obj = mongo_lib.MongoLib()
    if request.method == 'POST':
        position_name = request.form.get('position_name')
        company = request.form.get('company')
        description = request.form.get('description')
        comment = request.form.get('comment')
        al_db.db_session.query(Vacancy).filter(Vacancy.id == vacancy_id).update({
            Vacancy.position_name: position_name, Vacancy.company: company, Vacancy.description: description,
            Vacancy.comment: comment})
        al_db.db_session.commit()
    vacancy_desc = al_db.db_session.query(Vacancy.id, Vacancy.position_name, Vacancy.company, Vacancy.description,
                                          Vacancy.comment, Vacancy.contact_ids).\
        where(Vacancy.id == vacancy_id).filter_by(user_id=session.get('user_id')).all()
    events = al_db.db_session.query(Event.id, Event.title, Event.description,
                                    Event.due_to_date).where(Event.vacancy_id == vacancy_id)
    if not vacancy_desc:
        return render_template('error.html', message="Щось пішло не так(vacancy), або ж перервано спробу хаку")
    for item in vacancy_desc:
        contacts = item[5].split(',')
        contact_result = []
        for one_contact in contacts:
            data = mongo_obj.m_find_one({'_id': ObjectId(one_contact)})
            contact_result.append(data)
        result_data = {'id': item[0], 'position_name': item[1], 'company': item[2], 'description': item[3],
                       'comment': item[4], 'contacts': contact_result}
    return render_template('vacancy_update.html', vacancy_id=vacancy_id, vacancy_desc=result_data, events=events)


@app.route("/vacancy/<int:vacancy_id>/contacts/", methods=['GET', 'POST'])
def change_contacts(vacancy_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    mongo_obj = mongo_lib.MongoLib()
    if request.method == 'POST':
        record_id = request.form.get('record_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        delete = request.form.get('delete')
        if delete:
            mongo_obj.delete_one({"_id": ObjectId(record_id)})
            vacancy_desc = al_db.db_session.query(Vacancy.contact_ids).where(Vacancy.id == vacancy_id).\
                filter_by(user_id=session.get('user_id')).first()
            for obj_id in vacancy_desc:
                regex_replacements = [(rf"{record_id}", ""), (r",$", ""), (r"^,", ""), (r",,", ",")]
                for old, new in regex_replacements:
                    obj_id = re.sub(old, new, obj_id, flags=re.IGNORECASE)
                al_db.db_session.query(Vacancy).filter(Vacancy.id == vacancy_id).update({Vacancy.contact_ids: obj_id})
                al_db.db_session.commit()
        elif record_id:
            mongo_obj.update_one({"_id": ObjectId(record_id)}, {"$set": {"name": name, "email": email, "phone": phone}})
        else:
            contact_id = mongo_obj.m_insert_one({"name": name, "email": email, "phone": phone})
            vacancy_desc = al_db.db_session.query(Vacancy.contact_ids).where(Vacancy.id == vacancy_id).first()
            lst = f'{vacancy_desc[0]},{contact_id}'
            al_db.db_session.query(Vacancy).filter(Vacancy.id == vacancy_id).update({Vacancy.contact_ids: lst})
            al_db.db_session.commit()

    vacancy_desc = al_db.db_session.query(Vacancy.position_name, Vacancy.company, Vacancy.contact_ids).\
        where(Vacancy.id == vacancy_id).filter_by(user_id=session.get('user_id')).all()
    if not vacancy_desc:
        return render_template('error.html', message="Щось пішло не так(contacts), або ж перервано спробу хаку")
    for item in vacancy_desc:
        contacts = item[2].split(',')
        contact_result = []
        for one_contact in contacts:
            data = mongo_obj.m_find_one({'_id': ObjectId(one_contact)})
            contact_result.append(data)
        result_data = {'position_name': item[0], 'company': item[1], 'contacts': contact_result}
    return render_template('change_contacts.html', vacancy_id=vacancy_id, vacancy_desc=result_data)


@app.route("/vacancy/<int:vacancy_id>/events/", methods=['GET', 'POST'])
def vacancy_events(vacancy_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    if request.method == 'POST':
        description = request.form.get('description')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')
        add_event = Event(vacancy_id, title, description, due_to_date, status=1)
        al_db.db_session.add(add_event)
        al_db.db_session.commit()

    user_id = al_db.db_session.query(Vacancy.user_id).filter(Vacancy.id == vacancy_id).first()
    if user_id is None:
        return render_template('error.html', message="Щось пішло не так(events), або ж перервано спробу хаку")
    if user_id[0] == session.get('user_id'):
        result = al_db.db_session.query(Event.id, Event.title, Event.description,
                                        Event.due_to_date).where(Event.vacancy_id == vacancy_id)
        return render_template('event_add.html', vacancy_id=vacancy_id, events=result)
    else:
        return render_template('error.html', message="Щось пішло не так, або ж перервано спробу хаку")


@app.route("/vacancy/<int:vacancy_id>/events/<int:event_id>/", methods=['GET', 'POST'])
def show_event_content(vacancy_id, event_id):
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    if request.method == 'POST':
        description = request.form.get('description')
        title = request.form.get('title')
        due_to_date = request.form.get('due_to_date')
        al_db.db_session.query(Event).filter(Event.id == event_id, Event.vacancy_id == vacancy_id). \
            update({Event.title: title, Event.description: description, Event.due_to_date: due_to_date})
        al_db.db_session.commit()

    event_belong = al_db.db_session.query(Event.id, Event.vacancy_id, Event.title, Event.description). \
        filter(Event.id == event_id, Event.vacancy_id == vacancy_id).all()
    user_belong = al_db.db_session.query(Vacancy.user_id).filter(Vacancy.id == vacancy_id).first()
    if event_belong and user_belong and user_belong[0] == session.get('user_id'):
        event = al_db.db_session.query(Event.id, Event.title, Event.description, Event.due_to_date). \
            where(Event.id == event_id, Event.vacancy_id == vacancy_id).first()
        return render_template('event_update.html', vacancy_id=vacancy_id, event_id=event_id, event=event)
    else:
        return render_template('error.html', message="Щось пішло не так(event_id), або ж перервано спробу хаку")


@app.route("/vacancy/<vacancy_id>/history/", methods=['GET'])
def vacancy_history():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    return 'vacancy history'


@app.route("/user/registration/", methods=['GET', 'POST'])
def func_user_registration():
    if request.method == 'POST':
        user_login = request.form.get('user_login')
        user_password = request.form.get('user_password')
        user_email = request.form.get('user_email')
        user_name = request.form.get('user_name')
        user_add = User(login=user_login, password=user_password, email=user_email, name=user_name)
        al_db.db_session.add(user_add)
        al_db.db_session.commit()
        return redirect(url_for('func_user_login'))
    return render_template('user_registration.html')


@app.route("/user/login/", methods=['GET', 'POST'])
def func_user_login():
    if request.method == 'POST':
        user_login = request.form.get('user_login')
        user_password = request.form.get('user_password')
        user_obj = al_db.db_session.query(User).filter(User.login == user_login).first()
        if user_obj is None:
            return render_template('user_login.html',
                message="Користувач не знайдений! Можливо, ви помилилися, або ж вам потрібно зареєструватися")
        if user_obj.password != user_password:
            return render_template('user_login.html',
                                   message="Невдала спроба входу! Перевірте правильність логіну/паролю.")
        else:
            session['user_id'] = user_obj.id
            session['user_login'] = user_obj.login
            return redirect(url_for('user_main_page'))
    return render_template('user_login.html', message=None)


@app.route("/user/logout/", methods=['GET', 'POST'])
def func_user_logout():
    session.pop('user_id', None)
    session.pop('user_login', None)
    return render_template('user_login.html',
                           message="Ви вийшли з системи. Перенаправлено на сторінку входу...")


@app.route("/user/", methods=['GET', 'POST'])
def user_main_page():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    return render_template('user_home.html', user_name=session.get('user_login'))


@app.route("/user/calendar/", methods=['GET'])
def user_calendar():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    return 'user calendar'


@app.route("/user/mail/", methods=['GET', 'POST'])
def user_mail():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    user_settings = al_db.db_session.query(EmailCredentials).filter_by(user_id=session.get('user_id')).first()
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
            # email_obj.send_email(recipient, message)
            send_mail.apply_async(args=[user_settings.id, recipient, message])
            return render_template('sent_email_success.html')
        if protocol == 'none':
            pass
        else:
            emails = email_obj.get_emails([1, 3], protocol)
    return render_template('send_email.html', emails=emails, protocol=protocol)


@app.route("/user/settings/", methods=['GET', 'PUT'])
def user_settings_page():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    return 'user settings'


@app.route("/user/documents/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_documents():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    return 'user documents'


@app.route("/user/templates/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_templates():
    if session.get('user_id', None) is None:
        return redirect(url_for('func_user_login'))
    return 'user templates'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
