# 💳 **Bank Management System**

## 🚀 **Overview**

Welcome to the **Bank Management System** project! This is a full-fledged web application designed to handle all basic banking operations such as user registration, deposits, withdrawals, money transfers, loan management, and account monitoring. 

It offers a seamless experience for users to manage their finances, while administrators can efficiently monitor and manage user accounts and transactions.

---

## 🌟 **Features**

### 1. **User Registration and Email Verification 📧**
- Users can sign up with their details (name, email, password).
- After registration, a **verification email** is sent to activate the user account.

### 2. **Deposit and Withdrawal 💸**
- Users can **deposit** money into their bank account.
- Users can **withdraw** money from their account.
- **Email notifications** are sent after every deposit and withdrawal.

### 3. **Money Transfer 💰**
- Users can send money to other users by entering the recipient's account details.
- Both sender and recipient get **email notifications** confirming the transfer.

### 4. **Loan Management 💵**
- Users can apply for **loans** (up to **2 loans** per user).
- Loan applications, statuses, and repayment history can be tracked in the user’s dashboard.

### 5. **Bankruptcy Status 💥**
- Users can declare **bankruptcy** if they are unable to manage their financial obligations.
- **Bankrupt users** cannot perform transactions such as deposit, withdrawal, or money transfer.

### 6. **User Dashboard 📊**
- Users can view:
  - Transaction history (deposits, withdrawals, transfers).
  - Loan history (active loans and repayment status).
  - Account balance and **bankruptcy status**.
  - All actions and records are stored for transparency.

### 7. **Admin Dashboard 👨‍💻**
- Admins can manage user accounts, view transaction history, and approve/reject loan applications.
- Admins can monitor user balances, loan statuses, and handle bankruptcy cases.

---

## 🛠 **Workflow**

### **User Registration**
- User signs up with their details (email, name, password).
- An **email verification link** is sent to the user to activate the account.

### **Deposits and Withdrawals**
- After logging in, users can **deposit** funds or **withdraw** money.
- **Email notifications** sent on every transaction.

### **Money Transfer**
- Users can **transfer** money to others, and both users receive **email confirmations**.

### **Loan Applications**
- Users can apply for loans.
- Users can hold a **maximum of two loans** at any given time.

### **Bankruptcy**
- Users can declare bankruptcy if they are unable to pay their debts.
- **Bankrupt users** cannot perform any transactions.

### **Admin Dashboard**
- Admins can monitor user accounts, view transactions, approve/reject loans, and handle bankruptcy statuses.

---

## 🧑‍💻 **Technologies Used**

- **Frontend**: React.js, Bootstrap, React Router
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL or SQLite
- **Email Service**: SMTP (for email notifications)
- **Authentication**: JWT or session-based authentication

---

## ✨ **Project Structure**

