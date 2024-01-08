import sqlite3


def execute_script(cursor, script_file):
    with open(script_file, encoding='utf-8') as f:
        query = f.read()
    cursor.executescript(query)


if __name__ == '__main__':
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    scripts = [
        'sql/drop_tables.sql',
        'sql/users_init.sql',
        'sql/items_init.sql',
        'sql/reviews_init.sql',
        'sql/report_init.sql'
    ]

    for script in scripts:
        execute_script(cursor, script)

    conn.commit()
    conn.close()
