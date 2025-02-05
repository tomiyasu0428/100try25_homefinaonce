from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Record
from forms import RecordForm
from datetime import datetime
from sqlalchemy import extract, func
import os
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# アップロード先設定（OCR機能用）
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.cli.command("initdb")
def initdb_command():
    """データベースの初期化を行います。"""
    db.create_all()
    print("Initialized the database.")


@app.route("/", methods=["GET", "POST"])
def index():
    form = RecordForm()
    if form.validate_on_submit():
        # 「収入」なら正の値、支出の場合は入力金額を負の値として扱う
        amount = float(form.amount.data)
        if form.category.data != "収入":
            amount = -amount
        record = Record(date=form.date.data, amount=amount, category=form.category.data, memo=form.memo.data)
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
        amount = float(form.amount.data)
        if form.category.data != "収入":
            amount = -amount
        record.date = form.date.data
        record.amount = amount
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
    now = datetime.utcnow()
    # 今月の各カテゴリごとの合計を集計
    monthly_records = (
        db.session.query(Record.category, func.sum(Record.amount).label("total"))
        .filter(extract("year", Record.date) == now.year, extract("month", Record.date) == now.month)
        .group_by(Record.category)
        .all()
    )

    # 収入と支出を分離
    income_records = [r for r in monthly_records if r.category == "収入"]
    expense_records = [r for r in monthly_records if r.category != "収入"]

    total_income = sum(r.total for r in income_records)
    total_expense = abs(sum(r.total for r in expense_records))  # 支出は正の値で表示
    overall_total = total_income + sum(r.total for r in expense_records)

    # 支出のみの円グラフデータ
    expense_data = {
        "labels": [r.category for r in expense_records],
        "data": [abs(r.total) for r in expense_records],  # 支出は正の値で表示
    }

    return render_template(
        "aggregate.html",
        monthly_records=monthly_records,
        total_income=total_income,
        total_expense=total_expense,
        overall_total=overall_total,
        chart_data=expense_data,
    )


@app.route("/upload_receipt", methods=["GET", "POST"])
def upload_receipt():
    if request.method == "POST":
        if "file" not in request.files:
            flash("ファイルが選択されていません")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("ファイル名が空です")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            try:
                image = Image.open(save_path)
                # pytesseractを用いてOCRを実行。日本語モデルがインストール済みであれば lang='jpn'
                text = pytesseract.image_to_string(image, lang="jpn")
            except Exception as e:
                flash("OCR処理に失敗しました: " + str(e))
                text = ""
            flash("OCR結果: " + text)
            return redirect(url_for("upload_receipt"))
    return render_template("receipt.html")


if __name__ == "__main__":
    app.run()
