from database import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    ''' a function that processes welcome page

    Parameters
    ----------
    None 

    Returns
    -------
    render the template
    '''

    return render_template('welcome.html')

@app.route('/book_search', methods=['POST'])
def book_search():
    ''' a function that processes booksearch page

    Parameters
    ----------
    None 

    Returns
    -------
    render the template
    '''
    if request.form['category'] != '':
        category = request.form['category']
    else:
        category = 'no category'
    if request.form['sizebottom'] != '':
        sizebottom = request.form['sizebottom']
    else:
        sizebottom = '0'
    if request.form['sizetop'] != '':
        sizetop = request.form['sizetop']
    else:
        sizetop = '2000'

    filters = [category, sizebottom, sizetop]
    status = 0
    if sizebottom.isnumeric() and sizetop.isnumeric() and float(sizetop)>=float(sizebottom):
        pass
    else:
        status = 1
        return render_template('booksearch_result.html', filters=filters, status=status)
    books = search(category, sizebottom, sizetop)
    if len(books) == 0:
        status = 2
    for i in range(len(books)):
        books[i] = list(books[i])
        books[i].append(i+1) 
    return render_template('booksearch_result.html', filters=filters, books=books, status=status)

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    ''' a function that processes retrived data from welcome page form

    Parameters
    ----------
    None 

    Returns
    -------
    render the template
    '''

    user_option = request.form['searchorreview']
    if user_option == 'search':
        return render_template('booksearch.html')
    else:
        trend = request.form['trends']
        if trend == 'trends1':
            result, category_dict = trends1()
            category_status = [list(category_dict['qidian'].keys()),
                              list(category_dict['qidian'].values()),
                              list(category_dict['zongheng'].keys()),
                              list(category_dict['zongheng'].values()),
                              list(category_dict['youdu'].keys()),
                              list(category_dict['youdu'].values())]
            return render_template('trends_result.html', trend=trend, result=result, category_status=category_status)
        elif trend == 'trends2':
            return render_template('timeselect.html', trend=trend)
        else:
            infos = trends3()
            return render_template('trends_result.html', trend=trend, infos=infos)

@app.route('/trends2', methods=['POST'])
def trends2_process():
    ''' a function that processes retrived data from timeselect page

    Parameters
    ----------
    None 

    Returns
    -------
    render the template
    '''

    timebottom = request.form['timebottom']
    timetop = request.form['timetop']
    timescale = request.form['timescale']
    result = trends2(timebottom, timetop)
    source, num_category = trends2_distribution(timescale, result, timebottom, timetop)

    return render_template('trends_result.html', trend='trends2', source=source, num_category=num_category)

def search(category='no category', sizebottom='0', sizetop='2000'):
    ''' a function that helps user to search books

    Parameters
    ----------
    category: string
        The category of the book
    sizebottom: string
        The minimum size of the book (:万字)
    sizetop: string
        The maximum size of the book (:万字)

    Returns
    -------
    result: list
        a list of tuple with the retrived book infos
    '''

    dir = r'C:\\Users\\wyfdr\\Desktop\\graduatestudy\\SI507\\HW\\FINAL\\final.sqlite'
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    if sizebottom.isnumeric() and sizetop.isnumeric and float(sizetop)>=float(sizebottom):
        query = f'''
            SELECT namelist.Name, infos."Size(万)", Category, Date, Like, Source, Url, Description
            FROM infos
            JOIN namelist
                ON namelist.Id=infos.Id
            Where "Size(万)" >= {float(sizebottom)} AND "Size(万)" <= {float(sizetop)}
        '''
        if category != 'no category':
            query += f' AND Category LIKE "%{category}%"'

    result = cursor.execute(query).fetchall()
    return result

def trends1():
    ''' a function that helps user to review trend1

    Parameters
    ----------
    None

    Returns
    -------
    result: list
        a list of tuple with the retrived book infos
    category_dict: dict
        a dict contains the type distributions ({website:{type: count}}) 
    '''

    dir = r'C:\\Users\\wyfdr\\Desktop\\graduatestudy\\SI507\\HW\\FINAL\\final.sqlite'
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    website = ['qidian', 'zongheng', 'youdu']
    result = []
    category_dict = {}
    for w in website:
        query = f'''
            SELECT namelist.Name, infos."Size(万)", Category, Date, Like, Source, Url
            FROM infos
            JOIN namelist
                ON namelist.Id=infos.Id
            WHERE Source = '{w}'
            ORDER BY Like DESC
            LIMIT 20
        '''
        res = cursor.execute(query).fetchall()
        result += res  # Here we get the top20 books' infos
        category_dict[w] = {}
        for book in res:
            category = book[2]
            if category not in category_dict[w]:
                category_dict[w][category] = 1
            else:
                category_dict[w][category] += 1
    return result, category_dict

def trends2(timebottom, timetop):
    ''' a function that search the books within the specified time zone

    Parameters
    ----------
    timebottom: string
        the bottom of the time zone (e.g. 2014-02)
    timetop: string
        the top of the time zone (e.g. 2014-02)   

    Returns
    -------
    result: list
        a list of tuple with the retrived book infos
    '''

    dir = r'C:\\Users\\wyfdr\\Desktop\\graduatestudy\\SI507\\HW\\FINAL\\final.sqlite'
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    query = f'''
        SELECT Category, Date
        FROM infos
        Where "Date" >= "{timebottom}" AND "Date" <= "{timetop}" AND Source="qidian"
        ORDER BY Date ASC
    '''
    result = cursor.execute(query).fetchall()
    return result

def trends2_distribution(timescale, result, timebottom, timetop):
    ''' a function that processes the infos to get trends2 result

    Parameters
    ----------
    timescale: string
        the option that user wants to see the results in year/quarter/month
    result: list
        a list of tuple with the retrived book infos
    timebottom: string
        the bottom of the time zone (e.g. 2014-02)
    timetop: string
        the top of the time zone (e.g. 2014-02)   

    Returns
    -------
    source: list
        a list of list contains the data to present
    num_category: int
        the count of category
    '''

    result = [[r[0],r[1][:7]] for r in result]
    yeardif = int(timetop.split('-')[0]) - int(timebottom.split('-')[0])
    monthdif = int(timetop.split('-')[1]) - int(timebottom.split('-')[1])
    timezone = yeardif * 12 + monthdif
    distribution = {}
    # timescale = 'quarter'
    if timescale == 'year':
        for book in result:
            category = book[0]
            year = book[1].split('-')[0]
            if year not in distribution:
                distribution[year] = {category: 1}
            else:
                if category not in distribution[year]:
                    distribution[year][category] = 1
                else:
                    distribution[year][category] += 1
    elif timescale == 'month':
        for book in result:
            category = book[0]
            month = book[1]
            if month not in distribution:
                distribution[month] = {category: 1}
            else:
                if category not in distribution[month]:
                    distribution[month][category] = 1
                else:
                    distribution[month][category] += 1
    elif timescale == 'quarter':
        for book in result:
            category = book[0]
            year = book[1].split('-')[0]
            month = book[1].split('-')[1]
            quarter = ((int(month)-1)//3)+1
            key = f'{year}-q{quarter}'
            if key not in distribution:
                distribution[key] = {category: 1}
            else:
                if category not in distribution[key]:
                    distribution[key][category] = 1
                else:
                    distribution[key][category] += 1
    
    category = list(set([r[0] for r in result]))
    source = []
    for i in distribution:
        temp = distribution[i]
        row = [i]
        for c in category:
            if c not in temp:
                row.append(0)
            else:
                row.append(temp[c])
        source.append(row)
    row1 = ['time'] + category
    source = [row1] + source
    num_category = len(category)
    return source, num_category

def trends3():
    ''' a function that processes the infos to get trends3 result

    Parameters
    ----------
    None   

    Returns
    -------
    infos: list
        a list of list contains the label and data to present
    '''
    dir = r'C:\\Users\\wyfdr\\Desktop\\graduatestudy\\SI507\\HW\\FINAL\\final.sqlite'
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    query = '''
        SELECT Category, AVG(infos."Size(万)")
        FROM infos
        WHERE Source="zongheng"
        GROUP BY Category
    '''
    result_zongheng = cursor.execute(query).fetchall()
    x_z = [r[0] for r in result_zongheng]
    y_z = ['{0:.1f}'.format(r[1]) for r in result_zongheng]
    query = '''
        SELECT Category, AVG(infos."Size(万)")
        FROM infos
        WHERE Source="qidian"
        GROUP BY Category
    '''
    result_qidian = cursor.execute(query).fetchall()
    x_q = [r[0] for r in result_qidian]
    y_q = ['{0:.1f}'.format(r[1]) for r in result_qidian]

    query = '''
        SELECT Category, AVG(infos."Size(万)")
        FROM infos
        WHERE Source="youdu"
        GROUP BY Category
        HAVING COUNT(*) > 2
    '''
    result_youdu = cursor.execute(query).fetchall()
    x_y = [r[0] for r in result_youdu]
    y_y = ['{0:.1f}'.format(r[1]) for r in result_youdu]
    infos = [x_z, y_z, x_q, y_q, x_y, y_y]
    return infos

if __name__ == "__main__":
    # dir = 'final.sqlite'
    # create_database(dir)

    # insert(dir, "qidian")
    # print('create_database qidian done')
    # insert(dir, "zongheng")
    # print('create_database zongheng done')
    # insert(dir, "youdu")
    # print('create_database youdu done')
    # print('done')

    print('starting Flask app', app.name)  
    app.run(debug=True)

