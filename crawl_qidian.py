import requests
from bs4 import BeautifulSoup
import os
import json
import re
from fontTools.ttLib import TTFont
from basic_functions import *

def get_pages_qidian():
    ''' a function that gets the page urls

    This function gets the urls of the main pages which list the books

    Parameters
    ----------
    None   

    Returns
    -------
    pages_qidian: list
        a list of main page urls
    '''

    page_url1 = 'https://www.qidian.com/finish?action=hidden&orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=2&page=1'
    page_url2 = 'https://www.qidian.com/finish?action=hidden&orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=2&page=2'
    pages_qidian = [page_url1, page_url2]
    return pages_qidian
    
def get_books_qidian(page_url):
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
    book_list_parent = soup.find('tbody')
    ## loop through the child divs
    book_listing = book_list_parent.find_all('tr', recursive=False)

    count = 0
    booklist = []
    for book in book_listing:
        ### extract book details url
        temp = book.find_all('td')[1]
        book_header = temp.find('a').text
        book_href  = temp.find('a')['href']
        book_href = 'https:' + book_href
        count += 1
        if count % 10 == 0:
            print(f'Now retrieving book {count}')
        book = get_bookdetail_qidian(book_href)
        booklist.append(book)
        if count == 50:
            break
    return booklist

def number_transfer_qidian(response):
    ''' a function that transfers the unreadable number to readable  

    Parameters
    ----------
    response: string
        the original response retrivied   

    Returns
    -------
    html_page: string
        the transfered page content
    '''

    font_url = re.findall("; src: url\('(.*?)'\) format", response.text)[1]
    headers = {'User-Agent': 'UMSI 507 Course Project',
                  'From': 'yuanfenw@umich.edu',
                  'Course-Info': 'https://www.si.umich.edu/programs/courses/507'}
    font_response = requests.get(font_url, headers=headers)
    with open('font.woff', mode='wb') as f:
        f.write(font_response.content)
    fi = TTFont('font.woff')
    font_map = fi['cmap'].getBestCmap()
    dic = {'zero':'0', 'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','period':'.'}
    for key in font_map:
        font_map[key] = dic[font_map[key]]
    html_page = response.text
    for key in font_map:
        html_page = html_page.replace(f'&#{key};', font_map[key])
    return html_page

def get_bookdetail_qidian(book_url):
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
        html_page = number_transfer_qidian(response)
        cache_save('cache.json', book_url, html_page)
    ## extract book details
    soup_detail = BeautifulSoup(html_page, 'html.parser')
    book_info = soup_detail.find('div', class_='book-info')
    book_name = book_info.find('h1').find('em').text.strip()
    book_label = book_info.find('p', class_='tag').find_all('a')[0].text.strip()
    temp = (book_info.find_all('p')[2]).find_all('span')
    book_size = temp[0].text
    book_like = temp[1].text + '万'
    book_description = soup_detail.find('div', class_='book-intro').find('p').text.strip()
    book_date = soup_detail.find('em', class_='time').text
    book = Book(book_label, book_name, book_size, book_description, book_date, book_like, book_url)
    return book

