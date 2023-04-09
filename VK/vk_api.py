import requests
from dotenv import load_dotenv
import os

load_dotenv('../.env')
VK_API_VERSION = os.environ.get('VK_API_VERSION')


class VK_Api:
    API_URL = "https://api.vk.com/method"

    def __init__(self, access_token):
        self.access_token = access_token

    def get_upload_server(self, album_id, group_id=None, v=VK_API_VERSION):
        url = self.API_URL + "/photos.getUploadServer"
        params = {
            "access_token": self.access_token,
            "v": v
        }
        for param in [(group_id, "group_id")]:
            if not isinstance(param[0], type(None)):
                params[param[1]] = param[0]
        response = requests.get(url, params=params).json()
        print(response)
        return response

    def get_wall_upload_server(self, group_id=None, v=VK_API_VERSION):
        url = self.API_URL + "/photos.getWallUploadServer"
        params = {
            "access_token": self.access_token,
            "v": v
        }
        print("upload g_id:", group_id)
        for param in [(group_id, "group_id")]:
            if not isinstance(param[0], type(None)):
                params[param[1]] = param[0]
        response = requests.get(url, params=params).json()
        print(response)
        return response

    def upload_photo(self, upload_url, photo):
        # url = get_wall_upload_server(access_token, group_id, v)["response"]["upload_url"]
        response = requests.post(upload_url, files={'file': ("new_year_floppa.png", photo)}).json()
        print(response)
        return response

    def save_wall_photo(self, photo, server, hash_, user_id=None, group_id=None, latitude=None,
                        longitude=None,
                        caption=None, v=VK_API_VERSION):
        url = self.API_URL + "/photos.saveWallPhoto"
        params = {
            "access_token": self.access_token,
            "photo": photo,
            "server": server,
            "hash": hash_,
            "v": v
        }
        print("save g_id:", group_id)
        for param in [
            (user_id, "user_id"), (group_id, "group_id"),
            (latitude, "latitude"), (longitude, "longitude"), (caption, "caption")
        ]:
            if not isinstance(param[0], type(None)):
                params[param[1]] = param[0]
        response = requests.get(url, params=params).json()
        print(response)
        return response

    def post(self, owner_id=None, from_group=None, message=None, attachments=None, services=None,
             signed=None, publish_date=None, lat=None, long=None, place_id=None, guid=None, close_comments=None,
             donut_paid_duration=None, mute_notifications=None, copyright_=None, topic_id=None, v=VK_API_VERSION):
        url = self.API_URL + "/wall.post"

        params = {
            "access_token": self.access_token,
            "v": v
        }
        for param in [(owner_id, "owner_id"), (from_group, "from_group"), (message, "message"),
                      (attachments, "attachments"), (services, "services"), (signed, "signed"),
                      (publish_date, "publish_date"), (lat, "lat"), (long, "long"), (place_id, "place_id"),
                      (guid, "guid"),
                      (close_comments, "close_comments"), (donut_paid_duration, "donut_paid_duration"),
                      (mute_notifications, "mute_notifications"), (copyright_, "copyright_"), (topic_id, "topic_id")]:
            if not isinstance(param[0], type(None)):
                params[param[1]] = param[0]
        response = requests.get(url, params=params).json()
        # print(response)
        return response

    def groups_get(self, user_id=None, extended=None, filter=None, fields=None, offset=None, count=None, v=VK_API_VERSION):
        url = self.API_URL + "/groups.get"

        params = {
            "access_token": self.access_token,
            "v": v
        }
        for param in [(user_id, "user_id"), (extended, "extended"), (filter, "filter"), (fields, "fields"),
                      (offset, "offset"), (count, "count")]:
            if not isinstance(param, type(None)):
                params[param[1]] = param[0]
        response = requests.get(url, params=params).json()
        # print(response)
        return response
