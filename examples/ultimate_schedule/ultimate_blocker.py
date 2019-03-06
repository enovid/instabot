# -*- coding: utf-8 -*-

from glob import glob
import os
import sys
import threading
import time

sys.path.append(os.path.join(sys.path[0], '../../'))
import schedule
from instabot import Bot, utils

import config
import notify

block_words_list = utils.file(config.STALKER_FILE).list

bot = Bot(block_words=block_words_list)
bot.login()
bot_blocker = Bot()
bot_blocker.login()
bot.logger.info("ULTIMATE script. Safe to run 24/7!")

def stats():
    bot.save_user_stats(bot.user_id)

def block_followers_from_stalker_file():
    bot.logger.info("Checking followers for new stalkers.")
    followers = bot.get_user_followers(bot_blocker.user_id)
    bot._followers = followers
    bot.logger.info("CURRENT FOLLOWING: %s" % ', '.join(bot.following))
    bot.logger.info("CURRENT FOLLOWERS: %s" % ', '.join(followers))
    bot.logger.info("BLOCK WORDS: %s" % ', '.join(bot.block_words))
    
    bot.block_stalkers(bot_blocker=bot_blocker)

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()

# schedule.every(1).to(5).minutes.do(run_threaded, block_followers_from_stalker_file)
schedule.every(15).seconds.do(run_threaded, block_followers_from_stalker_file)

while True:
    schedule.run_pending()
    time.sleep(1)
