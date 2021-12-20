import requests



try:
    #https://api.twitter.com/1.1/search/tweets.json?q=drop your wallet
    access_token = "AAAAAAAAAAAAAAAAAAAAAJesOgEAAAAAhjjjXkVka1TtQ5lxdzIEJtKk6Tw%3DlkuKd4yJE1x29rdaMdvvvh6BoCxFOL8knOxSWL42QG2nU2auvL"
    my_headers = {'Authorization' : f'Bearer {access_token}'}
    response = requests.get('https://api.twitter.com/2/tweets/search/recent?query=drop your wallet', headers=my_headers)
    if (response.status_code == 200):
        print(response.json())
        print("The request was a success!")
    elif (response.status_code == 404):
        print("Result not found!")




# except Error as e:
#     print("Error while connecting to MySQL", e)
finally:
    print("MySQL connection is closed")