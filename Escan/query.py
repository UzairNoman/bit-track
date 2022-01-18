from typing import List, Dict

import pandas as pd
import time
from utils.static_params import ENC_ETH_TOKEN
from os.path import exists
from cryptography.fernet import Fernet
import requests
from tqdm import tqdm
import json

ETH_TOKEN = ""
API_ADDRESS = "https://api.etherscan.io/api?"


def decrypt_token():
    if exists("./utils/KEY_FILE"):
        with open("./utils/KEY_FILE") as f:
            key = f.read()
    else:
        key = input("input key for decryption: ")
    key = key.encode()
    fernet = Fernet(key)
    global ETH_TOKEN
    ETH_TOKEN = fernet.decrypt(ENC_ETH_TOKEN)


def get_addresses_from_csv(csv_file: str) -> List[str]:
    df = pd.read_csv(csv_file)
    return list(df["address"])


def get_balance(address: str) -> float:
    assert ETH_TOKEN != ""
    # addresses = ",".join(addresses)
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": ETH_TOKEN,
    }
    try:
        res = requests.get(API_ADDRESS, params=params)
        res = res.json()
        balance = int(res["result"]) * 1e-18
    except:
        balance = 0
    return balance


def get_balance_list(address_list: List[str]) -> List[float]:
    balance_list = []
    for address in tqdm(address_list):
        time.sleep(0.4)
        balance_list.append(get_balance(address))
    return balance_list


def get_transactions(address: str) -> str:
    assert ETH_TOKEN != ""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 100,
        "sort": "asc",
        "apikey": ETH_TOKEN,
    }
    res = requests.get(API_ADDRESS, params=params)
    res = res.json()
    transactions = res["result"]
    record = {"address": address, "transactions": transactions}
    return json.dumps(record)


def store_transactions(address_list: List[str], output_file: str) -> None:
    if not exists("./Escan/" + output_file):
        with open("./Escan/" + output_file, "w") as f:
            f.write("")
    else:
        with open("./Escan/" + output_file, "r+") as f:
            f.truncate(0)
    for address in tqdm(address_list):
        time.sleep(0.4)
        record = get_transactions(address)
        with open("./Escan/" + output_file, "a") as f:
            f.write(record + "\n")


def store_balance(address_list: List[str], balance_list: List[float]) -> None:
    df = pd.read_csv("./reddit_scrape/user_addresses_removed_dup.csv")
    df["balance"] = "-"
    for address, balance in zip(address_list, balance_list):
        df.loc[(df["address"] == address, "balance")] = balance
    df.to_csv("user_addresses_balance.csv", index=False)


if __name__ == "__main__":
    decrypt_token()
    address_list = get_addresses_from_csv(
        "./reddit_scrape/user_addresses_removed_dup.csv"
    )
    # address_list = ["0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
    #                 "0xC5dA9792E272691b890B29d4351268A3A9eD50d8",
    #                 "0xb915c55871d860666e740eda88389dfcd80112d6",
    #                 "0x1f6460410f226ca32a86874cfa725f1e7b3ebd61"]
    print("Query for balance")
    balance_list = get_balance_list(address_list)
    store_balance(address_list, balance_list)
    # print((get_transactions(address_list[0])))
    print("Query for transactions")
    store_transactions(address_list, "transaction_record.jsonl")
