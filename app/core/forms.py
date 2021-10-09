from app.models import User
from flask_babel import lazy_gettext as _l  # noqa: WPS347, WPS111
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])  # noqa: WPS221
    submit = SubmitField(_l('Edit'))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField(_l('Submit'))


class PostForm(FlaskForm):
    post = TextAreaField(
        _l('Write your post here'),
        validators=[DataRequired(), Length(min=1, max=10000)],
    )
    submit = SubmitField(_l('Create Post'))
