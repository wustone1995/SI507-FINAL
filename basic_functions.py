import json
import os

def cache_read():
    ''' Function that reads the cache file

    Parameters
    ----------
    None

    Returns
    -------
    cache: dict
        The cache file.
    '''
    cache_file = 'cache.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(fp=f)
            f.close()
    else:
        cache = {}
    return cache

def cache_save(cache_file=None, key=None, data=None):
    ''' Function that saves the cache file

    Parameters
    ----------
    cache_file: string
        The path of the cache_file to be saved.
    key: string
        The key of the saving data.
    data: string
        The content of the saving data.

    Returns
    -------
        None
    '''
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(fp=f)
            f.close()
        cache[key] = data
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
            f.close()
    else:
        cache = {}
        cache[key] = data
        with open('cache.json', 'w') as f:
            json.dump(cache, f)
            f.close()

class Book:
    '''a book

    Instance Attributes
    -------------------
    category: string
        the category of a book 
    
    name: string
        the name of a book

    size: string
        the number of the book size(e.g. 100) before unit '万字'

    description: string
        the description of a book

    date: string
        the date of the books' completed day

    like: string
        the number of people who vote like of the book
    
    url: string
        the url to book's webpage
    '''
    def __init__(self, category='no category', name='no name', size='0', description='no description', date='no date', like='0', url='no url'):
        self.category = category
        self.name = name
        self.size = size
        self.description = description
        self.date = date 
        self.like = like
        self.url = url

    def info(self):
        ''' returns a string of the book's information

        Parameters
        ----------
        None

        Returns
        -------
        str: string
            The format is <name> (<category>): <size>万字 <date> <like> like
        '''
        str = f'{self.name} ({self.category}): {self.size}万字 {self.date} {self.like} like'
        return str
