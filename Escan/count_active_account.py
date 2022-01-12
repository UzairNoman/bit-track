"""
calculate how many accounts have zero balance and no transactions
"""
import json
import pandas as pd

count = 0
balance_sheet = pd.read_csv("../merge_dataset/user_addresses_balance.csv")
with open("../merge_dataset/transaction_record_simplify.jsonl", "r") as f:
    for line in f.readlines():
        record = json.loads(line)
        address = record["address"]
        balance = balance_sheet.loc[balance_sheet["address"] == address]
        try:
            balance = float(balance["balance"].values[0])
        except:
            print(balance["balance"].values[0])
        if balance > 0 and len(record["transactions"]) > 0:
            count += 1
print(f"#active account {count}, percentage {count / balance_sheet.shape[0]}") # 2634

