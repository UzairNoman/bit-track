import requests
import time
import math
import pandas as pd
from cryptography.fernet import Fernet
from twitter_fetch.dummy import dummy_dataset
from utils.static_params import TWITTER_TOKEN
from os.path import exists


def twitter_api(q_string):
    if exists("./utils/KEY_FILE"):
        with open("./utils/KEY_FILE") as f:
            key = f.read()
    else:
        key = input("input key for decryption: ")
    key = key.encode()
    fernet = Fernet(key)
    access_token = fernet.decrypt(TWITTER_TOKEN).decode()
    my_headers = {"Authorization": f"Bearer {access_token}"}

    tweet_fields = "&tweet.fields=text&expansions=author_id"
    user_fields = "&user.fields=description,id,location,name,profile_image_url,protected,public_metrics,url,username,verified,withheld"

    response = requests.get(
        f"https://api.twitter.com/2/tweets/search/recent?query={q_string}{tweet_fields}{user_fields}",
        headers=my_headers,
    )
    print(
        f"https://api.twitter.com/2/tweets/search/recent?query={q_string}{tweet_fields}{user_fields}"
    )
    return response.json()


def makeCalls(
    ind,
    address_list,
    tweet_desc,
    tweet_location,
    tweet_realname,
    tweet_username,
    tweet_avatar,
):
    address_list[ind - 1] = (
        address_list[ind - 1].replace("\n", "").replace("\r", "").strip()
    )
    tweet_json = twitter_api(address_list[ind - 1])
    # tweet_json = dummy_dataset(ind-1,address_list[ind-1])
    print(f"Running call for {ind - 1}")
    if tweet_json.get("meta").get("result_count") == 0:
        tweet_person = {
            "description": "",
            "location": "",
            "name": "",
            "username": "",
            "profile_image_url": "",
        }
    else:

        tweet_person = tweet_json.get("includes").get("users")[0]

    tweet_desc.append(tweet_person.get("description"))
    tweet_location.append(tweet_person.get("location"))
    tweet_realname.append(tweet_person.get("name"))
    tweet_username.append(tweet_person.get("username"))
    tweet_avatar.append(tweet_person.get("profile_image_url"))


if __name__ == "__main__":
    df = pd.read_csv("reddit_scrape/user_addresses_removed_dup.csv")
    address_list = df["address"].tolist()
    users_list = df["user name"].tolist()
    addr_len = len(address_list)

    batch_index = 0
    max_calls = 450
    sleep_time = 16

    global_tweet_desc = []
    global_tweet_location = []
    global_tweet_realname = []
    global_tweet_username = []
    global_tweet_avatar = []

    for i in range(0, math.ceil((addr_len - 1) / max_calls)):
        tweet_desc = []
        tweet_location = []
        tweet_realname = []
        tweet_username = []
        tweet_avatar = []
        print(f"Second loop {i * max_calls} => {addr_len}")
        for j in range(
            (i * max_calls) + 1, addr_len + 1
        ):  # if first +1 is removed, loop will end on 16200 instead of 16374
            makeCalls(
                j,
                address_list,
                tweet_desc,
                tweet_location,
                tweet_realname,
                tweet_username,
                tweet_avatar,
            )
            print(j)

            if j % max_calls == 0:
                print("Getting to sleep")
                time.sleep(60 * sleep_time)
                break

        global_tweet_desc += tweet_desc
        global_tweet_location += tweet_location
        global_tweet_realname += tweet_realname
        global_tweet_username += tweet_username
        global_tweet_avatar += tweet_avatar

    print("--END--")
    result_frame = pd.DataFrame(
        data={
            "user name": users_list,
            "address": address_list,
            "description": global_tweet_desc,
            "location": global_tweet_location,
            "twitter_name": global_tweet_realname,
            "twitter_username": global_tweet_username,
            "avatar": global_tweet_avatar,
        }
    )
    result_frame.to_csv("twitter_data_append.csv", index=False)
