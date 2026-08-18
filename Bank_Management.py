import mysql.connector

con = mysql.connector.connect(
    user = 'root',
    password = 'sathvika@4260',
    database = 'bank_db',
    host = 'localhost'
)

crsr = con.cursor()

# query = """
#             CREATE TABLE ACCOUNTS
#             (ACC_NO INT PRIMARY KEY AUTO_INCREMENT,
#             CUST_NAME VARCHAR(30), BALANCE DECIMAL(10,2))
#         """
# crsr.execute(query)
# con.commit()

def create_account():
    name = input("Enter your name:")
    balance = float(input("Enter your initial balance:"))
    query = """
                INSERT INTO ACCOUNTS
                (CUST_NAME,BALANCE)
                VALUES(%s,%s)
            """
    crsr.execute(query,(name,balance))
    con.commit()
    print("Account created successfully !!")

def deposit():
    acc_no = int(input("Enter your account number:"))
    amount = int(input("Enter amount:"))
    if amount > 0:
        query = """
                    UPDATE ACCOUNTS
                    SET BALANCE = BALANCE + %s
                    WHERE ACC_NO = %s
                """
        crsr.execute(query,(amount,acc_no))
        con.commit()
        print("Amount credited successfully !!")
    else:
        print("Enter valid amount !")

def check_balance():
    acc_no = int(input("Enter your account number:"))
    query = """
                SELECT * FROM ACCOUNTS WHERE ACC_NO = %s
            """
    crsr.execute(query,(acc_no,))
    res = crsr.fetchone()
    if res != None:
       print("-------Account Details----------")
       print("Account Number:",res[0])
       print("Account Holer name:",res[1])
       print("Account balance:",res[2])
       print("--------------------------------")
    else:
        print("Account Not Found !")

def withdraw():
    acc_no = int(input("Enter your account number:"))
    amount = int(input("Enter amount:"))
    query = """
                SELECT BALANCE FROM ACCOUNTS WHERE ACC_NO = %s
            """
    crsr.execute(query,(acc_no,))
    res = crsr.fetchone()
    if res != None:
       bal = res[0] 
    else:
        print("Account Not Found !")
        return
    if bal  > amount:
        query = """
                    UPDATE ACCOUNTS
                    SET BALANCE = BALANCE - %s
                    WHERE ACC_NO = %s
                """
        crsr.execute(query,(amount,acc_no))
        con.commit()
        print("Amount Debited successfully !!")
    else:
        print("Insufficient Balance")

def transfer_amount():
    sender = int(input("Enter sender's account number:"))
    receiver = int(input("Enter reciever's account number:"))
    amount = int(input("Enter amount:"))
    if amount>0:
        query = """
                    SELECT BALANCE FROM ACCOUNTS WHERE ACC_NO = %s
                """
        crsr.execute(query,(sender,))
        res = crsr.fetchone()
        if res != None:
            money = res[0] 
            if money>=amount:
                try:
                    query1 = """
                                UPDATE ACCOUNTS
                                SET BALANCE = BALANCE - %s
                                WHERE ACC_NO = %s
                            """
                    crsr.execute(query1,(amount,sender))
                    query2 = """
                                SELECT BALANCE FROM ACCOUNTS WHERE ACC_NO = %s
                            """
                    crsr.execute(query2,(receiver,))
                    res = crsr.fetchone()
                    if res != None: 
                        query3 = """
                                    UPDATE ACCOUNTS
                                    SET BALANCE = BALANCE + %s
                                    WHERE ACC_NO = %s
                                """
                        crsr.execute(query3,(amount,receiver))
                    else:
                        raise Exception("Reciever Account not found!!")
                    con.commit()
                    print("Amount transfered successfully !!")
                except Exception as e:
                    con.rollback()
                    print("Transaction Failed..!")
                    print(e)
            else:
                print("Insufficient Balance")
            
        else:
            print("Account Not Found !")
            return
    else:
        print("Invalid amount !!")

def delete_account():
    acc_no = int(input("Enter your account number:"))
    query = """
                DELETE FROM ACCOUNTS WHERE ACC_NO=%s
            """
    crsr.execute(query,(acc_no,))
    if crsr.rowcount>0:
        print('Account Deleted Successfully!!')
        con.commit()
    else:
        print("account does not exists!!")

def view_all_accounts():
    query = """
                SELECT * FROM ACCOUNTS
            """
    crsr.execute(query)
    rows = crsr.fetchall()
    con.commit()
    print("---------All accounts details-----------")
    for row in rows:
        print("\nAccount No:",row[0])
        print("Account holder name:",row[1])
        print("Account holder name:",row[2])
        print("--------------------------------------")

print('<======= WELECOME TO BANK MANAGEMENT SYSTEM =======>')

while True:
    print('\n1. CREATE ACCOUNT')
    print('2. DEPOSIT AMOUNT')
    print('3. WITHDRAW AMOUNT')
    print('4. CHECK BALANCE')
    print('5. TRANSFER MONEY')
    print('6. DELETE ACCOUNT')
    print('7. VIEW ALL ACCOUNTS')
    print('8. EXIT FROM THE APP')

    choice = int(input('Enter your choice: '))

    match choice:
        case 1: create_account()
        case 2: deposit()
        case 3: withdraw()
        case 4: check_balance()
        case 5: transfer_amount()
        case 6: delete_account()
        case 7: view_all_accounts()
        case 8:
            print('THANK YOU, VISIT AGAIN..!')
            if crsr != None:
                crsr.close()
            if con != None:
                con.close()
            break
        case _: print('Invalid choice, Try again!')