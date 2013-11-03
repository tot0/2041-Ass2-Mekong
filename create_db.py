
import json, sqlite3
from collections import defaultdict

def default():
    return ""

def create_db():
    con = sqlite3.connect("mekong.db")
    cur = con.cursor()

    create_db = """
        create table books (
        isbn                 text primary key,
        ean                  cd publishertext,
        largeimageurl        text,
        largeimagewidth      integer,
        largeimageheight     integer,
        mediumimageurl       text,
        mediumimagewidth     integer,
        mediumimageheight    integer,
        smallimageurl        text,
        smallimagewidth      integer,
        smallimageheight     integer,
        publication_date     text,
        productdescription   text,
        publisher            text,
        releasedate          text,
        authors              text,
        catalog              text,
        binding              text,
        numpages             integer,
        salesrank            integer,
        price                integer,
        title                text,
        year                 integer,
        edition              text,
        default_search       text
    );
        create table users (
        id                   integer primary key autoincrement,
        username             text,
        first_name           text,
        last_name            text,
        email                text,
        password_hash        text,
        street               text,
        city                 text,
        state                text,
        postcode             text,
        verified             text
    );

    create table basket_items (
        user_id              integer references users(id),
        isbn                 text references books(isb),
        num                  integer
    );

    create table orders (
        id                   integer primary key autoincrement,
        user_id              integer references users(id),
        time_stamp           timestamp default current_timestamp,
        cc_num               integer,
        cc_exp               text
    );

    create table order_items (
        order_id             integer references orders(id),
        isbn                 text references books(isbn),
        num                  integer
    );
    """

    cur.executescript(create_db)

    insert_query = """
    insert into books values (:isbn,:ean,:largeimageurl,:largeimagewidth,:largeimageheight,
                            :mediumimageurl,:mediumimagewidth,:mediumimageheight,
                            :smallimageurl, :smallimagewidth,:smallimageheight,
                            :publication_date,:productdescription,:publisher,
                            :releasedate,:authors,:catalog,:binding,:numpages,
                            :salesrank,:price,:title,:year,:edition,:default_search)
    """

    f = open("books.json", 'r')
    books = json.load(f)

    with con:
        for isbn in books:
            authors = books[isbn]['authors']
            books[isbn]['authors'] = ",".join(authors)
            books[isbn]['default_search'] = books[isbn]['title'] + " " + books[isbn]['authors']
            cur.execute(insert_query, defaultdict(default, books[isbn]))