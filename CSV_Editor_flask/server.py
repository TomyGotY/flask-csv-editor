#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Friday Nov 21 18:38:58 2020
Please keep my name
@author: shuxin.jin@hotmail.com
"""

from flask import Flask, render_template, redirect, request, session
import csv
import uuid
import os


app = Flask(__name__)
#news label definatin, CSV fields.
label_news_like=["storytitles", "userstory", "acceptance", "business", "estimation", "status"]
def generate_id():
    new_id = uuid.uuid4()
    return str(new_id)


def read_csv():
    stories = []
    with open("stories.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #remove the blank row
            if  len(row):
                stories.append(row)
            else:
                pass
    csvfile.close()
    return stories


def append_csv(story):
    with open("stories.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(story)

    csvfile.close()

def write_csv(stories):
    with open("stories.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for story in stories:
            #remove the blank row
            if  len(story):
                writer.writerow(story)
            else:
                pass
    csvfile.close()

def edit_csv(stories, new_story):
    with open("stories.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for story in stories:
            if not len(story):
                pass
            else:
                if story[0] == new_story[0]:
                    writer.writerow(new_story)
                    continue
                writer.writerow(story)
    csvfile.close()

@app.route('/')
def route_index():
    stories = read_csv()
    return render_template('index.html', stories=stories)


@app.route('/story')
def route_new_story():
    stories = read_csv()
    return render_template('story.html', action="/save_story")


@app.route('/save_story', methods=["POST"])
def route_save_story():
    list_label = label_news_like
    story = []
    story.insert(0, generate_id())
    for input_name in list_label:
        story.append(request.form[input_name])
    append_csv(story)
    return redirect("/")


@app.route('/story/<post_id>')
def route_edit_story(post_id):
    stories = read_csv()
    for row in stories:
        if len(row):
            if row[0] == post_id:
                return render_template("story.html", row=row)
        else:
            pass
    return redirect("/")

@app.route("/save_edited_story/<post_id>", methods=["POST"])
def route_save_edited_story(post_id):
    list_label = label_news_like
    edited_story = []
    edited_story.insert(0, post_id)
    for input_name in list_label:
        edited_story.append(request.form[input_name])
    stories = read_csv()
    edit_csv(stories, edited_story)
    return redirect("/")


@app.route('/delete/<post_id>')
def route_delete_story(post_id):
    stories = read_csv()
    index = 0
    try:
        for row in stories:
            if row[0] == post_id:
                popindex = index
                stories.pop(popindex)
                write_csv(stories)
                return redirect("/")
    
            index += 1
            print('row index:'+str(index))
    except Exception as e:
        print(str(e))
        return redirect("/")
    return redirect("/")


if __name__ == "__main__":
    app.secret_key = 'asdadd'
    app.run(
        debug=False,  # Allow verbose error reports
        port=5000  # Set custom port
    )
