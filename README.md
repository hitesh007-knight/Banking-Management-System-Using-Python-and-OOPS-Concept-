A simple Bank Management System built in Python, with two versions:

Command-line interface (CLI) – Run in terminal

Streamlit Web App – Run in browser

The project allows users to create accounts, deposit money, withdraw money, update details, and delete accounts.
Data is stored persistently in a JSON file (data.json), so accounts remain saved even after closing the program.


📌 Features

Create a new bank account with:

Name, Age, Email, PIN

Randomly generated unique account number

Deposit money (limit: ₹1 Lakh per transaction)

Withdraw money (with balance check)

Show account details (secured with Account No. & PIN)

Update account details (Name, Email, PIN)

Delete account


🛠️ Tech Stack

Python 3.x

Streamlit (for web app)

JSON (for storage)

Random & String (for account number generation)

Pathlib (for file handling)
Persistent storage using data.json

Streamlit App UI for user-friendly web interface
