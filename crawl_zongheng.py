import requests
from bs4 import BeautifulSoup
import os
import json
import datetime
import time
from basic_functions import *

def get_pages_zongheng():
    # if cache_file is None:
    #     print('Fetching')
    #     ## Make the soup of zongheng
    #     pages_zongheng = {}
    #     for i in range(1,7):
    #         page_url = f'http://book.zongheng.com/store/c0/c0/b0/u0/p{i}/v9/s1/t0/u0/i0/ALL.html'
    #         headers = {'User-Agent': 'UMSI 507 Course Project',
    #                 'From': 'yuanfenw@umich.edu',
    #                 'Course-Info': 'https://www.si.umich.edu/programs/courses/507'} 
    #         response = requests.get(page_url, headers=headers)
    #         pages_zongheng[page_url] = response.text
    #     cache_save('cache.json', 'pages_zongheng', pages_zongheng)
    #     return pages_zongheng
    # else:
    #     print('Using cache')
    #     if not os.path.exists(cache_file):
    #         print("[ERROR] Please check the cache file.")
    #     else:
    #         cache = cache_read(cache_file)
    #         pages_zongheng = cache['pages_zongheng']
    #         return pages_zongheng
    pages_zongheng = []
    for i in range(1,7):
        page_url = f'http://book.zongheng.com/store/c0/c0/b0/u0/p{i}/v9/s1/t0/u0/i0/ALL.html'
        pages_zongheng.append(page_url)
    return pages_zongheng

def get_books_zongheng(page_url):
    cache_flag = 0
    if os.path.exists('cache.json'):
        cache = cache_read()
        if page_url in cache:
            print("Using cache")
            page_info = cache[page_url]
            cache_flag = 1
    if cache_flag == 0:
        print('Fetching')
        headers = {'User-Agent': 'UMSI 507 Course Project',
                  'From': 'yuanfenw@umich.edu',
                  'Course-Info': 'https://www.si.umich.edu/programs/courses/507'}
        response = requests.get(page_url, headers=headers)
        page_info = response.text
        cache_save('cache.json', page_url, page_info)
    
    soup = BeautifulSoup(page_info, 'html.parser')
    # Get the book_list_parent
    book_list_parent = soup.find('ul', class_='main_con')
    ## loop through the child divs
    book_listing = book_list_parent.find_all('li', recursive=False)

    count = 0
    booklist = []
    for book in book_listing:
        ### extract book details url
        temp = book.find('span', class_='bookname').find('a')
        book_header = temp.text
        book_href  = temp['href']
        book = get_bookdetail_zongheng(book_href)
        booklist.append(book)
        count += 1
        if count % 10 == 0:
            print(f'Now retrieving book {count}')
        if count == 50:
            break
        # break
    return booklist


def cal_date(update_date, current_date):
    if update_date[-1] != '前':
        return update_date
    else:
        timeArray = time.strptime(current_date, "%Y-%m-%d")
        timestamp = time.mktime(timeArray)
        if update_date[-2] == '月':
            diff = int(update_date[:-3]) * 30 * 24 * 3600
        elif update_date[-2] == '时':
            diff = int(update_date[:-3]) * 3600
        elif update_date[-2] == '周':
            diff = int(update_date[:-2]) * 7 * 24 * 3600
        elif update_date[-2] == '天':
            diff = int(update_date[:-2]) * 24 * 3600
        timestamp -= diff
        time_local = time.localtime(timestamp)
        res = time.strftime("%Y-%m-%d",time_local)
        return res

def get_bookdetail_zongheng(book_url):
    cache_flag = 0
    if os.path.exists('cache.json'):
        cache = cache_read()
        if book_url in cache:
            print("Using cache")
            html_page = cache[book_url]
            cache_flag = 1
    if cache_flag == 0:
        print("Fetching")
        headers = {'User-Agent': 'UMSI 507 Course Project',
                    'From': 'yuanfenw@umich.edu',
                    'Course-Info': 'https://www.si.umich.edu/programs/courses/507'}
        response = requests.get(book_url, headers=headers)
        html_page = response.text
        cache_save('cache.json', book_url, html_page)
    ## extract book details
    soup_detail = BeautifulSoup(html_page, 'html.parser')
    book_info = soup_detail.find('div', class_='book-info')
    book_name = book_info.find('div', class_='book-name').text.strip()
    book_label = book_info.find('div', class_='book-label').find_all('a')[1].text.strip()
    temp = book_info.find('div', class_='nums').find_all('span')
    book_size = temp[0].find('i').text.strip()[:-1]
    book_like = temp[1].find('i').text
    book_description = soup_detail.find('div', class_='book-dec Jbook-dec hide').find('p').text.strip()
    book_date = soup_detail.find('div', class_='time').text.strip().split()[1]
    current_date = datetime.datetime.now()
    current_date = str(current_date).split()[0]
    book_date = cal_date(book_date, current_date)
    book = Book(book_label, book_name, book_size, book_description, book_date, book_like, book_url)
    return book

# pages_zongheng = get_pages_zongheng()
# count = 0
# for i in pages_zongheng:
#     if count == 0:
#         count = 1
#         continue
#     url = i
#     book = get_books_zongheng(url)
#     for i in book:
#         print(i.info())
#     break