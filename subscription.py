from datetime import datetime, timedelta


def activate_subscription(
    credentials,
    username,
    plan,
    billing_cycle,
):

    if username not in credentials.get(
        "usernames",
        {}
    ):

        return False

    if billing_cycle == "monthly":

        duration_days = 30

    elif billing_cycle == "yearly":

        duration_days = 365

    else:

        return False

    start_date = datetime.now().date()

    expiry_date = (
        start_date
        + timedelta(
            days=duration_days
        )
    )

    user = credentials["usernames"][username]

    user["plan"] = plan

    user["billing_cycle"] = billing_cycle

    user["plan_start_date"] = (
        start_date.strftime("%Y-%m-%d")
    )

    user["plan_expiry_date"] = (
        expiry_date.strftime("%Y-%m-%d")
    )

    return True