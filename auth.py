from pathlib import Path

import streamlit_authenticator as stauth
import yaml
from dotenv import load_dotenv
import os

from datetime import datetime, timedelta

load_dotenv()


ACCOUNTS_PATH = Path(__file__).resolve().parent.parent / "accounts.yaml"


def load_credentials():

    if not ACCOUNTS_PATH.exists():

        credentials = {
            "usernames": {
                "admin": {
                    "email": "admin@leadpilot.com",
                    "name": "LeadPilot Admin",
                    "password": "admin123",
                    "plan": "Admin",
                }
            }
        }

        save_credentials(credentials)

        return credentials

    with open(
        ACCOUNTS_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file) or {}

    return config.get(
        "credentials",
        {"usernames": {}},
    )


def save_credentials(credentials):

    with open(
        ACCOUNTS_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        yaml.safe_dump(
            {
                "credentials": credentials,
            },
            file,
            sort_keys=False,
        )

def check_subscription_expiry(credentials):

    today = datetime.now().date()

    changed = False

    for username, user in credentials.get(
        "usernames",
        {}
    ).items():

        plan = user.get(
            "plan",
            "Free"
        )

        if plan not in [
            "Pro Monthly",
            "Pro Yearly",
        ]:
            continue

        expiry_date = user.get(
            "plan_expiry_date"
        )

        if not expiry_date:
            continue

        try:

            expiry = datetime.strptime(
                str(expiry_date),
                "%Y-%m-%d"
            ).date()

        except ValueError:

            continue

        if today >= expiry:

            user["plan"] = "Free"

            user["billing_cycle"] = ""

            user["plan_start_date"] = ""

            user["plan_expiry_date"] = ""

            changed = True

    if changed:

        save_credentials(
            credentials
        )

    return credentials

def get_authenticator():

    credentials = load_credentials()

    credentials = check_subscription_expiry(
        credentials
    )

    resend_api_key = os.getenv(
        "RESEND_API_KEY"
    )

    authenticator = stauth.Authenticate(
        credentials,
        "leadpilot_cookie",
        "leadpilot_secret_key",
        cookie_expiry_days=7,
        api_key=resend_api_key,
    )

    return authenticator, credentials