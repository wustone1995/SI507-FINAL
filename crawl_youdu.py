import requests
from bs4 import BeautifulSoup
import os
import json
from basic_functions import *

def get_pages_youdu():
    ''' a function that gets the page urls

    This function gets the urls of the main pages which list the books

    Parameters
    ----------
    None   

    Returns
    -------
    pages_youdu: list
        a list of main page urls
    '''

    baseurl = "https://www.youdubook.com"
    listurl = '/booklibrary/index/str/0_0_0_0_0_2_0'
    url = baseurl + listurl
    pages_youdu = []
    for i in range(1,9):    # there are page 1-8
        page_url = url + '?page=' + str(i)
        pages_youdu.append(page_url) 
    return pages_youdu
    
def get_books_youdu(page_url):
    ''' a function that gets the books' infos on one main page

    Parameters
    ----------
    page_url: string
        the url of the main page   

    Returns
    -------
    booklist: list
        a list of the retrived book
    '''

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
    book_list_parent = soup.find('div', class_='BooklibraryList').find('ul')
    ## loop through the child divs
    book_listing = book_list_parent.find_all('li', recursive=False)

    count = 0
    flag = 0
    booklist = []
    for book in book_listing:
    ### extract book details url
        if flag == 1:
            flag = 0
            count += 1
            if count % 10 == 0:
                print(f'Now retrieving book {count}')
            if count == 32:
                break
            continue
        flag = 1
        temp = book.find('span', recursive=False)
        book_header = temp.find('a').text
        book_href  = temp.find('a')['href']
        book = get_bookdetail_youdu(book_href)
        booklist.append(book)
    return booklist

def get_bookdetail_youdu(book_url):
    ''' a function that gets the book infos  

    Parameters
    ----------
    book_url: string
        the url of the book page  

    Returns
    -------
    book: Book
        a book instance with retrived infos
    '''

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

    soup_detail = BeautifulSoup(html_page, 'html.parser')
    ## extract book details
    book_label_temp = soup_detail.find('div', class_='label').find('ul').find_all('li', class_='')
    if len(book_label_temp) == 0:
        book_label = 'No category'
    else:
        book_label = book_label_temp[0].text
    book_size = soup_detail.find('div', class_='Font').find_all('span')[0].text
    book_description = soup_detail.find('div', class_='synopsisCon').text.strip()
    book_title = soup_detail.find('div', class_='title')
    book_name = book_title.find('span').text.strip()
    book_date = book_title.find('i').text.split(' ')[0][-10:]
    book_like = soup_detail.find('li', class_='TouRecommendedVotes').text
    book_like = book_like.split('票')[1]
    book = Book(book_label, book_name, book_size, book_description, book_date, book_like, book_url)
    return book

