import markdown
import os
import csv

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
quiz = Flask(__name__)
page_number = 0
right_answers=['0=so empty', 'בית החולים כפר שאול', 'next answer', 'etc']
@quiz.route('/')
def my_home():
    return render_template('intro.html')


@quiz.route('/<string:current_page>')
def page_name(current_page=''):
    return render_template(current_page)


@quiz.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST' and request.form.get('answer') != '':
        global page_number
        global answers
        try:
            answer = request.form.get('answer')
            answers[f'{page_number}'] = answer
            if answer == right_answers[page_number]:
                return redirect('/full_answer')
            else:
                return redirect('/wrong_answer.html')
        except:
            return 'couldnt get that, try again'
    else:
        return redirect('try_again')

@quiz.route('/try_again')
def try_again():
    global page_number
    return render_template(f'Q{page_number}.html')

@quiz.route('/full_answer')
def full_answer():
    global page_number
    return render_template(f'A{page_number}.html')


@quiz.route('/nextq')
def nextq():
    global  page_number
    page_number = find_page_number()
    page_number += 1
    return render_template(f'Q{page_number}.html')


@quiz.route('/back')
def back():
    global page_number
    page_number = find_page_number()
    page_number -= 1
    return render_template(f'Q{page_number}.html')

@quiz.route('/submit_quiz', methods=['POST', 'GET'])
def submit_quiz():
    global answers
    if request.method == 'POST':
        answer = request.form.get('answer')
        answers['feedback'] = answer
        return render_template('summary.html', answers=answers)

    else:
        return render_template('summary.html', answers=answers)

@quiz.route('/Q0.html')
def send_to():
    return render_template(f'intro.html')


def write_to_csv(answer, username):
    with open('database.csv', newline='', mode='a') as database:
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([answer])



def find_page_number():
    page_number = int(request.args.get('page_number'))
    if page_number == 0:
        return render_template('intro.html')
    elif page_number > 10:
        return render_template('colophone.html')
    else:
        return page_number



answers = {}

# implment all q&a in the html templet of q and a
# in the htmls change all <p> to <p dir="rtl"> to make rtl
# get a username
# export all answers to a csv/google sheets
# move nav bar to middle
# get right answers by order into the list and accsess by page num
    # you can use dict with numbers as keys to get multiple possible answers

#treat edge cases (first qustion back and last qustion next)
