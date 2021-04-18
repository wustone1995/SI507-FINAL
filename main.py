from database import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    user_option = request.form['searchorreview']
    if user_option == 'search':
        return render_template('booksearch.html', result_flag=0)
    else:
        return render_template('trendreview.html', result_flag=0)

@app.route('/book_search', methods=['POST'])
def book_search():
    category = request.form['category']
    size_bottom = request.form['sizebottom']
    size_top = request.form['sizetop']
    conn = sqlite3.connect('final.sqlite')
    cursor = conn.cursor()
    result = []
    query = f'''
        SELECT Name, Size, Category, Date, Like, Description, Url
        From qidian
        WHERE (Category={category} AND Size <= {size_top} AND Size >= {size_bottom})
    '''
    res = cursor.execute(query)
    result += [list(r) for r in res]

    query = f'''
        SELECT Name, Size, Category, Date, Like, Description, Url
        From zongheng
        WHERE (Category={category} AND Size <= {size_top} AND Size >= {size_bottom})
    '''
    res = cursor.execute(query)
    result += [list(r) for r in res]

    query = f'''
        SELECT Name, Size, Category, Date, Like, Description, Url
        From youdu
        WHERE (Category={category} AND Size <= {size_top} AND Size >= {size_bottom})
    '''
    res = cursor.execute(query)
    result += [list(r) for r in res]
    





    return render_template('booksearch_result.html', result_flag = 1)

if __name__ == "__main__":
    print('starting Flask app', app.name)  
    app.run(debug=True)
    # main()
    # dir = r'C:\\Users\\wyfdr\\Desktop\\graduatestudy\\SI507\\HW\\FINAL\\final.sqlite'
    # conn = sqlite3.connect(dir)
    # cursor = conn.cursor()
    # catrgory = []
    # query = '''
    #     SELECT DISTINCT Category
    #     FROM qidian
    # '''
    # res = cursor.execute(query).fetchall()
    # for r in res:
    #     catrgory.append(r[0])
    # query = '''
    #     SELECT DISTINCT Category
    #     FROM zongheng
    # '''
    # res = cursor.execute(query).fetchall()
    # for r in res:
    #     catrgory.append(r[0])
    # query = '''
    #     SELECT DISTINCT Category
    #     FROM youdu
    # '''
    # res = cursor.execute(query).fetchall()
    # for r in res:
    #     catrgory.append(r[0])
    # for c in catrgory:
    #     print(c)

    # filter = input('please input query (e.g. size 100 or type 都市)')
    # filter_head = filter[:4]
    # filter_condition = filter[5:]
    # print(filter_condition)
    # if filter_head == 'size':
    #     query = f'''
    #         SELECT Name
    #         FROM "qidian"
    #         where Size >= {filter_condition}
    #     '''
    # elif filter_head == 'type':
    #     query = f'''
    #         SELECT Name
    #         FROM "qidian"
    #         where Category = "{filter_condition}"
    #     '''
    # else:
    #     print("Please check your input")

    # result = cursor.execute(query).fetchall()
    # conn.close()
    # for row in result:
    #     print(str(row[0]))

