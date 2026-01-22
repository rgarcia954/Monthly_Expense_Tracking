import csv
from datetime import datetime
from pathlib import Path

# Constants
PAYEES = [
    "Ameritus", "Capital One", "Chase Visa", "Medicare N", "Amex",
    "HOA Q", "HOA M", "Citibank Visa", "Apple card RG", 
    "Apple card YG", "United Health", "Medicare Pre"
]

INCOME_SOURCES = ["SCCU Checking", "E-Trade Savings"]
SAFETY_MARGIN = 1000.0

def get_yes_no_input(prompt):
    """Get yes/no input from user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def parse_date(date_string):
    """Parse date string with multiple format support."""
    date_formats = [
        '%Y-%m-%d',      # 2026-02-10
        '%m/%d/%Y',      # 2/10/2026 or 02/10/2026
        '%m-%d-%Y',      # 2-10-2026 or 02-10-2026
        '%Y/%m/%d',      # 2026/02/10
        '%d/%m/%Y',      # 10/02/2026
        '%d-%m-%Y',      # 10-02-2026
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    # If none of the formats work, raise an error
    raise ValueError(f"Unable to parse date '{date_string}'. Please use format YYYY-MM-DD, M/D/YYYY, or similar.")

def read_csv_file(filename):
    """Read expense and income data from CSV file."""
    expenses = []
    income = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Type'] == 'Expense':
                    expenses.append({
                        'Payee': row['Payee'],
                        'Amount': float(row['Amount']),
                        'Due Date': parse_date(row['Due Date'])
                    })
                elif row['Type'] == 'Income':
                    income.append({
                        'Bank': row['Bank'],
                        'Amount': float(row['Amount']),
                        'Balance Date': parse_date(row['Balance Date'])
                    })
        return expenses, income
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def display_expenses(expenses):
    """Display all expenses in a formatted table."""
    if not expenses:
        print("  No expenses to display.")
        return
    
    print("\n" + "-" * 70)
    print(f"{'#':<4} {'Payee':<25} {'Amount':>12} {'Due Date':<15}")
    print("-" * 70)
    for i, exp in enumerate(expenses, 1):
        print(f"{i:<4} {exp['Payee']:<25} ${exp['Amount']:>10.2f} {exp['Due Date'].strftime('%Y-%m-%d'):<15}")
    print("-" * 70)

def display_income(income):
    """Display all income in a formatted table."""
    if not income:
        print("  No income to display.")
        return
    
    print("\n" + "-" * 70)
    print(f"{'#':<4} {'Bank':<25} {'Amount':>12} {'Balance Date':<15}")
    print("-" * 70)
    for i, inc in enumerate(income, 1):
        print(f"{i:<4} {inc['Bank']:<25} ${inc['Amount']:>10.2f} {inc['Balance Date'].strftime('%Y-%m-%d'):<15}")
    print("-" * 70)

def add_expense(expenses):
    """Add a new expense."""
    print("\n--- Add New Expense ---")
    print("Available payees:")
    for i, payee in enumerate(PAYEES, 1):
        print(f"  {i}. {payee}")
    
    payee_input = input("\nPayee name or number: ").strip()
    
    # Check if input is a number
    if payee_input.isdigit():
        idx = int(payee_input) - 1
        if 0 <= idx < len(PAYEES):
            payee = PAYEES[idx]
        else:
            print("Invalid payee number.")
            return False
    else:
        payee = payee_input
    
    try:
        amount = float(input("Amount: $"))
        due_date_str = input("Due Date (YYYY-MM-DD): ")
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        expenses.append({
            'Payee': payee,
            'Amount': amount,
            'Due Date': due_date
        })
        print(f"✓ Added: {payee} - ${amount:.2f} due on {due_date.date()}")
        return True
    except ValueError as e:
        print(f"Invalid input: {e}")
        return False

def modify_expense(expenses):
    """Modify an existing expense."""
    if not expenses:
        print("No expenses to modify.")
        return False
    
    display_expenses(expenses)
    
    try:
        choice = int(input("\nEnter expense number to modify (0 to cancel): "))
        if choice == 0:
            return False
        
        if 1 <= choice <= len(expenses):
            idx = choice - 1
            exp = expenses[idx]
            
            print(f"\nModifying: {exp['Payee']} - ${exp['Amount']:.2f} due on {exp['Due Date'].strftime('%Y-%m-%d')}")
            print("Press Enter to keep current value")
            
            # Modify payee
            payee_input = input(f"Payee [{exp['Payee']}]: ").strip()
            if payee_input:
                exp['Payee'] = payee_input
            
            # Modify amount
            amount_input = input(f"Amount [${exp['Amount']:.2f}]: $").strip()
            if amount_input:
                exp['Amount'] = float(amount_input)
            
            # Modify due date
            date_input = input(f"Due Date [{exp['Due Date'].strftime('%Y-%m-%d')}]: ").strip()
            if date_input:
                exp['Due Date'] = datetime.strptime(date_input, '%Y-%m-%d')
            
            print("✓ Expense modified successfully")
            return True
        else:
            print("Invalid expense number.")
            return False
    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")
        return False

def delete_expense(expenses):
    """Delete an expense."""
    if not expenses:
        print("No expenses to delete.")
        return False
    
    display_expenses(expenses)
    
    try:
        choice = int(input("\nEnter expense number to delete (0 to cancel): "))
        if choice == 0:
            return False
        
        if 1 <= choice <= len(expenses):
            idx = choice - 1
            deleted = expenses.pop(idx)
            print(f"✓ Deleted: {deleted['Payee']} - ${deleted['Amount']:.2f}")
            return True
        else:
            print("Invalid expense number.")
            return False
    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")
        return False

def add_income(income):
    """Add or update income entry."""
    print("\n--- Add/Update Income ---")
    print("Available banks:")
    for i, bank in enumerate(INCOME_SOURCES, 1):
        print(f"  {i}. {bank}")
    
    bank_input = input("\nBank name or number: ").strip()
    
    # Check if input is a number
    if bank_input.isdigit():
        idx = int(bank_input) - 1
        if 0 <= idx < len(INCOME_SOURCES):
            bank = INCOME_SOURCES[idx]
        else:
            print("Invalid bank number.")
            return False
    else:
        bank = bank_input
    
    try:
        amount = float(input("Amount: $"))
        balance_date_str = input("Balance Date (YYYY-MM-DD): ")
        balance_date = datetime.strptime(balance_date_str, '%Y-%m-%d')
        
        # Check if bank already exists and update, otherwise add
        existing = next((inc for inc in income if inc['Bank'] == bank), None)
        if existing:
            existing['Amount'] = amount
            existing['Balance Date'] = balance_date
            print(f"✓ Updated: {bank} - ${amount:.2f}")
        else:
            income.append({
                'Bank': bank,
                'Amount': amount,
                'Balance Date': balance_date
            })
            print(f"✓ Added: {bank} - ${amount:.2f}")
        return True
    except ValueError as e:
        print(f"Invalid input: {e}")
        return False

def modify_income(income):
    """Modify an existing income entry."""
    if not income:
        print("No income to modify.")
        return False
    
    display_income(income)
    
    try:
        choice = int(input("\nEnter income number to modify (0 to cancel): "))
        if choice == 0:
            return False
        
        if 1 <= choice <= len(income):
            idx = choice - 1
            inc = income[idx]
            
            print(f"\nModifying: {inc['Bank']} - ${inc['Amount']:.2f} as of {inc['Balance Date'].strftime('%Y-%m-%d')}")
            print("Press Enter to keep current value")
            
            # Modify amount
            amount_input = input(f"Amount [${inc['Amount']:.2f}]: $").strip()
            if amount_input:
                inc['Amount'] = float(amount_input)
            
            # Modify balance date
            date_input = input(f"Balance Date [{inc['Balance Date'].strftime('%Y-%m-%d')}]: ").strip()
            if date_input:
                inc['Balance Date'] = datetime.strptime(date_input, '%Y-%m-%d')
            
            print("✓ Income modified successfully")
            return True
        else:
            print("Invalid income number.")
            return False
    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")
        return False

def delete_income(income):
    """Delete an income entry."""
    if not income:
        print("No income to delete.")
        return False
    
    display_income(income)
    
    try:
        choice = int(input("\nEnter income number to delete (0 to cancel): "))
        if choice == 0:
            return False
        
        if 1 <= choice <= len(income):
            idx = choice - 1
            deleted = income.pop(idx)
            print(f"✓ Deleted: {deleted['Bank']} - ${deleted['Amount']:.2f}")
            return True
        else:
            print("Invalid income number.")
            return False
    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")
        return False

def manage_data(expenses, income):
    """Interactive menu to manage expenses and income."""
    while True:
        print("\n" + "="*60)
        print("DATA MANAGEMENT MENU")
        print("="*60)
        print("Expenses:")
        print("  1. View expenses")
        print("  2. Add expense")
        print("  3. Modify expense")
        print("  4. Delete expense")
        print("\nIncome:")
        print("  5. View income")
        print("  6. Add/Update income")
        print("  7. Modify income")
        print("  8. Delete income")
        print("\n  9. Continue to analysis")
        print("  0. Exit program")
        print("="*60)
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n--- Current Expenses ---")
            display_expenses(expenses)
        elif choice == '2':
            add_expense(expenses)
        elif choice == '3':
            modify_expense(expenses)
        elif choice == '4':
            delete_expense(expenses)
        elif choice == '5':
            print("\n--- Current Income ---")
            display_income(income)
        elif choice == '6':
            add_income(income)
        elif choice == '7':
            modify_income(income)
        elif choice == '8':
            delete_income(income)
        elif choice == '9':
            return True
        elif choice == '0':
            return False
        else:
            print("Invalid option. Please try again.")

def get_manual_expense_data():
    """Manually input expense data."""
    expenses = []
    print("\n--- Enter Expense Data ---")
    print("Available payees:")
    for i, payee in enumerate(PAYEES, 1):
        print(f"  {i}. {payee}")
    
    while True:
        print("\nEnter expense (or press Enter to finish):")
        payee_input = input("  Payee name or number: ").strip()
        
        if not payee_input:
            break
        
        # Check if input is a number
        if payee_input.isdigit():
            idx = int(payee_input) - 1
            if 0 <= idx < len(PAYEES):
                payee = PAYEES[idx]
            else:
                print("Invalid payee number. Please try again.")
                continue
        else:
            payee = payee_input
        
        try:
            amount = float(input("  Amount: $"))
            due_date_str = input("  Due Date (YYYY-MM-DD): ")
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            
            expenses.append({
                'Payee': payee,
                'Amount': amount,
                'Due Date': due_date
            })
            print(f"  Added: {payee} - ${amount:.2f} due on {due_date.date()}")
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    
    return expenses

def get_manual_income_data():
    """Manually input income data."""
    income = []
    print("\n--- Enter Income Data ---")
    print("Available banks:")
    for i, bank in enumerate(INCOME_SOURCES, 1):
        print(f"  {i}. {bank}")
    
    for bank in INCOME_SOURCES:
        print(f"\nEnter data for {bank}:")
        try:
            amount = float(input("  Amount: $"))
            balance_date_str = input("  Balance Date (YYYY-MM-DD): ")
            balance_date = datetime.strptime(balance_date_str, '%Y-%m-%d')
            
            income.append({
                'Bank': bank,
                'Amount': amount,
                'Balance Date': balance_date
            })
        except ValueError as e:
            print(f"Invalid input: {e}. Setting to 0.")
            income.append({
                'Bank': bank,
                'Amount': 0.0,
                'Balance Date': datetime.now()
            })
    
    return income

def save_to_csv(expenses, income, filename='expense_income_data.csv'):
    """Save expense and income data to CSV file."""
    with open(filename, 'w', newline='') as f:
        fieldnames = ['Type', 'Payee', 'Bank', 'Amount', 'Due Date', 'Balance Date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for expense in expenses:
            writer.writerow({
                'Type': 'Expense',
                'Payee': expense['Payee'],
                'Bank': '',
                'Amount': expense['Amount'],
                'Due Date': expense['Due Date'].strftime('%Y-%m-%d'),
                'Balance Date': ''
            })
        
        for inc in income:
            writer.writerow({
                'Type': 'Income',
                'Payee': '',
                'Bank': inc['Bank'],
                'Amount': inc['Amount'],
                'Due Date': '',
                'Balance Date': inc['Balance Date'].strftime('%Y-%m-%d')
            })
    
    print(f"\nData saved to '{filename}'")

def calculate_transfer(expenses, income):
    """Calculate recommended transfer from savings to checking."""
    current_date = datetime.now()
    current_day = current_date.day
    
    # Determine which half of the month we're in
    if current_day <= 15:
        period = "first half"
        start_day = 1
        end_day = 15
    else:
        period = "second half"
        start_day = 16
        end_day = 31  # Will handle month-end automatically
    
    # Filter expenses for current period that are due on or after today
    # Only include expenses in the current month, exclude next month
    relevant_expenses = [
        exp for exp in expenses
        if exp['Due Date'].month == current_date.month
        and exp['Due Date'].year == current_date.year
        and start_day <= exp['Due Date'].day <= end_day
        and exp['Due Date'].date() >= current_date.date()
    ]
    
    # Count excluded next month expenses for user information
    next_month_expenses = [
        exp for exp in expenses
        if (exp['Due Date'].year > current_date.year or 
            (exp['Due Date'].year == current_date.year and exp['Due Date'].month > current_date.month))
    ]
    
    total_expenses = sum(exp['Amount'] for exp in relevant_expenses)
    
    # Get account balances
    sccu_balance = next((inc['Amount'] for inc in income if inc['Bank'] == 'SCCU Checking'), 0.0)
    etrade_balance = next((inc['Amount'] for inc in income if inc['Bank'] == 'E-Trade Savings'), 0.0)
    
    # Calculate required balance (expenses + safety margin)
    required_balance = total_expenses + SAFETY_MARGIN
    
    # Determine if transfer is needed
    transfer_amount = 0.0
    if sccu_balance < required_balance:
        transfer_amount = required_balance - sccu_balance
    
    return {
        'period': period,
        'current_date': current_date,
        'relevant_expenses': relevant_expenses,
        'next_month_expenses': next_month_expenses,
        'total_expenses': total_expenses,
        'sccu_before': sccu_balance,
        'etrade_before': etrade_balance,
        'transfer_amount': transfer_amount,
        'sccu_after': sccu_balance + transfer_amount,
        'etrade_after': etrade_balance - transfer_amount
    }

def print_results(results):
    """Print the analysis results."""
    print("\n" + "="*60)
    print("MONTHLY EXPENSE ANALYSIS")
    print("="*60)
    print(f"Analysis Date: {results['current_date'].strftime('%Y-%m-%d')}")
    print(f"Period: {results['period'].upper()} of the month")
    print()
    
    print("UPCOMING EXPENSES:")
    print("-" * 60)
    if results['relevant_expenses']:
        for exp in sorted(results['relevant_expenses'], key=lambda x: x['Due Date']):
            print(f"  {exp['Due Date'].strftime('%Y-%m-%d')} | {exp['Payee']:<20} | ${exp['Amount']:>10.2f}")
        print("-" * 60)
        print(f"  {'TOTAL':<32} | ${results['total_expenses']:>10.2f}")
    else:
        print("  No upcoming expenses for this period.")
    print()
    
    # Show next month expenses if any
    if results['next_month_expenses']:
        print("NEXT MONTH EXPENSES (Not included in transfer calculation):")
        print("-" * 60)
        for exp in sorted(results['next_month_expenses'], key=lambda x: x['Due Date']):
            print(f"  {exp['Due Date'].strftime('%Y-%m-%d')} | {exp['Payee']:<20} | ${exp['Amount']:>10.2f}")
        print()
    
    print("ACCOUNT BALANCES:")
    print("-" * 60)
    print("BEFORE TRANSFER:")
    print(f"  SCCU Checking:    ${results['sccu_before']:>12.2f}")
    print(f"  E-Trade Savings:  ${results['etrade_before']:>12.2f}")
    print()
    
    if results['transfer_amount'] > 0:
        print(f"RECOMMENDED TRANSFER: ${results['transfer_amount']:.2f}")
        print(f"  (Expenses: ${results['total_expenses']:.2f} + Safety Margin: ${SAFETY_MARGIN:.2f})")
        print()
        print("AFTER TRANSFER:")
        print(f"  SCCU Checking:    ${results['sccu_after']:>12.2f}")
        print(f"  E-Trade Savings:  ${results['etrade_after']:>12.2f}")
        print()
        print("AFTER PAYING EXPENSES:")
        print(f"  SCCU Checking:    ${results['sccu_after'] - results['total_expenses']:>12.2f}")
        print(f"    (Includes ${SAFETY_MARGIN:.2f} safety margin)")
    else:
        print("NO TRANSFER NEEDED")
        print(f"  Current SCCU balance is sufficient (includes ${SAFETY_MARGIN:.2f} safety margin)")
        print()
        print("AFTER PAYING EXPENSES:")
        print(f"  SCCU Checking:    ${results['sccu_before'] - results['total_expenses']:>12.2f}")
        print(f"    (Includes ${SAFETY_MARGIN:.2f} safety margin)")
    
    print("="*60)

def main():
    """Main program function."""
    print("="*60)
    print("MONTHLY EXPENSE AND INCOME MANAGER")
    print("="*60)
    
    # Step 1: Check if user has CSV file
    has_csv = get_yes_no_input("\nDo you have a CSV file for processing? (yes/no): ")
    
    expenses = []
    income = []
    
    if has_csv:
        filename = input("Enter CSV filename: ").strip()
        expenses, income = read_csv_file(filename)
        
        if expenses is None or income is None:
            print("Failed to read CSV. Please enter data manually.")
            has_csv = False
        else:
            print(f"\n✓ Successfully loaded {len(expenses)} expense(s) and {len(income)} income source(s)")
            
            # Allow user to review and modify imported data
            if get_yes_no_input("\nWould you like to review/modify the imported data? (yes/no): "):
                if not manage_data(expenses, income):
                    print("\nProgram terminated by user.")
                    return
    
    if not has_csv:
        # Get manual input
        expenses = get_manual_expense_data()
        income = get_manual_income_data()
        
        # Allow user to review and modify manually entered data
        if expenses or income:
            if get_yes_no_input("\nWould you like to review/modify your entries? (yes/no): "):
                if not manage_data(expenses, income):
                    print("\nProgram terminated by user.")
                    return
    
    # Save data to CSV
    save_to_csv(expenses, income)
    
    # Calculate and display results
    results = calculate_transfer(expenses, income)
    print_results(results)

if __name__ == "__main__":
    main()