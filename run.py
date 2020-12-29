# General imports
import os
from datetime import datetime, timedelta, date
import subprocess
import re

# App specific imports
import markdown
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_misaka import Misaka


def createMarkdown(fileName):
    docxPath = "data/docx/" + fileName + ".docx"
    mdPath = "data/markdown/" + fileName + ".md"
    #print(docxPath)
    subprocess.check_call("./convertPandoc.sh %s %s" % (docxPath, mdPath), shell=True)
    return mdPath

# Gets rid of a few pandoc conventions that don't render with Misaka
def formatMarkdown(data):
    data = data.replace("{.underline}", "")
    data = data.replace("\\'", "'")
    return data

# Moved the function that writes to the .txt file here so it'll be easier to switch to an email
def sendFeedback(request):
    __rank = request.form["rank"]
    __name = request.form["name"]
    __email = request.form["email"]
    __feedback = request.form["feedback"]
    __emailRegex = re.compile(r'\w+.\w.\w+@uscga.edu')
    if __emailRegex.search(__email):
        now = datetime.now()
        dateText = now.strftime("%m/%d/%Y, %H:%M:%S")
        f = open("data/feedback.txt", "a")
        f.write(dateText + "\t")
        f.write(__rank + " ")
        f.write(__name + "\t")
        f.write(__email + "\n")
        f.write(__feedback + "\n\n")
        f.close()
        return True
    return False

    ## When we update the thisWeek.txt, it has to be done after the new docx file is added to the docx directory
    ## Update, thisWeek.txt updates itself. A basic error message will be flashed if the POD is not added for the day requested in /today

    ## For updating a preexisting POD, we need to first delete the markdown file with it, then update the .docx file w/ the same name. That should be it.




# Declare Flask object
app = Flask(__name__)
Misaka(app)

# Arbitrary, not used
app.secret_key = 'Made by Joram Stith'

# Sets default directory to today page
@app.route("/")
def home():
    return redirect(url_for("today"))

# Main page, displays the current day's POD
@app.route("/today/")
def today():
    current = date.today()
    fileName = current.strftime("%d%B%Y")
    #print("running today")
    #print(fileName)
    #fileName = '06June2020'
    if( os.path.isfile("data/markdown/" + fileName + ".md")):
        filePath = "data/markdown/" + fileName + ".md"
    elif( os.path.isfile("data/docx/" + fileName + ".docx")):
        filePath = createMarkdown(fileName)
    else:
        filePath = ""
    if 'data' in filePath:
        f = open(filePath)
        data = f.read()
        f.close()
        data = formatMarkdown(data)
        return render_template("today.html", data=data)
    else:
        dataStr = "POD not yet posted for " + fileName + "."
    return render_template("today.html", data=dataStr)

# List page, displays the week's PODs and has a search function
@app.route("/list/", methods=["POST", "GET"])
def listPage():
    if request.method == "POST":
        fileName = request.form["text"]
        fileName = fileName.replace(" ", "")
        fileName = fileName.replace(",", "")
        if( os.path.isfile("data/markdown/" + fileName + ".md")):
            filePath = "data/markdown/" + fileName + ".md"
        elif( os.path.isfile("data/docx/" + fileName + ".docx")):
            filePath = createMarkdown(fileName)
            f = open(filePath)
            data = f.read()
            f.close()
            data = formatMarkdown(data)
            return render_template("file.html", data=data)
        else:
            return redirect(url_for("listPage"))
    else:

        data = [None] * 7
        current = date.today()
        for x in range(7):
            data[x] = current.strftime("%d%B%Y")
            current = current - timedelta(1)
        data.reverse()
        return render_template("list.html", data=data)

# Feedback screen to send feedback on website functionality. Currently sends to text document on server
@app.route("/contact/", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
            flag = sendFeedback(request)
            if flag:
                flash("Feedback submitted. Thank you!")
            else:
                flash("Error submitting feedback. Check email and try again.")
    return render_template("contact.html")

# Page for finding a certain POD from the search bar, doesn't render itself, rather a file.html or a redirect to listPage
@app.route("/<fileName>")
def search(fileName):
    fileName = fileName.replace(" ", "")
    #print(fileName)
    if( os.path.isfile("data/markdown/" + fileName + ".md")):
        filePath = "data/markdown/" + fileName + ".md"
    elif( os.path.isfile("data/docx/" + fileName + ".docx")):
        filePath = createMarkdown(fileName)
    else:
        filePath = ""
    if 'data' in filePath:
        f = open(filePath)
        data = f.read()
        f.close()
        data = formatMarkdown(data)
        return render_template("file.html", data=data)
    else:
        return redirect(url_for("listPage"))

# Starts Flask object to run
if __name__ == "__main__":
    app.run(debug = False)
