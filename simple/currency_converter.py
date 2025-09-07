# Currency Converter - Pure Python (Offline) with country names

# Exchange rates relative to USD
exchange_rates = {
    'USD': 1.0,      # United States Dollar
    'INR': 83.0,     # Indian Rupee
    'EUR': 0.92,     # Euro
    'JPY': 145.0,    # Japanese Yen
    'GBP': 0.78,     # British Pound
    'AUD': 1.52,     # Australian Dollar
    'CAD': 1.36,     # Canadian Dollar
    'CNY': 7.24,     # Chinese Yuan
    'CHF': 0.85,     # Swiss Franc
    'SGD': 1.35      # Singapore Dollar
}

# Currency code to country name mapping
currency_names = {
    'USD': 'United States Dollar',
    'INR': 'Indian Rupee',
    'EUR': 'Euro (European Union)',
    'JPY': 'Japanese Yen',
    'GBP': 'British Pound Sterling',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'CNY': 'Chinese Yuan Renminbi',
    'CHF': 'Swiss Franc',
    'SGD': 'Singapore Dollar'
}

print("=== Simple Currency Converter ===")
print("Available currencies:")
for code, name in currency_names.items():
    print(f"{code} - {name}")
print("\nType 'exit' anytime to quit.\n")

while True:
    from_currency = input("From currency code: ").upper()
    if from_currency == "EXIT":
        break

    to_currency = input("To currency code: ").upper()
    if to_currency == "EXIT":
        break

    # Validate currency codes
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        print("\nInvalid currency code. Please choose from the available list:\n")
        for code, name in currency_names.items():
            print(f"{code} - {name}")
        print()
        continue

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.\n")
        continue

    # Convert to USD first, then to target currency
    amount_in_usd = amount / exchange_rates[from_currency]
    converted_amount = amount_in_usd * exchange_rates[to_currency]

    print(f"\n{amount} {currency_names[from_currency]} ({from_currency}) = "
          f"{converted_amount:.2f} {currency_names[to_currency]} ({to_currency})\n")
