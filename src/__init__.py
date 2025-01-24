import argparse, json, os, tempfile
from pathlib import Path
from datetime import datetime

# Use the system's temporary directory for storage
TEMP_DIR = Path(tempfile.gettempdir()) / "expense-tracker"
EXPENSES_FILE = TEMP_DIR / "expenses.json"


def ensure_expenses_file():
    """Ensure the storage directory and JSON file exist."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    if not EXPENSES_FILE.exists():
        # print(f"Creating file at {EXPENSES_FILE}")  # Debugging line
        with EXPENSES_FILE.open("w") as f:
            json.dump([], f)


def load_expenses():
    """Function to load expenses from file"""
    ensure_expenses_file()
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    """Function to save expenses to file"""
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)


def add_expense(description, amount):
    """Add expense function"""
    expenses = load_expenses()
    expense_id = len(expenses) + 1
    expense = {
        'id': expense_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'description': description,
        'amount': float(amount)
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f'Expense added successfully (ID: {expense_id})')


def delete_expense(expense_id):
    """Delete expense function"""
    expenses = load_expenses()
    expense = next((e for e in expenses if e['id'] == expense_id), None)
    if expense:
        expenses.remove(expense)
        save_expenses(expenses)
        print('Expense deleted successfully')
    else:
        print(f'Expense with ID {expense_id} not found')


def list_expenses():
    """List expenses function"""
    expenses = load_expenses()
    if expenses:
        print('ID  Date       Description  Amount')
        for expense in expenses:
            print(f'{expense["id"]}   {expense["date"]}  {expense["description"]}  ${expense["amount"]:.2f}')
    else:
        print('No expenses recorded.')


def summary(month=None):
    """View summary of expenses"""
    expenses = load_expenses()
    if month:
        expenses = [e for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').month == month]

    total = sum(e['amount'] for e in expenses)
    if month:
        print(f'Total expenses for month {month}: ${total:.2f}')
    else:
        print(f'Total expenses: ${total:.2f}')


def cli():
    """Main function to handle command-line arguments"""
    parser = argparse.ArgumentParser(description='Expense Tracker')

    subparsers = parser.add_subparsers()

    # Add expense
    add_parser = subparsers.add_parser('add', help='Add an expense')
    add_parser.add_argument('--description', required=True, help='Description of the expense')
    add_parser.add_argument('--amount', required=True, type=float, help='Amount of the expense')
    add_parser.set_defaults(func=lambda args: add_expense(args.description, args.amount))

    # Delete expense
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', required=True, type=int, help='ID of the expense to delete')
    delete_parser.set_defaults(func=lambda args: delete_expense(args.id))

    # List expenses
    list_parser = subparsers.add_parser('list', help='List all expenses')
    list_parser.set_defaults(func=lambda args: list_expenses())

    # Summary
    summary_parser = subparsers.add_parser('summary', help='Show summary of expenses')
    summary_parser.add_argument('--month', type=int, help='Month for which to show summary')
    summary_parser.set_defaults(func=lambda args: summary(args.month))

    args = parser.parse_args()
    args.func(args)
