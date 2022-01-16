"""
mine personal info from twitter account's introduction
"""
import pandas as pd


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
        # print(ind, description)
        # print(df.iloc[0,])
        if description.find("https") != -1:
            ind_list.append(ind)
        #break
    sub_table = df.iloc[ind_list]
    print(sub_table.shape) # 75 rows
    sub_table.to_csv("description_with_link.csv", index=False)


def count_contain_NFTs(df):
    df = pd.read_csv(df)
    descriptions = df["twitter_description"]
    count = 0
    for ind, description in enumerate(list(descriptions)):
        lower_description = description.lower()
        if lower_description.find("nfts") != -1:
            count += 1
            print(description)
            print("---------------")
    print(count)

def count_emails(df):
    pass


if __name__ == "__main__":
    #twitter = select_twitter_with_intro("./addresses_with_twitter.csv")
    #print(twitter.shape) # 916 with description
    #filter_out_link("./twitter_with_description.csv")
    count_contain_NFTs("./twitter_with_description.csv")