# -*- coding: utf-8 -*-

import os
import sys
import threading
import time

sys.path.append(os.path.join(sys.path[0], '../../'))
import schedule
from instabot import Bot, utils

import config

block_words_list = utils.file(config.STALKER_FILE).list

print("SELECT SLAVE ACCOUNT FOR QUERYING FOLLOWERS (HIGH VOLUME REQUESTS)")
bot = Bot(block_words=block_words_list)
bot.login()
print("SELECT MASTER ACCOUNT FOR BLOCKING FOLLOWERS")
bot_blocker = Bot()
bot_blocker.login()

bot.logger.info("Starting blocker. Runs 24/7!")

mastername = ""
follower_cache = set(bot.get_user_followers(mastername))

def stats():
    bot.save_user_stats(bot.user_id)

def block_followers_from_stalker_file():
    bot.logger.info("Checking followers for new stalkers.")
    # followers = bot.get_user_followers(bot_blocker.user_id)
    followers = bot.get_user_followers(mastername)
    bot._followers = followers
    new_followers = set(followers) - follower_cache
    bot.logger.info("TRACKED FOLLOWERS: %s" % len(followers))
    bot.logger.info("BLOCK WORDS: %s" % ', '.join(bot.block_words))
    
    if not new_followers:
        print('New followers not found')
    else:
        for user_id in new_followers: 
            username = bot.get_username_from_user_id(user_id)
            print(username)
    
    # bot.block_stalkers(bot_blocker)

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()

# schedule.every(1).to(5).minutes.do(run_threaded, block_followers_from_stalker_file)
# schedule.every(30).seconds.do(run_threaded, block_followers_from_stalker_file)
schedule.every(10).minutes.do(run_threaded, block_followers_from_stalker_file)
run_threaded(block_followers_from_stalker_file)

while True:
    schedule.run_pending()
    time.sleep(1)
