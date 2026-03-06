# ClearSec

AI-powered Microsoft 365 security analysis tool. Pulls your Secure Score from the Microsoft Graph API, normalizes the data with Pydantic models, and uses Claude to generate prioritized remediation recommendations ranked by risk-to-effort ratio.

## What it does

- Authenticates to Microsoft Graph using app credentials (client credentials flow)
- Fetches your tenant's current Secure Score and all control scores
- Parses and validates the data with Pydantic models
- Sends failing controls to Claude (Sonnet) for analysis
- Outputs a prioritized remediation report — highest impact, lowest effort first
- Optionally saves the report to a markdown file

## Requirements

- Python 3.9+
- Microsoft 365 tenant with an app registration
- Anthropic API key

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/clearsec.git
cd clearsec
```

### 2. Install dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Create an app registration in Entra

1. Go to [Entra Admin Center](https://entra.microsoft.com) > App registrations > New registration
2. Name it `clearsec`, single tenant, no redirect URI
3. Under API permissions > Add a permission > Microsoft Graph > Application permissions, add:
   - `SecurityEvents.Read.All`
   - `SecurityActions.Read.All`
   - `SecurityAlert.Read.All`
4. Grant admin consent
5. Go to Certificates & secrets > New client secret, copy the value immediately

### 4. Configure credentials

Create a `.env` file in the project root:

```
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
ANTHROPIC_API_KEY=your-anthropic-api-key
```

> ⚠️ Never commit `.env` to version control. It is included in `.gitignore`.

## Usage

Run a security analysis and print to terminal:

```bash
python3 main.py
```

Save the report to a markdown file:

```bash
python3 main.py --output report.md
```

## Example Output

```
Fetching Secure Score from Microsoft Graph...
Current Score: 53.0/64.0
Failing Controls: 6

Analyzing with Claude...

# Microsoft 365 Secure Score Remediation Report
**Current Score: 53.0/64.0 | Active Users: 3 | Failing Controls: 6**

## PRIORITY 1 - CRITICAL (High Risk, Low Effort)

### 1. IntegratedApps - User Consent Policy
- Risk Level: HIGH
- Effort to Fix: LOW
...
```

## Project Structure

```
clearsec/
├── clearsec/
│   ├── auth.py        # MSAL authentication, token acquisition
│   ├── graph.py       # Microsoft Graph API calls
│   ├── models.py      # Pydantic models for Secure Score data
│   ├── analyze.py     # Claude integration and prompt logic
│   └── cli.py         # Typer CLI definition
├── main.py            # Entrypoint
├── requirements.txt
└── .env               # Credentials (not committed)
```

## Tech Stack

- [MSAL](https://github.com/AzureAD/microsoft-authentication-library-for-python) — Microsoft authentication
- [httpx](https://www.python-httpx.org/) — HTTP client for Graph API calls
- [Pydantic](https://docs.pydantic.dev/) — Data validation and modeling
- [Anthropic Python SDK](https://github.com/anthropic/anthropic-sdk-python) — Claude integration
- [Typer](https://typer.tiangolo.com/) — CLI framework

## License

MIT
