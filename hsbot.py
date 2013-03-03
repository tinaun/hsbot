#homestuck bot, manages flair

import time
import praw
import re
import threading
from pprint import pprint

class Bot:
    """Clears Modqueue of tumblr posts"""
    def __init__(self, subreddit, account, pw, user_agent):
        self.sub = subreddit
        self.account = account
        self.password = pw
        self.ua = user_agent

    def start(self):
        timeout = 300
        self.r = praw.Reddit(user_agent=self.ua)
        self.r.login(self.account, self.password)
        pprint("Succesfully logged in as " + self.account)
        while True:
            self.clear_modqueue()
            if (time.localtime()[3] > 13) and (time.localtime()[3] < 15):
                self.check_inbox()
                
            time.sleep(timeout)
    
    def clear_modqueue(self):
        queue = list(self.r.get_mod_queue(self.sub))
        if (len(queue) > 0):
            for submission in queue:
                print('clearing...')
                if isinstance(submission, praw.objects.Comment):
                    text = submission.body.lower()
                else:
                    text = submission.selftext.lower() + submission.domain

                s = re.compile('\.tumblr\.com')
                p = re.compile('\.deviantart\.net')
                has_tumblr = s.search(text);
                has_deviant = p.search(text);
                if has_tumblr or has_deviant:
                    submission.approve()
                    print("Approved!")
                else:
                    print("Nah...")

    def check_inbox(self):
        inbox = list(self.r.get_unread(limit=None))

        n = 1
        for msg in inbox:
            print("Message " + str(n) + "of " + str(len(inbox)))
            print(msg)
            confirm = input("expand? ").lower()
            if (confirm[0] == 'y'):
                print(msg.body)
            confirm = input("reply? ").lower()
            if (confirm[0] == 'y'):
                rep = input("--> ")
                msg.reply(rep)
            msg.mark_as_read()

pw = ' '
user = 'homestuck moderator bot v0.9 by /u/tinaun'

hsbot = Bot('homestuck', 'homestuck-bot', pw, user)
hsbot.start()


                




