import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
from pathlib import Path

from src.local_ai import generate_lead_recommendation

# ============================================================
# SUBSCRIPTION CONFIG
# ============================================================

FREE_LEAD_LIMIT = 20

PRO_PLAN_NAME = "LeadPilot Pro"

PRO_PLAN_PRICE = 399

# ============================================================
# CURRENT SUBSCRIPTION
# ============================================================

CURRENT_PLAN = "Pro"

from src.scoring import (
    calculate_lead_score,
    get_recommended_action,
    get_lead_stage,
    get_next_action,
    get_lead_insight,
    get_priority_reason,
    get_conversion_bottleneck,
    get_ai_recommendation,
    get_lead_summary,
)

from auth import get_authenticator


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LeadPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# UI THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN APP
       ======================================================== */

    .stApp {
        background: #f5f7fb;
    }

    .main {
        background: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* ========================================================
       SIDEBAR / NAVIGATION
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
        box-shadow: 2px 0 12px rgba(15, 23, 42, 0.04);
    }

    section[data-testid="stSidebar"] > div {
        background: #ffffff;
    }

    /* Sidebar title */
    section[data-testid="stSidebar"] h1 {
        color: #111827;
        font-size: 1.55rem;
        font-weight: 750;
        margin-bottom: 0.15rem;
    }

    /* Sidebar subtitles */
    section[data-testid="stSidebar"] p {
        color: #6b7280;
    }

    /* Sidebar navigation label */
    section[data-testid="stSidebar"] label {
        color: #374151;
        font-weight: 600;
    }

    /* Navigation radio container */
    section[data-testid="stSidebar"] [data-testid="stRadio"] {
        margin-top: 0.5rem;
    }

    /* Navigation options */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: #ffffff;
        border-radius: 10px;
        padding: 10px 12px;
        margin: 3px 0;
        transition: all 0.15s ease;
        border: 1px solid transparent;
    }

    /* Navigation hover */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #f3f4f6;
        border-color: #e5e7eb;
    }

    /* Selected navigation item */
    section[data-testid="stSidebar"]
    [data-testid="stRadio"] label:has(input:checked) {
        background: #eef2ff;
        border-color: #c7d2fe;
        color: #3730a3;
        font-weight: 700;
    }

    /* Hide radio circle */
    section[data-testid="stSidebar"]
    [data-testid="stRadio"] input {
        display: none;
    }

    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1rem 0;
    }


    /* ========================================================
       SIDEBAR SELECTBOX
       ======================================================== */

    section[data-testid="stSidebar"] [data-baseweb="select"] {
        background: #ffffff;
        border-radius: 9px;
    }

    section[data-testid="stSidebar"]
    [data-baseweb="select"] > div {
        border-radius: 9px;
        border-color: #d1d5db;
        background: #ffffff;
    }


    /* ========================================================
       SIDEBAR LOGOUT BUTTON
       ======================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 9px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        color: #374151;
        font-weight: 600;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }


    /* ========================================================
       MAIN HEADINGS
       ======================================================== */

   h1 {
    color: #000000 !important;
    font-weight: 750;
    letter-spacing: -0.02em;
}

h2 {
    color: #000000 !important;
    font-weight: 700;
}

h3 {
    color: #1f2937 !important;
    font-weight: 650;
}

p {
    color: #000000 !important;
}


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 42px;
        border: 1px solid #d1d5db;
        background: #ffffff;
        color: #1f2937;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #9ca3af;
        background: #f9fafb;
    }

    .stLinkButton > a {
        border-radius: 9px;
        font-weight: 650;
        min-height: 42px;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #6b7280;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 750;
    }


    /* ========================================================
       DATA TABLES
       ======================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        background: #ffffff;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 9px;
    border: 1px solid #d1d5db;
    background: #ffffff !important;
    color: #000000 !important;
    caret-color: #000000 !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    background: #ffffff !important;
    color: #000000 !important;
    border-color: #6366f1;
    box-shadow: 0 0 0 1px #6366f1;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

[data-baseweb="select"] {
    border-radius: 9px;
    background: #ffffff !important;
}

[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #000000 !important;
    border-color: #d1d5db !important;
}

[data-baseweb="select"] input {
    color: #000000 !important;
}


    /* ========================================================
       FORMS / CONTAINERS
       ======================================================== */

    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }


    /* ========================================================
       LEAD CARDS
       ======================================================== */

    .lead-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 8px;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f3f4f6;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AUTHENTICATION
# ============================================================

authenticator = get_authenticator()
authenticator.login(location="main")

authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

if authentication_status is False:
    st.error("❌ Username/password is incorrect.")
    st.stop()

if authentication_status is None:
    st.warning("🔐 Please enter your username and password.")
    st.stop()

if authentication_status:
    authenticator.logout("Logout", "sidebar")


# ============================================================
# DATA CONFIG
# ============================================================

DATA_PATH = Path("data/leads.csv")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# DATA HELPERS
# ============================================================

REQUIRED_COLUMNS = [
    "lead_id",
    "name",
    "phone",
    "age",
    "qualification",
    "source",
    "number_saved",
    "zoom_invited",
    "zoom_attended",
    "purchase",
    "last_interaction",
    "follow_up_date",
    "follow_up_time",
    "follow_up_status",
    "follow_up_notes",
    "follow_up_outcome",
    "outcome_notes",
    "last_contacted",
    "follow_up_history",
]


INTELLIGENCE_COLUMNS = [
    "score",
    "priority",
    "recommended_action",
    "next_action",
    "lead_insight",
    "priority_reason",
    "conversion_bottleneck",
    "ai_recommendation",
    "lead_summary",
    "lead_stage",
]


def save_data(dataframe):
    """Save the current lead database safely."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(DATA_PATH, index=False)


def load_data():
    """Load leads.csv and guarantee the expected columns exist."""
    if not DATA_PATH.exists():
        dataframe = pd.DataFrame(columns=REQUIRED_COLUMNS)
        save_data(dataframe)
        return dataframe

    try:
        dataframe = pd.read_csv(DATA_PATH)
    except Exception as exc:
        st.error(f"❌ Could not read {DATA_PATH}: {exc}")
        st.stop()

    for column in REQUIRED_COLUMNS:
        if column not in dataframe.columns:
            dataframe[column] = ""

    for column in REQUIRED_COLUMNS:
        dataframe[column] = (
            dataframe[column]
            .fillna("")
            .astype(str)
        )

    return dataframe


def clean_phone(phone):
    """Return a WhatsApp-compatible numeric phone string."""
    value = str(phone).strip()

    if not value or value.lower() == "nan":
        return ""

    return (
        value
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )


def whatsapp_link(phone, message=""):
    number = clean_phone(phone)

    if not number:
        return ""

    if message:
        return f"https://wa.me/{number}?text={quote(str(message))}"

    return f"https://wa.me/{number}"


def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value)

# ============================================================
# SMART FOLLOW-UP HELPERS
# ============================================================

def get_follow_up_status_type(lead):
    """
    Determine whether a lead follow-up is overdue,
    due today, upcoming, completed, or unscheduled.
    """

    follow_up_date = safe_text(
        lead.get("follow_up_date", "")
    ).strip()

    follow_up_status = safe_text(
        lead.get("follow_up_status", "")
    ).strip()

    # No follow-up scheduled
    if not follow_up_date:
        return "⚪ Unscheduled"

    # Completed follow-up
    if follow_up_status == "Completed":
        return "✅ Completed"

    # Skipped follow-up
    if follow_up_status == "Skipped":
        return "⚪ Skipped"

    # Convert date safely
    try:
        follow_date = pd.to_datetime(
            follow_up_date,
            errors="coerce",
        )

        if pd.isna(follow_date):
            return "⚪ Unscheduled"

        follow_date = follow_date.normalize()

    except Exception:
        return "⚪ Unscheduled"

    today = pd.Timestamp.today().normalize()

    if follow_date < today:
        return "🔴 Overdue"

    elif follow_date == today:
        return "🟠 Due Today"

    else:
        return "🟢 Upcoming"


def add_follow_up_intelligence(dataframe):
    """
    Add smart follow-up status and recommended follow-up
    information to the lead database.
    """

    if dataframe.empty:
        dataframe["follow_up_type"] = pd.Series(
            dtype="object"
        )

        dataframe["follow_up_priority"] = pd.Series(
            dtype="object"
        )

        return dataframe

    dataframe["follow_up_type"] = dataframe.apply(
        get_follow_up_status_type,
        axis=1,
    )

    def calculate_follow_up_priority(row):

        follow_up_type = safe_text(
            row.get("follow_up_type", "")
        )

        priority = safe_text(
            row.get("priority", "")
        )

        if follow_up_type == "🔴 Overdue":
            return "🔴 Urgent"

        if follow_up_type == "🟠 Due Today":

            if priority == "🔥 High":
                return "🔴 Urgent"

            return "🟠 High"

        if follow_up_type == "🟢 Upcoming":

            if priority == "🔥 High":
                return "🟠 High"

            return "🟢 Normal"

        return "⚪ None"

    dataframe["follow_up_priority"] = dataframe.apply(
        calculate_follow_up_priority,
        axis=1,
    )

    return dataframe


def calculate_intelligence(dataframe):
    """Run the existing LeadPilot scoring/intelligence layer."""
    if dataframe.empty:
        for column in INTELLIGENCE_COLUMNS:
            dataframe[column] = pd.Series(dtype="object")
        return dataframe

    results = dataframe.apply(calculate_lead_score, axis=1)

    dataframe["score"] = results.apply(lambda item: item[0])
    dataframe["priority"] = results.apply(lambda item: item[1])

    dataframe["recommended_action"] = dataframe.apply(
        get_recommended_action,
        axis=1,
    )

    dataframe["next_action"] = dataframe.apply(
        get_next_action,
        axis=1,
    )

    dataframe["lead_insight"] = dataframe.apply(
        get_lead_insight,
        axis=1,
    )

    dataframe["priority_reason"] = dataframe.apply(
        get_priority_reason,
        axis=1,
    )

    dataframe["conversion_bottleneck"] = dataframe.apply(
        get_conversion_bottleneck,
        axis=1,
    )

    dataframe["ai_recommendation"] = dataframe.apply(
        get_ai_recommendation,
        axis=1,
    )

    dataframe["lead_summary"] = dataframe.apply(
        get_lead_summary,
        axis=1,
    )

    dataframe["lead_stage"] = dataframe.apply(
        get_lead_stage,
        axis=1,
    )

    return dataframe


def refresh_and_save(dataframe):
    """Recalculate intelligence, save source data, then rerun."""
    dataframe = calculate_intelligence(dataframe)
    save_data(dataframe)
    return dataframe


def make_unique_lead_id(dataframe):
    existing = set(dataframe["lead_id"].astype(str).tolist())

    counter = len(dataframe) + 1

    while True:
        candidate = f"L{counter:03d}"
        if candidate not in existing:
            return candidate
        counter += 1


def filter_search(dataframe, query):
    if not query:
        return dataframe.copy()

    query = str(query)

    mask = dataframe.astype(str).apply(
        lambda row: row.str.contains(
            query,
            case=False,
            na=False,
        ).any(),
        axis=1,
    )

    return dataframe[mask].copy()


def get_selected_row(dataframe, selected_name):
    matches = dataframe.index[
        dataframe["name"] == selected_name
    ].tolist()

    if not matches:
        return None, None

    index = matches[0]
    return index, dataframe.loc[index]


# ============================================================
# LOAD + INTELLIGENCE
# ============================================================

df = load_data()
df = calculate_intelligence(df)
df = add_follow_up_intelligence(df)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚀 LeadPilot")
st.sidebar.caption("AI Lead Conversion Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "👥 Leads",
        "📅 Follow-Ups",
        "📈 Analytics",
        "📥 Import Leads",
         "💳 Plans",
        "⚙️ Settings",
    ],
)

st.sidebar.divider()

st.sidebar.subheader("👤 Select Lead")

if len(df) > 0:
    sidebar_lead_names = df["name"].tolist()

    selected_lead = st.sidebar.selectbox(
        "Lead",
        sidebar_lead_names,
        key="sidebar_selected_lead",
    )
else:
    selected_lead = None
    st.sidebar.info("No leads available.")

st.sidebar.divider()

st.sidebar.caption(
    f"Logged in as: {name or username or 'User'}"
)


# ============================================================
# WHATSAPP MESSAGE GENERATOR
# ============================================================

def generate_whatsapp_message(lead):
    """
    Generate a concise WhatsApp follow-up using the local
    Ollama service already used by LeadPilot.
    """

    ollama_url = "http://localhost:11434/api/generate"
    model = "llama3.2:3b"

    prompt = f"""
You are LeadPilot, an AI sales assistant.

Write one short, friendly and non-pushy WhatsApp follow-up
message for this lead.

Lead information:
Name: {lead.get("name", "")}
Source: {lead.get("source", "")}
Qualification: {lead.get("qualification", "")}
Lead score: {lead.get("score", "")}
Priority: {lead.get("priority", "")}
Lead stage: {lead.get("lead_stage", "")}
Next action: {lead.get("next_action", "")}
Recommended action: {lead.get("recommended_action", "")}
Last interaction: {lead.get("last_interaction", "")}
Follow-up outcome: {lead.get("follow_up_outcome", "")}
Bottleneck: {lead.get("conversion_bottleneck", "")}

Rules:
- Do not sound desperate.
- Do not use fake urgency.
- Do not promise anything.
- Keep it under 70 words.
- Do not add a subject line.
- Return only the WhatsApp message.
"""

    response = requests.post(
        ollama_url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    message = result.get(
        "response",
        "",
    ).strip()

    if not message:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return message


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.title("🚀 LeadPilot")
    st.subheader("AI Lead Conversion Platform")

    st.write(
        "Helping affiliate entrepreneurs manage, "
        "prioritize, and convert their leads."
    )

    total_leads = len(df)

    high_priority = len(
        df[df["priority"] == "🔥 High"]
    )

    medium_priority = len(
        df[df["priority"] == "🟡 Medium"]
    )

    converted_leads = len(
        df[df["purchase"] == "Yes"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Leads", total_leads)

    with col2:
        st.metric("🔥 High Priority", high_priority)

    with col3:
        st.metric("🟡 Medium Priority", medium_priority)

    with col4:
        st.metric("✅ Converted", converted_leads)

    # ========================================================
    # TODAY'S FOCUS
    # ========================================================

    st.divider()
    st.subheader("🎯 Today's Focus")

    active_focus = df[
        df["purchase"] != "Yes"
    ].copy()

    if len(active_focus) > 0:

        active_focus = active_focus.sort_values(
            by="score",
            ascending=False,
        )

        focus_lead = active_focus.iloc[0]

        focus_col1, focus_col2 = st.columns(2)

        with focus_col1:

            st.write(
                f"### 👤 {focus_lead['name']}"
            )

            st.metric(
                "Lead Score",
                focus_lead["score"],
            )

            st.write(
                f"**Priority:** "
                f"{focus_lead['priority']}"
            )

            st.write(
                f"**Stage:** "
                f"{focus_lead['lead_stage']}"
            )

        with focus_col2:

            st.write(
                "### ⚡ Recommended Action"
            )

            st.info(
                focus_lead["recommended_action"]
            )

            st.success(
                f"**Next Action:** "
                f"{focus_lead['next_action']}"
            )

            st.write(
                f"**Bottleneck:** "
                f"{focus_lead['conversion_bottleneck']}"
            )

    else:

        st.success(
            "🎉 All leads have been converted!"
        )

    # ========================================================
    # TODAY'S ACTION CENTER
    # ========================================================

    st.divider()
    st.subheader("🤖 Today's Action Center")

    action_filter = st.selectbox(
        "🎯 What do you want to focus on?",
        [
            "All Active Leads",
            "🔥 High Priority",
            "🟡 Medium Priority",
            "📅 Follow-Ups Due",
            "📞 Contacted Today",
        ],
        key="action_center_filter",
    )

    action_center = df[
        df["purchase"] != "Yes"
    ].copy()

    if action_filter == "🔥 High Priority":
        action_center = action_center[
            action_center["priority"] == "🔥 High"
        ]

    elif action_filter == "🟡 Medium Priority":
        action_center = action_center[
            action_center["priority"] == "🟡 Medium"
        ]

    elif action_filter == "📅 Follow-Ups Due":

        today = pd.Timestamp.today().normalize()

        action_center["_follow_up_date"] = pd.to_datetime(
            action_center["follow_up_date"],
            errors="coerce",
        )

        action_center = action_center[
            (action_center["_follow_up_date"] <= today)
            & (
                action_center["follow_up_status"]
                .isin(["Pending", ""])
            )
        ]

    elif action_filter == "📞 Contacted Today":

        today_string = str(
            pd.Timestamp.today().date()
        )

        action_center = action_center[
            action_center["last_contacted"]
            == today_string
        ]

    action_center = action_center.sort_values(
        by="score",
        ascending=False,
    )

    if len(action_center) > 0:

        display_action_columns = [
            "name",
            "priority",
            "lead_stage",
            "score",
            "conversion_bottleneck",
            "next_action",
            "ai_recommendation",
            "last_contacted",
        ]

        st.dataframe(
            action_center[
                [
                    column
                    for column in display_action_columns
                    if column in action_center.columns
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.subheader("🎯 Action Center — Lead Details")

        action_lead = st.selectbox(
            "Select a lead",
            action_center["name"].tolist(),
            key="action_center_lead",
        )

        action_index, action_data = get_selected_row(
            df,
            action_lead,
        )

        if action_data is not None:

            st.write(
                f"### 👤 {action_data['name']}"
            )

            detail_col1, detail_col2 = st.columns(2)

            with detail_col1:
                st.write(
                    f"**🎯 Lead Score:** {action_data['score']}"
                )

                st.write(
                    f"**🎯 Priority:** "
                    f"{action_data['priority']}"
                )

                st.write(
                    f"**🧭 Stage:** "
                    f"{action_data['lead_stage']}"
                )

                st.write(
                    f"**📝 Priority Reason:** "
                    f"{action_data['priority_reason']}"
                )

                st.write(
                    f"**🚧 Conversion Bottleneck:** "
                    f"{action_data['conversion_bottleneck']}"
                )

            with detail_col2:

                st.write(
                    f"**⚡ Recommended Action:** "
                    f"{action_data['recommended_action']}"
                )

                st.write(
                    f"**🎯 Next Action:** "
                    f"{action_data['next_action']}"
                )

                st.write(
                    f"**🤖 AI Recommendation:** "
                    f"{action_data['ai_recommendation']}"
                )

                st.write(
                    f"**📋 Lead Summary:** "
                    f"{action_data['lead_summary']}"
                )

               
            
            # ====================================================
            # WHATSAPP CONTACT
            # ====================================================

            st.divider()
            st.subheader("💬 Contact Lead")

            action_phone = safe_text(
                action_data.get("phone", "")
            ).strip()

            if action_phone and action_phone.lower() != "nan":

                wa_url = whatsapp_link(action_phone)

                st.link_button(
                    "💬 Contact on WhatsApp",
                    wa_url,
                    use_container_width=True,
                )

            else:

                st.warning(
                    "⚠️ No WhatsApp number saved for this lead."
                )


            # ====================================================
            # WHATSAPP AI FOLLOW-UP
            # ====================================================

            st.divider()
            st.subheader("💬 WhatsApp AI Follow-Up")

            if action_phone and action_phone.lower() != "nan":

                if st.button(
                    "🤖 Generate WhatsApp Message",
                    use_container_width=True,
                    key="dashboard_generate_whatsapp",
                ):

                    with st.spinner(
                        "🧠 AI is creating a personalized message..."
                    ):

                        try:
                            generated_message = (
                                generate_whatsapp_message(
                                    action_data
                                )
                            )
                        except Exception as exc:
                            generated_message = (
                                "Hi! Just checking in to see "
                                "if you had any questions. "
                                "Happy to help whenever you're ready."
                            )
                            st.warning(
                                f"AI message generation fallback used: {exc}"
                            )

                    st.session_state[
                        "dashboard_whatsapp_message"
                    ] = generated_message

                if "dashboard_whatsapp_message" in st.session_state:

                    message_value = st.text_area(
                        "📝 Personalized WhatsApp Message",
                        value=st.session_state[
                            "dashboard_whatsapp_message"
                        ],
                        height=160,
                        key="dashboard_whatsapp_message_display",
                    )

                    st.session_state[
                        "dashboard_whatsapp_message"
                    ] = message_value

                    wa_ai_url = whatsapp_link(
                        action_phone,
                        message_value,
                    )

                    st.link_button(
                        "💬 Open WhatsApp with Message",
                        wa_ai_url,
                        use_container_width=True,
                    )

            else:

                st.warning(
                    "⚠️ No WhatsApp number saved for this lead."
                )


            # ====================================================
            # FOLLOW-UP INFORMATION
            # ====================================================

            st.divider()
            st.subheader("📅 Follow-Up Information")

            follow_col1, follow_col2 = st.columns(2)

            with follow_col1:

                st.write(
                    f"**Follow-Up Date:** "
                    f"{action_data['follow_up_date'] or 'Not scheduled'}"
                )

                st.write(
                    f"**Follow-Up Time:** "
                    f"{action_data['follow_up_time'] or 'Not scheduled'}"
                )

                st.write(
                    f"**Follow-Up Status:** "
                    f"{action_data['follow_up_status'] or 'Not set'}"
                )

            with follow_col2:

                st.write(
                    f"**Follow-Up Outcome:** "
                    f"{action_data['follow_up_outcome'] or 'Not recorded'}"
                )

                st.write(
                    f"**Outcome Notes:** "
                    f"{action_data['outcome_notes'] or 'No notes'}"
                )

                st.write(
                    f"**Last Contacted:** "
                    f"{action_data['last_contacted'] or 'Never'}"
                )


            # ====================================================
            # MARK CONTACTED
            # ====================================================

            st.divider()

            if st.button(
                "📞 Mark Lead as Contacted",
                use_container_width=True,
                key="dashboard_mark_contacted",
            ):

                if action_index is not None:

                    df.loc[
                        action_index,
                        "last_contacted",
                    ] = str(
                        pd.Timestamp.today().date()
                    )

                    save_data(df)

                    st.success(
                        f"✅ {action_lead} marked as contacted."
                    )

                    st.rerun()


            # ====================================================
            # LOCAL AI ACTION PLAN
            # ====================================================

            st.divider()
            st.subheader("🧠 Local AI Action Plan")

            if st.button(
                "🤖 Generate AI Action Plan",
                use_container_width=True,
                key="generate_action_plan",
            ):

                with st.spinner(
                    "🧠 Local AI is analyzing the lead..."
                ):

                    try:

                        action_plan = (
                            generate_lead_recommendation(
                                action_data
                            )
                        )

                        st.info(action_plan)

                    except Exception as exc:

                        st.error(
                            f"AI recommendation error: {exc}"
                        )

    else:

        st.success(
            "🎉 No active leads available for this filter."
        )


    # ========================================================
    # TODAY'S PRIORITY
    # ========================================================

    st.divider()
    st.subheader("🔥 Today's Priority")

    today_priority = df[
        (df["purchase"] != "Yes")
        & (df["priority"] == "🔥 High")
    ].sort_values(
        by="score",
        ascending=False,
    )

    if len(today_priority) > 0:

        today_columns = [
            "name",
            "source",
            "last_interaction",
            "score",
            "priority",
            "lead_stage",
            "recommended_action",
        ]

        st.dataframe(
            today_priority[today_columns],
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.success(
            "🎉 No high-priority leads require attention today!"
        )


    # ========================================================
    # SEARCH
    # ========================================================

    st.divider()
    st.subheader("🔎 Search Leads")

    search_query = st.text_input(
        "Search by name, source, qualification, or lead ID",
        placeholder="Example: Rahul or YouTube",
        key="dashboard_search",
    )

    if search_query:

        search_results = filter_search(
            df,
            search_query,
        )

        st.write(
            f"Found {len(search_results)} lead(s)"
        )

        st.dataframe(
            search_results,
            use_container_width=True,
            hide_index=True,
        )


    # ========================================================
    # FILTERS
    # ========================================================

    st.divider()
    st.subheader("🎚️ Filter Leads")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        priority_filter = st.selectbox(
            "Select Priority",
            [
                "All",
                "🔥 High",
                "🟡 Medium",
                "⚪ Low",
            ],
            key="dashboard_priority",
        )

    with filter_col2:

        stage_filter = st.selectbox(
            "Select Lead Stage",
            [
                "All Stages",
                "🆕 New Lead",
                "📱 Number Saved",
                "📅 Zoom Invited",
                "🎥 Zoom Attended",
                "💰 Purchased",
            ],
            key="dashboard_stage",
        )

    filtered_df = df.copy()

    if priority_filter != "All":
        filtered_df = filtered_df[
            filtered_df["priority"]
            == priority_filter
        ]

    if stage_filter != "All Stages":
        filtered_df = filtered_df[
            filtered_df["lead_stage"]
            == stage_filter
        ]

    st.write(
        f"Showing {len(filtered_df)} lead(s)"
    )


    # ========================================================
    # CONVERSION FUNNEL
    # ========================================================

    st.divider()
    st.subheader("📊 Lead Conversion Funnel")

    number_saved = len(
        df[df["number_saved"] == "Yes"]
    )

    zoom_invited = len(
        df[df["zoom_invited"] == "Yes"]
    )

    zoom_attended = len(
        df[df["zoom_attended"] == "Yes"]
    )

    purchased = len(
        df[df["purchase"] == "Yes"]
    )

    funnel_col1, funnel_col2, funnel_col3, funnel_col4, funnel_col5 = (
        st.columns(5)
    )

    with funnel_col1:
        st.metric("👥 Total Leads", total_leads)

    with funnel_col2:
        st.metric("📱 Number Saved", number_saved)

    with funnel_col3:
        st.metric("📅 Zoom Invited", zoom_invited)

    with funnel_col4:
        st.metric("🎥 Zoom Attended", zoom_attended)

    with funnel_col5:
        st.metric("💰 Purchased", purchased)


    # ========================================================
    # PRIORITY TABLE
    # ========================================================

    st.divider()
    st.subheader("🎯 Lead Priority")

    priority_columns = [
        "name",
        "age",
        "qualification",
        "source",
        "zoom_attended",
        "purchase",
        "score",
        "priority",
        "lead_stage",
        "recommended_action",
        "next_action",
    ]

    priority_columns = [
        column
        for column in priority_columns
        if column in filtered_df.columns
    ]

    if len(filtered_df) > 0:

        priority_df = (
            filtered_df[
                priority_columns
            ]
            .sort_values(
                by="score",
                ascending=False,
            )
        )

        st.dataframe(
            priority_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No leads match the selected filters."
        )


    # ========================================================
    # AI LEAD INTELLIGENCE
    # ========================================================

    st.divider()
    st.subheader("🧠 AI Lead Intelligence")

    active_leads = df[
        df["purchase"] != "Yes"
    ].copy()

    if len(active_leads) > 0:

        next_lead = active_leads.sort_values(
            by="score",
            ascending=False,
        ).iloc[0]

        ai_col1, ai_col2 = st.columns(2)

        with ai_col1:

            st.write(
                f"### 🎯 {next_lead['name']}"
            )

            st.metric(
                "Lead Score",
                next_lead["score"],
            )

            st.write(
                f"**Priority:** {next_lead['priority']}"
            )

            st.write(
                f"**Stage:** {next_lead['lead_stage']}"
            )

            st.write(
                f"**Bottleneck:** "
                f"{next_lead['conversion_bottleneck']}"
            )

            st.write(
                f"**Priority Reason:** "
                f"{next_lead['priority_reason']}"
            )

        with ai_col2:

            st.write("### 🤖 AI Recommendation")

            st.info(
                next_lead["lead_insight"]
            )

            st.success(
                f"**Next Action:** "
                f"{next_lead['next_action']}"
            )

            st.write(
                f"**Recommended Action:** "
                f"{next_lead['recommended_action']}"
            )

            st.write(
                f"**Lead Summary:** "
                f"{next_lead['lead_summary']}"
            )

    else:

        st.success(
            "🎉 All leads have been converted!"
        )


# ============================================================
# LEAD MANAGEMENT
# ============================================================

elif page == "👥 Leads":

    st.title("👥 Lead Management")

    st.write(
        "Search, filter, add, edit, and manage all your leads."
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()
    st.subheader("📊 Lead Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Leads", len(df))

    with col2:
        st.metric(
            "🔥 High Priority",
            len(df[df["priority"] == "🔥 High"]),
        )

    with col3:
        st.metric(
            "🟡 Medium Priority",
            len(df[df["priority"] == "🟡 Medium"]),
        )

    with col4:
        st.metric(
            "💰 Converted",
            len(df[df["purchase"] == "Yes"]),
        )


    # ========================================================
    # ADD NEW LEAD
    # ========================================================

    st.divider()
    st.subheader("➕ Add New Lead")

    # ========================================================
    # ADD NEW LEAD
    # ========================================================

    st.divider()
    st.subheader("➕ Add New Lead")

    # ========================================================
    # FREE PLAN LIMIT
    # ========================================================

    if CURRENT_PLAN == "Free" and len(df) >= FREE_LEAD_LIMIT:

        st.warning(
            f"🔒 Your Free plan allows up to "
            f"{FREE_LEAD_LIMIT} leads."
        )

        st.info(
            "🚀 Upgrade to LeadPilot Pro or Premium Pro "
            "for unlimited leads."
        )

    else:

        # ====================================================
        # ADD NEW LEAD FORM
        # ====================================================

        with st.form("add_lead_form"):

            add_col1, add_col2 = st.columns(2)

            with add_col1:

                new_name = st.text_input(
                    "👤 Lead Name",
                    placeholder="Enter lead name",
                )

                new_phone = st.text_input(
                    "📱 WhatsApp Number",
                    placeholder="Example: 919876543210",
                )

                new_age = st.number_input(
                    "🎂 Age",
                    min_value=1,
                    max_value=100,
                    value=25,
                )

                new_qualification = st.text_input(
                    "🎓 Qualification",
                    placeholder="Example: Graduate",
                )

                new_source = st.selectbox(
                    "📱 Lead Source",
                    [
                        "Instagram",
                        "YouTube",
                        "WhatsApp",
                        "Facebook",
                        "Referral",
                        "Other",
                    ],
                )

            with add_col2:

                new_number_saved = st.selectbox(
                    "📱 Number Saved?",
                    ["No", "Yes"],
                )

                new_zoom_invited = st.selectbox(
                    "📅 Zoom Invited?",
                    ["No", "Yes"],
                )

                new_zoom_attended = st.selectbox(
                    "🎥 Zoom Attended?",
                    ["No", "Yes"],
                )

                new_purchase = st.selectbox(
                    "💰 Purchased?",
                    ["No", "Yes"],
                )

            submitted = st.form_submit_button(
                "💾 Save New Lead",
                use_container_width=True,
            )

        # ====================================================
        # SAVE NEW LEAD
        # ====================================================

        if submitted:

            if not new_name.strip():

                st.error(
                    "⚠️ Please enter the lead name."
                )

            else:

                new_lead = {
                    "lead_id": make_unique_lead_id(df),
                    "name": new_name.strip(),
                    "phone": new_phone.strip(),
                    "age": new_age,
                    "qualification": new_qualification.strip(),
                    "source": new_source,
                    "number_saved": new_number_saved,
                    "zoom_invited": new_zoom_invited,
                    "zoom_attended": new_zoom_attended,
                    "purchase": new_purchase,
                    "last_interaction": str(
                        pd.Timestamp.today().date()
                    ),
                    "follow_up_date": "",
                    "follow_up_time": "",
                    "follow_up_status": "",
                    "follow_up_notes": "",
                    "follow_up_outcome": "",
                    "outcome_notes": "",
                    "last_contacted": "",
                }

                df = pd.concat(
                    [
                        df,
                        pd.DataFrame([new_lead]),
                    ],
                    ignore_index=True,
                )

                df = calculate_intelligence(df)

                save_data(df)

                st.success(
                    f"✅ {new_name} added successfully!"
                )

                st.rerun()


    # ========================================================
    # EDIT LEAD
    # ========================================================
 
    st.divider()
    st.subheader("✏️ Edit Lead")

    if len(df) > 0:

        edit_lead = st.selectbox(
            "Select Lead to Edit",
            df["name"].tolist(),
            key="edit_lead",
        )

        edit_index, edit_data = get_selected_row(
            df,
            edit_lead,
        )

        if edit_data is not None:

            source_options = [
                "Instagram",
                "YouTube",
                "WhatsApp",
                "Facebook",
                "Referral",
                "Other",
            ]

            current_source = safe_text(
                edit_data["source"]
            )

            source_index = (
                source_options.index(current_source)
                if current_source in source_options
                else 0
            )

            with st.form("edit_lead_form"):

                edit_col1, edit_col2 = st.columns(2)

                with edit_col1:

                    edit_name = st.text_input(
                        "👤 Lead Name",
                        value=safe_text(
                            edit_data["name"]
                        ),
                    )

                    edit_phone = st.text_input(
                        "📱 WhatsApp Number",
                        value=safe_text(
                            edit_data["phone"]
                        ),
                    )

                    try:
                        current_age = int(
                            float(edit_data["age"])
                        )
                    except Exception:
                        current_age = 25

                    edit_age = st.number_input(
                        "🎂 Age",
                        min_value=1,
                        max_value=100,
                        value=current_age,
                    )

                    edit_qualification = st.text_input(
                        "🎓 Qualification",
                        value=safe_text(
                            edit_data["qualification"]
                        ),
                    )

                    edit_source = st.selectbox(
                        "📱 Lead Source",
                        source_options,
                        index=source_index,
                    )

                with edit_col2:

                    edit_number_saved = st.selectbox(
                        "📱 Number Saved?",
                        ["No", "Yes"],
                        index=(
                            1
                            if safe_text(
                                edit_data["number_saved"]
                            ) == "Yes"
                            else 0
                        ),
                    )

                    edit_zoom_invited = st.selectbox(
                        "📅 Zoom Invited?",
                        ["No", "Yes"],
                        index=(
                            1
                            if safe_text(
                                edit_data["zoom_invited"]
                            ) == "Yes"
                            else 0
                        ),
                    )

                    edit_zoom_attended = st.selectbox(
                        "🎥 Zoom Attended?",
                        ["No", "Yes"],
                        index=(
                            1
                            if safe_text(
                                edit_data["zoom_attended"]
                            ) == "Yes"
                            else 0
                        ),
                    )

                    edit_purchase = st.selectbox(
                        "💰 Purchased?",
                        ["No", "Yes"],
                        index=(
                            1
                            if safe_text(
                                edit_data["purchase"]
                            ) == "Yes"
                            else 0
                        ),
                    )

                edit_submitted = st.form_submit_button(
                    "💾 Update Lead",
                    use_container_width=True,
                )

            if edit_submitted:

                if not edit_name.strip():

                    st.error(
                        "⚠️ Lead name cannot be empty."
                    )

                else:

                    df.loc[
                        edit_index,
                        "name",
                    ] = edit_name.strip()

                    df.loc[
                        edit_index,
                        "phone",
                    ] = edit_phone.strip()

                    df.loc[
                        edit_index,
                        "age",
                    ] = str(edit_age)

                    df.loc[
                        edit_index,
                        "qualification",
                    ] = edit_qualification.strip()

                    df.loc[
                        edit_index,
                        "source",
                    ] = edit_source

                    df.loc[
                        edit_index,
                        "number_saved",
                    ] = edit_number_saved

                    df.loc[
                        edit_index,
                        "zoom_invited",
                    ] = edit_zoom_invited

                    df.loc[
                        edit_index,
                        "zoom_attended",
                    ] = edit_zoom_attended

                    df.loc[
                        edit_index,
                        "purchase",
                    ] = edit_purchase

                    df = calculate_intelligence(df)
                    save_data(df)

                    st.success(
                        f"✅ {edit_name} updated successfully!"
                    )

                    st.rerun()


    # ========================================================
    # EXPORT
    # ========================================================

    st.divider()
    st.subheader("📤 Export Leads")

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📤 Download Lead Database",
        data=csv_data,
        file_name="leadpilot_leads.csv",
        mime="text/csv",
        use_container_width=True,
    )


    # ========================================================
    # SEARCH & FILTER
    # ========================================================

    st.divider()
    st.subheader("🔎 Search & Filter Leads")

    lead_search = st.text_input(
        "🔎 Search Leads",
        placeholder=(
            "Search by name, source, qualification, or lead ID"
        ),
        key="leads_search",
    )

    leads_page_df = filter_search(
        df,
        lead_search,
    )

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        lead_priority_filter = st.selectbox(
            "🎯 Priority",
            [
                "All",
                "🔥 High",
                "🟡 Medium",
                "⚪ Low",
            ],
            key="leads_priority",
        )

    with filter_col2:

        lead_stage_filter = st.selectbox(
            "🧭 Lead Stage",
            [
                "All Stages",
                "🆕 New Lead",
                "📱 Number Saved",
                "📅 Zoom Invited",
                "🎥 Zoom Attended",
                "💰 Purchased",
            ],
            key="leads_stage",
        )

    if lead_priority_filter != "All":

        leads_page_df = leads_page_df[
            leads_page_df["priority"]
            == lead_priority_filter
        ]

    if lead_stage_filter != "All Stages":

        leads_page_df = leads_page_df[
            leads_page_df["lead_stage"]
            == lead_stage_filter
        ]

    st.metric(
        "Leads Found",
        len(leads_page_df),
    )


    # ========================================================
    # LEAD TABLE
    # ========================================================

    display_columns = [
        "lead_id",
        "name",
        "phone",
        "source",
        "qualification",
        "score",
        "priority",
        "lead_stage",
        "recommended_action",
    ]

    display_columns = [
        column
        for column in display_columns
        if column in leads_page_df.columns
    ]

    if len(leads_page_df) > 0:

        priority_df = (
            leads_page_df[
                display_columns
            ]
            .sort_values(
                by="score",
                ascending=False,
            )
        )

        st.dataframe(
            priority_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("🔎 No leads found.")


    # ========================================================
    # SELECTED LEAD PROFILE
    # ========================================================

    st.divider()
    st.subheader("👤 Selected Lead Profile")

    if len(df) > 0:

        profile_lead = st.selectbox(
            "Select Lead",
            df["name"].tolist(),
            key="lead_profile_select",
        )

        profile_index, profile = get_selected_row(
            df,
            profile_lead,
        )

        if profile is not None:

            profile_col1, profile_col2 = st.columns(2)

            with profile_col1:

                st.write(
                    f"### 👤 {profile['name']}"
                )

                st.write(
                    f"**Lead ID:** {profile['lead_id']}"
                )

                st.write(
                    f"**Phone:** "
                    f"{profile['phone'] or 'Not saved'}"
                )

                st.write(
                    f"**Source:** {profile['source']}"
                )

                st.write(
                    f"**Qualification:** "
                    f"{profile['qualification']}"
                )

                st.write(
                    f"**Age:** {profile['age']}"
                )

            with profile_col2:

                st.metric(
                    "Lead Score",
                    profile["score"],
                )

                st.write(
                    f"**Priority:** {profile['priority']}"
                )

                st.write(
                    f"**Stage:** {profile['lead_stage']}"
                )

                st.write(
                    f"**Next Action:** "
                    f"{profile['next_action']}"
                )

                st.write(
                    f"**Bottleneck:** "
                    f"{profile['conversion_bottleneck']}"
                )

            st.info(
                f"🧠 {profile['lead_insight']}"
            )

            st.write(
                f"**Priority Reason:** "
                f"{profile['priority_reason']}"
            )

            st.write(
                f"**Recommended Action:** "
                f"{profile['recommended_action']}"
            )

            st.write(
                f"**Lead Summary:** "
                f"{profile['lead_summary']}"
            )


    # ========================================================
    # LEAD ACTIVITY
    # ========================================================

    st.divider()
    st.subheader("📋 Lead Activity")

    if len(df) > 0:

        activity_lead = st.selectbox(
            "Select Lead to View Activity",
            df["name"].tolist(),
            key="activity_lead",
        )

        activity_index, activity = get_selected_row(
            df,
            activity_lead,
        )

        if activity is not None:

            st.write(
                f"### 👤 {activity['name']}"
            )

            activity_col1, activity_col2, activity_col3 = (
                st.columns(3)
            )

            with activity_col1:
                st.metric(
                    "Lead Score",
                    activity["score"],
                )

            with activity_col2:
                st.metric(
                    "Priority",
                    activity["priority"],
                )

            with activity_col3:
                st.metric(
                    "Stage",
                    activity["lead_stage"],
                )

            st.divider()
            st.write("### 📋 Activity Timeline")

            if activity["number_saved"] == "Yes":
                st.success("📱 Number Saved")
            else:
                st.info("📱 Number Not Saved")

            if activity["zoom_invited"] == "Yes":
                st.success("📅 Zoom Invitation Sent")

            if activity["zoom_attended"] == "Yes":
                st.success("🎥 Zoom Meeting Attended")

            if activity["purchase"] == "Yes":
                st.success("💰 Purchase Completed")

            if activity["last_contacted"]:
                st.info(
                    f"📞 Last Contacted: "
                    f"{activity['last_contacted']}"
                )

            if activity["follow_up_date"]:
                st.info(
                    f"⏰ Follow-Up: "
                    f"{activity['follow_up_date']} "
                    f"{activity['follow_up_time']}"
                )

            if activity["follow_up_status"]:
                st.write(
                    f"Follow-Up Status: "
                    f"**{activity['follow_up_status']}**"
                )

            if activity["follow_up_outcome"]:
                st.success(
                    f"📝 Outcome: "
                    f"{activity['follow_up_outcome']}"
                )

            if activity["outcome_notes"]:
                st.write(
                    f"💬 Notes: "
                    f"{activity['outcome_notes']}"
                )

            st.divider()
            st.subheader("💬 Contact Lead")

            activity_phone = safe_text(
                activity.get("phone", "")
            ).strip()

            if activity_phone and activity_phone.lower() != "nan":

                st.link_button(
                    "💬 Open WhatsApp",
                    whatsapp_link(activity_phone),
                    use_container_width=True,
                )

            else:

                st.warning(
                    "⚠️ No WhatsApp number saved for this lead."
                )


# ============================================================
# FOLLOW-UPS
# ============================================================

elif page == "📅 Follow-Ups":

    st.title("📅 Follow-Up Management")

    st.write(
        "Schedule, update, and record follow-up activities."
    )

        # ========================================================
    # SMART FOLLOW-UP SUMMARY
    # ========================================================

    st.divider()
    st.subheader("🎯 Smart Follow-Up Overview")

    overdue_count = len(
        df[df["follow_up_type"] == "🔴 Overdue"]
    )

    due_today_count = len(
        df[df["follow_up_type"] == "🟠 Due Today"]
    )

    upcoming_count = len(
        df[df["follow_up_type"] == "🟢 Upcoming"]
    )

    completed_count = len(
        df[df["follow_up_type"] == "✅ Completed"]
    )

    unscheduled_count = len(
        df[df["follow_up_type"] == "⚪ Unscheduled"]
    )

    summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = (
        st.columns(5)
    )

    with summary_col1:
        st.metric(
            "🔴 Overdue",
            overdue_count,
        )

    with summary_col2:
        st.metric(
            "🟠 Due Today",
            due_today_count,
        )

    with summary_col3:
        st.metric(
            "🟢 Upcoming",
            upcoming_count,
        )

    with summary_col4:
        st.metric(
            "✅ Completed",
            completed_count,
        )

    with summary_col5:
        st.metric(
            "⚪ Unscheduled",
            unscheduled_count,
        )

            # ========================================================
    # TODAY'S FOLLOW-UP QUEUE
    # ========================================================

    st.divider()
    st.subheader("🎯 Today's Follow-Up Queue")

    follow_up_queue = df[
        df["follow_up_type"].isin(
            [
                "🔴 Overdue",
                "🟠 Due Today",
            ]
        )
        & (df["purchase"] != "Yes")
    ].copy()

    if len(follow_up_queue) > 0:

        follow_up_queue = follow_up_queue.sort_values(
            by=["follow_up_priority", "score"],
            ascending=[True, False],
        )

        queue_columns = [
            "name",
            "priority",
            "follow_up_type",
            "follow_up_date",
            "follow_up_time",
            "follow_up_priority",
            "lead_stage",
            "next_action",
        ]

        queue_columns = [
            column
            for column in queue_columns
            if column in follow_up_queue.columns
        ]

        st.dataframe(
            follow_up_queue[queue_columns],
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.success(
            "🎉 No overdue or due-today follow-ups!"
        )

            # ========================================================
    # QUICK FOLLOW-UP ACTION
    # ========================================================

    st.divider()
    st.subheader("⚡ Quick Follow-Up Action")

    if len(follow_up_queue) > 0:

        quick_lead = st.selectbox(
            "Select a lead to contact",
            follow_up_queue["name"].tolist(),
            key="quick_followup_lead",
        )

        quick_index, quick_data = get_selected_row(
            df,
            quick_lead,
        )

        if quick_data is not None:

            quick_col1, quick_col2 = st.columns(2)

            with quick_col1:

                st.write(
                    f"### 👤 {quick_data['name']}"
                )

                st.write(
                    f"**Priority:** "
                    f"{quick_data['priority']}"
                )

                st.write(
                    f"**Follow-Up:** "
                    f"{quick_data['follow_up_type']}"
                )

                st.write(
                    f"**Next Action:** "
                    f"{quick_data['next_action']}"
                )

            with quick_col2:

                st.write(
                    f"**Follow-Up Date:** "
                    f"{quick_data['follow_up_date']}"
                )

                st.write(
                    f"**Follow-Up Time:** "
                    f"{quick_data['follow_up_time'] or 'Not set'}"
                )

                st.write(
                    f"**Lead Stage:** "
                    f"{quick_data['lead_stage']}"
                )

                st.write(
                    f"**AI Recommendation:** "
                    f"{quick_data['ai_recommendation']}"
                )

                

            st.divider()

            quick_phone = safe_text(
                quick_data.get("phone", "")
            ).strip()

            if quick_phone and quick_phone.lower() != "nan":

                st.link_button(
                    "💬 Contact on WhatsApp",
                    whatsapp_link(quick_phone),
                    use_container_width=True,
                )

            else:

                st.warning(
                    "⚠️ No WhatsApp number saved for this lead."
                )

            if st.button(
                "📞 Mark as Contacted",
                use_container_width=True,
                key="quick_mark_contacted",
            ):

                if quick_index is not None:

                    df.loc[
                        quick_index,
                        "last_contacted",
                    ] = str(
                        pd.Timestamp.today().date()
                    )

                    # Automatically mark today's follow-up
                    # as completed after contact.
                    if quick_data["follow_up_type"] == "🟠 Due Today":

                        df.loc[
                            quick_index,
                            "follow_up_status",
                        ] = "Completed"

                    df = calculate_intelligence(df)

                    df = add_follow_up_intelligence(df)

                    save_data(df)

                    st.success(
                        f"✅ {quick_lead} marked as contacted."
                    )

                    st.rerun()

    if len(df) == 0:

        st.info("No leads available.")

    else:

        followup_lead = st.selectbox(
            "Select Lead",
            df["name"].tolist(),
            key="followup_lead",
        )

        followup_index, followup_data = get_selected_row(
            df,
            followup_lead,
        )

        if followup_data is not None:

            st.subheader(
                f"📅 Follow-Up for {followup_data['name']}"
            )

            follow_col1, follow_col2 = st.columns(2)

            with follow_col1:

                current_date = safe_text(
                    followup_data["follow_up_date"]
                )

                current_time = safe_text(
                    followup_data["follow_up_time"]
                )

                follow_date = st.date_input(
                    "📅 Follow-Up Date",
                    value=(
                        pd.to_datetime(
                            current_date,
                            errors="coerce",
                        ).date()
                        if pd.notna(
                            pd.to_datetime(
                                current_date,
                                errors="coerce",
                            )
                        )
                        else pd.Timestamp.today().date()
                    ),
                )

                follow_time = st.time_input(
                    "⏰ Follow-Up Time",
                    value=(
                        pd.to_datetime(
                            current_time,
                            errors="coerce",
                        ).time()
                        if pd.notna(
                            pd.to_datetime(
                                current_time,
                                errors="coerce",
                            )
                        )
                        else pd.Timestamp.now().time().replace(
                            second=0,
                            microsecond=0,
                        )
                    ),
                )

                follow_status = st.selectbox(
                    "📌 Follow-Up Status",
                    [
                        "Pending",
                        "Completed",
                        "Skipped",
                    ],
                    index=(
                        [
                            "Pending",
                            "Completed",
                            "Skipped",
                        ].index(
                            safe_text(
                                followup_data["follow_up_status"]
                            )
                        )
                        if safe_text(
                            followup_data["follow_up_status"]
                        )
                        in [
                            "Pending",
                            "Completed",
                            "Skipped",
                        ]
                        else 0
                    ),
                )

            with follow_col2:

                follow_notes = st.text_area(
                    "📝 Follow-Up Notes",
                    value=safe_text(
                        followup_data["follow_up_notes"]
                    ),
                    height=120,
                )

                follow_outcome = st.selectbox(
                    "📝 Follow-Up Outcome",
                    [
                        "",
                        "Interested",
                        "Needs More Information",
                        "No Response",
                        "Not Interested",
                        "Purchased",
                        "Call Back Later",
                    ],
                    index=(
                        [
                            "",
                            "Interested",
                            "Needs More Information",
                            "No Response",
                            "Not Interested",
                            "Purchased",
                            "Call Back Later",
                        ].index(
                            safe_text(
                                followup_data[
                                    "follow_up_outcome"
                                ]
                            )
                        )
                        if safe_text(
                            followup_data[
                                "follow_up_outcome"
                            ]
                        )
                        in [
                            "",
                            "Interested",
                            "Needs More Information",
                            "No Response",
                            "Not Interested",
                            "Purchased",
                            "Call Back Later",
                        ]
                        else 0
                    ),
                )

                outcome_notes = st.text_area(
                    "💬 Outcome Notes",
                    value=safe_text(
                        followup_data["outcome_notes"]
                    ),
                    height=120,
                )

            if st.button(
                "💾 Save Follow-Up",
                use_container_width=True,
                key="save_followup",
            ):

                df.loc[
                    followup_index,
                    "follow_up_date",
                ] = str(follow_date)

                df.loc[
                    followup_index,
                    "follow_up_time",
                ] = follow_time.strftime("%H:%M")

                df.loc[
                    followup_index,
                    "follow_up_status",
                ] = follow_status

                df.loc[
                    followup_index,
                    "follow_up_notes",
                ] = follow_notes

                df.loc[
                    followup_index,
                    "follow_up_outcome",
                ] = follow_outcome

                df.loc[
                    followup_index,
                    "outcome_notes",
                ] = outcome_notes

                  

                df = calculate_intelligence(df)
                save_data(df)

                st.success(
                    f"✅ Follow-up updated for {followup_lead}."
                )

                st.rerun()


        st.divider()
        st.subheader("📋 Upcoming & Pending Follow-Ups")

        follow_table = df.copy()

        follow_table["_date"] = pd.to_datetime(
            follow_table["follow_up_date"],
            errors="coerce",
        )

        follow_table = follow_table[
            follow_table["_date"].notna()
        ].sort_values(
            "_date"
        )

        if len(follow_table) > 0:

            follow_columns = [
                "name",
                "phone",
                "follow_up_date",
                "follow_up_time",
                "follow_up_status",
                "follow_up_outcome",
                "next_action",
                "priority",
            ]

            st.dataframe(
                follow_table[
                    [
                        column
                        for column in follow_columns
                        if column in follow_table.columns
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "📅 No scheduled follow-ups found."
            )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    st.title("📈 Lead Analytics")

    if len(df) == 0:

        st.info("Add leads to see analytics.")

    else:

        total = len(df)
        purchased = len(
            df[df["purchase"] == "Yes"]
        )

        conversion_rate = (
            (purchased / total) * 100
            if total
            else 0
        )

        avg_score = (
            pd.to_numeric(
                df["score"],
                errors="coerce",
            )
            .mean()
        )

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:
            st.metric(
                "👥 Total Leads",
                total,
            )

        with metric2:
            st.metric(
                "💰 Purchased",
                purchased,
            )

        with metric3:
            st.metric(
                "📈 Conversion Rate",
                f"{conversion_rate:.1f}%",
            )

        with metric4:
            st.metric(
                "🎯 Average Score",
                f"{avg_score:.1f}"
                if pd.notna(avg_score)
                else "0",
            )


        st.divider()

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.subheader("🎯 Lead Priority")

            priority_counts = (
                df["priority"]
                .value_counts()
                .rename_axis("Priority")
                .reset_index(name="Leads")
            )

            if len(priority_counts) > 0:
                st.bar_chart(
                    priority_counts.set_index(
                        "Priority"
                    )
                )

        with chart_col2:

            st.subheader("🧭 Lead Lifecycle")

            stage_counts = (
                df["lead_stage"]
                .value_counts()
                .rename_axis("Stage")
                .reset_index(name="Leads")
            )

            if len(stage_counts) > 0:
                st.bar_chart(
                    stage_counts.set_index(
                        "Stage"
                    )
                )


        st.divider()

        st.subheader("📊 Conversion Funnel")

        funnel_data = pd.DataFrame(
            {
                "Stage": [
                    "Total Leads",
                    "Number Saved",
                    "Zoom Invited",
                    "Zoom Attended",
                    "Purchased",
                ],
                "Leads": [
                    len(df),
                    len(
                        df[
                            df["number_saved"]
                            == "Yes"
                        ]
                    ),
                    len(
                        df[
                            df["zoom_invited"]
                            == "Yes"
                        ]
                    ),
                    len(
                        df[
                            df["zoom_attended"]
                            == "Yes"
                        ]
                    ),
                    len(
                        df[
                            df["purchase"]
                            == "Yes"
                        ]
                    ),
                ],
            }
        )

        st.dataframe(
            funnel_data,
            use_container_width=True,
            hide_index=True,
        )


        st.divider()

        st.subheader("🚧 Conversion Bottlenecks")

        bottleneck_counts = (
            df["conversion_bottleneck"]
            .value_counts()
            .rename_axis("Bottleneck")
            .reset_index(name="Leads")
        )

        if len(bottleneck_counts) > 0:

            st.bar_chart(
                bottleneck_counts.set_index(
                    "Bottleneck"
                )
            )


# ============================================================
# IMPORT LEADS
# ============================================================

elif page == "📥 Import Leads":

    st.title("📥 Import Leads")

    st.write(
        "Import a CSV file into LeadPilot."
    )

    st.info(
        "Your CSV should contain at least a name column. "
        "Other LeadPilot columns will be created automatically."
    )

    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"],
    )

    if uploaded_file is not None:

        try:

            imported_df = pd.read_csv(
                uploaded_file
            )

            st.subheader("👀 Preview")

            st.dataframe(
                imported_df.head(20),
                use_container_width=True,
                hide_index=True,
            )

            if st.button(
                "📥 Import into LeadPilot",
                use_container_width=True,
                key="import_csv_button",
            ):

                for column in REQUIRED_COLUMNS:
                    if column not in imported_df.columns:
                        imported_df[column] = ""

                imported_df = imported_df[
                    [
                        column
                        for column in REQUIRED_COLUMNS
                        if column in imported_df.columns
                    ]
                    + [
                        column
                        for column in imported_df.columns
                        if column not in REQUIRED_COLUMNS
                    ]
                ]

                imported_df = calculate_intelligence(
                    imported_df
                )

                save_data(imported_df)

                st.success(
                    f"✅ Imported {len(imported_df)} leads successfully."
                )

                st.rerun()

        except Exception as exc:

            st.error(
                f"❌ Import failed: {exc}"
            )


# ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.title("⚙️ LeadPilot Settings")

    st.subheader("📁 Data")

    st.write(
        f"**Lead database:** `{DATA_PATH}`"
    )

    st.write(
        f"**Total leads:** {len(df)}"
    )

    st.divider()

    st.subheader("📤 Backup")

    backup_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Full Backup",
        data=backup_data,
        file_name="leadpilot_backup.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.divider()

    st.subheader("🔄 Recalculate Intelligence")

    st.write(
        "Re-runs your existing LeadPilot scoring and "
        "intelligence functions for every lead."
    )

    if st.button(
        "🔄 Recalculate All Lead Intelligence",
        use_container_width=True,
        key="recalculate_all",
    ):

        df = calculate_intelligence(df)
        save_data(df)

        st.success(
            "✅ Lead intelligence recalculated successfully."
        )

        st.rerun()

    st.divider()

    st.subheader("🧹 Data Safety")

    st.warning(
        "Do not delete your original leads.csv unless "
        "you already have a backup."
    )

    # ============================================================
# PLANS & SUBSCRIPTION
# ============================================================

elif page == "💳 Plans":

    st.title("💳 LeadPilot Plans")

    st.write(
        "Choose the plan that fits your lead management needs."
    )

    st.divider()

    free_col, pro_col = st.columns(2)

      # ========================================================
    # PRICING PLANS
    # ========================================================

    st.divider()
    st.subheader("💳 Choose Your LeadPilot Plan")

    st.caption(
        "Start free and upgrade whenever you need more power."
    )

    # --------------------------------------------------------
    # PLAN COLUMNS
    # --------------------------------------------------------

    free_col, pro_col, premium_col = st.columns(3)

    # ========================================================
    # FREE PLAN
    # ========================================================

    with free_col:

        st.subheader("🆓 LeadPilot Free")

        st.write("### ₹0 / month")

        st.write(
            "Perfect for getting started."
        )

        st.markdown(
            """
            ✅ Up to **20 leads**

            ✅ Basic lead scoring

            ✅ Basic follow-ups

            ✅ Basic analytics

            ✅ Search & filtering

            ✅ Lead management

            ✅ Basic AI recommendations
            """
        )

        if CURRENT_PLAN == "Free":

            st.success(
                "✓ Your current plan"
            )

        else:

            st.info(
                "Free plan"
            )

    # ========================================================
    # PRO PLAN
    # ========================================================

    with pro_col:

        st.subheader("🚀 LeadPilot Pro")

        st.write("### ₹299 / month")

        st.write(
            "**₹1,999 / year**"
        )

        st.write(
            "For entrepreneurs who want to convert more leads."
        )

        st.markdown(
            """
            ✅ **Unlimited leads**

            ✅ Advanced lead scoring

            ✅ Full AI lead intelligence

            ✅ Smart Follow-Ups

            ✅ Advanced analytics

            ✅ AI Action Plans

            ✅ Advanced lead prioritization

            ✅ Full Action Center

            ✅ WhatsApp tools

            ✅ Future Pro features
            """
        )

        if CURRENT_PLAN == "Pro":

            st.success(
                "✓ Your current plan"
            )

        else:

            if st.button(
                "🚀 Upgrade to Pro",
                use_container_width=True,
                key="upgrade_pro_button",
            ):

                st.info(
                    "💳 Pro subscription — ₹299/month or ₹1,999/year"
                )

    # ========================================================
    # PREMIUM PRO PLAN
    # ========================================================

    with premium_col:

        st.subheader("💎 Premium Pro")

        st.write("### ₹499 / month")

        st.write(
            "**₹3,999 / year**"
        )

        st.write(
            "For serious entrepreneurs who want maximum growth."
        )

        st.markdown(
            """
            ✅ **Unlimited leads**

            ✅ Everything in Pro

            ✅ Advanced AI intelligence

            ✅ Premium analytics

            ✅ Advanced automation

            ✅ Priority recommendations

            ✅ Advanced Action Plans

            ✅ Premium lead intelligence

            ✅ WhatsApp automation*

            ✅ Premium features

            ✅ Priority feature access
            """
        )

        if CURRENT_PLAN == "Premium Pro":

            st.success(
                "✓ Your current plan"
            )

        else:

            if st.button(
                "💎 Upgrade to Premium Pro",
                use_container_width=True,
                key="upgrade_premium_button",
            ):

                st.info(
                    "💳 Premium Pro — ₹499/month or ₹3,999/year"
                )

        st.caption(
            "*WhatsApp automation availability depends on the integration."
        )

