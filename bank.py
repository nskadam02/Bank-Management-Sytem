from tkinter import*
from tkinter import messagebox
# from openpyxl import load_workbook
import xlrd
# import pandas as pd
import random
import pickle
import os
import pathlib
import pymongo

class Account :
    accNo = 0
    name = ''
    deposit=0
    type = ''
    
    def createAccount(self,fname,actype,deposit):
        # self.accNo=account_no
        self.name =fname 
        self.type =actype
        self.deposit =deposit
        print("\n\n\nAccount Created")
       
    
    def showAccount(self):
        print("Account Number : ",self.accNo)
        print("Account Holder Name : ", self.name)
        print("Type of Account",self.type)
        print("Balance : ",self.deposit)
    
    def modifyAccount(self):
        print("Account Number : ",self.accNo)
        self.name = input("Modify Account Holder Name :")
        self.type = input("Modify type of Account :")
        self.deposit = int(input("Modify Balance :"))
        
    def depositAmount(self,amount):
        self.deposit += amount
    
    def withdrawAmount(self,amount):
        self.deposit -= amount
    
    def report(self):
        print(self.accNo, " ",self.name ," ",self.type," ", self.deposit)
    
    def getAccountNo(self):
        return self.accNo
    def getAcccountHolderName(self):
        return self.name
    def getAccountType(self):
        return self.type
    def getDeposit(self):
        return self.deposit
    
def Connect():
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]

def writeAccount():
    # a=int(AccountNumber.get())
    f=First_name.get()
    t=Acc_type.get()
    d=int(deposit.get())
    if d<500:
         messagebox.showerror("Error","Please deposit ammount more than 500")
    else:     
         account = Account()
         account.createAccount(f,t,d)
         writeAccountsFile(account)
    clear_all()     

def writeAccountsFile(account) :
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mydb
    num=str(mydb.sequence.find_one_and_update(
         {'collection':'admin_collection'},
         {'$inc':{'id':1}},
     ).get('id'))
    print(num)

    dict={"Account_no":num,"name":account.name,"type":account.type,"balance":account.deposit}
    x = mydb.customers.insert_one(dict)
    if(x.inserted_id):
        messagebox.showinfo("Done","Account Created Successfully!!Account Number:"+num)
    else:
       messagebox.error("error","Account alresdy exist")   
    clear_all()

    
def displaySp(): 
    newEnquireAccountNumber=enquireAccountNumber.get()
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    y=mycol.find_one({"Account_no":newEnquireAccountNumber})
    enquire_name=y['name']
    enquireType=y['type']
    balance=y['balance']

    messagebox.showinfo("Done","Account number:"+newEnquireAccountNumber+"  account holders name:"+enquire_name+", account type: "+enquireType+", balance:"+str(balance))
    print(enquire_name)
    # print(enquireAccountNumber)
    print(enquireType)
    print(balance)
    clear_all()

def deposit_ammount(): 
    a=depositAccountNumber.get()
    d=int(Deposit_ammount.get())
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    y=mycol.find_one({"Account_no":a})
    z=y['balance']
    x=z+d
    myquery = { "Account_no":a }
    newvalues = { "$set": { "balance":x } }   
    y=mycol.update_one(myquery, newvalues)
    if y.modified_count==1:
      messagebox.showinfo("Done","Account Deposit Successfull ")
    
    for x in mycol.find():
       print(x)
    clear_all()

def withdraw():
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    a=withdrawAccountNumber.get()
    am=int(Withdraw_ammount.get())
    y=mycol.find_one({"Account_no":a})
    z=y['balance']
    if z<am:
        messagebox.showerror("error","Insufficient balance ")
    else:
        x=z-am
        myquery = { "Account_no":a }
        newvalues = { "$set": { "balance":x } }   
        y=mycol.update_one(myquery, newvalues)
        if y.modified_count==1:
          messagebox.showinfo("Done","Account withdraw Successfull ")
    
    for x in mycol.find():
       print(x)
    

    # db.sales.aggregate( [ { $project: { item: 1, dateDifference: { $subtract: [ new Date(), "$date" ] } } } ] )
    clear_all()
def deleteAccount():
    # print("hello")
    a=deleteAccountNumber.get()
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"] 
    myquery = { "Account_no": a }
    t=mycol.delete_one(myquery)
    # print(t.deleted_count)

#print the customers collection after the deletion:
    for x in mycol.find():
      print(x)
    if t.deleted_count==0:
        messagebox.showinfo("Done","Account does not exist ")

    if t.deleted_count==1:
      messagebox.showinfo("Done","Account Deleted Successfull ")
    clear_all()       
     
def modifyAccount():
    print("hello")
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    a=newAccountNumber.get()
    f=new_name.get()
    t=newAcc_type.get()
    d=int(newdeposit.get())
    myquery = { "Account_no":a }
    newvalues = { "$set": { "name":f,"type":t,"balance":d } }

    y=mycol.update_one(myquery, newvalues)
    if y.modified_count==1:
        messagebox.showinfo("Done","Account modified Successfull ")
     
    for x in mycol.find():
       print(x)
    clear_all()   

       
   



root=Tk()                               #Main window 
f=Frame(root)
frame1=Frame(root)
frame2=Frame(root)
frame3=Frame(root)
frame4=Frame(root)
frame5=Frame(root)
frame6=Frame(root)
frame7=Frame(root)
root.title("Bank Management System")
root.geometry("830x395")
root.configure(background="blue")

scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

AccountNumber=StringVar()  
First_name=StringVar() 
Acc_type=StringVar()
deposit=StringVar()
newAccountNumber=StringVar()  
new_name=StringVar() 
newAcc_type=StringVar()
newdeposit=StringVar()
Deposit_ammount=StringVar()
Withdraw_ammount=StringVar()
withdrawAccountNumber=StringVar()
depositAccountNumber=StringVar()
enquireAccountNumber=StringVar()
deleteAccountNumber=StringVar()
# enquire_name=StringVar()
# newEnquireAccountNumber=StringVar()
# enquireType=StringVar()
# balance=StringVar()


def getRandomNumber():
        ability = random.randrange(1000000,9999999)
        return ability

def clear_all():             #for clearing the entry widgets
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame5.pack_forget()
    frame6.pack_forget()
    frame7.pack_forget()


def Create_account():
     
    myclient = pymongo.MongoClient()
    mydb = myclient["test"]
    mycol = mydb["reviews"]
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame5.pack_forget()
    frame6.pack_forget()
    frame7.pack_forget() 
    # AccountNumber=getRandomNumber

    emp_first_name=Label(frame1,text="Enter Account holders name: ",bg="black",fg="white")
    emp_first_name.grid(row=1,column=1,padx=10)
    e1=Entry(frame1,textvariable=First_name)
    e1.grid(row=1,column=2,padx=20)
    e1.focus()
    # Account_number=Label(frame1,text="Account Number: ",bg="black",fg="white")
    # Account_number.grid(row=2,column=1,padx=10)
    # e2=Entry(frame1,textvariable=AccountNumber)
    # e2.grid(row=2,column=2,padx=20)
    AccountType=Label(frame1,text="Select Account Type: ",bg="black",fg="white")
    AccountType.grid(row=3,column=1,padx=10)
    Acc_type.set("Select Type")
    e3=OptionMenu(frame1,Acc_type,"Current","Savings")
    e3.grid(row=3,column=2,padx=20)
    Deposit=Label(frame1,text="Enter deposit amount grater than 500: ",bg="black",fg="white")
    Deposit.grid(row=4,column=1,padx=10)
    e4=Entry(frame1,textvariable=deposit)
    e4.grid(row=4,column=2,padx=20)
    button7=Button(frame1,text="Add account",command=writeAccount)
    button7.grid(row=5,column=2,pady=10)
    frame1.configure(background="black")
    frame1.pack(pady=10)
    # displayAll()

def Modify_account():
    frame1.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame5.pack_forget()
    frame6.pack_forget()
    frame7.pack_forget()
    
    emp_first_name=Label(frame2,text="Enter new Account holders name: ",bg="black",fg="white")
    emp_first_name.grid(row=2,column=1,padx=10)
    e1=Entry(frame2,textvariable=new_name)
    e1.grid(row=2,column=2,padx=20)
    Account_number=Label(frame2,text="Account Number: ",bg="black",fg="white")
    Account_number.grid(row=1,column=1,padx=10)
    e2=Entry(frame2,textvariable=newAccountNumber)
    e2.grid(row=1,column=2,padx=20)
    e2.focus()
    AccountType=Label(frame2,text="Select new Account Type: ",bg="black",fg="white")
    AccountType.grid(row=3,column=1,padx=10)
    newAcc_type.set("Select Type")
    e3=OptionMenu(frame2,newAcc_type,"Current","Savings")
    e3.grid(row=3,column=2,padx=20)
    Deposit=Label(frame2,text="Enter deposit amount grater than 500: ",bg="black",fg="white")
    Deposit.grid(row=4,column=1,padx=10)
    e4=Entry(frame2,textvariable=newdeposit)
    e4.grid(row=4,column=2,padx=20)
    button7=Button(frame2,text="Modify account",command=modifyAccount)
    button7.grid(row=5,column=2,pady=10)
    frame2.configure(background="black")
    frame2.pack(pady=10)
    # displayAll()

def Deposit():
    frame1.pack_forget()
    frame2.pack_forget()
    frame4.pack_forget()
    frame5.pack_forget()
    frame6.pack_forget()
    frame7.pack_forget()    

    Account_number=Label(frame3,text=" Enter Account Number: ",bg="black",fg="white")
    Account_number.grid(row=1,column=1,padx=10)
    e2=Entry(frame3,textvariable=depositAccountNumber)
    e2.grid(row=1,column=2,padx=20)
    e2.focus()
    DepositAmmount=Label(frame3,text="Enter ammount to deposit: ",bg="black",fg="white")
    DepositAmmount.grid(row=2,column=1,padx=10)
    e1=Entry(frame3,textvariable=Deposit_ammount)
    e1.grid(row=2,column=2,padx=20)
    button7=Button(frame3,text="Deposit ammount",command=deposit_ammount)
    button7.grid(row=5,column=2,pady=10)
    frame3.configure(background="black")
    frame3.pack(pady=10)
    # displayAll()

def Withdraw():
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame5.pack_forget()
    frame6.pack_forget()
    frame7.pack_forget() 
    
    Account_number=Label(frame4,text=" Enter Account Number: ",bg="black",fg="white")
    Account_number.grid(row=1,column=1,padx=10)
    e2=Entry(frame4,textvariable=withdrawAccountNumber)
    e2.grid(row=1,column=2,padx=20)
    e2.focus()
    DepositAmmount=Label(frame4,text="Enter ammount to withdraw: ",bg="black",fg="white")
    DepositAmmount.grid(row=2,column=1,padx=10)
    e1=Entry(frame4,textvariable=Withdraw_ammount)
    e1.grid(row=2,column=2,padx=20)
    button7=Button(frame4,text="Withdraw ammount",command=withdraw)
    button7.grid(row=5,column=2,pady=10)
    frame4.configure(background="black")
    frame4.pack(pady=10)
    # displayAll()

def Enquiry():
   
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame6.pack_forget()
    frame7.pack_forget() 

    Account_number=Label(frame5,text=" Enter Account Number: ",bg="black",fg="white")
    Account_number.grid(row=1,column=1,padx=10)
    e2=Entry(frame5,textvariable=enquireAccountNumber)
    e2.grid(row=1,column=2,padx=20)
    e2.focus()
    button7=Button(frame5,text="Enuire",command=displaySp)
    button7.grid(row=3,column=2,pady=10)
    # button7=Button(frame5,text="Show Info",command=GiveInfo)
    # button7.grid(row=4,column=2,pady=10)
    frame5.configure(background="black")
    frame5.pack(pady=10)

def Delete():
    
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame5.pack_forget()
    frame7.pack_forget() 

    Account_number=Label(frame6,text=" Enter Account Number to close: ",bg="black",fg="white")
    Account_number.grid(row=1,column=1,padx=10)
    e2=Entry(frame6,textvariable=deleteAccountNumber)
    e2.grid(row=1,column=2,padx=20)
    e2.focus()
    button7=Button(frame6,text="Delete Account",command=deleteAccount)
    button7.grid(row=5,column=2,pady=10)
    frame6.configure(background="black")
    frame6.pack(pady=10) 
    

def GiveInfo():
    newEnquireAccountNumber=enquireAccountNumber.get()
    myclient = pymongo.MongoClient()
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    y=mycol.find_one({"Account_no":newEnquireAccountNumber})
    enquire_name:StringVar()=y['name']
    enquireType=y['type']
    balance=y['balance']
    print(enquire_name)
    # print(enquireAccountNumber)
    print(enquireType)
    print(balance)

    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame5.pack_forget()
    # frame6.pack_forget()
    emp_first_name=Label(frame7,text=" Account holders name: ",bg="black",fg="white")
    emp_first_name.grid(row=2,column=1,padx=10)
    e1=Entry(frame7,textvariable=enquire_name)
    e1.grid(row=2,column=2,padx=20)
    e1.configure(textvariable=enquire_name)
    Account_number=Label(frame7,text="Account Number: ",bg="black",fg="white")
    Account_number.grid(row=1,column=1,padx=10)
    e2=Entry(frame7,textvariable=newEnquireAccountNumber)
    e2.grid(row=1,column=2,padx=20)
    e2.configure(textvariable=enquireAccountNumber)
    # e2.focus()
    Type=Label(frame7,text="Account type: ",bg="black",fg="white")
    Type.grid(row=3,column=1,padx=10)
    e3=Entry(frame7,textvariable=enquireType)
    e3.grid(row=3,column=2,padx=20)
    e3.configure(textvariable=enquireType)
    Total_ammount=Label(frame7,text="Total Balance: ",bg="black",fg="white")
    Total_ammount.grid(row=4,column=1,padx=10)
    e4=Entry(frame7,textvariable=balance)
    e4.grid(row=4,column=2,padx=20)
    e4.configure(textvariable=balance)
    frame7.configure(background="black")
    frame7.pack(pady=10) 






label1=Label(root,text="BANK MANAGEMENT SYSTEM")
label1.config(font=('Italic',16,'bold'), justify=CENTER, background="White",fg="Red", anchor="center")
label1.pack(fill=X)

label2=Label(f,text="Select: ",font=('bold',12), background="Black", fg="White")
label2.pack(side=LEFT,pady=8)
button1=Button(f,text="Create account", background="Brown", fg="White",command=Create_account,width=8)
button1.pack(side=LEFT,ipadx=20,pady=8)
button2=Button(f,text="Modify Account", background="Brown", fg="white", width=8,command=Modify_account)
button2.pack(side=LEFT,ipadx=20,pady=8)
button3=Button(f,text="Deposit", background="Brown", fg="White",  width=8,command=Deposit)
button3.pack(side=LEFT,ipadx=20,pady=8)
button4=Button(f,text="Withdraw", background="Brown", fg="White",  width=8,command=Withdraw)
button4.pack(side=LEFT,ipadx=20,pady=8)
button5=Button(f,text="Balance Enquiry", background="Brown", fg="White",  width=8,command=Enquiry)
button5.pack(side=LEFT,ipadx=20,pady=8)
button3=Button(f,text="Close Account", background="Brown", fg="White",  width=8,command=Delete)
button3.pack(side=LEFT,ipadx=20,pady=8)
button6=Button(f,text="Close", background="Brown", fg="White", width=8, command=root.destroy)
button6.pack(side=LEFT,ipadx=20,pady=10)
f.configure(background="Black")
f.pack()

root.mainloop()