def dummy_dataset(j,addr):

    ugly_res = {
        "includes": {
            "users": [
                {
                    "name": f"Kevin J{j}",
                    "url": "",
                    "protected": False,
                    "id": f"484269760_{j}",
                    "description": f"{addr}_{j}",
                    "location": f"Naija{j}",
                    "username": f"jeemmai{j}",
                    "public_metrics": {
                        "followers_count": 40,
                        "following_count": 294,
                        "tweet_count": 619,
                        "listed_count": 1
                    },
                    "profile_image_url": f"{j}https://pbs.twimg.com/profile_images/1319230711245754369/MsxQbjnu_normal.jpg",
                    "verified": False
                }
            ]
        },
        "meta": {
            "newest_id": "1472231060364791812",
            "oldest_id": "1471780673107148802",
            "result_count": 4
        }
    }
    return ugly_res