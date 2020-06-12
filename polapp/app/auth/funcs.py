from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from flask_wtf import FlaskForm, Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app import app, db, login

from app.messages.funcs import send_password_reset_email, send_validation_email

from app.search.forms import SearchForm

from hashlib import md5
from datetime import datetime
from time import time
import jwt

