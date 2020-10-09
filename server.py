import markdown
import os
import csv
import re
from flask import Flask, render_template, request, redirect

# def md_to_html(md_text):
#     md_text = md_text.read()
#     html = markdown.markdown(md_text)
#     return html
# for md_txt_filename in os.listdir(r'.\static\assets\texts'):
#     if md_txt_filename.endswith(".md"):
#         with open(f'.\\static\\assets\\texts\\{md_txt_filename}', 'r', encoding='utf-8') as md_file:
#             html_text = md_to_html(md_file)
#             html_txt_filename = md_txt_filename.replace('.md', '.html')
#         with open(f'.\\static\\assets\\texts\\{html_txt_filename}', 'w', encoding='utf-8') as html_file:
#             html_file.write(html_text)
app = Flask(__name__)
page_number = 1
answer = ''
@app.route('/')
def my_home():
    return render_template('intro.html')


@app.route('/<string:current_page>')  # to be removed in production
def page_name(current_page=''):
    return render_template(current_page)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        global page_number
        global answers
        global answer
        try:
            answer = request.form.to_dict()
            print(answer)
            answers[f'{page_number}'] = answer
            final_answer = (eval(f'check{page_number}(answer)'))
            if final_answer:
                return redirect('/full_answer')
            else:
                return render_template('/wrong_answer.html')
        except:
            raise
    else:
        return redirect('try_again')

@app.route('/try_again')
def try_again():
    global page_number
    return render_template(f'Q{page_number}.html')

@app.route('/full_answer')
def full_answer():
    global page_number
    return render_template(f'A{page_number}.html')


@app.route('/nextq')
def nextq():
    global page_number
    page_number = find_page_number()
    if page_number == 10:
        return render_template('colophone.html')
    else:
        page_number += 1
        return render_template(f'Q{page_number}.html')


@app.route('/back')
def back():
    global page_number
    page_number = find_page_number()
    if page_number <= 1:
        return render_template('intro.html')
    else:
        page_number -= 1
        return render_template(f'Q{page_number}.html')

@app.route('/submit_quiz', methods=['POST', 'GET'])
def submit_quiz():
    global answers
    global answer
    if request.method == 'POST':
        answer = request.form.get('answer')
        answers['feedback'] = answer
        return render_template('summary.html', answers=answers)

    else:

        return render_template('summary.html', answers=answers)

@app.route('/Q0.html')
def send_to():
    return render_template(f'intro.html')


def write_to_csv(answer, username):
    with open('database.csv', newline='', mode='a') as database:
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([answer])


def find_page_number():
    page_number = int(request.args.get('page_number'))
    return page_number

def check1(answer):
    local_answer=answer['answer']
    if re.search(r'(כפר שאול)', local_answer):
        return True
    else:
        return False

def check2(answer):
    local_answer = answer['answer']
    if local_answer == 'ניו יורק':
        return True
    else:
        return False

def check3(answer):
    local_answer = answer['answer']
    if local_answer == 'The Wall':
        return True
    else:
        return False

def check4(answer):
    local_answer = answer['answer']
    if local_answer == 'Henry':
        return True
    else:
        return False

def check5(answer):
    local_answer = answer['answer']
    if local_answer == '5':
        return True
    else:
        return False

def check6(answer):
    local_answer = answer['answer']
    if local_answer == 'מסדר הכותל':
        return True
    else:
        return False

def check7(answer):
    local_answer = answer['answer']
    if local_answer == 'בשבעת צבעי הקשת בכניסה לגן הילדים ברחוב':
        return True
    else:
        return False

def check8(answer):
    local_answer = answer['answer']
    if local_answer == 'Berlin':
        return True
    else:
        return False


def check9(answer):
    try:
        local_answer = [answer['answer'], answer['answer2'], answer['answer3']]
        if local_answer == ['Charlemagne', 'Hector', 'King Arthur']:
            return True
        else:
            return False
    except:
        return False

def check10(answer):
    answer = answer['answer']
    if answer == '10':
        return True
    else:
        return False

answers = {}

# in the htmls change all <p> to <p dir="rtl"> to make rtl
# export all answers to a csv/google sheets
# make the summary page presentable
