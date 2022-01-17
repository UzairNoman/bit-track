"""
this code is used to analyze the scraped data
"""
import pandas as pd
import json


def _count_active_account(balance_sheet):
    count = 0
    with open("./merge_dataset/transaction_record_simplify.jsonl", "r") as f:
        for line in f.readlines():
            record = json.loads(line)
            address = record["address"]
            balance = balance_sheet.loc[balance_sheet["address"] == address]
            try:
                balance = float(balance["balance"].values[0])
                if balance > 0 and len(record["transactions"]) > 0:
                    count += 1
            except:
                continue

    return count


def count_active_account():
    count = 0
    balance_sheet = pd.read_csv("./merge_dataset/user_addresses_balance.csv")
    count = _count_active_account(balance_sheet)
    print(f"==== #active account {count} in total , percentage {count / balance_sheet.shape[0] :.3f}")  # 2634
    print(f"==== #deat account {balance_sheet.shape[0] - count} in total, percentage {1 - count / balance_sheet.shape[0]:.3f}")


def count_total_reddit():
    final_info = pd.read_csv("./merge_dataset/user_addresses_balance.csv")
    print(f"==== #records from Reddit in total: {final_info.shape[0]}")


def count_matches_twitter():
    twitter_append = pd.read_csv("./merge_dataset/final_info.csv")
    final_info = pd.read_csv("./merge_dataset/user_addresses_balance.csv")
    total_reddit = final_info.shape[0]
    has_twitter = twitter_append[~twitter_append["twitter_username"].isna()]
    has_twitter.to_csv("./revelation/addresses_with_twitter.csv", index=False )
    active_account = _count_active_account(has_twitter)

    print(f"==== #matches in twitter : {has_twitter.shape[0]}; percentage : {has_twitter.shape[0] / total_reddit : .2f}")
    print(f"==== #matches in twitter with active address : {active_account}; percentage : {active_account / has_twitter.shape[0]: .2f}")


if __name__ == "__main__":
    count_total_reddit()
    count_active_account()
    count_matches_twitter()