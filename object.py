class Account(object):

    def __init__(self, holder, number, balance, credit_line=1500):
        self.Holder = holder
        self.Number = number
        self.Balance = balance
        self.CreditLine = credit_line

    def transfer(self, target, amount):
        if(self.Balance - amount < -self.CreditLine):
            #Insufficient funds.
            return False
        else:
            self.Balance -= amount
            target.Balance += amount
            return True

    def deposit(self, amount):
        self.Balance += amount

    def withdraw(self, amount):
        if(self.Balance - amount < -self.CreditLine):
            #Insufficient funds.
            return False
        else:
            self.Balance -= amount
            return True

    def balance(self):
        return self.Balance

    def __del__(self):
        print "Destructing Object"
