import logging
import os
from datetime import (datetime,
                      timedelta,
                      date)

from flask import current_app as app
from flask import (request,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   Blueprint)
from flask_login import (logout_user,
                         login_required,
                         current_user)

from .common.url import ServiceCaller
from .common.utils import (generate_uuid4_hex)
from .forms import NewNoteForm, ResetPasswordForm, ChangePasswordForm, EditNoteForm
from .models import db, Notes, Users, ActivationToken

app.config['RECAPTCHA_USE_SSL'] = bool(int(os.environ.get("RECAPTCHA_USE_SSL", 0)))
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get("RECAPTCHA_PUBLIC_KEY", None)
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get("RECAPTCHA_PRIVATE_KEY", None)
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

main = Blueprint('main', __name__)


@app.route('/notes/healthcheck', methods=['GET'])
def healthcheck():
    return "OK", 200


def get_current_user_id(current_user):
    user = current_user
    return user.id


@app.route('/notes/get/<string:service>/<string:path>/<int:https>', methods=['GET'])
def get_service_test(service, path, https):
    url = ServiceCaller()
    request = url.call_get_on_service(service=service, path=path, https=bool(https))
    return request.json()


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


@app.context_processor
def inject_today():
    return {'today': date.today()}


@app.route('/notes/test', methods=['GET'])
def test_mails():
    url = ServiceCaller()
    request = url.call_get_on_service(service="mailer", path="healthcheck", https=False)
    return request.json()


@app.route('/notes', methods=['GET'])
def homepage():
    return render_template('homepage.html')


@app.route('/notes/account/<alternative_id>/<activate_token>', methods=['GET'])
def activate_user_account(alternative_id, activate_token):
    url = ServiceCaller()
    user = {
        "alternative_id": alternative_id,
        "activate_token": activate_token}
    request = url.call_post_on_service(user_data=user,
                                       service="auth",
                                       endpoint="activate_user_account",
                                       api_version="v1",
                                       https=False)
    if request.ok and request.json()["code"] == "201":
        flash('Account activated successfully')
        return redirect(url_for('auth_bp.login'))
    else:
        flash('Account activation failed')
        return redirect(url_for('auth_bp.login'))


@app.route('/notes/create/<alt_id>', methods=['GET', 'POST'])
@login_required
def create_note(alt_id):
    """Create a note."""
    user_id = get_current_user_id(current_user)
    logging.info(f'web ::: create_note called by user ::: {user_id}')

    form = NewNoteForm()
    notes = Notes.get_user_notes(current_user.id)

    if request.method == 'POST':
        topic = request.form['topic']
        url = request.form['url']
        subject = request.form['subject']
        text = request.form.get('ckeditor')
        created = request.form['created']
        if form.validate():
            logging.info('web ::: create_note ::: form is valid')
            new_topic = Notes(topic=topic,
                              url=url,
                              text=text,
                              subject=subject,
                              user_id=user_id,
                              created=created,
                              repeat_at=datetime.now() + timedelta(days=7))
            db.session.add(new_topic)
            db.session.commit()
            notes = Notes.get_user_notes(current_user.id)
            logging.info(f'web ::: create_note "": note added successfully by user: {user_id}')
            flash('새로운 메모 추가')
        else:
            logging.info(f'create_note : FORM IS NOT VALID. Created by user_id:{user_id}')
            return render_template('notes.html',
                                   notes=notes,
                                   form=form)

    else:
        return render_template('notes.html',
                               notes=notes,
                               form=form)
    return render_template('notes.html',
                           notes=notes,
                           form=form)


@app.route('/notes/all/<alt_id>', methods=['GET'])
@login_required
def get_all_notes(alt_id):
    notes = Notes.get_user_notes(current_user.id)
    return render_template('all_notes.html',
                           notes=notes)


@app.route('/test', methods=['GET'])
def test_query():
    user = Users.query.filter_by(alternative_id="d7f7c03f50d545968f6b8b9673339421").first()
    q = db.session.query(Users, ActivationToken) \
        .join(Users, Users.id == user.id) \
        .filter(ActivationToken.token == "50630e8f0cd34b14b5f79be1c7dedb50") \
        .filter(ActivationToken.user_id == user.id).first()

    return render_template('test_template.html', q=q)


@app.route('/notes/account/new/password/<alternative_id>/<activate_token>', methods=['GET', 'POST'])
def new_password(alternative_id, activate_token):
    form = ChangePasswordForm()
    if form.validate_on_submit():

        url = ServiceCaller()
        user_data = {"alternative_id": alternative_id,
                     "activate_token": activate_token,
                     "password": form.password.data}
        #todo encrypt password
        logging.info(f"""web ::: new_password ::: calling service ::: validate_auth_token""")
        r = url.call_post_on_service(user_data=user_data,
                                     service="auth",
                                     endpoint="validate_auth_token",
                                     api_version="v1",
                                     https=False)

        if r.ok and r.json()["code"] == "201":
            logging.info("""web ::: new_password ::: password changed successfully""")
            flash('비밀번호가 변경되었습니다. 다시 로그인하십시오!')
            return redirect(url_for('auth_bp.login'))
    else:
        return render_template('change_password.html',
                               alternative_id=alternative_id,
                               activate_token=activate_token,
                               form=form)

    return render_template('change_password.html',
                           alternative_id=alternative_id,
                           activate_token=activate_token,
                           form=form)


@app.route('/notes/user/request/change/password', methods=['GET', 'POST'])
def request_change_password():
    logging.info('web ::: request_change_password ::: get called')
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            token = ActivationToken.query.filter_by(user_id=user.id).first()

            #todo check if token is not older than 20 minutes otherwise delete it
            if token:
                flash('Please check your e-mail. You have already requested password changing')
                return redirect(url_for('auth_bp.login'))

            url = ServiceCaller()
            user_data = {"user_id": user.id}

            logging.info("""web ::: request_change_password ::: calling service ::: auth gen_auth_token""")
            r = url.call_post_on_service(user_data=user_data,
                                               service="auth",
                                               endpoint="gen_auth_token",
                                               api_version="v1",
                                               https=False)
            if r.ok and r.json()["code"] == "201":
                logging.info("""web ::: request_change_password ::: auth gen_auth_token called successfully""")

                user_data = {
                    "auth_token": r.json()["auth_token"],
                    "alternative_id": user.alternative_id,
                    "email": form.email.data,
                    "topic": "change_password"}

                r = url.call_post_on_service(user_data=user_data,
                                             service="mailer",
                                             endpoint="send_email_to_user",
                                             api_version="v1",
                                             https=False)

                if r.json()["code"] == "200":
                    logging.info("""web ::: request_change_password ::: mails send_email_to_user called successfully""")
                flash('Reset password link send')
            else:
                flash('Error')
            return redirect(url_for('auth_bp.login'))

    return render_template('reset_password.html', form=form)


@app.route('/notes/edit/<int:id>/<alt_id>', methods=['GET', 'POST'])
@login_required
def edit_note(id, alt_id):
    # try:
    note = Notes.get_user_notes(user=current_user.id, note_id=id)
    form = EditNoteForm()

    if request.method == "POST":
        note.topic = request.form['topic']
        note.url = request.form['url']
        note.subject = request.form['subject']
        note.text = request.form.get('ckeditor')
        note.created = request.form['created']
        note.repeat_at = request.form['repeat_at']
        db.session.commit()

        return redirect(url_for('get_all_notes', alt_id=alt_id))
    return render_template('edit_note.html',
                           form=form,
                           note=note)
    # except:
    #     #todo create an exception error
    #     notes = Notes.get_user_notes(current_user.id)
    #     return render_template('all_notes.html',
    #                            notes=notes)


@app.route('/notes/get/<int:note_id>/<topic>', methods=['GET', 'POST'])
@login_required
def get_note(note_id, topic):
    try:
        data = Notes.get_user_note_by_id(note_id=note_id)
        if data.repeat_at >= date.today():
            flash('연기 된 메모')
        return render_template('get_note.html', data=data)
    except:
        return render_template('404.html')


@app.route('/notes/postphone/<int:note_id>/<topic>/<int:days>', methods=['GET', 'POST'])
@login_required
def postphone_note(note_id, topic, days):
    data = Notes.get_user_note_by_id(note_id=note_id)
    data.repeat_at = datetime.now() + timedelta(days=int(days))
    db.session.commit()

    return redirect(url_for('get_note', note_id=note_id, topic=topic))


@app.route('/notes/delete/<int:id>/<alt_id>', methods=['GET', 'POST'])
@login_required
def delete(id, alt_id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    try:
        Notes.query.filter(Notes.id == id).delete()
        db.session.commit()
        logging.info('"web ::: A note with id:{id} was deleted')
        return redirect(url_for('get_all_notes', alt_id=alt_id))
    except:
        return "Error"


@app.route("/notes/logout/<alt_id>")
@login_required
def logout(alt_id):
    """User log-out logic."""
    current_user.alternative_id = generate_uuid4_hex()
    db.session.commit()
    logging.info('web ::: A new alternative_id generated')

    logout_user()
    return redirect(url_for('auth_bp.login'))


@app.route('/notes/send/email/notes/<alt_id>', methods=['GET'])
@login_required
def send_email_notes_manual_to_all(alt_id):
    url = ServiceCaller()

    logging.info("""web ::: send_email_notes_manual_to_all ::: calling service""")

    user_data = {
        'topic': 'repetitions'
    }

    r = url.call_post_on_service(user_data=user_data,
                                 service="mailer",
                                 endpoint="send_email_notes_manual_to_all",
                                 api_version="v1",
                                 https=False)

    if r.json()["code"] == "200":
        logging.info("""web ::: send_email_notes_manual_to_all ::: mails called successfully""")
    else:
        flash('ERROR')

    return redirect(url_for('get_all_notes', alt_id=alt_id))


@app.route('/notes/send/email/note/<alt_id>', methods=['GET'])
@login_required
def send_email_notes_manual_to_single_user(alt_id):
    url = ServiceCaller()

    logging.info("""web ::: send_email_notes_manual_to_single_user ::: calling service""")

    user_data = {
        "alternative_id": alt_id,
        "user_id": current_user.id,
        "email": current_user.email,
        "topic": "repetitions"
    }

    r = url.call_post_on_service(user_data=user_data,
                                 service="mailer",
                                 endpoint="send_email_to_user",
                                 api_version="v1",
                                 https=False)

    if r.json()["code"] == "200":
        logging.info("""web ::: send_email_notes_manual_to_single_user ::: mails called successfully""")
    else:
        flash('ERROR')

    return redirect(url_for('get_all_notes', alt_id=alt_id))