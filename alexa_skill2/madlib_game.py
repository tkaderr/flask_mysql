import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app =Flask(__name__)
ask =Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def get_wiki(search):
    # sess.post ('')
    time.sleep(1)
    url= "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&indexpageids=&titles='+search"
    html=sess.get(url)
    data=json.loads(html.content.decode('utf-8'))
    titles=[unidecode.unidecode(listing["data"][])]
    return

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("YesIntent")
def next_round():
    message="Can you give me a name?"
    return statement(message)

@ask.intent("NoIntent")
def next_round():
    message="Okay Bye"
    return statement(message)

@ask.intent("AnswerIntent")
def answer_name(name):
    session.attributes['name']=name
    session.attributes['arr_of_words'] = get_wiki(session.attributes["name"])
    wiki_message=get_wiki(session.attributes["name"])
    message=render_template("name", name=session.attributes['name'], message=wiki_message)
    return question(message)

# @ask.intent("AnswerIntent")
# def keep_asking(answer):
#     session.attributes['name']=answer
#     message=render_template("name",name=session.attributes['name'])
#
#
#
#
# def name_one(name):
#     message="Can you give me a {} ?".format(arr[0])
#     return question(message)
#
# def capture_one(name):
#     session.attributes["first"]=name
#
# def name_two(name):
#     message="Can you give me a {} ?".format(arr[1])
#     return question(message)
#
# def capture_two(name):
#     session.attributes["second"]=name
#
# def name_three(name):
#     message="Can you give me a {} ?".format(arr[2])
#     return question(message)
#
# def capture_three(name):
#     session.attributes["third"]=name
#
# def name_four(name):
#     message="Can you give me a {} ?".format(arr[3])
#     return question(message)
#
# def capture_four(name):
#     session.attributes["fourth"]=name
#
# def name_five(name):
#     message="Can you give me a {} ?".format(arr[4])
#     return question(message)
#
# def capture_five(name):
#     session.attributes["fifth"]=name
#
# def name_sixth(name):
#     message="Can you give me a {} ?".format(arr[5])
#     return question(message)
#
# def capture_sixth(name):
#     session.attributes["sixth"]=name
#
# def name_seventh(name):
#     message="Can you give me a {} ?".format(arr[6])
#     return question(message)
#
# def capture_seventh(name):
#     session.attributes["seventh"]=name
#
# def name_eigth(name):
#     message="Can you give me a {} ?".format(arr[7])
#     return question(message)
#
# def capture_eigth(name):
#     session.attributes["eigth"]=name
#
# def name_ninth(name):
#     message="Can you give me a {} ?".format(arr[8])
#     return question(message)
#
# def capture_ninth(name):
#     session.attributes["ninth"]=name
#
# def name_tenth(name):
#     message="Can you give me a {} ?".format(arr[9])
#     return question(message)
#
# def capture_tenth(name):
#     session.attributes["tenth"]=name
#
# def name_eleventh(name):
#     message="Can you give me a {} ?".format(arr[10])
#     return question(message)
#
# def capture_eleventh(name):
#     session.attributes["eleventh"]=name
#
# def name_twelth(name):
#     message="Can you give me a {} ?".format(arr[11])
#     return question(message)
#
# def capture_twelth(name):
#     session.attributes["twelth"]=name
#
#
#
#
#
#
# #
# #     for i in range(0,len(arr)):
# #         message="Can you give me a {} ?".format(arr[i])
# #     name_message=render_template('name',name = name)
# #     return statement(name_message)
# #
# #
# #
# #
# # for i in range(0,len(arr)):
# #     message="Can you give me a {} ?".format(arr[i])
# #     return question(message)
# #
# # @ask.intent("AnswerIntent")
# # def word(word):
# #     arr.append(word)
