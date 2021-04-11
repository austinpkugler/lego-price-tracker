# Lego Price Tracker
A realtime tracker of Lego's price per pound using eBay listings. A mean
selling price is calculated every 2.5 seconds by averaging 100 listings
of bulk Lego for sale. This value is visualized in a live graph.

Built in Python using the ebaysdk, tkinter, matplotlib, and pandas modules.

# Using the Price Tracker
## Setting Up the Repository
Clone this repository with:
```
$ git clone https://github.com/austinpkugler/lego-price-tracker.git
```
Create a Python virtual environment inside the cloned repo:
```
$ python3 -m venv env
```
Activate the environment (modify path as needed):
```
$ source /home/user/Documents/projects/lego-price-tracker/env/bin/activate
```
Install the required modules:
```
$ pip3 install -r requirements.txt
```

## Connecting to the eBay API
1. Register an account for the
[eBay developers program](https://developer.ebay.com/). You will likely
need to wait for your account to be approved after registering. Accounts
are usually approved by eBay after one business day.

2. Create a production keyset by clicking "create a keyset."

3. Copy your app ID token and replace the
`LEGO_PRICE_TRACKER_APPID_HERE` with it in the `ebay.yaml` file included
in this repository.

**Note:** eBay's developer API limits calls to 5,000 per day. The price
tracker app performs a call every 2.5 seconds, exceeding this limit
after ~3.5 hours.

## Running the Price Tracker
Simply execute the `main.py` script to run the app:
```
python3 main.py
```
