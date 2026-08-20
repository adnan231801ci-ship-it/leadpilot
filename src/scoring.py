from datetime import datetime


def calculate_lead_score(lead):
    score = 0

    # Number saved
    if lead["number_saved"] == "Yes":
        score += 15

    # Zoom invited
    if lead["zoom_invited"] == "Yes":
        score += 15

    # Zoom attended
    if lead["zoom_attended"] == "Yes":
        score += 30

    # Recency of interaction
    try:
        last_interaction = datetime.strptime(
            str(lead["last_interaction"]),
            "%Y-%m-%d"
        )

        today = datetime.today()

        days_since_interaction = (
            today - last_interaction
        ).days

        if days_since_interaction <= 2:
            score += 20
        elif days_since_interaction <= 7:
            score += 10
        elif days_since_interaction <= 14:
            score += 5

    except:
        pass

    # Purchased leads
    if lead["purchase"] == "Yes":
        score = 100

    # Priority
    if score >= 70:
        priority = "🔥 High"
    elif score >= 40:
        priority = "🟡 Medium"
    else:
        priority = "⚪ Low"

    return score, priority


def get_recommended_action(lead):

    if lead["purchase"] == "Yes":
        return "✅ Converted - No follow-up needed"

    if lead["zoom_attended"] == "Yes":
        return "🔥 Follow up about the purchase"

    if lead["zoom_invited"] == "Yes":
        return "🎯 Encourage Zoom attendance"

    if lead["number_saved"] == "Yes":
        return "📅 Move lead toward Zoom"

    return "👋 Start lead qualification"


def get_lead_stage(lead):

    if lead["purchase"] == "Yes":
        return "💰 Purchased"

    if lead["zoom_attended"] == "Yes":
        return "🎥 Zoom Attended"

    if lead["zoom_invited"] == "Yes":
        return "📅 Zoom Invited"

    if lead["number_saved"] == "Yes":
        return "📱 Number Saved"

    return "🆕 New Lead"


def get_next_action(lead):

    outcome = str(
        lead.get("follow_up_outcome", "")
    ).strip()

    purchase = str(
        lead.get("purchase", "")
    ).strip()

    if purchase == "Yes" or outcome == "Purchased":
        return "🎉 Converted - Focus on customer retention"

    if outcome == "Interested":
        return "📞 Follow up within 24 hours"

    if outcome == "Thinking":
        return "📩 Send additional information and follow up"

    if outcome == "Call Later":
        return "📅 Schedule another follow-up call"

    if outcome == "No Response":
        return "🔄 Retry contact within 24 hours"

    if outcome == "Not Interested":
        return "💤 Reduce priority and stop active follow-ups"

    return get_recommended_action(lead)


def get_lead_insight(lead):

    if lead["purchase"] == "Yes":
        return "💰 This lead has already converted. Focus on retention and referrals."

    if lead["zoom_attended"] == "Yes":
        return "🔥 High-intent lead. Follow up and focus on closing the purchase."

    if lead["zoom_invited"] == "Yes":
        return "🎯 Lead has been invited to Zoom. Encourage attendance and answer objections."

    if lead["number_saved"] == "Yes":
        return "📱 Lead has shown initial interest. Move them toward a Zoom conversation."

    return "🆕 New lead. Start qualification and understand their needs."


def get_priority_reason(lead):

    if lead["purchase"] == "Yes":
        return "💰 Converted lead — highest priority due to completed purchase."

    if lead["zoom_attended"] == "Yes":
        return "🔥 High intent — lead attended the Zoom meeting."

    if lead["zoom_invited"] == "Yes":
        return "🎯 Strong interest — lead has been invited to Zoom."

    if lead["number_saved"] == "Yes":
        return "📱 Initial interest shown — lead saved the number."

    return "🆕 New lead — qualification is still required."

def get_conversion_bottleneck(lead):

    if lead["purchase"] == "Yes":
        return "💰 Already Converted"

    if lead["number_saved"] != "Yes":
        return "📱 Contact not established"

    if lead["zoom_invited"] != "Yes":
        return "📅 Zoom invitation is the next step"

    if lead["zoom_attended"] != "Yes":
        return "🎥 Zoom attendance is the bottleneck"

    outcome = str(
        lead.get("follow_up_outcome", "")
    ).strip()

    if outcome == "Thinking":
        return "🤔 Lead is still considering"

    if outcome == "No Response":
        return "📞 Lead is not responding"

    if outcome == "Not Interested":
        return "💤 Lead currently shows low interest"

    if outcome == "Call Later":
        return "📅 Follow-up call required"

    return "🔥 Lead is close to conversion"

def get_ai_recommendation(lead):

    if lead["purchase"] == "Yes":
        return "🎉 Lead converted. Focus on customer retention and referrals."

    outcome = str(
        lead.get("follow_up_outcome", "")
    ).strip()

    if outcome == "Interested":
        return "🔥 High opportunity. Follow up within 24 hours and move toward conversion."

    if outcome == "Thinking":
        return "🤔 Lead needs more confidence. Send useful information and schedule a follow-up."

    if outcome == "Call Later":
        return "📅 Respect the requested timing and schedule the next call."

    if outcome == "No Response":
        return "🔄 Retry contact and use a different approach or channel."

    if outcome == "Not Interested":
        return "💤 Reduce active follow-ups and revisit this lead later."

    if lead["zoom_attended"] == "Yes":
        return "🔥 Strong conversion opportunity. Follow up and focus on closing the purchase."

    if lead["zoom_invited"] == "Yes":
        return "🎯 Encourage Zoom attendance and resolve any objections."

    if lead["number_saved"] == "Yes":
        return "📅 Move the lead toward a Zoom conversation."

    return "👋 Start qualification and understand the lead's needs."

def get_lead_summary(lead):

    name = str(lead.get("name", "This lead"))

    score = lead.get("score", 0)

    priority = str(
        lead.get("priority", "")
    )

    stage = str(
        lead.get("lead_stage", "")
    )

    bottleneck = str(
        lead.get("conversion_bottleneck", "")
    )

    recommendation = str(
        lead.get("ai_recommendation", "")
    )

    return (
        f"👤 {name} has a lead score of {score} "
        f"and is classified as {priority}. "
        f"Current stage: {stage}. "
        f"Main bottleneck: {bottleneck}. "
        f"Recommendation: {recommendation}"
    )

def get_lead_summary(lead):

    name = str(lead.get("name", "This lead"))
    score = lead.get("score", 0)

    priority = str(
        lead.get("priority", "")
    )

    stage = str(
        lead.get("lead_stage", "")
    )

    bottleneck = str(
        lead.get("conversion_bottleneck", "")
    )

    recommendation = str(
        lead.get("ai_recommendation", "")
    )

    return (
        f"👤 {name} has a lead score of {score} "
        f"and is classified as {priority}. "
        f"Current stage: {stage}. "
        f"Main bottleneck: {bottleneck}. "
        f"Recommendation: {recommendation}"
    )