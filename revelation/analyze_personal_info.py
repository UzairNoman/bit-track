"""
mine personal info from twitter account's introduction
"""
import pandas as pd
import re


def select_twitter_with_intro(df):
    twitter = pd.read_csv(df)
    print(twitter.shape)
    twitter = twitter[~twitter["twitter_description"].isna()]
    twitter.to_csv("twitter_with_description.csv", index=False)
    return twitter


def filter_out_link(df):
    df = pd.read_csv(df)
    descriptions = df["twitter_description"]
    ind_list = []
    for ind, description in enumerate(list(descriptions)):
        if description.find("https") != -1:
            ind_list.append(ind)
    sub_table = df.iloc[ind_list]
    print(sub_table.shape) # 75 rows
    sub_table.to_csv("description_with_link.csv", index=False)


# def count_contain_NFTs(df):
#     df = pd.read_csv(df)
#     descriptions = df["twitter_description"]
#     count = 0
#     for ind, description in enumerate(list(descriptions)):
#         lower_description = description.lower()
#         if lower_description.find("nfts") != -1:
#             count += 1
#             print(description)
#             print("---------------")
#     print(count)


def count_info(df):
    df = pd.read_csv(df)
    descriptions = df["twitter_description"]
    email_count = 0
    phone_count = 0
    nft_count = 0
    IG_count = 0
    discord_count = 0
    email_regex = re.compile(r"[\w-]+@([\w-]+\.)+[\w-]+")
    for ind, description in enumerate(list(descriptions)):
        if email_regex.search(description) is not None:
            email_count += 1
        if description.lower().find("phone") != -1:
            phone_count += 1
        if description.lower().find("nft") != -1:
            nft_count += 1
        if description.lower().find("discord") != -1:
            discord_count += 1
    print(f"==== # rows contains email: {email_count}") # 10
    print(f"==== # rows contains phone: {phone_count}")
    print(f"==== # rows contains NFTs: {nft_count}")
    print(f"==== # rows contains Discord: {discord_count}")


if __name__ == "__main__":
    #twitter = select_twitter_with_intro("./addresses_with_twitter.csv")
    #print(twitter.shape) # 916 with description
    count_info("./twitter_with_description.csv")