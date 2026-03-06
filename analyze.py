import anthropic
from clearsec.models import SecureScoreReport

client = anthropic.Anthropic()

def analyze(report: SecureScoreReport) -> str:
    failing = report.failing_controls

    controls_text = ""
    for c in failing:
        controls_text += f"""
Control: {c.control_name}
Category: {c.control_category}
Score: {c.score_in_percentage}%
Status: {c.implementation_status}
Description: {c.description}
---"""

    prompt = f"""You are a Microsoft 365 security analyst. Analyze the following failing Secure Score controls and provide prioritized remediation recommendations ranked by risk-to-effort ratio (highest impact, lowest effort first).

Tenant Overview:
- Current Score: {report.current_score}/{report.max_score}
- Active Users: {report.active_user_count}
- Failing Controls: {len(failing)}

Failing Controls:
{controls_text}

For each recommendation provide:
1. Control name
2. Risk level (High/Medium/Low)
3. Effort to fix (Low/Medium/High)
4. Specific remediation steps
5. Why it matters

Format as a clear, actionable CLI report."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
