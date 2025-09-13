import json
import random
import string
from pathlib import Path
import streamlit as st

# -------------------- Bank Class --------------------
class Bank:
    database = "data.json"
    data = []

    # Load existing data
    try:
        if Path(database).exists():
            with open(database, "r") as fs:
                data = json.loads(fs.read())
        else:
            data = []
    except Exception as err:
        st.error(f"An exception occurred: {err}")

    @staticmethod
    def update():
        with open(Bank.database, "w") as fs:
            fs.write(json.dumps(Bank.data, indent=4))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        acc_id = alpha + num + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18:
            return None, "❌ Sorry, you are not eligible for creating an account."
        
        info = {
            "Name": name,
            "Age": age,
            "Email": email,
            "Pin": pin,
            "AccountNo.": cls.__accountgenerate(),
            "Balance": 0
        }
        cls.data.append(info)
        cls.update()
        return info, "✅ Your account has been created successfully!"

    @classmethod
    def deposit(cls, accno, pin, amount):
        userdata = [i for i in cls.data if i["AccountNo."] == accno and i["Pin"] == pin]
        if not userdata:
            return None, "❌ No such user found"
        if amount <= 0 or amount > 100000:
            return None, "❌ Deposit amount must be between 1 and 100000."
        
        userdata[0]["Balance"] += amount
        cls.update()
        return userdata[0], f"✅ {amount} deposited successfully!"

    @classmethod
    def withdraw(cls, accno, pin, amount):
        userdata = [i for i in cls.data if i["AccountNo."] == accno and i["Pin"] == pin]
        if not userdata:
            return None, "❌ No such user found"
        if userdata[0]["Balance"] < amount:
            return None, "❌ Insufficient balance."
        
        userdata[0]["Balance"] -= amount
        cls.update()
        return userdata[0], f"✅ {amount} withdrawn successfully!"

    @classmethod
    def show_details(cls, accno, pin):
        userdata = [i for i in cls.data if i["AccountNo."] == accno and i["Pin"] == pin]
        if not userdata:
            return None, "❌ No such user found"
        return userdata[0], "✅ Account details found!"

    @classmethod
    def update_details(cls, accno, pin, name=None, email=None, new_pin=None):
        userdata = [i for i in cls.data if i["AccountNo."] == accno and i["Pin"] == pin]
        if not userdata:
            return None, "❌ No such user found"
        
        if name:
            userdata[0]["Name"] = name
        if email:
            userdata[0]["Email"] = email
        if new_pin:
            userdata[0]["Pin"] = new_pin
        
        cls.update()
        return userdata[0], "✅ Details updated successfully!"

    @classmethod
    def delete_account(cls, accno, pin):
        userdata = [i for i in cls.data if i["AccountNo."] == accno and i["Pin"] == pin]
        if not userdata:
            return None, "❌ No such user found"
        
        cls.data.remove(userdata[0])
        cls.update()
        return None, "✅ Account deleted successfully!"


# -------------------- Streamlit UI --------------------
st.title("🏦 Bank Management System")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Select Operation", menu)

if choice == "Create Account":
    st.subheader("📝 Create New Account")
    name = st.text_input("Enter your Name")
    age = st.number_input("Enter your Age", min_value=1, step=1)
    email = st.text_input("Enter your Email")
    pin = st.number_input("Enter a 4-digit PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Create Account"):
        info, msg = Bank.create_account(name, age, email, pin)
        st.info(msg)
        if info:
            st.json(info)

elif choice == "Deposit Money":
    st.subheader("💰 Deposit Money")
    accno = st.text_input("Enter Account Number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)
    amount = st.number_input("Enter Amount", min_value=1, step=1)

    if st.button("Deposit"):
        info, msg = Bank.deposit(accno, pin, amount)
        st.info(msg)
        if info:
            st.json(info)

elif choice == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")
    accno = st.text_input("Enter Account Number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)
    amount = st.number_input("Enter Amount", min_value=1, step=1)

    if st.button("Withdraw"):
        info, msg = Bank.withdraw(accno, pin, amount)
        st.info(msg)
        if info:
            st.json(info)

elif choice == "Show Details":
    st.subheader("📋 Show Account Details")
    accno = st.text_input("Enter Account Number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Show"):
        info, msg = Bank.show_details(accno, pin)
        st.info(msg)
        if info:
            st.json(info)

elif choice == "Update Details":
    st.subheader("✏️ Update Account Details")
    accno = st.text_input("Enter Account Number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)
    name = st.text_input("Enter new Name (optional)")
    email = st.text_input("Enter new Email (optional)")
    new_pin = st.number_input("Enter new PIN (optional)", min_value=1000, max_value=9999, step=1, value=0)

    if st.button("Update"):
        new_pin_val = new_pin if new_pin != 0 else None
        info, msg = Bank.update_details(accno, pin, name or None, email or None, new_pin_val)
        st.info(msg)
        if info:
            st.json(info)

elif choice == "Delete Account":
    st.subheader("🗑️ Delete Account")
    accno = st.text_input("Enter Account Number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Delete"):
        _, msg = Bank.delete_account(accno, pin)
        st.info(msg)
