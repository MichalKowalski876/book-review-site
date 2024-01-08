import sqlite3


def get_connection():
    conn = sqlite3.connect('../database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


def get_all_items():
    conn = get_connection()
    c = conn.cursor()

    result = c.execute('SELECT * FROM "items"')
    return result.fetchall()


def perform_search(search_query):
    conn = get_connection()
    c = conn.cursor()

    search_query = f"%{search_query}%"

    query = """
    SELECT * FROM "items" 
    WHERE ("id" LIKE ? OR "name" LIKE ? OR "author" LIKE ? OR "year_published" LIKE ?)
    AND "status" != 1
    """
    c.execute(query, (search_query, search_query, search_query, search_query))

    results = c.fetchall()

    return results


def get_status(*args):
    conn = get_connection()
    c = conn.cursor()
    query = 'SELECT * FROM "items" WHERE "status" = ? OR "status" = ? OR "status" = ?'

    result = c.execute(query, (args[0], args[1], args[2],))
    return result.fetchall()


def get_item_by_id(item_id):
    conn = get_connection()
    c = conn.cursor()

    query = 'SELECT * FROM "items" WHERE "id" = ?'

    result = c.execute(query, (item_id,))
    conn.commit()

    return result.fetchone()


def get_report_by_id(item_id):
    conn = get_connection()
    c = conn.cursor()

    query = 'SELECT * FROM "reports" WHERE "item_id" = ?'
    result = c.execute(query, (item_id,))
    conn.commit()

    return result.fetchall()


def add_report_db(item_id, desc):
    conn = get_connection()
    c = conn.cursor()

    query = 'UPDATE "items" SET "status" = 2 WHERE "id" = ?'

    c.execute(query, (item_id,))
    conn.commit()

    query = 'INSERT INTO "reports" VALUES (NULL, ?, ?)'
    params = (item_id, desc)

    c.execute(query, params)
    conn.commit()


def db_status_change(book_id, accepted):  # status  0 - active  1 - pending add   2 - delete req
    conn = get_connection()
    c = conn.cursor()

    status = (get_item_by_id(book_id))['status']
    delete_reports(book_id)

    if accepted:
        if status == 1:
            query = """ 
            UPDATE "items"
            SET "status" = 0
            WHERE "id" = ?;
            """

            c.execute(query, (book_id,))
            conn.commit()
        elif status == 2:
            delete_reviews(book_id)
            query = """ 
            DELETE FROM "items"
            WHERE "id" = ?;
            """

            c.execute(query, (book_id,))
            conn.commit()
    else:
        if status == 1:
            query = """ 
            DELETE FROM "items"
            WHERE "id" = ?;
            """
            c.execute(query, (book_id,))
            conn.commit()

        elif status == 2:
            query = """ 
            UPDATE "items"
            SET "status" = 0
            WHERE "id" = ?;
            """
            c.execute(query, (book_id,))
            conn.commit()


def fetch_user(username):
    conn = get_connection()
    c = conn.cursor()

    result = c.execute('SELECT * FROM users WHERE username = ?', (username,))
    return result.fetchone()


def add_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    params = (username, password)
    query = """
            INSERT INTO "users" VALUES (NULL, ?, ?, 0)
            """

    c.execute(query, params)
    conn.commit()


def check_if_user_exists(username):
    conn = get_connection()
    c = conn.cursor()

    query = "SELECT count(username) from users WHERE username = ?"
    c.execute(query, (username,))
    result = c.fetchone()[0]

    if result != 0:
        return True
    else:
        return False


def db_add_review(book_id, user_id, review):
    conn = get_connection()
    c = conn.cursor()

    params = (book_id, user_id, review)
    query = """
        INSERT INTO "reviews" VALUES (NULL, ?, ?, ?)
        """

    c.execute(query, params)
    conn.commit()

    insert_reviews_mean(book_id)


def get_reviews_sum(book_id):
    conn = get_connection()
    c = conn.cursor()

    query = 'SELECT SUM(score) FROM "reviews" WHERE "item_id" = ?'
    result = c.execute(query, (book_id,))
    conn.commit()

    sum_result = result.fetchone()[0]

    return sum_result


def get_reviews_mean(book_id):
    conn = get_connection()
    c = conn.cursor()

    query = 'SELECT COUNT(*) FROM "reviews" WHERE item_id = ?'

    amount = c.execute(query, (book_id,))
    count_result = amount.fetchone()
    count = count_result[0]

    mean = round(get_reviews_sum(book_id) / count, 2)

    return mean


def insert_reviews_mean(book_id):
    conn = get_connection()
    c = conn.cursor()

    mean = get_reviews_mean(book_id)

    query = """ 
     UPDATE "items" SET "score" = ? WHERE "id" = ?;
     """

    c.execute(query, (mean, book_id))
    conn.commit()


def count_reviews(book_id):
    conn = get_connection()
    c = conn.cursor()

    query = 'SELECT COUNT(*) FROM "reviews" WHERE item_id = ?'

    amount = c.execute(query, (book_id,))
    count_result = amount.fetchone()
    count = count_result[0]

    return count


def refresh_score():
    all_items = get_all_items()
    for item in all_items:
        if count_reviews(item['id']) != 0:
            insert_reviews_mean(item['id'])


def add_book(title, author, year, cover):
    conn = get_connection()
    c = conn.cursor()

    query = """
    INSERT INTO "items" VALUES (NULL, ?, ?, ?, 0, 1, ?)
    """
    params = (title, author, year, cover)

    c.execute(query, params)
    conn.commit()


def get_user_review(user_id, book_id):
    conn = get_connection()
    c = conn.cursor()

    query = """
    SELECT user_id, item_id, score FROM reviews WHERE user_id = ? AND item_id = ?
    """
    result = c.execute(query, (user_id, book_id))

    if result == None:
        return False

    return result.fetchone()


def delete_reports(book_id):
    conn = get_connection()
    c = conn.cursor()

    query = """
    DELETE from 'reports' WHERE item_id = ?
    """

    c.execute(query, (book_id,))
    conn.commit()


def delete_reviews(book_id):
    conn = get_connection()
    c = conn.cursor()

    query = """
    DELETE from 'reviews' WHERE item_id = ?
    """

    c.execute(query, (book_id,))
    conn.commit()
