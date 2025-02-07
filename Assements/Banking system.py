class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited: ${amount}")
            print(f"${amount} has been deposited.")
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        elif amount > self.balance:
            print("Insufficient funds!")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrew: ${amount}")
            print(f"${amount} has been withdrawn.")

    def check_balance(self):
        print(f"Your current balance is: ${self.balance}")

    def view_transactions(self):
        if not self.transactions:
            print("No transactions available.")
        else:
            print("Transaction History:")
            for transaction in self.transactions:
                print(transaction)

# Example usage
def main():
    account = BankAccount(owner="John Doe", balance=100)  # Starting with $100 balance
    
    while True:
        print("\n--- Welcome to the Bank ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Transactions")
        print("5. Exit")
        
        choice = input("Enter choice: ")

        if choice == '1':
            account.check_balance()
        elif choice == '2':
            amount = float(input("Enter deposit amount: "))
            account.deposit(amount)
        elif choice == '3':
            amount = float(input("Enter withdrawal amount: "))
            account.withdraw(amount)
        elif choice == '4':
            account.view_transactions()
        elif choice == '5':
            print("Thank you for using the Bank. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
