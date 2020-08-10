from flask import Blueprint, flash, g, redirect, render_template, url_for, request, current_app, abort
from flask_login import login_required, current_user

bp = Blueprint('messages', __name__)

from app import db

from app.auth.models import User
from app.organization.models import Organization
from app.messages.models import Message, Alert, Thread, user_to_message

from app.search.forms import SearchForm
from app.messages.forms import MessageForm

from app.main.funcs import isint

from datetime import datetime

from sqlalchemy import update

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()

@bp.route('/')
@login_required
def messages():
    current_user.add_notification('unread_message_count', current_user.new_messages_count())
    db.session.commit()

    page = request.args.get('page', 1, type=int)

    q = current_user.threads.filter(Thread.messages != None).order_by(Thread.last_updated.desc())
    threads = q.all()[:current_app.config['POSTS_PER_PAGE']]

    threadIDs = []
    for thread in threads:
        members = User.query.filter(User.threads.any(Thread.id == thread.id)).all()
        if len(members) == 2 and current_user in members:
            members.remove(current_user)
            threadIDs.append(members[0].username)
        else:
            threadIDs.append(thread.id)

    threads = q.paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('messages.messages', page=threads.next_num) \
        if threads.has_next else None
    prev_url = url_for('messages.messages', page=threads.prev_num) \
        if threads.has_prev else None
    return render_template('messages/messages.html', threadIDs_threads=zip(threadIDs, threads.items),
                           next_url=next_url, prev_url=prev_url)

@bp.route('/t/<string:thread_id>', methods=['GET', 'POST'])
@login_required
def view_message(thread_id: str):
    current_user.add_notification('unread_message_count', current_user.new_messages_count())
    db.session.commit()
    form = MessageForm()

    if isint(thread_id):
        thread = current_user.threads.filter_by(id=thread_id).first_or_404()

    else:
        recipient = User.query.filter_by(username = thread_id).first_or_404()
        thread = recipient.threads.intersect(current_user.threads).first()
        if not thread:
            thread = Thread()
            db.session.add(thread)
            recipient.add_thread(thread)
            recipient.add_notification('unread_message_count', recipient.new_messages_count())
            current_user.add_thread(thread)
            db.session.commit()
            return redirect(url_for('messages.view_message', thread_id=recipient.username))

    recipients = User.query.filter(User.id!=current_user.id).filter(User.threads.any(Thread.id == thread.id)).all()

    for message in thread.messages:
        if not message.get_read_time(current_user):
           message.set_read_time(current_user, datetime.utcnow())

    if form.validate_on_submit():
        thread.last_updated = datetime.utcnow()
        for recipient in recipients:
                msg = Message(sender=current_user, 
                              thread = thread,
                              body=form.message.data)
                db.session.add(msg)
                msg.add_recipient(recipient)
                recipient.add_notification('unread_message_count', recipient.new_messages_count())
                db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('messages.view_message', thread_id=thread.id))
    return render_template('messages/view_message.html', thread=thread, recipients=recipients, form=form)

@bp.route('/send/<org_id>', methods=['GET', 'POST'])
@login_required
def send_message_to_org(id):
    recipient_org = Organization.query.filter_by(id=id).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        thread = Thread()
        db.session.add(thread)
        recipients = User.query
        for recipitent in recipients:
            recipitent.add_thread(thread)
        current_user.add_thread(thread)
        msg = Message(sender = current_user, 
                      recipient_org = recipient_org,
                      thread = thread,
                      body = form.message.data)
        db.session.add(msg)
        
        recipient.add_notification('unread_message_count', recipient.new_messages_count())
        
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('messages.messages'))
    return render_template('messages/send_message.html', title='Send Message',
                           form=form, recipient_org=recipient_org)

@bp.route('/alerts')
@login_required
def alerts():
    current_user.add_notification('unread_alerts_count', current_user.new_alerts_count())
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    threads = current_user.threads.filter(Thread.alerts != None).order_by(
        Thread.last_updated.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages.alerts', page=threads.next_num) \
        if threads.has_next else None
    prev_url = url_for('messages.alerts', page=threads.prev_num) \
        if threads.has_prev else None
    return render_template('messages/alerts.html', threads=threads.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/alerts/t/<thread_id>')
@login_required
def view_alert(thread_id):
    thread = Thread.query.filter_by(id=thread_id).first_or_404()
    if thread.id not in [t.id for t in current_user.threads.all()]:
        flash('You cannot view this message')
        return redirect(url_for('main.index'))
    for alert in thread.alerts:
        if not alert.read_time:
            alert.read_time = datetime.utcnow()
            db.session.commit()
    return render_template('messages/view_alert.html', thread=thread)