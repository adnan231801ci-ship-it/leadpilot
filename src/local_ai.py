
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


# ============================================================
# LOCAL AI — LEAD ACTION PLAN
# ============================================================

def generate_lead_recommendation(lead):

    prompt = f"""
You are LeadPilot, an AI sales assistant.

Analyze this lead and create a practical sales action plan.

Lead information:
Name: {lead.get("name", "")}
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
Conversion bottleneck: {lead.get("conversion_bottleneck", "")}

Give your response in exactly this format:

🎯 WHY THIS LEAD:
Briefly explain why this lead should or should not be contacted now.

⚡ NEXT ACTION:
Give ONE specific action the entrepreneur should take.

⏰ TIMING:
Recommend when the lead should be contacted.

💬 MESSAGE:
Write a short, friendly and non-pushy message the entrepreneur can send.

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


# ============================================================
# WHATSAPP MESSAGE GENERATOR
# ============================================================

def generate_whatsapp_message(lead):

    prompt = f"""
You are LeadPilot, an AI sales assistant.

Create a personalized WhatsApp follow-up message for this lead.

Lead information:

Name: {lead.get("name", "")}
Source: {lead.get("source", "")}
Qualification: {lead.get("qualification", "")}
Lead score: {lead.get("score", "")}
Priority: {lead.get("priority", "")}
Lead stage: {lead.get("lead_stage", "")}
Recommended action: {lead.get("recommended_action", "")}
Next action: {lead.get("next_action", "")}
Follow-up outcome: {lead.get("follow_up_outcome", "")}
Follow-up notes: {lead.get("follow_up_notes", "")}
Conversion bottleneck: {lead.get("conversion_bottleneck", "")}

Write ONE short WhatsApp message.

Rules:
- Start naturally using the lead's name.
- Be friendly and professional.
- Do not sound robotic.
- Do not pressure the lead.
- Do not mention lead score, priority, AI, or internal information.
- Do not make unrealistic promises.
- Keep it between 30 and 70 words.
- Use 1-3 suitable emojis.
- Do not include quotation marks.
- Return ONLY the WhatsApp message.
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

        message = result.get(
            "response",
            ""
        ).strip()

        if message:

            return message

        return "Unable to generate WhatsApp message."

    except Exception as e:

        return f"Local AI unavailable: {e}"
