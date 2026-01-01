"""
HealthAI Frontend - Streamlit Application
Uses service layer for all business logic and data access.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.auth_service import AuthService
from backend.services.chat_service import ChatService
from backend.services.health_service import HealthService
from backend.services.treatment_service import TreatmentService
from backend.utils.database import get_db_manager
from backend.utils.logger import get_logger
from backend.exceptions.auth_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from backend.exceptions.validation_exceptions import ValidationError
from config import config

# Initialize logger
logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title=f"{config.APP_NAME} - Intelligent Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize database manager
@st.cache_resource
def init_services():
    """Initialize database and return service instances"""
    try:
        db_manager = get_db_manager()
        logger.info("Database initialized successfully")
        return db_manager
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        st.error(f"Failed to initialize application: {str(e)}")
        st.stop()


db_manager = init_services()

# Check API key
if not config.OPENROUTER_API_KEY:
    st.error("⚠️ OPENROUTER_API_KEY not found. Please add your OpenRouter API key in .env file.")
    st.info("Get your free API key at: https://openrouter.ai/keys")
    st.stop()

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


def show_medical_disclaimer():
    """Display medical disclaimer"""
    st.sidebar.markdown("---")
    st.sidebar.warning(
        """
    ⚠️ **Medical Disclaimer**
    
    HealthAI is an AI assistant for informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified healthcare provider with any questions you may have regarding a medical condition.
    """
    )


def login_page():
    """Display login/registration page"""
    st.title(f"🏥 {config.APP_NAME} - Intelligent Healthcare Assistant")

    st.markdown(
        """
    Welcome to HealthAI, your intelligent healthcare companion powered by advanced AI technology.
    
    **Features:**
    - 💬 AI-Powered Health Chat
    - 🔍 Symptom Checker
    - 📋 Treatment Plan Generator
    - 📊 Health Analytics Dashboard
    """
    )

    show_medical_disclaimer()

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to Your Account")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            if not login_username or not login_password:
                st.error("Please enter both username and password")
            else:
                try:
                    session = db_manager.get_session()
                    auth_service = AuthService(session)
                    user_data = auth_service.login_user(login_username, login_password)

                    st.session_state.logged_in = True
                    st.session_state.user = user_data
                    st.success(f"Welcome back, {user_data['full_name']}!")
                    logger.info(f"User logged in: {login_username}")
                    st.rerun()

                except InvalidCredentialsError:
                    st.error("Invalid username or password")
                except ValidationError as e:
                    st.error(str(e))
                except Exception as e:
                    logger.error(f"Login error: {str(e)}")
                    st.error("An error occurred during login. Please try again.")
                finally:
                    session.close()

    with tab2:
        st.subheader("Create New Account")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_password_confirm = st.text_input(
            "Confirm Password", type="password", key="reg_password_confirm"
        )
        reg_full_name = st.text_input("Full Name", key="reg_full_name")
        reg_age = st.number_input("Age", min_value=1, max_value=120, value=25, key="reg_age")
        reg_gender = st.selectbox(
            "Gender", ["Male", "Female", "Other", "Prefer not to say"], key="reg_gender"
        )

        if st.button("Register", type="primary"):
            if not all([reg_username, reg_password, reg_full_name]):
                st.error("Please fill in all required fields")
            elif reg_password != reg_password_confirm:
                st.error("Passwords do not match")
            else:
                try:
                    session = db_manager.get_session()
                    auth_service = AuthService(session)
                    auth_service.register_user(
                        username=reg_username,
                        password=reg_password,
                        full_name=reg_full_name,
                        age=reg_age,
                        gender=reg_gender,
                    )
                    st.success("Account created successfully! Please login.")
                    logger.info(f"New user registered: {reg_username}")

                except UserAlreadyExistsError as e:
                    st.error(str(e))
                except ValidationError as e:
                    st.error(str(e))
                except Exception as e:
                    logger.error(f"Registration error: {str(e)}")
                    st.error(f"Registration failed: {str(e)}")
                finally:
                    session.close()


def patient_chat_page():
    """AI-powered patient chat interface"""
    st.title("💬 Patient Chat")
    st.markdown("Ask me anything about your health concerns. I'm here to help!")

    # Load chat history
    if not st.session_state.chat_messages:
        try:
            session = db_manager.get_session()
            chat_service = ChatService(session)
            history = chat_service.get_chat_history(st.session_state.user["id"], limit=20)

            for h in history:
                st.session_state.chat_messages.append({"role": "user", "content": h["message"]})
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": h["response"]}
                )

            session.close()
        except Exception as e:
            logger.error(f"Error loading chat history: {str(e)}")

    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your health question here..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    session = db_manager.get_session()
                    chat_service = ChatService(session)
                    result = chat_service.send_message(st.session_state.user["id"], prompt)
                    response = result["response"]

                    st.markdown(response)
                    st.session_state.chat_messages.append(
                        {"role": "assistant", "content": response}
                    )

                    session.close()
                except Exception as e:
                    logger.error(f"Chat error: {str(e)}")
                    error_msg = "I'm experiencing technical difficulties. Please try again."
                    st.error(error_msg)
                    st.session_state.chat_messages.append(
                        {"role": "assistant", "content": error_msg}
                    )


def symptom_checker_page():
    """Symptom checker interface"""
    st.title("🔍 Symptom Checker")
    st.markdown("Describe your symptoms and I'll help you understand possible conditions.")

    st.info(
        "💡 **Tip:** Be as detailed as possible. Include when symptoms started, severity, and any other relevant information."
    )

    symptoms = st.text_area(
        "Describe your symptoms:",
        height=150,
        placeholder="Example: I've had a headache for 3 days, mild fever (100°F), and fatigue...",
    )

    if st.button("Analyze Symptoms", type="primary"):
        if not symptoms:
            st.warning("Please describe your symptoms first.")
        else:
            with st.spinner("Analyzing symptoms..."):
                try:
                    session = db_manager.get_session()
                    chat_service = ChatService(session)
                    result = chat_service.analyze_symptoms(st.session_state.user["id"], symptoms)

                    st.markdown("### Analysis Results")
                    st.markdown(result["analysis"])

                    session.close()
                except Exception as e:
                    logger.error(f"Symptom analysis error: {str(e)}")
                    st.error("Failed to analyze symptoms. Please try again.")

    st.markdown("---")
    st.warning(
        "⚠️ **Important:** This is not a medical diagnosis. Please consult a healthcare professional for proper evaluation and treatment."
    )


def treatment_plan_page():
    """Treatment plan generator"""
    st.title("📋 Treatment Plans")

    # Initialize session state for generated plan
    if "generated_plan" not in st.session_state:
        st.session_state.generated_plan = None
    if "plan_condition" not in st.session_state:
        st.session_state.plan_condition = None

    tab1, tab2 = st.tabs(["Generate New Plan", "View Saved Plans"])

    with tab1:
        st.subheader("Generate Treatment Plan")

        condition = st.text_input(
            "Condition or Health Concern:",
            placeholder="e.g., Type 2 Diabetes, High Blood Pressure, etc.",
        )

        if st.button("Generate Treatment Plan", type="primary"):
            if not condition:
                st.warning("Please enter a condition or health concern.")
            else:
                with st.spinner("Generating personalized treatment plan..."):
                    try:
                        session = db_manager.get_session()
                        chat_service = ChatService(session)

                        patient_info = {
                            "age": st.session_state.user["age"],
                            "gender": st.session_state.user["gender"],
                        }

                        plan = chat_service.generate_treatment_plan(
                            st.session_state.user["id"], condition, patient_info
                        )

                        st.session_state.generated_plan = plan
                        st.session_state.plan_condition = condition

                        session.close()
                    except Exception as e:
                        logger.error(f"Treatment plan generation error: {str(e)}")
                        st.error("Failed to generate treatment plan. Please try again.")

        # Display generated plan if available
        if st.session_state.generated_plan:
            st.markdown("### Generated Treatment Plan")
            st.markdown(st.session_state.generated_plan)

            # Option to save plan
            plan_title = st.text_input(
                "Save this plan as:", value=f"Treatment Plan for {st.session_state.plan_condition}"
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Save Plan"):
                    try:
                        session = db_manager.get_session()
                        treatment_service = TreatmentService(session)
                        treatment_service.create_plan(
                            user_id=st.session_state.user["id"],
                            title=plan_title,
                            condition=st.session_state.plan_condition,
                            plan_details=st.session_state.generated_plan,
                        )
                        st.success("Treatment plan saved successfully!")
                        st.session_state.generated_plan = None
                        st.session_state.plan_condition = None
                        session.close()
                    except Exception as e:
                        logger.error(f"Error saving plan: {str(e)}")
                        st.error("Failed to save plan. Please try again.")
            with col2:
                if st.button("Clear"):
                    st.session_state.generated_plan = None
                    st.session_state.plan_condition = None
                    st.rerun()

    with tab2:
        st.subheader("Your Saved Treatment Plans")

        try:
            session = db_manager.get_session()
            treatment_service = TreatmentService(session)
            plans = treatment_service.get_user_plans(st.session_state.user["id"])
            session.close()

            if not plans:
                st.info("You don't have any saved treatment plans yet.")
            else:
                for plan in plans:
                    with st.expander(
                        f"📄 {plan['title']} - {plan['created_at'].strftime('%Y-%m-%d')}"
                    ):
                        st.markdown(f"**Condition:** {plan['condition']}")
                        st.markdown(f"**Created:** {plan['created_at'].strftime('%Y-%m-%d %H:%M')}")
                        st.markdown("---")
                        st.markdown(plan["plan_details"])
        except Exception as e:
            logger.error(f"Error loading treatment plans: {str(e)}")
            st.error("Failed to load treatment plans.")


def health_analytics_page():
    """Health analytics dashboard"""
    st.title("📊 Health Analytics")

    tab1, tab2 = st.tabs(["Add Health Data", "View Analytics"])

    with tab1:
        st.subheader("Record Health Metrics")

        col1, col2 = st.columns(2)

        with col1:
            metric_type = st.selectbox(
                "Metric Type",
                [
                    "Heart Rate",
                    "Blood Pressure (Systolic)",
                    "Blood Pressure (Diastolic)",
                    "Blood Glucose",
                    "Weight",
                    "Temperature",
                    "Oxygen Saturation",
                ],
            )

        with col2:
            # Set appropriate units based on metric type
            unit_mapping = {
                "Heart Rate": "bpm",
                "Blood Pressure (Systolic)": "mmHg",
                "Blood Pressure (Diastolic)": "mmHg",
                "Blood Glucose": "mg/dL",
                "Weight": "kg",
                "Temperature": "°F",
                "Oxygen Saturation": "%",
            }
            unit = unit_mapping.get(metric_type, "unit")
            st.text_input("Unit", value=unit, disabled=True)

        value = st.number_input("Value", min_value=0.0, step=0.1)
        notes = st.text_area("Notes (optional)", placeholder="Any additional observations...")

        if st.button("Record Metric", type="primary"):
            if value <= 0:
                st.warning("Please enter a valid value.")
            else:
                try:
                    session = db_manager.get_session()
                    health_service = HealthService(session)
                    health_service.record_metric(
                        user_id=st.session_state.user["id"],
                        metric_type=metric_type,
                        value=value,
                        unit=unit,
                        notes=notes if notes else None,
                    )
                    st.success(f"Successfully recorded {metric_type}: {value} {unit}")
                    session.close()
                except ValidationError as e:
                    st.error(str(e))
                except Exception as e:
                    logger.error(f"Error recording metric: {str(e)}")
                    st.error("Failed to record metric. Please try again.")

    with tab2:
        st.subheader("Your Health Trends")

        # Metric selector for visualization
        available_metrics = [
            "Heart Rate",
            "Blood Pressure (Systolic)",
            "Blood Pressure (Diastolic)",
            "Blood Glucose",
            "Weight",
            "Temperature",
            "Oxygen Saturation",
        ]

        selected_metric = st.selectbox("Select Metric to Visualize", available_metrics)

        try:
            session = db_manager.get_session()
            health_service = HealthService(session)
            metrics = health_service.get_metrics(st.session_state.user["id"], selected_metric)
            session.close()

            if not metrics:
                st.info(
                    f"No data recorded for {selected_metric} yet. Start tracking by adding metrics above!"
                )
            else:
                # Prepare data for visualization
                df = pd.DataFrame(
                    [
                        {
                            "Date": m["recorded_at"],
                            "Value": m["value"],
                            "Notes": m["notes"] if m["notes"] else "",
                        }
                        for m in reversed(metrics)
                    ]
                )

                # Create interactive plot
                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=df["Date"],
                        y=df["Value"],
                        mode="lines+markers",
                        name=selected_metric,
                        line=dict(color="#1f77b4", width=2),
                        marker=dict(size=8),
                        hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>",
                    )
                )

                fig.update_layout(
                    title=f"{selected_metric} Trend",
                    xaxis_title="Date",
                    yaxis_title=f'{selected_metric} ({metrics[0]["unit"]})',
                    hovermode="x unified",
                    height=400,
                )

                st.plotly_chart(fig, use_container_width=True)

                # Show statistics
                stats = health_service.get_statistics(st.session_state.user["id"], selected_metric)

                if stats:
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Latest", f"{stats['latest']:.1f} {stats['unit']}")
                    with col2:
                        st.metric("Average", f"{stats['average']:.1f} {stats['unit']}")
                    with col3:
                        st.metric("Minimum", f"{stats['minimum']:.1f} {stats['unit']}")
                    with col4:
                        st.metric("Maximum", f"{stats['maximum']:.1f} {stats['unit']}")

                # Show data table
                st.markdown("### Recent Measurements")
                display_df = df.copy()
                display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d %H:%M")
                st.dataframe(display_df, use_container_width=True)

        except Exception as e:
            logger.error(f"Error loading health analytics: {str(e)}")
            st.error("Failed to load health analytics.")


def main():
    """Main application logic"""

    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar navigation
        st.sidebar.title(f"Welcome, {st.session_state.user['full_name']}!")

        st.sidebar.markdown("---")

        # Navigation menu
        page = st.sidebar.radio(
            "Navigation",
            ["💬 Patient Chat", "🔍 Symptom Checker", "📋 Treatment Plans", "📊 Health Analytics"],
            key="navigation",
        )

        # Logout button
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.chat_messages = []
            logger.info(f"User logged out")
            st.rerun()

        # Show medical disclaimer
        show_medical_disclaimer()

        # Route to selected page
        if page == "💬 Patient Chat":
            patient_chat_page()
        elif page == "🔍 Symptom Checker":
            symptom_checker_page()
        elif page == "📋 Treatment Plans":
            treatment_plan_page()
        elif page == "📊 Health Analytics":
            health_analytics_page()


if __name__ == "__main__":
    main()
