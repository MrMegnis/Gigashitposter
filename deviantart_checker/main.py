import datetime
import time
import logging
import schedule
from dotenv import load_dotenv

from data import db_session
from sqlalchemy import update, select

from data.posts import Posts
from data.tags import Tags
from deviantart_checker.parser import get_tag_last_deviant_id


def create_posts(tag, deviant_id):
    db_sess = db_session.create_session()
    groups = db_sess.execute(select(Posts.group_id).where(Posts.tag == tag))


def job():
    db_sess = db_session.create_session()
    tags = db_sess.execute(select(Tags.tag, Tags.last_deviant_id)).all()
    logging.warning(tags)
    for tag, last_deviant in tags:
        cur_last = get_tag_last_deviant_id(tag)
        # logging.warning(tag)
        # logging.warning(last_deviant)
        # logging.warning(cur_last)
        if cur_last != last_deviant:
            logging.warning(tag, last_deviant, cur_last)
            # create posts
            db_sess.execute(update(Tags).values(last_deviant_id=cur_last).where(Tags.tag == tag))
            db_sess.commit()


def main():
    schedule.every(15).minutes.do(job)


if __name__ == "__main__":
    load_dotenv('.env')
    db_session.global_init()
    db_sess = db_session.create_session()
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
