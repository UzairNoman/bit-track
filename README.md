# bit-track
A project for Blockchain(ETH) user identity revelation in Seminar *Data Ethics and Data Security* WS2021.  

<details>
<summary>Structure of the code</summary>
<pre><code>
bit-track.
│  .gitignore
│  README.md
│  requirements.txt
├─Escan # query Etherscan API for ETH balance and transaction history
│  │  clean_tran_records.py
│  │  count_active_account.py
│  │  query.py
│  │  transaction_record.jsonl
├─merge_dataset # merge dataset from Reddit, Twitter. Eliminate useless attributes of transactions
│  |   final_info.csv
│  |   final_info_transactions.jsonl
│  |   merge_dataset.py
│  |   reddit_more_info.csv
│  |   transaction_record_simplify.jsonl
│  |   twitter_data_append.csv
│  |   user_addresses_balance.csv
├─reddit_scrape # scrape users with addresses from Reddit 
│  │  check_duplicate.py
│  │  reddit_more_info.py
│  │  search.py
│  │  user_addresses.csv
│  │  user_addresses_removed_dup.csv
├─twitter_fetch # find matches from Twitter
│  │  dummy.py
│  │  main.py
├─revelation # Analyze matches for personal information 
│  │  data_analysis.py
│  │  addresses_with_twitter.csv
└─utils # static params such as encryped API tokens 
    │  static_params.py
</code></pre>
</details>

## Getting Started
This project is built with `python 3.8.8` in Miniconda environment.

### Installation
```bash
git clone https://github.com/UzairNoman/bit-track.git
cd bit-track 
conda create -n bit-track python=3.8.8 
conda activate bit-track
pip install -r requirements.txt
mv PATH_TO_THE_KEY_FILE/KEY_FILE ./utils/
```

## Usage

### 1. Scrape Reddit

```bash
cd bit-track 
python -m reddit_scrape.search
python -m reddit_scrape.reddit_more_info
```

`reddit_scrape/search.py` and `reddit_scrape/reddit_more_info.py` are responsible for scraping  user info and addresses from Reddit.

- `reddit_scrape/search.py` will search queries from `utils/static_params.py` and get 100 results for each query. For each result, we will iterate all comments for valid addresses. The result is stored as `reddit_scrape/user_addresses_removed_dup.csv`. It will take about 5 minutes.
- `reddit_scrape/reddit_more_info.py` will read the `reddit_scrape/user_addresses_removed_dup.csv` generated before, access the Reddit API for more personal info, like avatars and account creation date, for each record. It will take about 3 hours. 



### 2. Scrape Twitter
```bash
cd bit-track
python -m twitter_fetch.main
```

- `twitter_fetch/main.py` will read `reddit_scrape/user_addresses_removed_dup.csv` generated before, access the API from twitter to search for posts containing address in each record from Reddit, and to obtain the Twitter user information to `twitter_data_append.csv`. 
- The file contains the necessary sleep function which runs after 450 Twitter API calls to work around the rate limiting of Twitter APIs. It will approximately take 9 hours.

### 3. Scrape Etherscan 

```bash
cd bit-track
python -m Escan.query
```

- `Escan/query.py` will read `./reddit_scrape/user_addresses_removed_dup.csv` and query Etherscan API for balance and transaction history. 
- The results are stored as file `user_addresses_balance.csv` and `transaction_record.jsonl`
- Query for balance will take 2 hours and query for transactions will take 3 hours or so.

```bash 
cd Escan
python clean_tran_records.py
```

- `Escan/clean_tran_records.py` is used to delete several attributes from transaction history.
- The output is `transaction_record_simplify.jsonl`

### 4. Merge Dataset 

```bash
cd merge_dataset
python merge_dataset.py
```

- `merge_dateset/merge_dataset.py` will merge data from Reddit, Twitter and balance together and generate `final_info.csv`
- `final_info.csv` is further merged with transaction history and result in `final_info_transactions.jsonl`.
- These final results are used in `bit-track-app`, the web front, for final demonstration.


### 5. Data Analysis 
```bash
cd bit-track
python -m revelation.data_analysis
```

- count how many active accounts, how many matches in Twitter. 

```bash
cd revelation
python analyze_personal_info.py
```
- count how many mails, links in Twitter descriptions. 


## Contact 

- Shuo Chen, shuo.chen@campus.lmu.de
- Uzair Norman, u.noman@campus.lmu.de