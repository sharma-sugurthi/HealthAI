"""
HealthAI Frontend - Streamlit Application
Uses service layer for all business logic and data access.
"""

import os
import sys
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from backend.exceptions.auth_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from backend.services.auth_service import AuthService
from backend.services.chat_service import ChatService
from backend.services.health_service import HealthService
from backend.services.treatment_service import TreatmentService
from backend.utils.database import get_db_manager
from backend.utils.logger import get_logger
from config import config
from validation import ValidationError

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
if "chat_draft_prompt" not in st.session_state:
    st.session_state.chat_draft_prompt = ""


def apply_custom_styles():
    """Apply modern, clean UI styling."""
    st.markdown(
        """
    <style>
    :root {
        --ha-bg: #f8fafc;
        --ha-surface: #ffffff;
        --ha-primary: #2563eb;
        --ha-primary-dark: #1d4ed8;
        --ha-text: #0f172a;
        --ha-muted: #64748b;
        --ha-border: #e2e8f0;
        --ha-success: #16a34a;
    }

    .stApp {
        background: var(--ha-bg);
        color: var(--ha-text);
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
        max-width: 1200px;
    }

    [data-testid="stSidebar"] {
        background: #0b1220;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    .ha-page-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        color: var(--ha-text);
    }

    .ha-page-subtitle {
        color: var(--ha-muted);
        margin-bottom: 1rem;
    }

    .ha-glass-card {
        background: var(--ha-surface);
        border: 1px solid var(--ha-border);
        border-radius: 16px;
        padding: 1rem 1rem;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    }

    .healthai-chip {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        border: 1px solid #bfdbfe;
        background: #eff6ff;
        color: #1e40af;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.5rem;
    }

    .tool-card {
        border: 1px solid var(--ha-border);
        border-radius: 14px;
        padding: 0.95rem;
        margin-bottom: 0.85rem;
        background: var(--ha-surface);
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.03);
    }
    .tool-title {
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: #1e293b;
    }
    .workspace-title {
        margin-bottom: 0.2rem;
    }
    .workspace-subtitle {
        color: var(--ha-muted);
        margin-bottom: 0.9rem;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid var(--ha-border);
        font-weight: 600;
    }
    .stButton > button[kind="primary"] {
        background: var(--ha-primary);
        border-color: var(--ha-primary);
        color: white;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--ha-primary-dark);
        border-color: var(--ha-primary-dark);
        color: white;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str):
    """Reusable page header."""
    st.markdown(f"<div class='ha-page-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ha-page-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


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
    left, right = st.columns([1.1, 1], gap="large")

    with left:
        render_page_header(
            "HealthAI Care Platform",
            "A modern AI-assisted healthcare workspace for consultations, plans, and health tracking.",
        )
        st.markdown(
            """
        <div class="ha-glass-card">
            <div style="font-weight:700; margin-bottom:0.6rem;">Why HealthAI</div>
            <ul style="margin:0; padding-left:1.1rem; color:#334155; line-height:1.7;">
                <li>Structured patient conversations with medical disclaimers</li>
                <li>Symptom analysis and treatment drafting in one workspace</li>
                <li>Personal health metric tracking with trend visualization</li>
                <li>Secure account-based data history</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="ha-glass-card">', unsafe_allow_html=True)
        st.markdown("#### Account Access")
        st.caption("Login or create your account to continue.")

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", type="primary", use_container_width=True):
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
            reg_username = st.text_input("Username", key="reg_username")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input(
                "Confirm Password", type="password", key="reg_password_confirm"
            )
            reg_full_name = st.text_input("Full Name", key="reg_full_name")
            reg_age = st.number_input("Age", min_value=1, max_value=120, value=25, key="reg_age")
            reg_gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other", "Prefer not to say"],
                key="reg_gender",
            )

            if st.button("Create Account", type="primary", use_container_width=True):
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
                        st.error("Registration failed. Please check details and retry.")
                    finally:
                        session.close()

        st.markdown("</div>", unsafe_allow_html=True)

    show_medical_disclaimer()


def patient_chat_page():
    """ChatGPT-style AI care workspace with embedded clinical tools."""
    render_page_header(
        "🧠 AI Care Workspace",
        "Conversational care assistant with embedded symptom and treatment tools.",
    )
    st.markdown(
        """
    <span class="healthai-chip">Chat</span>
    <span class="healthai-chip">Symptom Analysis</span>
    <span class="healthai-chip">Treatment Guidance</span>
    """,
        unsafe_allow_html=True,
    )

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

    left_col, right_col = st.columns([2.4, 1], gap="large")

    with left_col:
        quick_cols = st.columns(3)
        with quick_cols[0]:
            if st.button("Headache + Fever", use_container_width=True, key="quick_prompt_1"):
                st.session_state.chat_draft_prompt = (
                    "I have had headache and mild fever for the last 2 days. " "What should I do?"
                )
        with quick_cols[1]:
            if st.button("Diet Advice", use_container_width=True, key="quick_prompt_2"):
                st.session_state.chat_draft_prompt = (
                    "Suggest a one-day healthy meal plan for weight management."
                )
        with quick_cols[2]:
            if st.button("When to See Doctor", use_container_width=True, key="quick_prompt_3"):
                st.session_state.chat_draft_prompt = (
                    "How do I know if my symptoms require urgent medical care?"
                )

        # Display chat messages
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        prompt = st.chat_input("Message HealthAI...")
        if not prompt and st.session_state.chat_draft_prompt:
            prompt = st.session_state.chat_draft_prompt
            st.session_state.chat_draft_prompt = ""

        if prompt:
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
                        error_msg = "I'm experiencing technical difficulties. " "Please try again."
                        st.error(error_msg)
                        st.session_state.chat_messages.append(
                            {"role": "assistant", "content": error_msg}
                        )

    with right_col:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("<div class='tool-title'>Patient Snapshot</div>", unsafe_allow_html=True)
        st.caption(
            f"{st.session_state.user['full_name']} • "
            f"{st.session_state.user['age']} yrs • "
            f"{st.session_state.user['gender']}"
        )
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("<div class='tool-title'>🔍 Symptom Analyzer</div>", unsafe_allow_html=True)
        symptom_text = st.text_area(
            "Symptoms",
            placeholder="e.g., headache for 3 days with mild fever and fatigue",
            height=110,
            key="workspace_symptoms_input",
            label_visibility="collapsed",
        )
        if st.button("Analyze", key="workspace_analyze_btn", use_container_width=True):
            if not symptom_text.strip():
                st.warning("Enter symptoms first.")
            else:
                try:
                    session = db_manager.get_session()
                    chat_service = ChatService(session)
                    result = chat_service.analyze_symptoms(
                        st.session_state.user["id"], symptom_text
                    )
                    analysis = f"### Symptom Analysis\n\n{result['analysis']}"
                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": analysis,
                        }
                    )
                    session.close()
                    st.success("Analysis added to chat.")
                    st.rerun()
                except Exception as e:
                    logger.error(f"Workspace symptom analysis error: {str(e)}")
                    st.error("Failed to analyze symptoms.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("<div class='tool-title'>📋 Treatment Draft</div>", unsafe_allow_html=True)
        condition = st.text_input(
            "Condition",
            placeholder="e.g., Type 2 Diabetes",
            key="workspace_condition_input",
            label_visibility="collapsed",
        )
        if st.button("Generate Draft", key="workspace_plan_btn", use_container_width=True):
            if not condition.strip():
                st.warning("Enter a condition first.")
            else:
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
                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": f"### Treatment Plan Draft: {condition}\n\n{plan}",
                        }
                    )
                    session.close()
                    st.success("Treatment draft added to chat.")
                    st.rerun()
                except Exception as e:
                    logger.error(f"Workspace treatment plan error: {str(e)}")
                    st.error("Failed to generate treatment plan.")
        st.caption("For educational use only. Always verify with a clinician.")
        st.markdown("</div>", unsafe_allow_html=True)


def symptom_checker_page():
    """Symptom checker interface"""
    st.title("🔍 Symptom Checker")
    st.markdown("Describe your symptoms and I'll help you understand possible conditions.")

    st.info(
        "💡 **Tip:** Be as detailed as possible. Include when symptoms started, "
        "severity, and any other relevant information."
    )

    symptoms = st.text_area(
        "Describe your symptoms:",
        height=150,
        placeholder="Example: I've had a headache for 3 days, "
        "mild fever (100°F), and fatigue...",
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
        "⚠️ **Important:** This is not a medical diagnosis. "
        "Please consult a healthcare professional for proper evaluation and treatment."
    )


def treatment_plan_page():
    """Treatment plan generator"""
    render_page_header(
        "📋 Treatment Plans",
        "Generate practical treatment drafts and manage your saved plans.",
    )

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
                "Save this plan as:",
                value=f"Treatment Plan for {st.session_state.plan_condition}",
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
    render_page_header(
        "📊 Health Analytics",
        "Track key health metrics and visualize trends over time.",
    )

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

    apply_custom_styles()

    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar navigation
        st.sidebar.title("🏥 HealthAI")
        st.sidebar.caption(f"Signed in as {st.session_state.user['full_name']}")
        st.sidebar.success("System Status: Online")

        st.sidebar.markdown("---")

        # Navigation menu
        page = st.sidebar.radio(
            "Workspace",
            ["🧠 AI Care Workspace", "📋 Treatment Plans", "📊 Health Analytics"],
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
        if page == "🧠 AI Care Workspace":
            patient_chat_page()
        elif page == "📋 Treatment Plans":
            treatment_plan_page()
        elif page == "📊 Health Analytics":
            health_analytics_page()


if __name__ == "__main__":
    main()
