"""
merge info from reddit, twitter, ETH Scan together
"""
import pandas as pd
import json


def merge_reddit_twitter_balance(
    reddit_data: str, twitter_data: str, balance_data: str
) -> pd.DataFrame:
    """
    merge reddit csv, twitter csv and balance. Store the result
    :param reddit_data: path to reddit csv
    :param twitter_data: path to twitter csv
    :param balance_data: path to balance csv
    :return: None
    """
    reddit_data = pd.read_csv(reddit_data)
    twitter_data = pd.read_csv(twitter_data)
    balance_data = pd.read_csv(balance_data)

    reddit_data.rename(
        columns={
            "user name": "reddit_user_name",
            "icon_img": "reddit_avatar",
            "account_creation_time": "reddit_account_creation_time",
        },
        inplace=True,
    )
    twitter_data.rename(
        columns={
            "user name": "reddit_user_name",
            "description": "twitter_description",
            "location": "twitter_location",
            "avatar": "twitter_avatar",
        },
        inplace=True,
    )

    balance_data.rename(columns={"user name": "reddit_user_name",}, inplace=True)
    twitter_data.drop(twitter_data.columns[-4:], axis=1, inplace=True)

    reddit_data = reddit_data.merge(twitter_data)
    reddit_data = reddit_data.merge(balance_data)
    return reddit_data


def merge_all_info_to_jsonl(final_info: str, transactions: str, output: str) -> None:
    """
    merge all info into json line with transactions
    :param final_info: csv with all info from twitter, reddit, balance
    :param transactions: transaction records jsonl
    :param output: output file path
    :return: None
    """
    final_info = pd.read_csv(final_info)
    with open(transactions, "r") as f:
        for line in f.readlines():
            record = json.loads(line)
            row = final_info.loc[final_info["address"] == record["address"]]
            for attribute in final_info.columns:
                if attribute == "address":
                    continue
                try:
                    record[attribute] = row[attribute].values[0]
                except:
                    print(row[attribute])
            with open(output, "a") as f2:
                record = json.dumps(record)
                f2.write(record + "\n")


if __name__ == "__main__":
    result = merge_reddit_twitter_balance("./reddit_more_info.csv", "./twitter_data_append.csv", "./user_addresses_balance.csv")
    result.to_csv("./final_info.csv", index=False)
    merge_all_info_to_jsonl(
        "./final_info.csv",
        "./transaction_record_simplify.jsonl",
        "./final_info_transactions.jsonl",
    )
