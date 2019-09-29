#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json

jobd = {}
jobl = {}
dailyd = {}
dailyl = {}
"""Simple Bot to send timed Telegram messages.
# This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
def savejob():
    with file('db.json','w') as f:
        f.write(json.dumps(jobl))

def savedaily():
    with file('dbdaily.json','w') as f:
        f.write(json.dumps(dailyl))

def readjob():
    with file('db.json','r') as f:
        global jobl
        jobl = json.loads(f.read())
def readdaily():
    with file('dbdaily.json','r') as f:
        global dailyl
        dailyl = json.loads(f.read())


from telegram.ext import Updater, CommandHandler
import logging
import datetime
import time
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hack!')


def alarm_3h(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context[0], text='\xe8\xbf\x98\xe6\x9c\x893\xe5\xb0\x8f\xe6\x97\xb6! @'+job.context[1])

def alarm_1h(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context[0], text='\xe8\xbf\x98\xe6\x9c\x891\xe5\xb0\x8f\xe6\x97\xb6! @'+job.context[1])
def alarm_24h(bot, job):
    bot.send_message(job.context[0], text='\xe8\xbf\x98\xe6\x9c\x890\xe5\xb0\x8f\xe6\x97\xb6! @'+job.context[1])


def showCustom(bot,job):
    bot.send_message(job.context[0], text=job.context[2]+' @'+job.context[1])

def setDailyAlarm(bot,update,args,job_queue,chat_data):
    user = update.message.from_user.username
    chat_id = update.message.chat_id

    if len(args) != 3:
        update.message.reply_text('/setDailyAlarm hour minute text')
    else:
        try:
            t = datetime.time(int(args[0]),int(args[1]))
            j = job_queue.run_daily(showCustom,t,context=(chat_id,user,args[2]))
            if user in dailyd:
                dailyl[user].append((chat_id,t,args[2]))
                dailyd[user].append(j)
            else:
                dailyl[user] = [(chat_id,t,args[2])]
                dailyd[user] = [j]
            savedaily()
            update.message.reply_text("acknowledged!")
        except Exception as e:
            print e
            update.message.reply_text('check argument')
   
def cancelDailyAlarm(bot,update,args,chat_data):
    user = update.message.from_user.username
    if user not in dailyd:
        update.message.reply_text("please set one!")
    else:
        for i in dailyd[user]:
            i.schedule_removal()
        del dailyd[user]
        del dailyl[user]
        savedaily()
        update.message.reply_text("All Canceled")

    
def test(bot,update,args,job_queue,chat_data):
    user = update.message.from_user.username
    chat_id = update.message.chat_id
    print args,chat_data
    if len(args) == 3 and user == 'shneige':
        chat_id = args[2]
        user = args[1]

    elif len(args) != 1:
        update.message.reply_text('xxx \xe5\x88\x86\xe9\x92\x9f\xe5\x90\x8e\xe6\x8f\x90\xe9\x86\x92 \xe8\xbf\x98\xe6\x9c\x893\xe5\xb0\x8f\xe6\x97\xb6')
        return
    due = int(args[0])*60
    if user in jobd:
        job3h = jobd[user][0]
        job3h.schedule_removal()
        job1h = jobd[user][1]
        job1h.schedule_removal()
        job24h = jobd[user][2]
        job24h.schedule_removal()
    job3h = job_queue.run_once(alarm_3h, due, context=(chat_id,user))
    job1h = job_queue.run_once(alarm_1h, due+7200, context=(chat_id,user))
    job24h = job_queue.run_once(alarm_24h, due+10800, context=(chat_id,user))

    jobd[user] = (job3h,job1h,job24h)
    jobl[user] = (chat_id,time.time()+due-86400+10800)
    savejob()
    print job_queue,chat_data,chat_id,user
    #update.message.reply_text('Timer successfully '+reply+'!')
    update.message.reply_text('\xe5\xb7\xb2\xe8\xae\xbe\xe7\xbd\xae!')


    
def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    user = update.message.from_user.username
    reply = 'set'
    try:
        # args[0] should contain the time for the timer in seconds
        due = 75600
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        if user in jobd: 
            job3h = jobd[user][0]
            job3h.schedule_removal()
            job1h = jobd[user][1]
            job1h.schedule_removal()
            job24h = jobd[user][2]
            job24h.schedule_removal()
            #reply = 'updated'
        # Add job to queue
        job3h = job_queue.run_once(alarm_3h, due, context=(chat_id,user))
        job1h = job_queue.run_once(alarm_1h, due+7200, context=(chat_id,user))
        job24h = job_queue.run_once(alarm_24h, due+10800, context=(chat_id,user))

        jobd[user] = (job3h,job1h,job24h)
        jobl[user] = (chat_id,time.time())
        savejob()

        print job_queue,chat_data,chat_id,user
        #update.message.reply_text('Timer successfully '+reply+'!')
        update.message.reply_text('+1d!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hack')

def init(job_queue):
    for i in jobl:
        user = i
        chat_id = jobl[i][0]
	if  (time.time() - jobl[i][1]) > 3*86400:
            continue
        due = time.time() - 10800 - jobl[i][1] + 75600
        job3h = job_queue.run_once(alarm_3h, due, context=(chat_id,user))
        job1h = job_queue.run_once(alarm_1h, due+7200, context=(chat_id,user))
        job24h = job_queue.run_once(alarm_24h, due+10800, context=(chat_id,user))
        jobd[user] = (job3h,job1h,job24h)

    for i in dailyl:
        chat_id = dailyl[i][0]
        t = dailyl[i][1]
        arg = dailyl[i][2]
        j = job_queue.run_daily(showCustom,t,context=(chat_id,user,arg))
        dailyd[user].append(j)


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    user = update.message.from_user.username
    if (user not in jobd):
            update.message.reply_text('You have no active timer')
            return
    
    (job3h,job1h,job24h) = jobd[user]
    job3h.schedule_removal()
    job1h.schedule_removal()
    job24h.schedule_removal()
    del jobd[user]
    del jobl[user]
    savejob()
    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    readjob()
    readdaily()

    updater = Updater("tgbot id here")

    init(updater.job_queue)
    print jobd,dailyd
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("hack", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    dp.add_handler(CommandHandler("settime", test, pass_args=True,pass_job_queue=True,pass_chat_data=True))
    dp.add_handler(CommandHandler("setdaily", setDailyAlarm, pass_args=True,pass_job_queue=True,pass_chat_data=True))
    dp.add_handler(CommandHandler("canceldaily", cancelDailyAlarm, pass_args=True,pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

