import streamlit as st
import numpy as np
import pandas as pd
import joblib
import bcrypt
import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="wide"
)

# ======================================================
# MONGODB CONNECTION
# ======================================================

MONGO_URI = st.secrets["MONGO_URI"]
try:

    client = MongoClient(MONGO_URI)

    client.admin.command('ping')

    print("✅ MongoDB Connected Successfully")

    db = client["customer_churn"]

    users_collection = db["users"]

    predictions_collection = db["predictions"]

except ConnectionFailure:

    print("❌ MongoDB Connection Failed")

# ======================================================
# LOAD MODEL
# ======================================================


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "churn_model.pkl"
)

model = joblib.load(MODEL_PATH)

# ======================================================
# SESSION STATE
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ======================================================
# FUNCTIONS
# ======================================================

# ---------------- SIGNUP ---------------- #

def signup(username, password):

    existing_user = users_collection.find_one({
        "username": username
    })

    if existing_user:
        return False

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return True

# ---------------- LOGIN ---------------- #

def login(username, password):

    user = users_collection.find_one({
        "username": username
    })

    if user:

        if bcrypt.checkpw(
            password.encode('utf-8'),
            user['password']
        ):
            return True

    return False

# ======================================================
# LOGIN / SIGNUP PAGE
# ======================================================

if not st.session_state.logged_in:

    st.title("🔐 Customer Churn Login System")

    st.markdown("""
    Welcome to the AI-powered telecom churn prediction platform.
    """)

    # ======================================================
    # LOGIN & SIGNUP TABS
    # ======================================================

    login_tab, signup_tab = st.tabs(
        ["Login", "Signup"]
    )

    # ======================================================
    # LOGIN TAB
    # ======================================================

    with login_tab:

        st.subheader("Login")

        login_username = st.text_input(
            "Username",
            key="login_user"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            if login(
                login_username,
                login_password
            ):

                st.session_state.logged_in = True

                st.session_state.username = login_username

                st.success("✅ Login Successful")

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )

    # ======================================================
    # SIGNUP TAB
    # ======================================================

    with signup_tab:

        st.subheader("Create Account")

        signup_username = st.text_input(
            "Create Username",
            key="signup_user"
        )

        signup_password = st.text_input(
            "Create Password",
            type="password",
            key="signup_pass"
        )

        if st.button("Signup"):

            success = signup(
                signup_username,
                signup_password
            )

            if success:

                st.success(
                    "✅ Account Created Successfully"
                )

            else:

                st.error(
                    "❌ Username Already Exists"
                )

# ======================================================
# MAIN DASHBOARD
# ======================================================

else:

    # ======================================================
    # SIDEBAR
    # ======================================================

    st.sidebar.title("📂 Navigation")

    st.sidebar.success(
        f"Logged in as: {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Go To",
        [
            "Prediction Dashboard",
            "Prediction History",
            "Business Explanation"
        ]
    )

    # ======================================================
    # LOGOUT
    # ======================================================

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()

    # ======================================================
    # PREDICTION DASHBOARD
    # ======================================================

    if page == "Prediction Dashboard":

        st.title("📊 Customer Churn Prediction Dashboard")

        st.markdown("""
        This AI-powered system predicts whether a telecom customer is likely to churn.
        """)

        st.divider()

        # ======================================================
        # INPUT SECTION
        # ======================================================

        st.header("📝 Enter Customer Details")

        col1, col2 = st.columns(2)

        # ======================================================
        # COLUMN 1
        # ======================================================

        with col1:

            gender = st.selectbox(
                "Gender",
                ["Female", "Male"]
            )

            senior = st.selectbox(
                "Senior Citizen",
                ["No", "Yes"]
            )

            partner = st.selectbox(
                "Partner",
                ["No", "Yes"]
            )

            dependents = st.selectbox(
                "Dependents",
                ["No", "Yes"]
            )

            tenure = st.number_input(
                "Tenure (Months)",
                min_value=0,
                max_value=100
            )

            phone_service = st.selectbox(
                "Phone Service",
                ["No", "Yes"]
            )

            multiple_lines = st.selectbox(
                "Multiple Lines",
                ["No", "Yes", "No phone service"]
            )

            internet_service = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No"]
            )

            online_security = st.selectbox(
                "Online Security",
                ["No", "Yes", "No internet service"]
            )

        # ======================================================
        # COLUMN 2
        # ======================================================

        with col2:

            online_backup = st.selectbox(
                "Online Backup",
                ["No", "Yes", "No internet service"]
            )

            device_protection = st.selectbox(
                "Device Protection",
                ["No", "Yes", "No internet service"]
            )

            tech_support = st.selectbox(
                "Tech Support",
                ["No", "Yes", "No internet service"]
            )

            streaming_tv = st.selectbox(
                "Streaming TV",
                ["No", "Yes", "No internet service"]
            )

            streaming_movies = st.selectbox(
                "Streaming Movies",
                ["No", "Yes", "No internet service"]
            )

            contract = st.selectbox(
                "Contract Type",
                ["Month-to-month", "One year", "Two year"]
            )

            paperless_billing = st.selectbox(
                "Paperless Billing",
                ["No", "Yes"]
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer",
                    "Credit card"
                ]
            )

            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0
            )

            total_charges = st.number_input(
                "Total Charges",
                min_value=0.0
            )

        # ======================================================
        # ENCODING MAPS
        # ======================================================

        gender_map = {
            "Female": 0,
            "Male": 1
        }

        yes_no_map = {
            "No": 0,
            "Yes": 1
        }

        multiple_lines_map = {
            "No": 0,
            "Yes": 1,
            "No phone service": 2
        }

        internet_service_map = {
            "DSL": 0,
            "Fiber optic": 1,
            "No": 2
        }

        internet_feature_map = {
            "No": 0,
            "Yes": 1,
            "No internet service": 2
        }

        contract_map = {
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2
        }

        payment_method_map = {
            "Electronic check": 0,
            "Mailed check": 1,
            "Bank transfer": 2,
            "Credit card": 3
        }

        # ======================================================
        # PREDICT BUTTON
        # ======================================================

        if st.button("Predict Churn"):

            input_data = np.array([[
                gender_map[gender],
                yes_no_map[senior],
                yes_no_map[partner],
                yes_no_map[dependents],
                tenure,
                yes_no_map[phone_service],
                multiple_lines_map[multiple_lines],
                internet_service_map[internet_service],
                internet_feature_map[online_security],
                internet_feature_map[online_backup],
                internet_feature_map[device_protection],
                internet_feature_map[tech_support],
                internet_feature_map[streaming_tv],
                internet_feature_map[streaming_movies],
                contract_map[contract],
                yes_no_map[paperless_billing],
                payment_method_map[payment_method],
                monthly_charges,
                total_charges
            ]])

            prediction = model.predict(input_data)

            probability = model.predict_proba(input_data)

            churn_probability = probability[0][1] * 100

            # ======================================================
            # SAVE TO DATABASE
            # ======================================================

            predictions_collection.insert_one({

                "username": st.session_state.username,

                "prediction": (
                    "Churn"
                    if prediction[0] == 1
                    else "Stay"
                ),

                "churn_probability": float(churn_probability),

                "timestamp": datetime.now()

            })

            # ======================================================
            # RESULT DISPLAY
            # ======================================================

            st.divider()

            st.subheader("📌 Prediction Result")

            st.write(
                f"### Churn Probability: {churn_probability:.2f}%"
            )

            if churn_probability < 30:

                st.success("🟢 Low Churn Risk")

                st.info("""
                Recommended Action:
                - Maintain customer engagement
                - Continue standard support
                """)

            elif churn_probability < 70:

                st.warning("🟡 Medium Churn Risk")

                st.info("""
                Recommended Action:
                - Offer loyalty rewards
                - Improve customer experience
                """)

            else:

                st.error("🔴 High Churn Risk")

                st.info("""
                Recommended Action:
                - Offer discounts
                - Contact customer directly
                - Provide retention benefits
                """)

    # ======================================================
    # PREDICTION HISTORY
    # ======================================================

    elif page == "Prediction History":

        st.title("📜 Prediction History")

        history = list(
            predictions_collection.find({
                "username": st.session_state.username
            })
        )

        if history:

            df = pd.DataFrame(history)

            if "_id" in df.columns:
                df.drop("_id", axis=1, inplace=True)

            st.dataframe(df)

        else:

            st.info("No prediction history found")

    # ======================================================
    # BUSINESS EXPLANATION
    # ======================================================

    elif page == "Business Explanation":

        st.title("📘 Business Explanation")

        st.markdown("""
        # Customer Churn Prediction System
        """)

        st.markdown("""
        This AI-powered application predicts whether a telecom customer is likely to leave the company.

        The system helps businesses identify high-risk customers early and take proactive retention actions.
        """)

        st.divider()

        # ======================================================
        # PROJECT OBJECTIVE
        # ======================================================

        st.header("🎯 Project Objective")

        st.markdown("""
        - Predict customer churn risk
        - Improve customer retention
        - Reduce revenue loss
        - Support business decisions
        - Increase customer satisfaction
        """)

        st.divider()

        # ======================================================
        # HOW SYSTEM WORKS
        # ======================================================

        st.header("🧠 How the System Works")

        st.markdown("""
        The machine learning model analyzes:

        - Customer tenure
        - Contract type
        - Internet service
        - Monthly charges
        - Customer support services
        - Payment behavior

        Based on these patterns, the model predicts churn probability.
        """)

        st.divider()

        # ======================================================
        # BUSINESS BENEFITS
        # ======================================================

        st.header("💼 Business Benefits")

        st.markdown("""
        ✅ Reduce customer loss

        ✅ Improve customer retention

        ✅ Increase revenue

        ✅ Support data-driven decisions

        ✅ Identify high-risk customers early
        """)

        st.divider()

        # ======================================================
        # AI MODEL
        # ======================================================

        st.header("🤖 Machine Learning Model")

        st.markdown("""
        Technologies used:

        - Random Forest Classifier
        - Feature Engineering
        - Data Preprocessing
        - Probability-Based Prediction
        - MongoDB Database
        - Streamlit Dashboard
        """)

        st.divider()

        # ======================================================
        # RISK LEVELS
        # ======================================================

        st.header("🚨 Risk Levels")

        st.markdown("""
        ### 🟢 Low Risk
        Customer is likely to stay.

        ### 🟡 Medium Risk
        Customer may churn in future.

        ### 🔴 High Risk
        Customer is highly likely to leave.
        """)

        st.divider()

        # ======================================================
        # FEATURE EXPLANATION GUIDE
        # ======================================================

        st.header("📚 Feature Explanation Guide")

        st.markdown("""
        ### 👤 Gender
        Customer gender information.

        ---

        ### 👴 Senior Citizen
        Indicates whether customer is a senior citizen.

        ---

        ### ❤️ Partner
        Indicates whether customer has a partner.

        ---

        ### 👨‍👩‍👧 Dependents
        Indicates whether customer has dependents.

        ---

        ### 📅 Tenure
        Number of months customer stayed with company.

        ---

        ### 🌐 Internet Service
        Type of internet service used.

        ---

        ### 🔒 Online Security
        Indicates whether security service is active.

        ---

        ### 🧑‍💻 Tech Support
        Indicates whether technical support service is active.

        ---

        ### 📄 Contract Type
        Customer subscription duration.

        ---

        ### 💰 Monthly Charges
        Monthly amount paid by customer.

        ---

        ### 💵 Total Charges
        Total amount paid during customer lifetime.
        """)

        st.divider()

        # ======================================================
        # PROJECT FEATURES
        # ======================================================

        st.header("⚙️ System Features")

        st.markdown("""
        - User Authentication
        - MongoDB Database Integration
        - Prediction History Tracking
        - AI-Based Churn Prediction
        - Business Dashboard
        - Risk Probability Analysis
        - Stakeholder Explanation Page
        """)

        st.success(
            "✅ This project demonstrates a complete AI-powered customer retention solution."
        )