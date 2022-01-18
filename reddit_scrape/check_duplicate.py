import pandas as pd

info = pd.read_csv("./user_addresses.csv")
user_name = set()
addresses = set()
for name in info["user name"]:
    user_name.add(name)
for addres in info["address"]:
    addresses.add(addres)
print(len(user_name))
print(len(addresses))
