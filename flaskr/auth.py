import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Blueprintの作成
# アプリケーションに定義場所を通知するため__name__は引数として必須
bp = Blueprint('auth', __name__, url_prefix='/auth')

# ビューの登録
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                db.close()
                
            except db.IntegrityError:

                # f-strings(python3.6からの機能)
                error = f'User {username} is already registerd.'
            
            else:
                # /auth/login/にリダイレクト
                return redirect(url_for("auth.login"))

        # セッションにメッセージ格納
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        error = None
        user_execute = cursor.execute(

            # fetchoneでクエリから1行を返却する。なかった場合はNoneを返却する
            "SELECT * FROM user WHERE username = ?", (username,)
            
        )

        user = user_execute.fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:

            # session情報の登録。ユーザidは新しいsessionに保存され、データはブラウザに送信されるCookieに保存される。
            # その後リクエストでデータを送り返す。Flaskは、データが改ざんされないようにデータに署名する。
            # idが保存されたため、以降のリクエストで利用可能となる。
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# factoryにユーザネームを登録
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',(user_id,)).fetchone()

# ログアウト
# sessionクリア
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ユーザがログインしていることをデコレータを用いて確認する
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
