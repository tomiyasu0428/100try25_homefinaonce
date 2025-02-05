from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange


class RecordForm(FlaskForm):
    date = DateField("日付", format="%Y-%m-%d", validators=[DataRequired()])
    amount = DecimalField("金額", validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = SelectField(
        "カテゴリ",
        choices=[("食費", "食費"), ("交通費", "交通費"), ("家賃", "家賃"), ("その他", "その他")],
        validators=[DataRequired()],
    )
    memo = TextAreaField("メモ")
    submit = SubmitField("保存")
