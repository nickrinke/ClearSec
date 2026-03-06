import httpx
from clearsec.auth import get_access_token

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def get_headers() -> dict:
    token = get_access_token()
    return {"Authorization": f"Bearer {token}"}

def get_secure_scores() -> dict:
    url = f"{GRAPH_BASE}/security/secureScores?$top=1"
    response = httpx.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def get_security_alerts() -> dict:
    url = f"{GRAPH_BASE}/security/alerts_v2?$top=20"
    response = httpx.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()
