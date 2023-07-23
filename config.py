from functions import load_json_data

OFFERS_PATH = "data/offers.json"
ORDERS_PATH = "data/orders.json"
USERS_PATH = "data/users.json"

offers = load_json_data(OFFERS_PATH)
orders = load_json_data(ORDERS_PATH)
users = load_json_data(USERS_PATH)
