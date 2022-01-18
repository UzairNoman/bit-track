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

### Scrape Reddit


### Scrape Twitter
Make sure to have pandas installed `pip install pandas` `conda install -c anaconda pandas`.
You can tinker with the code using deds.ipynb code or simply run the main.py file. The file contains the necessary sleep function which runs after 450 twitter API calls to workaround the rate limiting of twitter APIs.

Leave the code running for hours :)

![Screenshot_5](https://user-images.githubusercontent.com/12785891/149800129-20fea26b-b4ac-4346-8af8-8a2ae441af35.jpg)



### Scrape Etherscan 


### Merge Dataset 


### Data Analysis 


## Contact 

- Shuo Chen, shuo.chen@campus.lmu.de
- Uzair Norman, u.noman@campus.lmu.de