import os
from openai import OpenAI


def get_ai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)

def generate_ai_recommendation(lead):
    client = get_ai_client()

    if client is None:
        return "⚠️ AI is not configured."

    prompt = f"""
You are LeadPilot, an AI lead-conversion assistant.

Analyze this lead:

Name: {lead.get("name", "")}
Source: {lead.get("source", "")}
Qualification: {lead.get("qualification", "")}
Lead Score: {lead.get("score", "")}
Priority: {lead.get("priority", "")}
Stage: {lead.get("lead_stage", "")}
Number Saved: {lead.get("number_saved", "")}
Zoom Invited: {lead.get("zoom_invited", "")}
Zoom Attended: {lead.get("zoom_attended", "")}
Purchase: {lead.get("purchase", "")}
Last Interaction: {lead.get("last_interaction", "")}
Follow-Up Outcome: {lead.get("follow_up_outcome", "")}
Conversion Bottleneck: {lead.get("conversion_bottleneck", "")}

Give a concise recommendation for the entrepreneur.

Return exactly these four sections:

WHY:
Explain why this lead deserves attention.

NEXT ACTION:
Give the single best action to take next.

MESSAGE:
Write a short WhatsApp-style message the entrepreneur can send.

TIMING:
Say when the entrepreneur should take the action.
"""

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        return f"⚠️ AI error: {str(e)}"