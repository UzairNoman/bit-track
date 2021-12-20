from typing import List, Dict, Tuple
import time
from os.path import exists
from cryptography.fernet import Fernet

from static_params import ENC_PASSWORD, ENC_USERNAME, ENC_SECRET_TOKEN

import requests
import praw
from praw.models import MoreComments
from praw import Reddit

CLIENT_ID = 'etAstulzAzEmtbmXhprohw'
SECRET_TOKEN = ''
USERNAME = ''
PASSWORD = ''
SEARCH_API_ADDRESS = "https://oauth.reddit.com/r/all/search?"


def decrypt():
    """
    call this function before all other functions
    decrypt secret token, username, password
    :return:
    """
    if exists("./KEY_FILE"):
        with open("./KEY_FILE") as f:
            key = f.read()
    else:
        key = input("input key for decryption: ")
    key = key.encode()
    fernet = Fernet(key)
    global SECRET_TOKEN, USERNAME, PASSWORD
    SECRET_TOKEN = fernet.decrypt(ENC_SECRET_TOKEN).decode()
    USERNAME = fernet.decrypt(ENC_USERNAME).decode()
    PASSWORD = fernet.decrypt(ENC_PASSWORD).decode()


def update_login_headers() -> Dict:
    """
    login in and update headers
    :return: headers
    """
    assert USERNAME != ''
    assert PASSWORD != ''
    assert SECRET_TOKEN != ''
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
    data = {'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD}
    headers = {'User-Agent': 'PostSearch/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    return {**headers, **{'Authorization': f"bearer {token}"}}


def search(query: str, headers: Dict, limit: int = 100,) -> List[str]:
    """
    search a query and return 100 results, results are post link
    :param query:
    :param headers:
    :param limit:
    :return:
    """
    params = {
        "q": query,
        "limit": limit
    }
    res = requests.get(
        SEARCH_API_ADDRESS,
        headers=headers,
        params=params
    )
    res = res.json()
    return ["https://www.reddit.com"+post["data"]["permalink"] for post in res["data"]["children"]]


def login_praw() -> Reddit:
    assert USERNAME != ''
    assert PASSWORD != ''
    assert SECRET_TOKEN != ''
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=SECRET_TOKEN,
        user_agent="PostSearch/0.0.1",
        username=USERNAME,
        password=PASSWORD,
    )
    return reddit


def get_comments(url: str, reddit: Reddit) -> Tuple[List[str], List[str]]:
    """
    get comments from one specific post, return comments' authors and contents
    :param url: post url, e.g. https://www.reddit.com/r/NFTsMarketplace/comments/qjkn6x/giveaway_elitenft_presents_diamond_death_50_up/
    :param reddit: Reddit object from praw after logging in
    :return: two lists with authors and content
    """
    submission = reddit.submission(url=url)
    authors, comments = [], []
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        authors.append(top_level_comment.author)
        comments.append(top_level_comment.body)
    return authors, comments


if __name__ == "__main__":
    # headers = update_login_headers()
    # results = search(query="ETH address",
    #                  headers=headers)
    # for r in results:
    #     print(r)
    decrypt()
    url = "https://www.reddit.com/r/NFTsMarketplace/comments/qjkn6x/giveaway_elitenft_presents_diamond_death_50_up/"
    reddit = login_praw()
    authors, comments = get_comments(url, reddit)
    for a in authors:
        print(a)