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
├─twitter_fetch
│  │  dummy.py
│  │  main.py
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
Make sure to have pandas installed `pip install pandas` `conda install -c anaconda pandas`.
You can tinker with the code using deds.ipynb code or simply run the main.py file. The file contains the necessary sleep function which runs after 450 twitter API calls to workaround the rate limiting of twitter APIs.

Leave the code running for hours :)

![Screenshot_5](https://user-images.githubusercontent.com/12785891/149800129-20fea26b-b4ac-4346-8af8-8a2ae441af35.jpg)



## EthScan Scrape 


## Merge Dataset 


## Data Analysis 
