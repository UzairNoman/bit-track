"""
remove useless attributes in transaction records
"""
import json

with open("transaction_record.jsonl", "r") as f:
    for line in f.readlines():
        record = json.loads(line)
        for i, tran in enumerate(record["transactions"]):
            del tran["blockNumber"]
            del tran["hash"]
            del tran["nonce"]
            del tran["blockHash"]
            del tran["transactionIndex"]
            del tran["gas"]
            del tran["gasPrice"]
            del tran["isError"]
            del tran["txreceipt_status"]
            del tran["input"]
            del tran["contractAddress"]
            del tran["cumulativeGasUsed"]
            del tran["gasUsed"]
            del tran["confirmations"]
            record["transactions"][i] = tran
        with open("../merge_dataset/transaction_record_simplify.jsonl", "a") as f2:
            record = json.dumps(record)
            f2.write(record + "\n")
