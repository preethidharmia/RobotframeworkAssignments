# Create a class BankAccount with methods to deposit money, withdraw money, and check balance.
# Add validation for insufficient balance.

class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount

    def check_balance(self):
        return self.balance

acc = BankAccount()
acc.deposit(100)
acc.withdraw(50)
print(acc.check_balance())
