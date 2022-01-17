# bit-track
Blockchain re-identification of users

Structure of the code:

```
bit-track.
│  .gitignore
│  README.md
│  requirements.txt
├─Escan
│  │  clean_tran_records.py
│  │  count_active_account.py
│  │  query.py
│  │  transaction_record.jsonl
├─merge_dataset
│  |   final_info.csv
│  |   final_info_transactions.jsonl
│  |   merge_dataset.py
│  |   reddit_more_info.csv
│  |   transaction_record_simplify.jsonl
│  |   twitter_data_append.csv
│  |   user_addresses_balance.csv
├─reddit_scrape
│  │  check_duplicate.py
│  │  reddit_more_info.py
│  │  search.py
│  │  user_addresses.csv
│  │  user_addresses_removed_dup.csv
├─revelation
│  │  data_analysis.py
│  │  addresses_with_twitter.csv
└─utils
    │  static_params.py
```

## Reddit Scrape
1. install dependencies `pip install -r requirements.txt`
2. ask for key file `KEY_FILE` or key string for decryption of logging information 
3. run code `python search.py` to get a `csv` file with username and addresses. Search queries could be modified in `./reddit_scrape/static_params.py`

## Twitter Scrape 


## EthScan Scrape 


## Merge Dataset 


## Data Analysis 