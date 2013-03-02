#homestuck bot, manages flair

import time
import praw
import re
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
            pprint("clearing modqueue...")
            self.clear_modqueue()
            time.sleep(timeout)
    
    def clear_modqueue(self):
        queue = list(self.r.get_mod_queue(self.sub))
        if (len(queue) > 0):
            for submission in queue:
                print('clearing...')
                if isinstance(submission, praw.objects.Comment):
                    text = submission.body.lower()
                else:
                    text = submission.selftext.lower() + submission.domain()

                s = re.compile("\.tumblr\.com")
                has_tumblr = s.search(text);
                if has_tumblr:
                    submission.approve()
                    print("Approved!")
                else:
                    print("Nah...")

pw = ' '
user = 'homestuck moderator bot v0.9 by /u/tinaun'

hsbot = Bot('homestuck', 'homestuck-bot', pw, user)
hsbot.start()


                




