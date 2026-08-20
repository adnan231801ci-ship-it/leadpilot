import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def generate_lead_recommendation(lead):
    prompt = f"""
You are LeadPilot, an AI sales assistant.

Analyze this lead and give a practical recommendation.

Lead name: {lead.get("name", "")}
Source: {lead.get("source", "")}
Qualification: {lead.get("qualification", "")}
Lead score: {lead.get("score", "")}
Priority: {lead.get("priority", "")}
Lead stage: {lead.get("lead_stage", "")}
Number saved: {lead.get("number_saved", "")}
Zoom invited: {lead.get("zoom_invited", "")}
Zoom attended: {lead.get("zoom_attended", "")}
Purchase: {lead.get("purchase", "")}
Last interaction: {lead.get("last_interaction", "")}
Follow-up outcome: {lead.get("follow_up_outcome", "")}

Give your response in this format:

WHY:
NEXT ACTION:
TIMING:
MESSAGE:

Keep the response concise and practical.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result.get(
            "response",
            "No AI recommendation generated."
        ).strip()

    except Exception as e:
        return f"Local AI unavailable: {e}"