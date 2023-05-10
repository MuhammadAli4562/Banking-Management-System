import secrets
import string
import pickle
import os
import pathlib
from datetime import datetime
import datetime
from random import randint


class Account:
    def __init__(self):
        self.ID = 0
        self.name = ''
        self.address = ''
        self.number = 0
        self.type = ''
        self.deposit = 0
        self.key = 0
        self.interest = 0
        self.businessName = ''
        self.businessRegNo = ''
        self.businessOwnerName = ''

    def createAccount(self):
        idFile = open("ID.txt", "r")
        if idFile.mode == 'r':
            self.ID = idFile.read()
        idFile.close()
        idFile = open("ID.txt", "w")
        idFile.write(str(int(self.ID) + 1))
        idFile.close()
        print("\nYour account number is: ", self.ID)
        self.name = input("Enter the account holder name: ")
        self.address = input("Enter the account holder address: ")
        self.number = int(input("Ente the acount holder number: "))
        self.deposit = int(input("Enter The Initial amount: "))
        print("\n\tAccount Created Successfully!")
        self.key = ''.join(secrets.choice(string.ascii_letters + string.digits)
                           for i in range(3)) + str(randint(100, 999))
        while 1:
            self.type = input("Ente the type of account [A/S/B]: ")
            if self.type.upper() == 'A':
                self.interest = 3
                break
            if self.type.upper() == 'S':
                self.interest = 7
                break
            if self.type.upper() == 'B':
                self.interest = 3
                break
            else:
                continue
        if self.type.upper() == 'B':
            self.businessName = input("Enter the account holder name: ")
            self.businessRegNo = input("Enter the account holder name: ")
            self.businessOwnerName = input("Enter the account holder name: ")

    def showAccount(self):
        print("Unique ID : ", self.ID)
        print("Name : ", self.name)
        print("Address : ", self.ID)
        print("Number : ", self.ID)
        print("Type", self.type)
        print("Balance : ", self.deposit)

    def modifyAccount(self):
        print("Account Number : ", self.ID)
        self.name = input("Modify account Holder Name: ")
        self.address = input("Modify account holder address: ")
        self.number = int(input("Modify account holder number: "))
        self.type = input("Modify type of account: ")
        self.deposit = int(input("Modify Balance: "))

    def depositAmount(self, amount):
        self.deposit += amount

    def withdrawAmount(self, amount):
        self.deposit -= amount

    def report(self):
        print(self.ID, " ", self.name, " ", self.type, " ", self.deposit)

    def getAccountNo(self):
        return self.ID

    def getAcccountHolderName(self):
        return self.name

    def getAccountType(self):
        return self.type

    def getDeposit(self):
        return self.deposit


class UnitedBank:
    def __init__(self):
        choice = ''
        print("\t__WELCOME TO UNITED BANK__")
        while choice != 8:
            print("\n _MAIN MENU_\n")
            print("1. NEW ACCOUNT")
            print("2. DEPOSIT AMOUNT")
            print("3. WITHDRAW AMOUNT")
            print("4. BALANCE ENQUIRY")
            print("5. ALL ACCOUNTS")
            print("6. CLOSE AN ACCOUNT")
            print("7. MODIFY AN ACCOUNT")
            print("8. EXIT")
            choice = input("\n\tEnter you Choice: ")
            if choice == '1':
                self.writeAccount()
            elif choice == '2':
                accountNo = int(input("\nEnter The account No: "))
                self.depositAndWithdraw(accountNo, 1)
            elif choice == '3':
                accountNo = int(input("\nEnter The account No: "))
                self.depositAndWithdraw(accountNo, 2)
            elif choice == '4':
                accountNo = int(input("\nEnter The account No: "))
                self.displaySp(accountNo)
            elif choice == '5':
                self.displayAll()
            elif choice == '6':
                accountNo = int(input("\nEnter The account No: "))
                self.deleteAccount(accountNo)
            elif choice == '7':
                accountNo = int(input("\nEnter The account No: "))
                self.modifyAccount(accountNo)
            elif choice == '8':
                print("\n\t__Thank You!__")
            else:
                print("Invalid choice")
            print("\n\tPress any key tou continue...")
            input()

    def writeAccount(self):
        account = Account()
        account.createAccount()
        self.writeAccountsFile(account)

    def displayAll(self):
        file = pathlib.Path("accounts.data")
        if file.exists():
            infile = open('accounts.data', 'rb')
            mylist = pickle.load(infile)
            print("__" * 60)
            print(
                "Account No\t\tName\t\tAddress\t\tNumber\t\tType\t\tDeposit\t\tSecret Key")
            print("__" * 60)
            for item in mylist:
                print(item.ID, "\t\t", item.name, "\t\t", item.address, "\t\t",
                      item.number, "\t\t", item.type, "\t\t", item.deposit, "\t\t", item.key)
            infile.close()
        else:
            print("\nNo records to display!")

    def displaySp(self, num):
        file = pathlib.Path("accounts.data")
        if file.exists():
            infile = open('accounts.data', 'rb')
            mylist = pickle.load(infile)
            infile.close()
            found = False
            for item in mylist:
                if int(item.ID) == num:
                    print("Your account Balance is = ", item.deposit)
                    found = True
        else:
            print("No records to Search")
        if not found:
            print("No record with this number")

    def depositAndWithdraw(self, accountNo, function):
        file = pathlib.Path("accounts.data")
        invalid = False
        if file.exists():
            infile = open('accounts.data', 'rb')
            mylist = pickle.load(infile)
            infile.close()
            attempts = 1
            check = False
            for item in mylist:
                if int(item.ID) == accountNo:
                    check = True
                    inputKey = input("Enter your secret key: ")
                    while inputKey != item.key and attempts < 3:
                        inputKey = input("Enter your secret key: ")
                        attempts += 1
                    if inputKey != item.key and attempts == 3:
                        print("Invalid key! existing System...")
                        invalid = True
                        break
                    if function == 1:
                        amount = int(input("Enter the amount to deposit: "))
                        item.deposit += amount
                        print("\tSuccessfully Deposited!")
                    elif function == 2:
                        amount = int(input("Enter the amount to withdraw: "))
                        if amount <= item.deposit:
                            if item.type == 'A':
                                if item.deposit - amount > 100:
                                    item.deposit -= amount
                                    print("\tSuccessfully Withdrawn!")
                                else:
                                    print(
                                        "You must have 100AED balance, Withdrawl unsuccessful!")
                                    break
                            elif item.type == 'S':
                                if item.deposit - amount > 1000:
                                    item.deposit -= amount
                                    print("\tSuccessfully Withdrawn!")
                                else:
                                    print(
                                        "You must have 1000AED balance, Withdrawl unsuccessful!")
                                    break
                            else:
                                if item.deposit - amount > 2000:
                                    item.deposit -= amount
                                    print("\tSuccessfully Withdrawn!")
                                else:
                                    print(
                                        "You must have 2000AED balance, Withdrawl unsuccessful!")
                                    break
                        else:
                            print("You don't have enough money!")
            if check is False:
                print("No record found with this account Number!")
        os.remove('accounts.data')
        outfile = open('newaccounts.data', 'wb')
        pickle.dump(mylist, outfile)
        outfile.close()
        os.rename('newaccounts.data', 'accounts.data')
        if invalid == True:
            exit()

    def deleteAccount(self, num):
        file = pathlib.Path("accounts.data")
        if file.exists():
            infile = open('accounts.data', 'rb')
            oldlist = pickle.load(infile)
            infile.close()
            newlist = []
            check = False
            for item in oldlist:
                if int(item.ID) != num:
                    newlist.append(item)
                if int(item.ID) == num:
                    print("Account deleted successfully!")
                    check = True
            if check == False:
                print("No account with this ID!")
            os.remove('accounts.data')
            outfile = open('newaccounts.data', 'wb')
            pickle.dump(newlist, outfile)
            outfile.close()
            os.rename('newaccounts.data', 'accounts.data')

    def modifyAccount(self, num):
        file = pathlib.Path("accounts.data")
        if file.exists():
            infile = open('accounts.data', 'rb')
            oldlist = pickle.load(infile)
            infile.close()
            check = False
            for item in oldlist:
                if int(item.ID) == num:
                    print("\nYour account number is: ", item.ID)
                    item.name = input("Enter the account holder name : ")
                    item.address = input("Enter the account holder address: ")
                    item.number = int(input("Ente the acount holder number: "))
                    item.type = input("Ente the type of account [A/S/B]: ")
                    item.deposit = int(input("Enter The Initial amount: "))
                    print("\n\tAccount Modified Successfully!")
                    check = True
            if check == False:
                print("No account with this ID!")
            os.remove('accounts.data')
            outfile = open('newaccounts.data', 'wb')
            pickle.dump(oldlist, outfile)
            outfile.close()
            os.rename('newaccounts.data', 'accounts.data')

    def writeAccountsFile(self, account):
        file = pathlib.Path("accounts.data")
        if file.exists():
            infile = open('accounts.data', 'rb')
            oldlist = pickle.load(infile)
            oldlist.append(account)
            infile.close()
            os.remove('accounts.data')
        else:
            oldlist = [account]
        outfile = open('newaccounts.data', 'wb')
        pickle.dump(oldlist, outfile)
        outfile.close()
        os.rename('newaccounts.data', 'accounts.data')


main = UnitedBank()
date = datetime.datetime.now()
print(date)
