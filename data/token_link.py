# https://oauth.vk.com/authorize?client_id=51593041&client_secret=9DqqHq7CTmThwEGyPEM2&redirect_uri=https://ca55-2a01-540-316-8000-716e-d8db-1cb3-805b.eu.ngrok.io/api/set_token&scope=friends&response_type=code&state="1"
import os

from dotenv import load_dotenv

user_accept_rights = {
    "notify": 1 << 0,
    "friends": 1 << 1,
    "photos": 1 << 2,
    "audio": 1 << 3,
    "video": 1 << 4,
    "stories": 1 << 6,
    "pages": 1 << 7,
    "menu": 1 << 8,
    "status": 1 << 10,
    "notes": 1 << 11,
    "messages": 1 << 12,
    "wall": 1 << 13,
    "ads": 1 << 15,
    "offline": 1 << 16,
    "docs": 1 << 17,
    "groups": 1 << 18,
    "notifications": 1 << 19,
    "stats": 1 << 20,
    "email": 1 << 22,
    "market": 1 << 27,
}

group_accept_rights = {
    "stories": 1 << 0,
    "photos": 1 << 2,
    "app_widget": 1 << 6,
    "messages": 1 << 12,
    "docs": 1 << 17,
    "manage": 1 << 18
}


def get_user_authorization_code_flow_link(client_id: str, client_secret: str, redirect_uri: str, scope: list,
                                          state: str) -> str:
    scope_mask = sum([user_accept_rights[i] for i in scope])
    link = f"https://oauth.vk.com/authorize?client_id={client_id}&client_secret={client_secret}" \
           f"&redirect_uri={redirect_uri}&scope={scope_mask}&response_type=code&state={state}"
    return link


def get_user_implicit_flow_link(client_id: str, client_secret: str, redirect_uri: str, scope: list,
                                state: str) -> str:
    scope_mask = sum([user_accept_rights[i] for i in scope])
    link = f"https://oauth.vk.com/authorize?client_id={client_id}&client_secret={client_secret}" \
           f"&redirect_uri={redirect_uri}&scope={scope_mask}&response_type=token&state={state}"
    return link

def get_user_token_link(client_id: str, client_secret: str, redirect_uri: str, scope: list,
                                state: str) -> str:
    scope_mask = sum([user_accept_rights[i] for i in scope])
    link = f"https://oauth.vk.com/authorize?client_id={client_id}&client_secret={client_secret}" \
           f"&scope={scope_mask}&response_type=token&state={state}"
    return link


def get_groups_authorization_code_flow_link(client_id: str, client_secret: str, redirect_uri: str, group_ids: list,
                                            scope: list,
                                            state: str) -> str:
    scope_mask = sum([group_accept_rights[i] for i in scope])
    link = f"https://oauth.vk.com/authorize?client_id={client_id}&client_secret={client_secret}" \
           f"&redirect_uri={redirect_uri}&group_ids={','.join(group_ids)}" \
           f"&scope={scope_mask}&response_type=code&state={state}"
    return link


def get_groups_implicit_flow_link(client_id: str, client_secret: str, redirect_uri: str, group_ids: list, scope: list,
                                  state: str) -> str:
    scope_mask = sum([group_accept_rights[i] for i in scope])
    link = f"https://oauth.vk.com/authorize?client_id={client_id}&client_secret={client_secret}" \
           f"&redirect_uri={redirect_uri}&group_ids={','.join(group_ids)}" \
           f"&scope={scope_mask}&response_type=token&state={state}"
    return link


if __name__ == "__main__":
    load_dotenv('../.env')
    token_link = get_user_authorization_code_flow_link("51593041", "9DqqHq7CTmThwEGyPEM2",
                                                       "https://1f1f-2a01-540-316-8000-5d1c-3ce8-b9b0-3cb0.eu.ngrok.io/api/set_token",
                                                       ["manage"],
                                                       "1")
    print(token_link)
    token_link = get_user_authorization_code_flow_link(os.environ.get('VK_CLIENT_ID'),
                                                       os.environ.get('VK_CLIENT_SECRET'),
                                                       os.environ.get('SET_TOKEN_SITE_LINK') + os.environ.get(
                                                           'SET_TOKEN_PATH'),
                                                       ["manage"], "1")
    print(token_link)
