import sqlite3
from crawl_qidian import *
from crawl_youdu import *
from crawl_zongheng import *

def get_all_books(website):
    if website == 'qidian':
        pages = get_pages_qidian()
    if website == 'zongheng':
        pages = get_pages_zongheng()
    if website == 'youdu':
        pages = get_pages_youdu()
    print(f'Now retrieving {website}')
    print('*' * 50)
    books_all = []
    page_index = 1
    for page_url in pages:
        print(f'Retrieving {website} page {page_index}')
        page_index += 1
        if website == 'qidian':
            booklist = get_books_qidian(page_url)
        if website == 'zongheng':
            booklist = get_books_zongheng(page_url)
        if website == 'youdu':
            booklist = get_books_youdu(page_url)
        books_all += booklist
    return books_all

def create_database(dir):
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    drop_namelist = '''
        DROP TABLE IF EXISTS namelist;
    '''
    create_namelist = '''
        CREATE TABLE IF NOT EXISTS namelist(
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "Name" TEXT NOT NULL
        );
    '''
    cursor.execute(drop_namelist)
    cursor.execute(create_namelist)
    conn.commit()

    drop_infos = '''
        DROP TABLE IF EXISTS infos;
    '''
    create_infos = '''
        CREATE TABLE IF NOT EXISTS infos(
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "Size(万)" DOUBLE NOT NULL,
            "Category" TEXT NOT NULL,
            "Date" VARCHAR(8000),
            "Like" INTEGER NOT NULL,
            "Description" TEXT NOT NULL,
            "Url" TEXT NOT NULL,
            "Source" TEXT NOT NULL
        );
    '''
    cursor.execute(drop_infos)
    cursor.execute(create_infos)        
    conn.commit()

# def insert(dir, website):
#     conn = sqlite3.connect(dir)
#     cursor = conn.cursor()
#     books_all = get_all_books(website)
#     for b in books_all:
#         insert = f'''
#             INSERT INTO {website}
#             VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
#         '''
#         if b.like[-1] == '万':
#             blike = float(b.like[:-1])*10000
#         else:
#             blike = float(b.like)
#         bsize = float(b.size[:-1])
#         book_info = [b.name, bsize, b.category, b.date, blike, b.description, b.url]
#         cursor.execute(insert, book_info)
#         conn.commit()
def insert(dir, website):
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    books_all = get_all_books(website)
    for b in books_all:
        insert = '''
            INSERT INTO namelist
            VALUES (NULL, ?)
        '''
        if b.like[-1] == '万':
            blike = float(b.like[:-1])*10000
        else:
            blike = float(b.like)
        bsize = float(b.size[:-1])
        book_name = [b.name]
        book_info = [bsize, b.category, b.date, blike, b.description, b.url, website]
        cursor.execute(insert, book_name)
        conn.commit()

        insert = '''
            INSERT INTO infos
            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(insert, book_info)
        conn.commit()


if __name__ == "__main__":
    dir = r'C:\\Users\\wyfdr\\Desktop\\graduatestudy\\SI507\\HW\\FINAL\\final.sqlite'
    create_database(dir)
    insert(dir, "qidian")
    print('create_database qidian done')
    # create_database(dir,"zongheng")
    insert(dir, "zongheng")
    print('create_database zongheng done')
    # create_database(dir,"youdu")
    insert(dir, "youdu")
    print('create_database youdu done')
    print('done')