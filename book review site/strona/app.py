from flask import Flask, render_template, request, redirect, session, url_for

from db_utils import (add_user, fetch_user, get_status, get_item_by_id, perform_search, db_status_change, db_add_review,
                      refresh_score, check_if_user_exists, add_book, get_report_by_id, add_report_db, get_user_review, )

from auth import login_required, admin_required

from config import Config

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    refresh_score()
    items = get_status(0, 0, 2)
    username = session.get('username')
    context = {'items': items, 'username': username}
    return render_template('index.html', **context)


@app.route('/login')
def login():
    return render_template('login_register.html')


@app.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    item = get_item_by_id(id)
    admin = False
    active_session = False
    review = None
    if session:
        admin = fetch_user(session.get('username'))['admin']
        active_session = True
        user_id = fetch_user(session.get('username'))['id']

        if get_user_review(user_id, item['id']):
            review = get_user_review(user_id, item['id'])
    reports = get_report_by_id(item['id'])

    context = {
        'item': item,
        'admin': admin,
        'reports': reports,
        'review': review,
        'active_session': active_session
    }

    return render_template('view.html', **context)


@app.route('/report', methods=['POST'])
@login_required
def report_book():
    item = get_item_by_id(request.form.get('id'))

    return render_template('report.html', item=item)


@app.route('/add_report', methods=['POST'])
@login_required
def add_report():
    description = request.form.get('desc')
    item_id = request.form.get('id')

    add_report_db(item_id, description)
    return redirect(url_for('view', id=item_id))


@app.route('/add_request')
def add_request():
    items = get_status(1, 2, 3)  # status  0 - active  1 - pending add   2 - delete req

    context = {'items': items}
    return render_template('add_request.html', **context)


@app.route('/add', methods=['POST'])
@login_required
def add_book_action():
    title = request.form.get('name')
    author = request.form.get('author')
    year = request.form.get('year_published')
    cover_url = request.form.get('cover')

    add_book(title, author, year, cover_url)

    return redirect('/add_request')


@app.route('/search_results')
def search():
    search_query = request.args.get('search_query')

    results = perform_search(search_query)

    context = {'results': results, 'search_query': search_query}
    return render_template('search_results.html', **context)


@app.route('/accept_change_status', methods=['POST'])
@admin_required
def accepted_change_status():
    book_id = request.form.get('id')
    db_status_change(book_id, True)

    return redirect('/')


@app.route('/deny_change_status', methods=['POST'])
@admin_required
def deny_change_status():
    book_id = request.form.get('id')
    db_status_change(book_id, False)

    return redirect('/')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('login_register.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = fetch_user(username)

        if user_data:
            password_from_db = user_data['password']
            if check_password_hash(password_from_db, password):
                session['user_id'] = user_data['id']
                session['username'] = user_data['username']

                return redirect('/')

        return 'Wrong username or password'


@app.route('/register', methods=['POST'])
def register():
    username = request.form['register_username']
    password = request.form['register_password']
    confirm_password = request.form['register_confirm_password']

    if check_if_user_exists(username):
        return "username already in use"

    if password == confirm_password:
        add_user(username, generate_password_hash(password))

        user_data = fetch_user(username)
        session['user_id'] = user_data['id']
        session['username'] = user_data['username']

        return redirect('/')

    return "Passwords not identical"


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/add_review', methods=["POST"])
@login_required
def add_review():
    book_id = request.form.get('book_id')
    user_id = session['user_id']
    review = request.form.get('review')

    if get_user_review(user_id, book_id):
        return 'Book has been reviewed'

    db_add_review(book_id, user_id, review)
    return redirect(url_for('view', id=book_id))


if __name__ == '__main__':
    app.run()
