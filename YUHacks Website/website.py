from flask import Flask, redirect, url_for, render_template, request, session, flash, current_app, g
from flask.cli import with_appcontext
from datetime import timedelta
import sqlite3
import discord
from discord.ext import commands
import pandas as pd
from threading import Thread
from functools import partial
import asyncio
from asyncio import sleep
from sqlalchemy import null
import random

TOKEN='OTQ0Mjk2MDQ1MzM1MTc1MjM4.Yg_iOQ.SQBPdSISOnByLmVed-_2IGivlQM'
data =[]
# x
client = commands.Bot(command_prefix="-")
client.remove_command('help')
helpLinks = ["https://solvingprocrastination.com/how-to-stop-procrastinating/%22,%22https://www.edutopia.org/article/5-research-backed-studying-techniques%22,%22https://www.umassd.edu/dss/resources/students/classroom-strategies/how-to-get-good-grades/"]
helpLinkNames = ["Solving Procrastination","5 Studying Techniques","How to Get Good Grades"]
app = Flask(__name__)

app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes = 5)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods = ["POST", "GET"])
def tasks():
    tasksetup()
    if request.method == "POST":
        try:
            head = request.form["header"]
            print(head)
            addHeader(head)
        except:
            try:
                tas = request.form["task"]
                head = request.form["taskHeader"]
                addTask(head,tas)
            except:
                print("error")

        # asyncio.run(addHeader1(head))
        # asyncio.run_in_executor(None, lambda: addHeader1(header=head))
        return redirect(url_for("tasks"))
    return render_template("tasks.html")

async def addHeader1(header):
    addHeader(header)
    global x
    await x.edit(content = listFormat())
    
@app.route('/logout')
def logout():
    return redirect(url_for('home'))


@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] =='admin' and request.form['password'] == 'admin' :

            flash('You were just logged in!')
            return redirect(url_for('tasks'))
        elif request.form['username'] =='AJ' and request.form['password'] == 'AJ' :

            flash('You were just logged in!')
            return redirect(url_for('tasks'))
        elif request.form['username'] =='Kris' and request.form['password'] == 'Kris' :

            flash('You were just logged in!')
            return redirect(url_for('tasks'))
        elif request.form['username'] =='Joaquin' and request.form['password'] == 'Joaquin' :

            flash('You were just logged in!')
            return redirect(url_for('tasks'))
        elif request.form['username'] =='Kiet' and request.form['password'] == 'Kiet' :
            flash('You were just logged in!')
            return redirect(url_for('tasks'))


        else:
            error = 'Invalid credentials. Please try again'




    return render_template('login.html',error=error)



def tasksetup():
    global data
    # newdata = data
    # headers = []
    # task = []
    # for i in range(len(newdata)):
    #     headers.append(newdata[i][0])
    #     print("hello")
    #     print(newdata[i][0])
    #     for j in range(1,len(newdata[i])):
    #         task[i][j]=newdata[i][j]

    
    df = pd.DataFrame(data)
    df.to_html('templates/tasklist.html', justify='left', header = False, index = False)

partial_run = partial(app.run, debug = True, use_reloader=False)

t = Thread(target=partial_run)
t.start()
#-------------|When bot is started|-------------#
@client.event
async def on_ready():
    global x
    print('We have logged in as {0.user}'.format(client))
    print("------------------------")
    channel = client.get_channel(944299026646437913)
    x = await channel.send('```List will go here```')
    print(data)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Be sure to take breaks so you don't get burnt out!"))

    

#-------------|Bot Commands|-------------#
@client.command()
async def help(ctx):
    print('hello')
    await ctx.send("```css\nADDING AND REMOVING HEADERS/TASKS\n-addHeader [headername]\n-addTask [headername] [taskname]\n-deleteHeader [headername]\n-deleteTask [headername] [taskname]\n\nLIST COMMANDS\n-bringList\n-deleteList\n\nCHECK COMMANDS\n-checkTask [headername] [taskname]\n-uncheckTask [headername] [taskname]\n\nOTHERS\n-reminder [seconds] [message]```")
    return

@client.command()
async def reminder(ctx,time: int,*, msg):
    global helpLinks
    global helpLinkNames
    await sleep(time)
    randomNum = random.randint(0,2)
    em = discord.Embed(title = "Reminder",url= "http://127.0.0.1:5000/", description = str(msg) ,colour = 0x2cdddd)
    em2 = discord.Embed(title = helpLinkNames[randomNum],url= helpLinks[randomNum], description = "Check out this site for some useful study tips on how you can keep on meeting those deadlines!" ,colour = 0xe1644b)
    await ctx.send(ctx.author.mention) 
    await ctx.send(embed=em)
    await ctx.send(embed=em2)

#addHeader command adds header to data array          
@client.command()
async def addHeader(ctx,header):
    addHeader(header)
    await x.edit(content = listFormat())
    return

@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

#addTask command adds task to data array          
@client.command()
async def addTask(ctx,header,*,task):
    global x
    addTask(header,task)
    await x.edit(content = listFormat())
    return

#Bring list to current line         
@client.command()
async def bringList(ctx):
    global x
    await x.delete()
    x = await ctx.send(listFormat()) 
    return

#Deletes List        
@client.command()
async def deleteList(ctx):
    global data
    global x
    await x.delete()
    data = [] 
    x = await ctx.send("```List goes here```") 
    return

#Deletes a task from the list
@client.command()
async def deleteTask(ctx,header,*,task):
    global x
    deleteTask(header,task)
    await x.edit(content = listFormat()) 
    return

#Deletes a header from the list
@client.command()
async def deleteHeader(ctx,header):
    global x
    deleteHeader(header)
    await x.edit(content = listFormat()) 
    return

@client.command()
async def checkTask(ctx,header,*,task):
    global x
    check(header,task)
    await x.edit(content = listFormat()) 
    return

@client.command()
async def uncheckTask(ctx,header,*,task):
    global x
    unCheck(header,task)
    await x.edit(content = listFormat()) 
    return

@client.command()
async def jsonFile(ctx):
    await ctx.send(file=discord.File(r'tasks.json'))
    return

#-------------|File Functions|-------------#

def deleteTask(header, task):
    global data
    for i in range(len(data)):
        if (data[i][0] == header):
            for j in range(len(data[i])):
                if (data[i][j] == task):
                    del data[i][j]
    return

def deleteHeader(header):
    global data
    for i in range(len(data)):
        if (data[i][0] == header):
            del data[i]
    return

#when addHeader is typed, add header as column in 2d array
def addHeader(header):
    global data
    arr = []
    arr.append(header)
    if not(any(arr[0] in sublist for sublist in data)): #If the header doesn't already exist, make a new list and add that header to the list
        data.append(arr)
    print(data)    

#when addTask [Header] is typed, add task to header
def addTask(header, task):
    global data
    x = False
    task = "- " + task
    for i in range(len(data)):
        if (header == data[i][0]): #if the typed header exists, add task to the header's list
            data[i].append(task)
            x = True
    if (x == False):
        #error case if the header doesn't exist
        print('no header')
    print(data)    
                   
#Format list into a string, returns string        
def listFormat():
    global data
    arr = [1,2,3]
    s="```diff\n"
    if (len(data) == 0):
        return "```Please add a header```"
    else:
        for i in range(len(data)):
            s+=data[i][0]
            s+="\n"
            for j in range(1,len(data[i])):
                s+=data[i][j] + "\n"
            s+="\n" 
        s+="```"               
        return s        

#Checks off given task
def check(header, task):
    global data
    task = "- " + task
    for i in range(len(data)):
        if (data[i][0] == header):
            for j in range(len(data[i])):
                if (data[i][j] == task):
                    data[i][j] = data[i][j].replace("-","+",1)
    return

#Un checks given task
def unCheck(header, task):
    global data
    task = "+ " + task
    for i in range(len(data)):
        if (data[i][0] == header):
            for j in range(len(data[i])):
                if (data[i][j] == task):
                    data[i][j] = data[i][j].replace("+","-",1)
    return



if __name__ == "__main__":
    client.run(TOKEN)
    