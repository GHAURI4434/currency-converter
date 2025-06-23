import requests

def convert_currency(amount, from_currency, to_currency):
    api_key = "726643e5a8b40fecb29a24d3"  # ← Your API key here
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency.upper()}/{to_currency.upper()}/{amount}"

    try:
        response = requests.get(url)
        data = response.json()

        print("🔍 API Response:", data)  # Optional: for debugging

        if data['result'] == 'success':
            result = data['conversion_result']
            print(f"\n✅ {amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}")
        else:
            print("❌ Conversion failed. Reason:", data.get('error-type', 'Unknown'))
    except Exception as e:
        print("❌ Error occurred:", e)

def main():
    print("💱 Currency Converter (using exchangerate-api)\n")

    try:
        amount = float(input("Enter amount: "))
        from_currency = input("From currency (e.g., USD): ").strip()
        to_currency = input("To currency (e.g., PKR): ").strip()

        if not from_currency or not to_currency:
            print("❌ Currency code cannot be empty.")
            return

        convert_currency(amount, from_currency, to_currency)

    except ValueError:
        print("❌ Invalid amount.")

if __name__ == "__main__":
    main()
10