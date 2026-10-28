class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({'amount': amount, 'description': description})
    
    def withdraw(self, amount, description=""):
        if self.get_balance() >= amount:
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False
    
    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item['amount']
        return balance  

    def transfer(self, amount, category):
        if self.check_funds(amount) and self.withdraw(amount, f"Transfer to {category.name}"):
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False
    
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else: 
            return True

    def __str__(self):
        result = self.name.center(30, '*') + '\n'
        for item in self.ledger:
            desc = item['description'][:23]
            result += f"{desc:<23}{item['amount']:>7.2f}\n"
        result += f"Total: {self.get_balance():.2f}"
        return result
    

def create_spend_chart(categories):
    total_spent = 0
    spent = []
    
    for category in categories:
        total_withdrawal = 0
        for item in category.ledger:
            if item['amount'] < 0:
                total_withdrawal -= item['amount']
        spent.append(total_withdrawal)
        total_spent += total_withdrawal

    percentages = []
    for category, amount in zip(categories, spent):
        if total_spent > 0:
            percentage = (amount / total_spent) * 100
            percentage = (percentage // 10) * 10
        else:
            percentage = 0
        percentages.append(percentage)

    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}|"
        for percentage in percentages:
            if percentage >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
        
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    max_len = max(len(cat.name) for cat in categories)
    names = [cat.name.ljust(max_len) for cat in categories]

    for i in range(max_len):
        chart += "    "
        for name in names:
            chart += f" {name[i]} "
        chart += " "
        
        if i < max_len - 1:
            chart += "\n"

    return chart