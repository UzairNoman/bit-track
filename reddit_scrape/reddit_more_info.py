"""
scrape more info from Reddit based on User Name
"""
from typing import List, Dict
from .search import decrypt_login_info, update_login_headers
import json
import time
import pandas as pd
import requests
import datetime
from tqdm import trange

USER_ABOUT_API_ADDRESS = "https://oauth.reddit.com/user/username/about?"


def get_user_names_from_csv(csv_file: str) -> List[str]:
    """
    read scraped user name from csv data
    :param csv_file: path to csv file
    :return: user name list
    """
    df = pd.read_csv(csv_file)
    return list(df["user name"])


def calculate_creation_date(seconds: float) -> str:
    start = datetime.datetime(1970, 1, 1, 0, 0, 0)
    creation_date = start + datetime.timedelta(seconds=seconds)
    return str(creation_date)


def find_user(username: str, headers: Dict) -> Dict:
    params = {"username": username}
    res = requests.get(USER_ABOUT_API_ADDRESS, headers=headers, params=params)
    try:
        res = res.json()
        icon_img = res["data"]["icon_img"]
        # seconds from 1970.1.1
        account_creation_time = res["data"]["created"]
        account_creation_time = calculate_creation_date(account_creation_time)
    except KeyError:
        return {
            "user name": username,
            "icon_img": "-",
            "account_creation_time": "-",
        }
    except json.decoder.JSONDecodeError:
        return {
            "user name": username,
            "icon_img": "-",
            "account_creation_time": "-",
        }

    return {
        "user name": username,
        "icon_img": icon_img,
        "account_creation_time": account_creation_time,
    }


if __name__ == "__main__":
    names = get_user_names_from_csv("./reddit_scrape/user_addresses_removed_dup.csv")
    decrypt_login_info()
    headers = update_login_headers()
    df = pd.read_csv("./reddit_scrape/user_addresses_removed_dup.csv")
    df["icon_img"] = "-"
    df["account_creation_time"] = "-"
    for ind in trange(len(names)):
        name = names[ind]
        time.sleep(1)
        res = find_user(name, headers)
        df.loc[(df['user name'] == res["user name"], "icon_img")] = res["icon_img"]
        df.loc[(df['user name'] == res["user name"],"account_creation_time")] = res["account_creation_time"]
    df.to_csv("test.csv", index=False)



