import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベース接続設定 (Renderの環境変数から取得)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/booklog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースのテーブル定義
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)

# 初回アクセス時にテーブルを作成
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    new_book = Book(
        title=request.form.get('title'),
        author=request.form.get('author'),
        rating=request.form.get('rating'),
        review=request.form.get('review')
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/delete/<int:id>')
def delete_book(id):
    # 指定されたIDの本をデータベースから探す
    book_to_delete = Book.query.get_or_404(id)
    
    try:
        db.session.delete(book_to_delete) # 削除の準備
        db.session.commit()                # データベースに反映
        return redirect(url_for('index'))
    except:
        return "削除中にエラーが発生しました"