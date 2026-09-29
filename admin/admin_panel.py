import streamlit as st
from datetime import datetime, timedelta

from auth import load_credentials, save_credentials


PLANS = {
    "Free": {
        "price": 0,
        "duration": None,
    },
    "Pro Monthly": {
        "price": 299,
        "duration": 30,
    },
    "Pro Yearly": {
        "price": 1999,
        "duration": 365,
    },
    "Premium Monthly": {
        "price": 499,
        "duration": 30,
    },
    "Premium Yearly": {
        "price": 3999,
        "duration": 365,
    },
}


def is_admin(username, credentials):
    if not username:
        return False

    user = credentials.get("usernames", {}).get(username, {})

    return user.get("plan") == "Admin"

def activate_plan(username, plan, payment_confirmed):
    credentials = load_credentials()

    user = credentials.get("usernames", {}).get(username)

    if not user:
        return False, "Client not found."

    if plan not in PLANS or plan == "Free":
        return False, "Invalid plan."

    today = datetime.now().date()
    duration = PLANS[plan]["duration"]

    expiry = today + timedelta(days=duration)

    user["plan"] = plan
    user["billing_cycle"] = (
        "Yearly" if "Yearly" in plan else "Monthly"
    )
    user["plan_start_date"] = today.strftime("%Y-%m-%d")
    user["plan_expiry_date"] = expiry.strftime("%Y-%m-%d")

    if payment_confirmed:
        user["payment_status"] = "Paid"
        user["payment_date"] = today.strftime("%Y-%m-%d")
        user["payment_amount"] = PLANS[plan]["price"]
    else:
        user["payment_status"] = "Pending"
        user["payment_date"] = ""
        user["payment_amount"] = 0

    save_credentials(credentials)

    return True, f"{plan} activated successfully."

def set_free(username):
    credentials = load_credentials()

    user = credentials.get("usernames", {}).get(username)

    if not user:
        return False, "Client not found."

    user["plan"] = "Free"
    user["billing_cycle"] = ""
    user["plan_start_date"] = ""
    user["plan_expiry_date"] = ""

    user["payment_status"] = ""
    user["payment_date"] = ""
    user["payment_amount"] = 0

    save_credentials(credentials)

    return True, "Client moved to Free plan."


def suspend_client(username):
    credentials = load_credentials()

    user = credentials.get("usernames", {}).get(username)

    if not user:
        return False, "Client not found."

    user["account_status"] = "Suspended"

    save_credentials(credentials)

    return True, "Client suspended."


def activate_client(username):
    credentials = load_credentials()

    user = credentials.get("usernames", {}).get(username)

    if not user:
        return False, "Client not found."

    user["account_status"] = "Active"

    save_credentials(credentials)

    return True, "Client activated."


def show_admin_panel(username):

    credentials = load_credentials()

    if not is_admin(username, credentials):
        st.error("Access denied.")
        st.stop()

    st.title("🛡️ LeadPilot Admin Panel")
    st.caption("LeadPilot Control Room")

    users = credentials.get("usernames", {})

    clients = {
        key: value
        for key, value in users.items()
        if value.get("plan") != "Admin"
    }

    st.subheader("📊 Overview")

    total_clients = len(clients)

    paid_clients = sum(
        1
        for user in clients.values()
        if user.get("payment_status") == "Paid"
    )

    revenue = sum(
        float(user.get("payment_amount", 0) or 0)
        for user in clients.values()
        if user.get("payment_status") == "Paid"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Clients", total_clients)
    col2.metric("Paid Clients", paid_clients)
    col3.metric("Recorded Revenue", f"₹{revenue:,.0f}")

    st.divider()

    st.subheader("👥 Client Management")

    if not clients:
        st.info("No clients registered yet.")
        return

    selected_username = st.selectbox(
        "Select Client",
        list(clients.keys()),
    )

    client = clients[selected_username]

    st.write(
        f"**Name:** {client.get('name', 'N/A')}"
    )

    st.write(
        f"**Email:** {client.get('email', 'N/A')}"
    )

    st.write(
        f"**Current Plan:** {client.get('plan', 'Free')}"
    )

    st.write(
        f"**Status:** {client.get('account_status', 'Active')}"
    )

    if client.get("plan_expiry_date"):
        st.write(
            f"**Expiry:** {client.get('plan_expiry_date')}"
        )

    st.divider()

    st.subheader("💳 Plan Management")

    selected_plan = st.selectbox(
        "Select Plan",
        [
            "Pro Monthly",
            "Pro Yearly",
            "Premium Monthly",
            "Premium Yearly",
        ],
    )

    payment_confirmed = st.checkbox(
        "💰 Payment received and verified",
        key="payment_confirmed",
    )

    if st.button(
        "✅ Activate Selected Plan",
        use_container_width=True,
    ):
        if not payment_confirmed:
            st.warning(
                "Please confirm that payment has been received and verified."
            )
        else:
            success, message = activate_plan(
                selected_username,
                selected_plan,
                payment_confirmed,
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "⬇️ Move to Free",
            use_container_width=True,
        ):
            success, message = set_free(
                selected_username
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    with col2:
        status = client.get(
            "account_status",
            "Active",
        )

        if status == "Suspended":
            if st.button(
                "🟢 Activate Account",
                use_container_width=True,
            ):
                success, message = activate_client(
                    selected_username
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        else:
            if st.button(
                "🔴 Suspend Account",
                use_container_width=True,
            ):
                success, message = suspend_client(
                    selected_username
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)