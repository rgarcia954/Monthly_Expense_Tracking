# Monthly Expense and Income Manager

A Python program for tracking monthly expenses and income, with intelligent transfer recommendations between checking and savings accounts.

## Features

- **Flexible Data Input**: Import from CSV files or enter data manually
- **Interactive Data Management**: Add, modify, view, and delete expenses and income entries
- **Smart Transfer Calculations**: Automatically calculates recommended transfers from savings to checking based on upcoming expenses
- **Period-Based Analysis**: Divides the month into two periods (1st-15th and 16th-end) for targeted expense management
- **Safety Margin**: Ensures a $1,000 buffer remains in checking account after all expenses
- **Multiple Date Format Support**: Reads CSV files with various date formats (YYYY-MM-DD, M/D/YYYY, etc.)
- **Persistent Storage**: Save and reload data across multiple program runs

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/monthly-expense-manager.git
cd monthly-expense-manager
```

2. Run the program:
```bash
python expense_manager.py
```

## Usage

### First Run (Manual Entry)

1. Run the program
2. Answer "no" when asked if you have a CSV file
3. Enter expense data for each payee
4. Enter income data for checking and savings accounts
5. Review and modify entries if needed
6. Program generates `expense_income_data.csv` and displays analysis

### Subsequent Runs (Using CSV)

1. Run the program
2. Answer "yes" when asked if you have a CSV file
3. Enter filename: `expense_income_data.csv`
4. Review, add, modify, or delete entries as needed
5. Program updates the CSV file and displays analysis

### Data Management Menu

After loading or entering data, you can:
- **View** expenses or income in formatted tables
- **Add** new expenses or income entries
- **Modify** existing entries (amounts, dates, payees)
- **Delete** unwanted entries
- **Continue** to analysis when done

## Supported Payees

- Ameritus
- Capital One
- Chase Visa
- Medicare N
- Amex
- HOA Q
- HOA M
- Citibank Visa
- Apple card RG
- Apple card YG
- United Health
- Medicare Pre
- Other

## Income Sources

- SCCU Checking
- E-Trade Savings

## How Transfer Calculations Work

The program determines transfer needs based on:

1. **Current Date**: Automatically detects which half of the month you're in
2. **Upcoming Expenses**: Only counts expenses due in the current period that haven't passed yet
3. **Safety Margin**: Adds $1,000 buffer to ensure sufficient funds
4. **Smart Filtering**: 
   - Ignores expenses from previous dates (assumes already paid)
   - Excludes next month's expenses from current calculations
   - Only processes expenses in the current month

### Transfer Rules

- **First Half (Days 1-15)**: Transfer covers all expenses due between days 1-15
- **Second Half (Days 16-31)**: Transfer covers all expenses due between days 16-31
- Maximum of two transfers per month (one per period)

## CSV File Format

The program generates and reads CSV files with the following structure:

```csv
Type,Payee,Bank,Amount,Due Date,Balance Date
Expense,Capital One,,250.00,2026-01-15,
Expense,Medicare N,,150.00,2026-01-20,
Income,,SCCU Checking,5000.00,,2026-01-01
Income,,E-Trade Savings,25000.00,,2026-01-01
```

### Supported Date Formats

When reading CSV files, the program accepts:
- `YYYY-MM-DD` (2026-02-10)
- `M/D/YYYY` (2/10/2026)
- `MM/DD/YYYY` (02/10/2026)
- `M-D-YYYY` (2-10-2026)
- `YYYY/M/D` (2026/2/10)
- `D/M/YYYY` (10/2/2026)

Output files always use `YYYY-MM-DD` format.

## Example Output

```
============================================================
MONTHLY EXPENSE ANALYSIS
============================================================
Analysis Date: 2026-01-23
Period: SECOND HALF of the month

UPCOMING EXPENSES:
------------------------------------------------------------
  2026-01-25 | Capital One          |     $250.00
  2026-01-28 | Chase Visa           |     $500.00
------------------------------------------------------------
  TOTAL                             |     $750.00

ACCOUNT BALANCES:
------------------------------------------------------------
BEFORE TRANSFER:
  SCCU Checking:          $1500.00
  E-Trade Savings:       $25000.00

RECOMMENDED TRANSFER: $250.00
  (Expenses: $750.00 + Safety Margin: $1000.00)

AFTER TRANSFER:
  SCCU Checking:          $1750.00
  E-Trade Savings:       $24750.00

AFTER PAYING EXPENSES:
  SCCU Checking:          $1000.00
    (Includes $1000.00 safety margin)
============================================================
```

## Tips

- Use the same CSV filename (`expense_income_data.csv`) for all runs to maintain your data
- Run the program at the beginning of each pay period to plan transfers
- The $1,000 safety margin can be adjusted by modifying the `SAFETY_MARGIN` constant in the code
- Press Enter when modifying entries to keep the current value
- Add expenses for the next month - they'll be tracked but won't affect current calculations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created for personal expense management and budgeting.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
