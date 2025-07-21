import requests
import time
import datetime
import numpy as np
from sklearn.cluster import DBSCAN
from collections import defaultdict

ETHERSCAN_API_KEY = 'YourApiKeyHere'
BASE_URL = 'https://api.etherscan.io/api'

def get_transactions(address, start_block=0, end_block=99999999):
    url = f'{BASE_URL}?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return data['result']
    return []

def extract_timestamps(transactions):
    return [int(tx['timeStamp']) for tx in transactions]

def cluster_activity(timestamps):
    if not timestamps:
        return []

    timestamps = np.array(timestamps).reshape(-1, 1)
    clustering = DBSCAN(eps=3600 * 6, min_samples=2).fit(timestamps)
    return clustering.labels_

def analyze_address(address):
    txs = get_transactions(address)
    ts = extract_timestamps(txs)
    clusters = cluster_activity(ts)
    cluster_count = len(set(clusters)) - (1 if -1 in clusters else 0)

    if cluster_count > 1:
        print(f"[ALERT] Suspicious cluster activity detected for {address}: {cluster_count} clusters")
    else:
        print(f"[OK] Address {address} shows normal behavior")

def monitor_whales(addresses):
    print(f"[{datetime.datetime.now()}] Starting WhaleWatch...\n")
    for addr in addresses:
        analyze_address(addr)
        time.sleep(1)  # avoid API rate limits

if __name__ == "__main__":
    whales = [
        "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",  # пример "кита"
        "0xfe9e8709d3215310075d67e3ed32a380ccf451c8"
    ]
    monitor_whales(whales)
