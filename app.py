import streamlit as st
from bank import Bank


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)


# ---------------- BANK OBJECT ----------------

bank = Bank()


# ---------------- SIDEBAR ----------------

st.sidebar.title("🏦 Bank Management")

menu = st.sidebar.radio(
    "Select Operation",
    [
        "🏠 Home",
        "➕ Create Account",
        "💰 Deposit",
        "💸 Withdraw",
        "📋 Account Details",
        "✏️ Update Account",
        "🗑️ Delete Account"
    ]
)


# =====================================================
# HOME
# =====================================================

if menu == "🏠 Home":

    st.title("🏦 Bank Management System")

    st.write(
        "Welcome to the Bank Management System."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Accounts",
            len(bank.data)
        )

    with col2:

        total_balance = sum(
            account["balance"]
            for account in bank.data
        )

        st.metric(
            "Total Balance",
            f"₹{total_balance}"
        )

    with col3:

        st.metric(
            "System Status",
            "Online"
        )

    st.divider()

    st.info(
        "Use the sidebar to create accounts, "
        "deposit money, withdraw money or manage accounts."
    )


# =====================================================
# CREATE ACCOUNT
# =====================================================

elif menu == "➕ Create Account":

    st.title("➕ Create New Account")

    with st.form("create_account"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "Create Account"
        )

        if submit:

            if not name or not email or not pin:

                st.error(
                    "Please fill all fields."
                )

            else:

                success, result = bank.create_account(
                    name,
                    age,
                    gender,
                    email,
                    pin
                )

                if success:

                    st.success(
                        "Account created successfully!"
                    )

                    st.subheader(
                        "Your Account Number"
                    )

                    st.code(
                        result["account_number"]
                    )

                    st.warning(
                        "Please save your account number."
                    )

                else:

                    st.error(result)


# =====================================================
# DEPOSIT
# =====================================================

elif menu == "💰 Deposit":

    st.title("💰 Deposit Money")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    amount = st.number_input(
        "Amount",
        min_value=0,
        step=100
    )

    if st.button("Deposit Money"):

        success, result = bank.deposit(
            account_number,
            pin,
            amount
        )

        if success:

            st.success(
                "Amount deposited successfully!"
            )

            st.metric(
                "New Balance",
                f"₹{result}"
            )

        else:

            st.error(result)


# =====================================================
# WITHDRAW
# =====================================================

elif menu == "💸 Withdraw":

    st.title("💸 Withdraw Money")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    amount = st.number_input(
        "Amount",
        min_value=0,
        step=100
    )

    if st.button("Withdraw Money"):

        success, result = bank.withdraw(
            account_number,
            pin,
            amount
        )

        if success:

            st.success(
                "Amount withdrawn successfully!"
            )

            st.metric(
                "Remaining Balance",
                f"₹{result}"
            )

        else:

            st.error(result)


# =====================================================
# ACCOUNT DETAILS
# =====================================================

elif menu == "📋 Account Details":

    st.title("📋 Account Details")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button("View Account"):

        success, result = bank.get_account(
            account_number,
            pin
        )

        if success:

            st.success(
                "Account found!"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Name:** {result['name']}"
                )

                st.write(
                    f"**Age:** {result['age']}"
                )

                st.write(
                    f"**Gender:** {result['gender']}"
                )

            with col2:

                st.write(
                    f"**Email:** {result['email']}"
                )

                st.write(
                    f"**Account Number:** {result['account_number']}"
                )

                st.metric(
                    "Balance",
                    f"₹{result['balance']}"
                )

        else:

            st.error(result)


# =====================================================
# UPDATE ACCOUNT
# =====================================================

elif menu == "✏️ Update Account":

    st.title("✏️ Update Account")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "Current PIN",
        type="password"
    )

    field = st.selectbox(
        "What do you want to update?",
        [
            "name",
            "email",
            "pin",
            "age",
            "gender"
        ]
    )

    if field == "age":

        value = str(
            st.number_input(
                "New Age",
                min_value=1,
                max_value=120
            )
        )

    elif field == "gender":

        value = st.selectbox(
            "New Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

    else:

        value = st.text_input(
            "New Value",
            type="password" if field == "pin" else "default"
        )

    if st.button("Update Account"):

        success, result = bank.update_account(
            account_number,
            pin,
            field,
            value
        )

        if success:
            st.success(result)

        else:
            st.error(result)


# =====================================================
# DELETE ACCOUNT
# =====================================================

elif menu == "🗑️ Delete Account":

    st.title("🗑️ Delete Account")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    st.warning(
        "⚠️ Deleting an account cannot be undone."
    )

    confirm = st.checkbox(
        "I understand that this account will be permanently deleted."
    )

    if st.button("Delete Account"):

        if not confirm:

            st.error(
                "Please confirm account deletion."
            )

        else:

            success, result = bank.delete_account(
                account_number,
                pin
            )

            if success:

                st.success(result)

            else:

                st.error(result)

    #run program
    #streamlit run app.py