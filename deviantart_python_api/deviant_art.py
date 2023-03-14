import requests
from bs4 import BeautifulSoup


class DeviantArt:
    """
    Python DeviantArt api. Doesn't support user auth.
    Parameter category_path is deprecated, it has no effect on the results and it will be removed in future versions of api, so i don't use it.
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.main_link = "https://www.deviantart.com/api/v1/oauth2"
        self.access_token = self.get_client_access_token()

    def get_client_access_token(self):
        url = "https://www.deviantart.com/oauth2/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.get(url, params=params).json()
        # print(response)
        return response["access_token"]

    def browse_daily_deviations(self, date: str = None, with_session: bool = False, mature_content: bool = False):
        """GET /browse/dailydeviations - Browse daily deviations """
        url = self.main_link + "/browse/dailydeviations"
        params = {
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(date, type(None)):
            params["date"] = date
        response = requests.get(url, params=params).json()
        return response

    def browse_newest(self, q: str = None, offset: int = None, limit: int = None, with_session: bool = False,
                      mature_content: bool = False):
        """GET /browse/newest - Browse newest deviations"""
        url = self.main_link + "/browse/newest"
        params = {
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(q, type(None)):
            params["q"] = q
        if not isinstance(offset, type(None)):
            params["offset"] = offset
        if not isinstance(limit, type(None)):
            params["limit"] = limit
        response = requests.get(url, params=params).json()
        return response

    def browse_popular(self, q: str = None, offset: int = None, limit: int = None, with_session: bool = False,
                       mature_content: bool = False):
        """GET /browse/popular - Browse popular deviations"""
        url = self.main_link + "/browse/popular"
        params = {
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(q, type(None)):
            params["q"] = q
        if not isinstance(offset, type(None)):
            params["offset"] = offset
        if not isinstance(limit, type(None)):
            params["limit"] = limit
        response = requests.get(url, params=params).json()
        return response

    def browse_tag(self, tag, cursor=None, offset=None, limit=None, with_session: bool = False,
                   mature_content: bool = False):
        """GET /browse/tags/ - Browse a tag"""
        url = self.main_link + "/browse/tags"
        params = {
            "tag": tag,
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(cursor, type(None)):
            params["cursor"] = cursor
        if not isinstance(offset, type(None)):
            params["offset"] = offset
        if not isinstance(limit, type(None)):
            params["limit"] = limit
        response = requests.get(url, params=params).json()
        # print(response)
        return response

    def browse_search_tags(self, tag_name: str, with_session: bool = False, mature_content: bool = False):
        """GET /browse/tags/search -  Autocomplete tags\n
        The tag_name parameter must contain at least least 3 characters long
        The tag_name parameter should not contain spaces. If it does, spaces will be stripped and remainder will be treated as a single tag"""
        url = self.main_link + "/browse/tags/search"
        params = {
            "tag_name": tag_name,
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        response = requests.get(url, params=params).json()
        return response

    def browse_topic(self, topic: str, q: str = None, offset: int = None, limit: int = None, with_session: bool = False,
                     mature_content: bool = False):
        """GET /browse/topic - Fetch topic deviations"""
        url = self.main_link + "/browse/topic"
        params = {
            "access_token": self.access_token,
            "topic": topic,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(q, type(None)):
            params["q"] = q
        if not isinstance(offset, type(None)):
            params["offset"] = offset
        if not isinstance(limit, type(None)):
            params["limit"] = limit
        response = requests.get(url, params=params).json()
        return response

    def browse_topics(self, q: str = None, offset: int = None, limit: int = None, num_deviations_per_topic: int = None,
                      with_session: bool = False, mature_content: bool = False):
        """GET /browse/topics - Fetch topics and deviations from each topic"""
        url = self.main_link + "/browse/topics"
        params = {
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(q, type(None)):
            params["q"] = q
        if not isinstance(offset, type(None)):
            params["offset"] = offset
        if not isinstance(limit, type(None)):
            params["limit"] = limit
        if not isinstance(num_deviations_per_topic, type(None)):
            params["num_deviations_per_topic"] = num_deviations_per_topic
        response = requests.get(url, params=params).json()
        return response

    def browse_toptopics(self, with_session: bool = False, mature_content: bool = False):
        """GET /browse/toptopics - Fetch top topics with example deviation for each one"""
        url = self.main_link + "/browse/toptopics"
        params = {
            "access_token": self.access_token,
            "with_session": with_session,
            "mature_content": mature_content
        }
        response = requests.get(url, params=params).json()
        return response

    def browse_user_journals(self, username: str, featured: bool = None, offset: int = None, limit: int = None,
                             with_session: bool = False, mature_content: bool = False):
        """GET /browse/user/journals - Browse journals of a user"""
        url = self.main_link + "/browse/toptopics"
        params = {
            "access_token": self.access_token,
            "username": username,
            "with_session": with_session,
            "mature_content": mature_content
        }
        if not isinstance(featured, type(None)):
            params["featured"] = featured
        if not isinstance(offset, type(None)):
            params["offset"] = offset
        if not isinstance(limit, type(None)):
            params["limit"] = limit
        response = requests.get(url, params=params).json()
        return response


if __name__ == "__main__":
    da = DeviantArt("24178", "7b472c20aea66646e9f9219c6c3da2c9")
    # print(da.browse_daily_deviations())
    # print(da.browse_newest())
    # print(da.browse_popular())
    # print(da.browse_tag("anime"))
    # print(da.browse_search_tags("ani"))
    # print(da.browse_topic("3d"))
    # print(da.browse_topics())
    # print(da.browse_toptopics())
    # print(da.browse_user_journals("cryptid-creations"))