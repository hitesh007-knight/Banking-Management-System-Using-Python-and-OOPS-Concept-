import json
import random
import string
from pathlib import Path



class Bank:
    database="data.json"
    data= []

    try: # Koi bhi glti se error na aaye isiliye pure code ko try block me daal dia
        if Path(database).exists(): # Agr exist krta h to hi open krna file ko
            with open(database,"r") as fs: #kuch nhi dia h to by default "r" mode hi rhta h
                data=json.loads(fs.read()) #Isse json file se data read hoke data waale dummy variable me aajayega
        else:
            print("No such file exists")        
    except Exception as err:
        print(f"An exception occured as {err}")

    @staticmethod
    def update():
        with open(Bank.database,"w") as fs:
            fs.write(json.dumps(Bank.data))# isse humne jo dummy data variable tha usse data leke main data.json file jo h usme data fill krdia
    @classmethod
    def __accountgenerate(cls):  #This function creates a random account number containing 3letters,3 numbers,and 1 sp. char
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spchar=random.choices("!@#$%^&*",k=1) # saare choices mese koi ek hi hum use kr skte h
        id=alpha+num+spchar
        random.shuffle(id)
        return "".join(id)



    def CreateAccount(self):
        info={
            "Name":input("Tell Your Name:-"),
            "Age":int(input("Tell your age:-")),
            "Email":input("Tell your emailid:-"),
            "Pin":int(input("Tell your 4 digit pin:-")),
            "AccountNo.":Bank.__accountgenerate(),
            "Balance":0
            }
        if info["Age"]<18:
            print("Sorry you are not eligible for creating an account")
        else:
            print("Your account has been created successfully")
            for i in info:
                print(f"{i}:{info[i]}")
            print("Please note down your account number")   

            Bank.data.append(info) #Phle info se data variable me bhra phir usse data.json me bhrenge
            Bank.update()  

    def Depositmoney(self):
        accno=input("Please tell your account number:-")
        pin=int(input("Please tell ypur pin:-"))

        userdata=[i for i in Bank.data if i["AccountNo."]==accno and i["Pin"]==pin] #Ye ek list comprehension h dummy data me jaake dekhega ki dia gya jo accno, and pin koi bhi dummy data me pde dictionary se match hota h to wo dictionary userdata me extract krlega

        if userdata==False: #False aata tha jb koi empty dictionary,list,0 ye sb rhta tha
            print("Sorry no data found") 
        else:
            amount=int(input("Please tell how much you want to deposit:-"))
            if amount>100000 or amount<0:
                print("You cannot deposit amount greater than 1Lakh or less than 0")
            else:
                print(userdata)
                userdata[0]["Balance"]+=amount   #Deep copy-- The good thing is data userdata waali dictionary ko update krne se dummy data ki wo waali dictionary bhi update ho jayegi
                #[0] lia kyuki userdata ki dictionary ek list me aa rhi h to uss list ka oth index yaani uski phli dictionary kyuki ek hi honi h usme to wo access kr rhe h
                
                Bank.update() #The hume to dummy data ke saath saath json file me bhi update krna h
                print("Your money amount has been deposited successfully ")

    def Withdrawmoney(self):
        accno=input("Please tell your account number:-")
        pin=int(input("Please tell ypur pin:-"))

        userdata=[i for i in Bank.data if i["AccountNo."]==accno and i["Pin"]==pin] #Ye ek list comprehension h dummy data me jaake dekhega ki dia gya jo accno, and pin koi bhi dummy data me pde dictionary se match hota h to wo dictionary userdata me extract krlega

        if userdata==False: #False aata tha jb koi empty dictionary,list,0 ye sb rhta tha
            print("Sorry no data found") 
        else:
            amount=int(input("Please tell how much you want to withdraw:-"))
            if userdata[0]["Balance"]<amount:
                print("Sorry you do not have this much balance in the account in order to be withdrwan")
            else:
                print(userdata)
                userdata[0]["Balance"] -=amount   #Deep copy-- The good thing is data userdata waali dictionary ko update krne se dummy data ki wo waali dictionary bhi update ho jayegi
                #[0] lia kyuki userdata ki dictionary ek list me aa rhi h to uss list ka oth index yaani uski phli dictionary kyuki ek hi honi h usme to wo access kr rhe h
                
                Bank.update() #The hume to dummy data ke saath saath json file me bhi update krna h
                print("Your money amount has been withdrawn successfully ")

    def Showdetails(self):
        accno=input("Please tell your account number:-")
        pin=int(input("Please tell ypur pin:-"))

        userdata=[i for i in Bank.data if i["AccountNo."]==accno and i["Pin"]==pin] #Ye ek list comprehension h dummy data me jaake dekhega ki dia gya jo accno, and pin koi bhi dummy data me pde dictionary se match hota h to wo dictionary userdata me extract krlega

        if userdata==False: #False aata tha jb koi empty dictionary,list,0 ye sb rhta tha
            print("Sorry no such user found")
        else:
            print("Your account details are--\n\n")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")

    def Updatedetails(self):
        accno=input("Please tell your account number:-")
        pin=int(input("Please tell ypur pin:-"))

        userdata=[i for i in Bank.data if i["AccountNo."]==accno and i["Pin"]==pin] #Ye ek list comprehension h dummy data me jaake dekhega ki dia gya jo accno, and pin koi bhi dummy data me pde dictionary se match hota h to wo dictionary userdata me extract krlega

        if userdata==False: #False aata tha jb koi empty dictionary,list,0 ye sb rhta tha
            print("Sorry no such user found")
        else:
            print("You cannot change age,account no.,balance\n")

            print("Fill the details for chamge or leave it empty for no change\n")

            newdata={
                "Name": input("Enter new name or Press Enter to skip:-\n"),
                "Email":input("Enter new email or Press Enter to skip:-\n"),
                "Pin": input("Enter new Pin or Press Enter to skip:-\n")
            }  

            if newdata["Name"]=="":
                newdata["Name"]=userdata[0]["Name"]  
            if newdata["Email"]=="":
                newdata["Email"]=userdata[0]["Email"]       
            if newdata["Pin"]=="":
                newdata["Pin"]=userdata[0]["Pin"]       

            newdata["Age"]=userdata[0]["Age"] 
            newdata["AccountNo."]=userdata[0]["AccountNo."]
            newdata["Balance"]=userdata[0]["Balance"]

            if type(newdata["Pin"])==str:
                newdata["Pin"]=int(newdata["Pin"])    

            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]
            Bank.update()
            print("Your bank details are successfully updated")            
    
    def Deletedetails(self):
        accno=input("Please tell your account number:-\n")
        pin=int(input("Please tell ypur pin:-"))

        userdata=[i for i in Bank.data if i["AccountNo."]==accno and i["Pin"]==pin] #Ye ek list comprehension h dummy data me jaake dekhega ki dia gya jo accno, and pin koi bhi dummy data me pde dictionary se match hota h to wo dictionary userdata me extract krlega

        if userdata==False: #False aata tha jb koi empty dictionary,list,0 ye sb rhta tha
            print("Sorry no such user found")
        else:
            check=print("Press Y if you want to delete the account or press N")

            if check=="N" or check=="n":
                print("Bypassed")
            else:
                index=Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account deleted successfully")
                Bank.update()







user=Bank()


print("Press 1 for creating an account ")
print("Press 2 for depositing the money in the account ")
print("Press 3 for withdrawing the money ")
print("Press 4 for details")
print("Press 5 for updating the details")
print("Press 6 for deleting the account")

check=int(input("Enter your response:-"))

if check==1:
    user.CreateAccount()

if check==2:
    user.Depositmoney()

if check==3:
    user.Withdrawmoney()    

if check==4:
    user.Showdetails()    

if check==5:
    user.Updatedetails()    

if check==6:
    user.Deletedetails()
