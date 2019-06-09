# -*- coding: utf-8 -*-

import os
import sys
import threading
import time

sys.path.append(os.path.join(sys.path[0], '../../'))
import schedule
from instabot import Bot, utils

import config
import functools

block_words_list = utils.file(config.STALKER_FILE).list

print("SELECT SLAVE ACCOUNT FOR QUERYING FOLLOWERS (HIGH VOLUME REQUESTS)")
bot = Bot(block_words=block_words_list)
bot.login()
print("SELECT MASTER ACCOUNT FOR BLOCKING FOLLOWERS")
bot_blocker = Bot()
bot_blocker.login()

bot.logger.info("Starting blocker. Runs 24/7!")
bot.logger.info("Caching followers for %s" % bot_blocker.username)
follower_cache = set(bot.get_user_followers(bot_blocker.user_id))


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@catch_exceptions(cancel_on_failure=True)
def block_followers_from_stalker_file():
    global follower_cache
    bot.logger.info("Checking followers for new stalkers.")
    followers = bot.get_user_followers(bot_blocker.user_id)
    if len(followers) < len(follower_cache):
        bot.logger.info("Follower count reduced - resetting cache.")
        follower_cache = set(followers)
    new_followers = set(followers) - follower_cache
    bot.logger.info("TRACKED FOLLOWERS: %s" % len(followers))
    bot.logger.info("BLOCK WORDS: %s" % ', '.join(bot.block_words))
    
    if not new_followers:
        print('New followers not found')
    else:
        print('Evaluating new followers:')
        for user_id in new_followers:
            username = bot.get_username_from_user_id(user_id)
            print(username)
        bot._followers = new_followers
        bot.block_stalkers(bot_blocker)
        bot.logger.info("Caching followers for %s" % bot_blocker.username)
        follower_cache = set(bot.get_user_followers(bot_blocker.user_id))

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()

schedule.every(30).seconds.do(block_followers_from_stalker_file)
# schedule.every(30).seconds.do(run_threaded, block_followers_from_stalker_file)
# schedule.every(1).to(5).minutes.do(run_threaded, block_followers_from_stalker_file)
# run_threaded(block_followers_from_stalker_file)

while True:
    schedule.run_pending()
    time.sleep(1)
