import unittest
from unittest.mock import patch, MagicMock
from src import load_expenses, add_expense, delete_expense, list_expenses, summary


class TestExpenseTracker(unittest.TestCase):

    @patch("builtins.open")
    @patch("src.ensure_expenses_file")
    @patch("os.path.exists", return_value=True)  # Mocking os.path.exists to return True
    def test_load_expenses_file_exists_with_data(self, mock_exists, mock_ensure_expenses_file, mock_open):
        # Mock the file contents to be returned by json.load
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = '[{"id": 1, "description": "Lunch", "amount": 10.0}]'
        mock_file.__enter__.return_value.read.return_value = '[{"id": 1, "description": "Lunch", "amount": 10.0}]'

        # Simulate the behavior of json.load
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = '[{"id": 1, "description": "Lunch", "amount": 10.0}]'

        # Call the function
        expenses = load_expenses()

        # Verify that the expenses were loaded correctly
        self.assertEqual(expenses, [{"id": 1, "description": "Lunch", "amount": 10.0}])

    @patch("builtins.open")
    @patch("src.ensure_expenses_file")
    @patch("os.path.exists", return_value=True)  # File exists but is empty
    def test_load_expenses_file_exists_but_empty(self, mock_exists, mock_ensure_expenses_file, mock_open):
        # Simulate an empty file
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = '[]'

        # Call the function
        expenses = load_expenses()

        # Verify that the expenses list is empty
        self.assertEqual(expenses, [])

    @patch("builtins.open")
    @patch("src.ensure_expenses_file")
    @patch("os.path.exists", return_value=False)  # Simulate the file does not exist
    def test_load_expenses_file_does_not_exist(self, mock_exists, mock_ensure_expenses_file, mock_open):
        # We expect the file to be created during the execution
        mock_open.return_value.__enter__.return_value = MagicMock()

        # Call the function
        expenses = load_expenses()

        # Ensure that ensure_expenses_file was called to create the file
        mock_ensure_expenses_file.assert_called_once()

        # Ensure that an empty list is returned
        self.assertEqual(expenses, [])

    @patch("src.save_expenses")
    @patch("src.load_expenses")
    def test_add_expense(self, mock_load_expenses, mock_save_expenses):
        # Mock data
        expenses = [{"id": 1, "description": "Lunch", "amount": 10.0}]
        description = "Coffee"
        amount = 5.0

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to add the expense
        add_expense(description, amount)

        # Ensure that save_expenses was called with the correct arguments
        mock_save_expenses.assert_called_once_with(expenses)

        # Ensure the ID is incremented correctly and the expense is added
        self.assertEqual(expenses[1]['description'], "Coffee")
        self.assertEqual(expenses[1]['amount'], 5.0)

    @patch("builtins.print")
    @patch("src.save_expenses")
    @patch("src.load_expenses")
    def test_add_expense_print_message(self, mock_load_expenses, mock_save_expenses, mock_print):
        # Mock data
        expenses = [{"id": 1, "description": "Lunch", "amount": 10.0}]
        description = "Dinner"
        amount = 20.0

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to add the expense
        add_expense(description, amount)

        # Verify that print was called with the correct message
        expected_message = f"Expense added successfully (ID: {len(expenses)})"
        mock_print.assert_called_once_with(expected_message)

    @patch("src.save_expenses")
    @patch("src.load_expenses")
    @patch("builtins.print")
    def test_delete_expense(self, mock_print, mock_load_expenses, mock_save_expenses):
        # Mock data
        expenses = [
            {"id": 1, "description": "Lunch", "amount": 10.0},
            {"id": 2, "description": "Coffee", "amount": 5.0}
        ]
        expense_id = 1

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to delete the expense
        delete_expense(expense_id)

        # Ensure that the expense was deleted and save_expenses was called with updated expenses
        mock_save_expenses.assert_called_once_with([{"id": 2, "description": "Coffee", "amount": 5.0}])

        # Verify that print was called with the correct success message
        mock_print.assert_called_once_with('Expense deleted successfully')

    @patch("src.save_expenses")
    @patch("src.load_expenses")
    @patch("builtins.print")
    def test_delete_expense_not_found(self, mock_print, mock_load_expenses, mock_save_expenses):
        # Mock data
        expenses = [
            {"id": 1, "description": "Lunch", "amount": 10.0}
        ]
        expense_id = 999  # ID that does not exist

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to delete the expense
        delete_expense(expense_id)

        # Ensure save_expenses was not called since the expense wasn't found
        mock_save_expenses.assert_not_called()

        # Verify that print was called with the correct error message
        mock_print.assert_called_once_with(f'Expense with ID {expense_id} not found')

    @patch("builtins.print")
    @patch("src.load_expenses")
    def test_list_expenses(self, mock_load_expenses, mock_print):
        # Mock data
        expenses = [
            {"id": 1, "date": "2025-01-01", "description": "Lunch", "amount": 10.0},
            {"id": 2, "date": "2025-01-02", "description": "Coffee", "amount": 5.0}
        ]

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to list expenses
        list_expenses()

        # Verify that print was called with the correct formatted output
        expected_output = [
            "ID  Date       Description  Amount",
            "1   2025-01-01  Lunch  $10.00",
        ]
        for line in expected_output:
            mock_print.assert_any_call(line)

    @patch("builtins.print")
    @patch("src.load_expenses")
    def test_list_expenses_empty(self, mock_load_expenses, mock_print):
        # Mock data (empty list of expenses)
        mock_load_expenses.return_value = []

        # Call the function to list expenses
        list_expenses()

        # Verify that print was called with "No expenses recorded."
        mock_print.assert_called_once_with('No expenses recorded.')

    @patch("builtins.print")
    @patch("src.load_expenses")
    def test_summary(self, mock_load_expenses, mock_print):
        # Mock data
        expenses = [
            {"id": 1, "date": "2025-01-01", "description": "Lunch", "amount": 10.0},
            {"id": 2, "date": "2025-01-02", "description": "Coffee", "amount": 5.0}
        ]

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to get summary (no month specified)
        summary()

        # Verify that print was called with the correct total expenses
        mock_print.assert_called_once_with('Total expenses: $15.00')

    @patch("builtins.print")
    @patch("src.load_expenses")
    def test_summary_with_month(self, mock_load_expenses, mock_print):
        # Mock data
        expenses = [
            {"id": 1, "date": "2025-01-01", "description": "Lunch", "amount": 10.0},
            {"id": 2, "date": "2025-01-02", "description": "Coffee", "amount": 5.0}
        ]

        # Mock load_expenses to return existing expenses
        mock_load_expenses.return_value = expenses

        # Call the function to get summary for a specific month (January)
        summary(month=1)

        # Verify that print was called with the correct total for January
        mock_print.assert_called_once_with('Total expenses for month 1: $15.00')


if __name__ == "__main__":
    unittest.main()
