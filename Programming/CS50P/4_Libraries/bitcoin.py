import sys
import requests

def main():
    # Validate command-line input
    if len(sys.argv) != 2:
        sys.exit("Usage: python bitcoin.py <number_of_bitcoins>")

    try:
        n = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument must be a number")

    # Replace with your real API key
    API_KEY = "51eae59644bd1b3cac51642a0a794dc1dc41c3b1d4140818af6cf1ff9d9eb167"
    url = f"https://rest.coincap.io/v3/assets/bitcoin?apiKey={API_KEY}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        sys.exit("Request failed")

    try:
        data = r.json()
        price_usd_str = data["data"]["priceUsd"]
        price_usd = float(price_usd_str)
    except (KeyError, TypeError, ValueError):
        sys.exit("Invalid data format")

    total_cost = n * price_usd
    # Format with thousands separator and four decimal places
    print(f"${total_cost:,.4f}")

if __name__ == "__main__":
    main()
