import datetime
import logging
import os
import requests
from dotenv import load_dotenv
from VK import vk_api
from dotenv import load_dotenv

VK_API_VERSION = vk_api.VK_API_VERSION


class Post:
    def __init__(self, access_token, photo, owner_id=None, from_group=None, message=None, services=None,
                 signed=None, publish_date=None, lat=None, long=None, place_id=None, guid=None, close_comments=None,
                 donut_paid_duration=None, mute_notifications=None, copyright_=None, topic_id=None, caption=None,
                 v=VK_API_VERSION):
        self.v_api = vk_api.VK_Api(access_token)
        self.owner_id = owner_id
        group_id = None
        user_id = None
        if int(owner_id) < 0:
            group_id = owner_id
        else:
            user_id = owner_id
        if not isinstance(group_id, type(None)):
            group_id = abs(int(group_id))
        response = self.v_api.get_wall_upload_server(group_id, v)
        logging.warning(response)
        upload_url = response["response"]["upload_url"]
        # photo_info = response["response"]["photo"]
        response = self.v_api.upload_photo(upload_url=upload_url, photo=photo)
        photo_multipart = response["photo"]
        server = response["server"]
        hash_ = response["hash"]
        response = self.v_api.save_wall_photo(photo_multipart, server, hash_, user_id, group_id, lat, long, caption, v)
        logging.warning(response)
        self.photo_owner_id = response["response"][0]["owner_id"]
        self.photo_id = response["response"][0]["id"]
        self.from_group = from_group
        self.message = message
        self.services = services
        self.signed = signed
        self.publish_date = publish_date
        self.lat = lat
        self.long = long
        self.place_id = place_id
        self.guid = guid
        self.close_comments = close_comments
        self.donut_paid_duration = donut_paid_duration
        self.mute_notifications = mute_notifications
        self.copyright_ = copyright_
        self.topic_id = topic_id

    def post(self):
        logging.warning("owner_id:"+self.owner_id)
        r = self.v_api.post(self.owner_id, self.from_group, self.message, f"photo{self.photo_owner_id}_{self.photo_id}",
                        self.services, self.signed, self.publish_date, self.lat, self.long, self.place_id, self.guid,
                        self.close_comments, self.donut_paid_duration, self.mute_notifications, self.copyright_,
                        self.topic_id, VK_API_VERSION)
        logging.warning(r)
        logging.warning("SUCCESS")


def create_posts(access_token: str, photos: list, group_id, start_on, interval, messages: list = []) -> list:
    if len(photos) > len(messages):
        while len(messages) != len(photos):
            messages.append("")
    posts = list()
    publish_date = start_on
    time_delta = datetime.timedelta(hours=interval.hour, minutes=interval.minute, seconds=interval.second)
    for photo, message in zip(photos, messages):
        post = Post(access_token, photo, group_id, "1", message, publish_date=publish_date.timestamp())
        # post="a"
        # print(publish_date)
        # logging.warning(publish_date.timestamp())
        publish_date += time_delta
        posts.append(post)
    return posts


if __name__ == "__main__":
    load_dotenv('../.env')
    url = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/61a5bf18-09b0-4cb9-9cd0-7a791870f17e/dbc0ols-52ed6ff0-fa84-43ea-a88d-87333d462259.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzYxYTViZjE4LTA5YjAtNGNiOS05Y2QwLTdhNzkxODcwZjE3ZVwvZGJjMG9scy01MmVkNmZmMC1mYTg0LTQzZWEtYTg4ZC04NzMzM2Q0NjIyNTkucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.hLnlTjPrHfucJfzNMCJ3pgroc8aLfTQYvLBcl6y7XH0'
    response = requests.get(url)
    # print(response.content)
    with open("aboba.png", "wb") as f:
        f.write(response.content)
    # print(response.raw == open("aboba.png", 'rb'))
    post = Post(os.getenv('VK_ACCESS_TOKEN'), response.content, owner_id="-219613882", from_group="1", message="aboba")
    post.post()
