
from collections import defaultdict
import shutil
import datetime
import json
import os

class UserAuth:
    def __init__(self):
#init user authentification class
        self.users_file = 'users.json' #Userdata stored.
        self.users = self.load_users() #Load existing users from file.
        self.financial_report = None #init financial_report attribute for future use in functions.

#Load the users from file.
    def load_users(self): 
        if not os.path.exists(self.users_file): #If file doesnt exist, return empty dictionary. 
            return {}

        with open(self.users_file, 'r') as file: #Open file in readmode, return contents of file.
            return json.load(file)

#Save users to JSON file, open file in write mode, write the user data to the file.
    def save_users(self): 
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

#Create datafile for new user, set filename based on username given.
    def create_user_data_file(self, username):
        data_file = f'{username}_data.json'
#Initial balance of the account when registering.
        initial_balance = input("Enter initial balance (0 if none): ")
        try:
            initial_balance = float(initial_balance)
        except ValueError:
            initial_balance = 0
#Data structure for the user/users
        initial_data = {
            "transactions": [],
            "budgets": {},
            "spendable_amount": initial_balance
        }

#Create new file for user, and save the data.
        with open(data_file, 'w') as f:
            json.dump(initial_data, f, indent=4)

#Register new user function, with checking if username already exists to prevent application failure.
    def register(self, username, password):
        if username in self.users:
            return False, "Username already exists."

#if username is not taken, add it to the list. 
        self.users[username] = password
        self.save_users()
        self.create_user_data_file(username) # Create datafile for new user.
        return True, "User registered successfully."

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True, "Login successful."
        else:
            return False, "Invalid username or password."

## --------------
# Example of it's use case, the "classes below"

# -- transaction_manager = TransactionManager("username")

# User enters transaction details
# -- transaction_type = "expense" or "income"
# -- amount = 50.00
# -- category = "Food"

# Date can be provided

# Create a Transaction object
# -- new_transaction = Transaction(transaction_type, amount, category)

# Add the transaction to the users data
# transaction_manager.add_transaction(new_transaction)

#The basic structure template for spending/reciving money.
#Class representing a transaction. Initialize the transaction with the neccessary data shown below.
class Transaction:
    def __init__(self, type, amount, category, date=None):
        self.type = type
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.datetime.now().strftime("%d-%m-%Y")

#Managing transactions for the user.
#Init the class TransactionManager with username of the user.
class TransactionManager:
    def __init__(self, username):
        self.data_file = f'{username}_data.json'
        self.user_data = self.load_user_data()

#Load user data from JSON file, if it doesnt exist. it creates one from default structure.
    def load_user_data(self):
        if not os.path.exists(self.data_file):
            return {"transactions": [], "budgets": {}, "spendable_amount": 0}

        with open(self.data_file, 'r') as file:
            data = json.load(file)
            data.setdefault("transactions", [])
            data.setdefault("budgets", {})
            data.setdefault("spendable_amount", 0)
            return data

#Save the users data back to the JSON file.
    def save_user_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.user_data, file, indent=4)

#New transaction created and updated spendable amount.
    def add_transaction(self, transaction):
        if transaction.type == "income":
            self.user_data["spendable_amount"] += transaction.amount
        elif transaction.type == "expense":
            self.user_data["spendable_amount"] -= transaction.amount

#Converting the transaction object to a dictionary and append it to the list.
        transaction_dict = {
            "type": transaction.type,
            "amount": transaction.amount,
            "category": transaction.category,
            "date": transaction.date
        }
        self.user_data["transactions"].append(transaction_dict)
        
        #Save the updates data to the file
        self.save_user_data()
        
    def get_transactions(self):
        #Returning the list of transactions for the user from the json file.
        return self.user_data["transactions"]


#Here user_data also exists, because that's what's being used and retrive information from.
#The budget class for handling the budget functions. Init with userdata and categories

#budget related acitivites class. 
class BudgetManager:
    def __init__(self, user_data):
        self.user_data = user_data # Stores user data
        self.default_categories = ['Salary', 'Food', 'Transport', 'Entertainment', 'Utilities', 'Other']

#Compare user budget with their expenses and returns a summary
    def get_budget_comparison_data(self):
        budgets = self.user_data["budgets"]
        expenses_summary = defaultdict(float)

#Calculate total expenses for each category
        for transaction in self.user_data["transactions"]:
            if transaction["type"] == "expense":
                expenses_summary[transaction["category"]] += transaction["amount"]

#Compare budgets with expenses and calculate remaining budget
        budget_comparison_data = {}
        for category, budget in budgets.items():
            spent = expenses_summary[category]
            remaining = budget - spent
            budget_comparison_data[category] = {'budget': budget, 'spent': spent, 'remaining': remaining}
        
        return budget_comparison_data #Return the comparison data

#Prints a comparison of budgets with expenses for each category
    def compare_budgets_with_expenses(self):
        budgets = self.user_data["budgets"]
        expenses_summary = defaultdict(float) 
        for transaction in self.user_data["transactions"]:
            if transaction["type"] == "expense":
                expenses_summary[transaction["category"]] += transaction["amount"]

#Output the comparison of budget and expenses
        print("\nBudget vs Expenses:")
        for category, budget in budgets.items():
            spent = expenses_summary[category]
            remaining = budget - spent 
            print(f"{category}: Budget: {budget} SEK, Spent: {spent} SEK, Remaining: {remaining} SEK")
    
#Loads user data from a file
    def load_user_data(self):
        if not os.path.exists(self.data_file):
            return {"transactions": [], "budgets": {}}
        with open(self.data_file, 'r') as file:
            data = json.load(file)
            data.setdefault("transactions", [])
            data.setdefault("budgets", {})
            return data

#Saves user data to a file
    def save_user_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.user_data, file, indent=4)

#Creates a new budget for a given category
    def create_budget(self, category, limit):
        if category not in self.user_data["budgets"]:
            self.user_data["budgets"][category] = limit
            self.save_user_data()
            print(f"Budget for {category} set at {limit}.")
        else:
            print(f"A budget for {category} already exists.")

#Returns the set budgets for the user
    def get_budgets(self):
        return self.user_data["budgets"]

#Allows user to select a budget category
    def select_category(self, exclude_salary=True):
        categories_to_display = self.default_categories
        if exclude_salary:
            categories_to_display = [cat for cat in self.default_categories if cat != 'Salary']
        print("\nSelect a category:")

#Display categories for user selection
        for idx, category in enumerate(categories_to_display, 1):
            print(f"{idx}. {category}")

#Handle user's category choice
        choice = input("Enter your choice (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories_to_display):
            return categories_to_display[int(choice) - 1]
        else:
            print("Invalid choice. Please enter a valid number.")
            return None

#Initializes the FinancialReport class with transaction and budget managers.
class FinancialReport:
    def __init__(self, transaction_manager, budget_manager):
        self.transaction_manager = transaction_manager
        self.budget_manager = budget_manager
 
#Exports financial reports to a file.       
    def export_report(self, report_type, data, filename):
        with open(filename, 'w') as file:
            if report_type == 'summary':
                for key, values in data.items():
                    file.write(f"{key} - Income: {values['income']} SEK, Expense: {values['expense']} SEK\n")
            elif report_type == 'budget':
                for category, info in data.items():
                    file.write(f"{category} - Budget: {info['budget']} SEK, Spent: {info['spent']} SEK, Remaining: {info['remaining']} SEK\n")
            print(f"Report exported to {filename}")

#Generates a financial summary for a specific period.
    def generate_summary(self, period, year=None, month=None, week=None):
        if period not in ['week', 'month', 'year']:
            print("Invalid period. Please enter 'week', 'month', or 'year'.")
            return None

        summary = defaultdict(lambda: {'income': 0, 'expense': 0})
        for transaction in self.transaction_manager.user_data['transactions']:
            transaction_date = datetime.datetime.strptime(transaction['date'], "%d-%m-%Y")

#Check if the transaction date falls within the specified period.

            if period == 'week' and transaction_date.isocalendar()[1] == week and transaction_date.year == year:
                period_key = self.get_period_key(transaction_date, period)
            elif period == 'month' and transaction_date.month == month and transaction_date.year == year:
                period_key = self.get_period_key(transaction_date, period)
            elif period == 'year' and transaction_date.year == year:
                period_key = self.get_period_key(transaction_date, period)
            else:
                continue

#Accumulate income and expenses in the summary.

            if transaction['type'] == 'income':
                summary[period_key]['income'] += transaction['amount']
            else:
                summary[period_key]['expense'] += transaction['amount']

        return summary

#Determines the period key based on the transaction date and period type.

    def get_period_key(self, transaction_date, period):
        if period == 'week':
            return transaction_date.isocalendar()[0], transaction_date.isocalendar()[1]
        
        elif period == 'month':
            return transaction_date.strftime('%Y-%m')
        
        elif period == 'year':
            return transaction_date.strftime('%Y')
    
#Handles the generation and export of financial reports.

    def generate_report(self):
        financial_report = FinancialReport(self.transaction_manager, self.budget_manager)
        
        print("\nGenerate Financial Report")
        print("1. Summary Report")
        print("2. Budget Report")
        print("3. Go Back")

        choice = input("Enter your choice (1-4): ")

#Process the user's choice and generate the corresponding report.

        if choice == '1':
            period = input("Enter period for summary (week/month/year): ").lower()
            year, week, month = None, None, None
            if period == 'year':
                year = self.get_valid_input("Enter the year (e.g., 2023): ", int)
                
            elif period == 'week':
                year = self.get_valid_input("Enter the year (e.g., 2023): ", int)
                week = self.get_valid_input("Enter the week number (1-52): ", int, range(1, 53))
                
            elif period == 'month':
                year = self.get_valid_input("Enter the year (e.g., 2023): ", int)
                month = self.get_valid_input("Enter the month number (1-12): ", int, range(1, 13))

            summary = financial_report.generate_summary(period, year, week, month)
            if summary:
#Display the summary and offer an export option.
                for key, values in summary.items():
                    print(f"{key} - Income: {values['income']} SEK, Expense: {values['expense']} SEK")
                self.export_decision('summary', summary, self.financial_report)
                
        elif choice == '2':
            print("\nBudget Report")
            budget_data = self.budget_manager.get_budget_comparison_data()
            self.export_decision('budget', budget_data, self.financial_report)

        elif choice == '3':
            return
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

class FinanceManagerApp:
#Initialize the application with user authentication and other components set to None initially.
    def __init__(self):
        self.user_auth = UserAuth() #Handles user authentication
        self.current_user = None #Currently logged in user
        self.transaction_manager = None #Manages user transactions
        self.budget_manager = None #Manages user budgets

#Main loop of the application
    def run(self):
        while True:
            print("\nWelcome to the Personal Finance Manager")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("Exiting the application. Have a nice day!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

#Handles user login
    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        success, message = self.user_auth.login(username, password)
        print(message)
        
        if success:
            self.current_user = username
            self.transaction_manager = TransactionManager(username)
            self.budget_manager = BudgetManager(self.transaction_manager.user_data)
            self.financial_report = FinancialReport(self.transaction_manager, self.budget_manager)
            self.user_menu() # Show menu after successful login with init the neccessary classes.
#Handles user registration
    def register(self):
        username = input("Enter your desired username: ")
        password = input("Enter your desired password: ")
        success, message = self.user_auth.register(username, password)
        print(message)

#User after logged in menu loop.
    def user_menu(self):
        while True:
            print("\nFinance Manager - User Menu")
            print("1. Track Income/Expense")
            print("2. Create/Monitor Budget")
            print("3. Generate Financial Report")
            print("4. Backup Data")
            print("5. Restore Data")
            print("6. Logout")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.track_income_expense()
            elif choice == '2':
                self.manage_budget()
            elif choice == '3':
                self.generate_report()
            elif choice == '4':
                self.backup_user_data()
            elif choice == '5':
                self.restore_user_data()
            elif choice == '6':
                print("Logging out.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

#Handles the tracking of income and expenses.
    def track_income_expense(self):
        print("\nTrack Income and Expense")
        print("1. Income")
        print("2. Expense")
        choice = input("Select transaction type (1 for Income, 2 for Expense): ")

#Ensures the user chooses a valid transaction type
        while choice not in ['1', '2']:
            print("Invalid choice. Please enter 1 for Income or 2 for Expense.")
            choice = input("Select transaction type (1 for Income, 2 for Expense): ")

        transaction_type = 'income' if choice == '1' else 'expense'

        amount = input("Enter amount: ")
#Validates the input amount
        while not amount.isdigit():
            print("Invalid amount. Please enter a numeric value.")
            amount = input("Enter amount: ")

#Category selection for the transaction
        if transaction_type == 'income':
            category = 'Salary'
        else:
            category = self.budget_manager.select_category()

        amount = float(amount)
#input for user transaction.
        date_input = input("Enter the date of the transaction (DD-MM-YYYY) or 'now' for the current date: ").strip()
        if date_input.lower() == 'now':
            transaction_date = datetime.datetime.now().strftime("%d-%m-%Y")
        else:
            try:
                transaction_date = datetime.datetime.strptime(date_input, "%d-%m-%Y").strftime("%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Using the current date instead.")
                transaction_date = datetime.datetime.now().strftime("%d-%m-%Y")

        transaction = Transaction(transaction_type, amount, category, transaction_date)
        self.transaction_manager.add_transaction(transaction)

        print(f"Transaction recorded successfully. Current Spendable Amount: {self.transaction_manager.user_data['spendable_amount']} SEK")

#Retrive budgets from budgetmanager, check if expense exeeds the budget for selected category
    def check_budget_before_expense(self, category, amount):
        budgets = self.budget_manager.get_budgets()
        if category in budgets and amount > budgets[category]:
            print(f"Warning: This expense exceeds your budget for {category}.")
#Warn user if expense exceeds budget.
            confirmation = input("Do you still want to proceed? (yes/no): ").lower()
            if confirmation != 'yes':
                print("Expense transaction cancelled.")
                return False #cancel transaction.
        return True
    
    def manage_budget(self):
#display spendable amount to the user.
        current_spendable = self.transaction_manager.user_data['spendable_amount']
        print(f"\nCurrent Available Money: {current_spendable}")

#userlogin budgetmanagement.
        print("Budget Management")
        print("1. Create Budget")
        print("2. View Budgets")
        print("3. Go Back")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            self.create_budget()
        if choice == '2':
            self.view_budgets()
        elif choice == '3':
            self.budget_manager.compare_budgets_with_expenses()
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    
    def create_budget(self):
        print("\nCreate a New Budget")
#User can create budget, exclude salary.
        category = self.budget_manager.select_category(exclude_salary=True)
        if category:
            limit = input(f"Enter budget limit for {category}: ")
            try:
                limit = float(limit)
                self.budget_manager.create_budget(category, limit)
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

#Retrive and display current budgets.
    def view_budgets(self):
        print("\nCurrent Budgets:")
        budgets = self.budget_manager.get_budgets()
        if budgets:
            for category, limit in budgets.items():
                print(f"{category}: {limit}")
        else:
            print("No budgets set yet.")

#generate report menu.
    def generate_report(self):
        financial_report = FinancialReport(self.transaction_manager, self.budget_manager)
        
        print("\nGenerate Financial Report")
        print("1. Summary Report")
        print("2. Budget Report")
        print("3. Export Report")
        print("4. Go Back")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            period = input("Enter period for summary (week/month/year): ").lower()
            year = int(input("Enter the year (e.g., 2023): "))

#Determines the summary report and generate it
            if period == 'week':
                week = int(input("Enter the week number (1-52): "))
                summary = self.financial_report.generate_summary(period, year=year, week=week)
            elif period == 'month':
                month = int(input("Enter the month number (1-12): "))
                summary = self.financial_report.generate_summary(period, year=year, month=month)
            elif period == 'year':
                summary = self.financial_report.generate_summary(period, year=year)
#display the generated summary.
            for key, values in summary.items():
                print(f"{key} - Income: {values['income']} SEK, Expense: {values['expense']} SEK")
            self.export_decision('summary', summary, self.financial_report)

        elif choice == '2':
            print("\nBudget Report")
            budget_data = self.budget_manager.get_budget_comparison_data()
            self.export_decision('budget', budget_data, financial_report)
        elif choice == '3':
            print("Export functionality not implemented yet.")
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

#offering option to export when viewing the report.
    def export_decision(self, report_type, data, financial_report):
        if data:
            export = input("Do you want to export this report? (yes/no): ").lower()
            if export == 'yes':
                filename = input("Enter filename to export: ")
                financial_report.export_report(report_type, data, filename) #Export report
            elif report_type == 'budget':
                self.budget_manager.compare_budgets_with_expenses() #compare budget with expenses.
    def get_valid_input(self, prompt, input_type, valid_range=None):
        while True:
            try:
                value = input_type(input(prompt))
                if valid_range and value not in valid_range:
                    raise ValueError
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    def restore_user_data(self):
#Get the current username
        username = self.current_user
#Define the paths for the backup and original data files
        backup_file = f"{username}_data_backup.json" 
        original_file = f"{username}_data.json"

#Check if the backup file exists
        if os.path.exists(backup_file):
#Check if the original data file exists to prevent accidental overwrite
            if os.path.exists(original_file):
                print("A current user data file exists. Please ensure it is removed or backed up before restoring.")
                return
#Replace the original file with the backup
            shutil.move(backup_file, original_file)
            print("Data has been restored successfully.")
            print("Please restart the program for the backup to take full effect.")
        else:
            print("No backup file found.")
            
    def backup_user_data(self):
#Get the current username
        username = self.current_user 
#Define the paths for the user data file and the backup file

        user_data_file = f'{username}_data.json'
        backup_file = f'backup_{username}.json'

#Check if the user data file exists
        if os.path.exists(user_data_file):
            shutil.copy(user_data_file, backup_file)
            print(f"Backup created: {backup_file}")
        else:
            print("No data file found to backup.")

if __name__ == "__main__":
    app = FinanceManagerApp()
    app.run()

