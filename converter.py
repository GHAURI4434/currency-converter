import requests
from datetime import datetime

API_KEY = "726643e5a8b40fecb29a24d3" 
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_supported_currencies():
    url = f"{BASE_URL}/codes"
    try:
        response = requests.get(url)
        data = response.json()

        if data['result'] == 'success':
            codes = [code[0] for code in data['supported_codes']]
            return codes
        else:
            print("❌ Could not fetch supported currencies.")
            return []
    except Exception as e:
        print("❌ Error fetching currencies:", e)
        return []

def convert_currency(amount, from_currency, to_currency):
    url = f"{BASE_URL}/pair/{from_currency.upper()}/{to_currency.upper()}/{amount}"
    try:
        response = requests.get(url)
        data = response.json()

        if data['result'] == 'success':
            return data['conversion_result']
        else:
            print("❌ Conversion failed:", data.get('error-type', 'Unknown error'))
            return None
    except Exception as e:
        print("❌ Error occurred during conversion:", e)
        return None

def save_to_history(amount, from_currency, to_currency, result):
    try:
        with open("history.txt", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now()} | {amount} {from_currency} → {result:.2f} {to_currency}\n")
    except Exception as e:
        print("⚠️ Failed to write to history:", e)


def main():
    print("💱 Advanced Currency Converter (API-based)\n")

    supported = get_supported_currencies()
    if not supported:
        return

    try:
        amount = float(input("Enter amount: "))
        from_currency = input("From currency (e.g., USD): ").strip().upper()
        to_currency = input("To currency (e.g., PKR): ").strip().upper()

        if from_currency not in supported or to_currency not in supported:
            print("❌ Invalid currency code. Check supported currencies.")
            return

        result = convert_currency(amount, from_currency, to_currency)

        if result is not None:
            print(f"\n✅ {amount} {from_currency} = {result:.2f} {to_currency}")
            save_to_history(amount, from_currency, to_currency, result)

            reverse = input("\n🔁 Do you want to reverse convert (y/n)? ").strip().lower()
            if reverse == 'y':
                reverse_result = convert_currency(result, to_currency, from_currency)
                if reverse_result is not None:
                    print(f"↩️  {result:.2f} {to_currency} = {reverse_result:.2f} {from_currency}")
                    save_to_history(result, to_currency, from_currency, reverse_result)

    except ValueError:
        print("❌ Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
