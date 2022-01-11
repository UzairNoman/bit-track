from typing import List, Dict, Tuple
import time
from os.path import exists
from cryptography.fernet import Fernet
from tqdm import trange

from utils.static_params import (
    ENC_CLIENT_ID,
    ENC_PASSWORD,
    ENC_USERNAME,
    ENC_SECRET_TOKEN,
    QUERIES,
)

import pandas as pd
import requests
import praw
from praw.models import MoreComments
from praw import Reddit

CLIENT_ID = ""
SECRET_TOKEN = ""
USERNAME = ""
PASSWORD = ""

SEARCH_API_ADDRESS = "https://oauth.reddit.com/r/all/search?"


def decrypt_login_info():
    """
    call this function before all other functions
    decrypt secret token, username, password
    :return:
    """
    if exists("./utils/KEY_FILE"):
        with open("./utils/KEY_FILE") as f:
            key = f.read()
    else:
        key = input("input key for decryption: ")
    key = key.encode()
    fernet = Fernet(key)
    global CLIENT_ID, SECRET_TOKEN, USERNAME, PASSWORD
    CLIENT_ID = fernet.decrypt(ENC_CLIENT_ID).decode()
    SECRET_TOKEN = fernet.decrypt(ENC_SECRET_TOKEN).decode()
    USERNAME = fernet.decrypt(ENC_USERNAME).decode()
    PASSWORD = fernet.decrypt(ENC_PASSWORD).decode()


def update_login_headers() -> Dict:
    """
    login in and update headers
    :return: headers
    """
    assert CLIENT_ID != ""
    assert USERNAME != ""
    assert PASSWORD != ""
    assert SECRET_TOKEN != ""
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
    data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD}
    headers = {"User-Agent": "PostSearch/0.0.1"}

    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )
    token = res.json()["access_token"]
    return {**headers, **{"Authorization": f"bearer {token}"}}


def search(query: str, headers: Dict, limit: int = 100,) -> List[str]:
    """
    search a query and return 100 results, results are post link
    :param query:
    :param headers:
    :param limit:
    :return:
    """
    params = {"q": query, "limit": limit}
    res = requests.get(SEARCH_API_ADDRESS, headers=headers, params=params)
    res = res.json()
    return [
        "https://www.reddit.com" + post["data"]["permalink"]
        for post in res["data"]["children"]
    ]


def login_praw() -> Reddit:
    assert CLIENT_ID != ""
    assert USERNAME != ""
    assert PASSWORD != ""
    assert SECRET_TOKEN != ""
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


def filter_addresses(
    authors: List[str], comments: List[str]
) -> Tuple[List[str], List[str]]:
    """
    delete comments without addresses
    :param authors:
    :param comments:
    :return:
    """
    filtered_authors = []
    filtered_comments = []
    for author, comment in zip(authors, comments):
        address = find_address(comment)
        if (
            address
            and (author not in filtered_authors)
            and (address not in filtered_comments)
        ):
            filtered_authors.append(author)
            filtered_comments.append(address)
    return filtered_authors, filtered_comments


def find_address(content: str) -> str:
    """
    judge whether a str contains an address
    :param content: post or comment content
    :return: the address we find or None
    """
    ind = content.find("0x")
    if ind == -1:
        return None
    else:
        return content[ind : ind + 40 + 2]


def store_author_address(
    pairs: List[Tuple[str, str]], output_name="user_addresses.csv"
) -> None:
    df = pd.DataFrame(data=pairs, columns=["user name", "address"])
    df.to_csv(output_name, index=False)


if __name__ == "__main__":
    decrypt_login_info()
    headers = update_login_headers()
    reddit = login_praw()
    for query in QUERIES:
        results = search(query=query, headers=headers)
        #all_authors = []
        #all_comments = []
        authors_comments_pairs = set()
        print(f"length of results {len(results)}")
        for ind in trange(len(results)):
            # print(url)
            url = results[ind]
            time.sleep(2)
            # url = "https://www.reddit.com/r/NFTsMarketplace/comments/qjkn6x/giveaway_elitenft_presents_diamond_death_50_up/"
            authors, comments = get_comments(url, reddit)
            authors, comments = filter_addresses(authors, comments)
            # all_authors += authors
            # all_comments += comments
            for t in zip(authors, comments):
                authors_comments_pairs.add(t)

    store_author_address(authors_comments_pairs, "user_addresses_removed_dup.csv")
