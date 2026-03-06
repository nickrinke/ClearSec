import typer
from typing import Optional
from pathlib import Path
from clearsec.graph import get_secure_scores
from clearsec.models import SecureScoreReport
from clearsec.analyze import analyze

app = typer.Typer(
    name="clearsec",
    help="AI-powered Microsoft 365 security analysis and remediation tool."
)

@app.command()
def scan(
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Save the report to a markdown file (e.g. --output report.md)"
    )
):
    """
    Fetch your Microsoft 365 Secure Score and generate AI-powered remediation recommendations.
    """
    typer.echo("Fetching Secure Score from Microsoft Graph...")
    raw = get_secure_scores()
    report = SecureScoreReport.from_graph(raw["value"][0])
    typer.echo(f"Current Score: {report.current_score}/{report.max_score}")
    typer.echo(f"Failing Controls: {len(report.failing_controls)}")
    typer.echo("\nAnalyzing with Claude...\n")
    recommendations = analyze(report)
    if output:
        output.write_text(recommendations)
        typer.echo(f"\nReport saved to {output}")
    else:
        typer.echo(recommendations)

def main():
    app()
