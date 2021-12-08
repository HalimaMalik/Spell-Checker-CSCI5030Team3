from collections import Counter
import nltk;
from nltk.tokenize import word_tokenize
import os
import re

from textblob import TextBlob

from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

def irish_file_read(): # Irish File Reading
    file = open("frequent_irish_3500.txt", encoding="utf8").read() # Edit Filename
    tokens = word_tokenize(file)
    tokens_words = [word for word in tokens if word.isalnum()]
    vocab = Counter(tokens_words)
    return vocab

def english_file_read(): # English File Reading
    file = open("frequent_english_3000.txt", encoding="utf8").read() # Edit Filename
    tokens = word_tokenize(file)
    tokens_words = [word for word in tokens if word.isalnum()]
    vocab = Counter(tokens_words)
    return vocab
    
def detect_language(text): # Detecting Language on backend
    text_language = TextBlob(text)
    language = text_language.detect_language()
    return language
    
def english_word_suggestions(word): # Main function to give suggestions for English
    english_term_list = english_file_read()
    english_suggestions = {}
    if (word.isalnum() == False):
         return word
    elif(word in english_term_list):   
        return ""
    else:
        if (len(word)<=4):
            for key,value in english_term_list.items():
                edit = nltk.edit_distance(word, key)
                if (edit == 1):
                    english_suggestions[key] = value
            top_five = Counter(english_suggestions) 
            return [key for key,values in top_five.most_common(5)] 
        else:
            if (5<=len(word)<=12):
                for key,value in english_term_list.items():
                    edit = nltk.edit_distance(word, key)
                    if (edit == 1 or edit == 2):
                        english_suggestions[key] = value
                top_five = Counter(english_suggestions) 
                return [key for key,values in top_five.most_common(5)]
                
def irish_word_suggestions(word): # Main function to give suggestions for Irish
    irish_term_list = irish_file_read()
    irish_suggestions = {}
    if (word.isalnum() == False):
         return word
    else:    
        if (len(word)<=4):
            for key,value in irish_term_list.items():
                edit = nltk.edit_distance(word, key)
                if (edit == 1):
                    irish_suggestions[key] = value
            top_five = Counter(irish_suggestions) 
            return [key for key,values in top_five.most_common(5)]
        else:
            if (5<=len(word)<=12):
                for key,value in irish_term_list.items():
                    edit = nltk.edit_distance(word, key)
                    if (edit == 1 or edit == 2):
                         irish_suggestions[key] = value
                top_five = Counter(irish_suggestions) 
                return [key for key,values in top_five.most_common(5)]
    
def spellCheck(text,languagetowrite): # Main function
    suggestions=[]
    language = languagetowrite
    words = text.split()
    if (language == "English"):
        for i in words:
            word= i + ":"
            e = english_word_suggestions(i)
            if(e!=""):
                x= ','.join([str(element) for element in e])
                word=word + x + "\n"
                suggestions.append(word) #appending suggestion if there are more than a single word          
        return suggestions
    else:
        for i in words:            
            word= i + ":"
            e=irish_word_suggestions(i)  # appending suggestion if there are more than a single word 
            if(e!=""):           
                x= ','.join([str(element) for element in e])            
                word=word + x + "\n"
                suggestions.append(word)
        return suggestions

@app.route('/', methods=['POST'])
def check():
    if request.method == 'POST':
        p=request.form.getlist('word') # getting wordlist from front end
        languagetowrite=request.form.get('language')
        textoutput = spellCheck(p[0],languagetowrite)# send wordlist to function
        listToStr = ''.join([str(element) for element in textoutput])
        return listToStr
    

@app.route('/')
def index():
    return render_template("team03.html")

if __name__ == '__main__':
    app.run()
