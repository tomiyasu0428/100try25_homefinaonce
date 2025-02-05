from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Record
from forms import RecordForm
from datetime import datetime
from sqlalchemy import extract

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# 初期化用コマンド（初回実行時に利用）
@app.cli.command("initdb")
def initdb_command():
    """データベースの初期化を行います。"""
    db.create_all()
    print("Initialized the database.")


@app.route("/", methods=["GET", "POST"])
def index():
    form = RecordForm()
    if form.validate_on_submit():
        # 入力された日付はdatetime.date型なのでそのまま利用
        record = Record(
            date=form.date.data,
            amount=float(form.amount.data),
            category=form.category.data,
            memo=form.memo.data,
        )
        db.session.add(record)
        db.session.commit()
        flash("記録を保存しました。")
        return redirect(url_for("index"))

    records = Record.query.order_by(Record.date.desc()).all()
    return render_template("index.html", form=form, records=records)


@app.route("/edit/<int:record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    record = Record.query.get_or_404(record_id)
    form = RecordForm(obj=record)
    if form.validate_on_submit():
        record.date = form.date.data
        record.amount = float(form.amount.data)
        record.category = form.category.data
        record.memo = form.memo.data
        db.session.commit()
        flash("記録を更新しました。")
        return redirect(url_for("index"))
    return render_template("edit_record.html", form=form, record=record)


@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    record = Record.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash("記録を削除しました。")
    return redirect(url_for("index"))


@app.route("/aggregate")
def aggregate():
    # 例: 現在の月の集計
    now = datetime.utcnow()
    records = Record.query.filter(
        extract("year", Record.date) == now.year, extract("month", Record.date) == now.month
    ).all()
    total_income = sum(r.amount for r in records if r.amount > 0)
    total_expense = sum(r.amount for r in records if r.amount < 0)
    balance = total_income + total_expense  # expenseは負の数とする
    return render_template(
        "aggregate.html", total_income=total_income, total_expense=abs(total_expense), balance=balance
    )


if __name__ == "__main__":
    app.run()
