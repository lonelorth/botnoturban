import sqlite3


def initiate_db():
    connection = sqlite3.connect('products2.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products2.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products WHERE id > ?', (0,))
    return cursor.fetchall()

    connection.commit()
    connection.close()
