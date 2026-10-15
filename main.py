import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DATA_FILE = Path(__file__).with_name("budget_data.json")


def load_data():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("Invalid data format. Starting with an empty budget.")
        return []

    except (json.JSONDecodeError, OSError):
        print("Could not read saved data. Starting with an empty budget.")
        return []


def save_data(transactions):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)


def get_amount():
    try:
        amount = float(input("Enter amount (₹): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return None

        if not amount < float("inf"):
            print("Please enter a valid amount.")
            return None

        return round(amount, 2)

    except ValueError:
        print("Please enter a valid number.")
        return None


def add_transaction(transactions, transaction_type):
    amount = get_amount()

    if amount is None:
        return

    category = input("Enter category: ").strip().title()

    if not category:
        print("Category cannot be empty.")
        return

    description = input("Enter description: ").strip()

    if not description:
        description = category

    transaction = {
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    transactions.append(transaction)
    save_data(transactions)

    print(f"{transaction_type.title()} recorded successfully!")


def view_transactions(transactions):
    if not transactions:
        print("\nNo transactions recorded yet.")
        return

    print("\n========== TRANSACTION HISTORY ==========")

    for index, transaction in enumerate(transactions, start=1):
        print(
            f"{index}. {transaction['date']} | "
            f"{transaction['type'].title()} | "
            f"₹{transaction['amount']:.2f} | "
            f"{transaction['category']} | "
            f"{transaction['description']}"
        )


def show_summary(transactions):
    income = sum(
        t["amount"] for t in transactions
        if t["type"] == "income"
    )

    expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "expense"
    )

    print("\n========== BUDGET SUMMARY ==========")
    print(f"Total Income:   ₹{income:.2f}")
    print(f"Total Expenses: ₹{expenses:.2f}")
    print(f"Balance:        ₹{income - expenses:.2f}")


def category_summary(transactions):
    categories = defaultdict(float)

    for transaction in transactions:
        if transaction["type"] == "expense":
            categories[transaction["category"]] += transaction["amount"]

    if not categories:
        print("\nNo expenses available for category analysis.")
        return

    print("\n========== EXPENSES BY CATEGORY ==========")

    for category, amount in sorted(categories.items()):
        print(f"{category}: ₹{amount:.2f}")


def delete_transaction(transactions):
    if not transactions:
        print("\nNo transactions available to delete.")
        return

    view_transactions(transactions)

    try:
        number = int(input("\nEnter transaction number to delete: "))

        if not 1 <= number <= len(transactions):
            print("Invalid transaction number.")
            return

        removed = transactions[number - 1]

        confirmation = input(
            f"Delete '{removed['description']}' "
            f"(₹{removed['amount']:.2f})? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            transactions.pop(number - 1)
            save_data(transactions)
            print("Transaction deleted successfully.")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid number.")


def main():
    transactions = load_data()

    while True:
        print("\n========== PERSONAL BUDGET PLANNER ==========")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Budget Summary")
        print("4. View Transactions")
        print("5. View Expenses by Category")
        print("6. Delete Transaction")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            add_transaction(transactions, "income")

        elif choice == "2":
            add_transaction(transactions, "expense")

        elif choice == "3":
            show_summary(transactions)

        elif choice == "4":
            view_transactions(transactions)

        elif choice == "5":
            category_summary(transactions)

        elif choice == "6":
            delete_transaction(transactions)

        elif choice == "7":
            print("Thank you for using Personal Budget Planner!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()