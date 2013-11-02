# database.py contains all the functions used for interfacing with the data base and such.
import config
import sqlite3

def read_user(user_id, username):
    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from users')
        
        rows = cur.fetchall()
        found = 0
        for row in rows:
            if (username == None):
                if (row['id'] == int(user_id)):
                    found = 1
                    break
            else:
                if (row['username'] == username):
                    found = 1
                    break
                else:
                    found = 0

        if (found == 0):
            config.last_error = "Sorry that we can't find that username in our banks."
            return None
            
    return row

def check_user_email(email):
    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute('select * from users where email=?', (email,))

        user = cur.fetchone()

    return user

def reset_user_pass(user_id):
    password = "password"

    update_user(("password_hash=?"),(password, user_id))

    return password

def write_user(user):
    con = sqlite3.connect(config.db_dir)

    with con:
        cur = con.cursor()

        cur.execute("insert into users(username,first_name,last_name,email,password_hash,street,city,state,postcode,verified) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user)

def update_user(fields, user):
    con = sqlite3.connect(config.db_dir)

    with con:
        cur = con.cursor()

        cur.execute("update users set " + fields + " where id=?", user)

def read_books():

    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from books')

        books = cur.fetchall()

    return books

def read_book(isbn):

    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from books where isbn=?', (isbn,))
        book = cur.fetchone()

    return book

def read_books_by_author(author):
    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from books where authors like '%%%s%%'" % author)

        books = cur.fetchall()    

    return books

def get_user_cart(user_id):
    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute('select * from basket_items where user_id=?', (user_id,))

        books = cur.fetchall()

    return books

def get_user_cart_num_items(user_id):
    cart = get_user_cart(user_id)
    total_items = 0
    for item in cart:
        total_items += item['num']
    return total_items  

def add_to_cart(isbn, num):
    num = int(num)
    con = sqlite3.connect(config.db_dir)
    with con:
        cur = con.cursor()
        cart_item = (
            config.cur_user_id,
            isbn,
            int(num)
        )

        cur.execute('select * from basket_items where user_id=? and isbn=?', (config.cur_user_id, isbn))

        item = cur.fetchone()
        if (item is not None):
            num += item[2]
            cur.execute('update basket_items set num=? where user_id=? and isbn=?', (num, config.cur_user_id, isbn))
        else:
            cur.execute('insert into basket_items values (?,?,?)', cart_item)

def update_cart(form):

    to_remove = []
    cur_num_values = {}
    for book in get_user_cart(config.cur_user_id):
        remove_name = "remove_" + book['isbn']
        num_name = "num_books_" + book['isbn']
        if (form.getvalue(remove_name) == "remove"):
            to_remove.append(book['isbn'])
        cur_num_values[book['isbn']] = form.getvalue(num_name)

    con = sqlite3.connect(config.db_dir)
    with con:
        cur = con.cursor()

        for isbn in to_remove:
            cur.execute("delete from basket_items where isbn=? and user_id=?", (isbn, config.cur_user_id))

        cur.execute("select * from basket_items where user_id=?", (config.cur_user_id,))
        rows = cur.fetchall()
        for row in rows:
            isbn = row[1]
            if (row[2] != int(cur_num_values[isbn])):
                cur.execute("update basket_items set num=? where isbn=? and user_id=?", (cur_num_values[isbn], isbn, config.cur_user_id))

def clear_user_cart(user_id):
    con = sqlite3.connect(config.db_dir)

    with con:
        cur = con.cursor()

        cur.execute('delete from basket_items where user_id=?', (user_id,))

def write_order(user_id, cc_num, cc_exp):
    con = sqlite3.connect(config.db_dir)

    cart = get_user_cart(user_id)

    with con:
        cur = con.cursor()

        cur.execute('insert into orders(user_id, cc_num, cc_exp) values(?, ?, ?)', (user_id, cc_num, cc_exp))  
        order_id = cur.lastrowid
        for item in cart:
            cur.execute('insert into order_items values(?, ?, ?)', (order_id, item['isbn'], item['num']))

def get_user_orders(user_id):
    con = sqlite3.connect(config.db_dir)

    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute('select * from orders where user_id=?', (user_id,))

        orders = cur.fetchall()

        user_orders = []
        for order in orders:
            user_order = {}
            for key in order.keys():
                user_order[key] = order[key]
                cur.execute('select * from order_items where order_id=?', (order['id'],))
                user_order['items'] = cur.fetchall()
            user_orders.append(user_order)

    return user_orders
