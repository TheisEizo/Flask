from flask import Blueprint, flash, g, redirect, render_template, url_for, request, current_app
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('messages', __name__)

from app import db

from app.auth.models import User
from app.messages.forms import MessageForm
from app.messages.models import Message, Alert, Thread
from app.search.forms import SearchForm

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()

@bp.route('/messages')
@login_required
def messages():
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    threads = current_user.threads.filter(Thread.messages != None).order_by(
        Thread.last_updated.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages.messages', page=threads.next_num) \
        if threads.has_next else None
    prev_url = url_for('messages.messages', page=threads.prev_num) \
        if threads.has_prev else None
    return render_template('messages/messages.html', threads=threads.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/messages/<thread_id>', methods=['GET', 'POST'])
@login_required
def view_message(thread_id):
    thread = Thread.query.filter_by(id=thread_id).first_or_404()

    if thread.id not in [t.id for t in current_user.threads.all()]:
        flash('You cannot view this message')
        return redirect(url_for('main.index'))

    for message in thread.messages:
        if not message.read_time:
            message.read_time = datetime.utcnow()
            db.session.commit()

    form = MessageForm()

    recipient_users = User.query.filter(User.threads.any(Thread.id == thread.id)).all()
    if len(recipient_users) > 1:
        recipient_users.remove(current_user)

    if form.validate_on_submit():
        thread.last_updated = datetime.utcnow()
        for recipient_user in recipient_users:
                msg = Message(sender=current_user, 
                              recipient=recipient_user,
                              thread = thread,
                              body=form.message.data)
                db.session.add(msg)
                recipient_user.add_notification('unread_message_count', recipient_user.new_messages_count())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('messages.view_message', thread_id=thread.id))
    return render_template('messages/view_message.html', thread=thread, recipients=recipient_users, form=form)

@bp.route('/messages/send/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    recipient_user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        thread = Thread()
        db.session.add(thread)
        recipient_user.add_thread(thread)
        current_user.add_thread(thread)
        msg = Message(sender = current_user, 
                      recipient = recipient_user,
                      thread = thread,
                      body = form.message.data)
        db.session.add(msg)
        recipient_user.add_notification('unread_message_count', recipient_user.new_messages_count())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('messages.messages'))
    return render_template('messages/send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@bp.route('/alerts')
@login_required
def alerts():
    current_user.add_notification('unread_alerts_count', 0)
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

@bp.route('/alerts/<thread_id>')
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
