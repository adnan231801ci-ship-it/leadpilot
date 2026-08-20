import streamlit as st
import streamlit_authenticator as stauth


def get_authenticator():

    credentials = {
        "usernames": {
            "admin": {
                "email": "admin@leadpilot.com",
                "name": "LeadPilot Admin",
                "password": "admin123"
            }
        }
    }

    authenticator = stauth.Authenticate(
        credentials,
        "leadpilot_cookie",
        "leadpilot_secret_key",
        cookie_expiry_days=7
    )

    return authenticator