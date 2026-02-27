"""
cli_app.py
----------
Interactive terminal interface for the Medical Expert System.
Uses the 'rich' library for colored, formatted output.

Usage:
    python ui/cli_app.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.text import Text
from rich import box

from core.knowledge_base import KnowledgeBase
from core.working_memory import WorkingMemory
from core.inference_engine import InferenceEngine
from core.explanation import ExplanationModule

console = Console()

# ── Load symptom display labels ──────────────

def load_symptom_labels() -> dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "diseases.json")
    with open(path) as f:
        data = json.load(f)
    return data["symptoms_display"]


# ── Severity colors ──────────────────────────

SEV_STYLE = {
    "low"      : "bold green",
    "medium"   : "bold yellow",
    "high"     : "bold red",
    "critical" : "bold magenta",
}


# ── Header ───────────────────────────────────

def print_header():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]🏥  MEDICAL EXPERT SYSTEM[/bold cyan]\n"
        "[dim]Rule-Based Diagnostic Assistant for Fever-Related Diseases[/dim]\n"
        "[dim]Diseases: Common Flu | Dengue | Malaria | Typhoid[/dim]",
        border_style="cyan",
        padding=(1, 4)
    ))
    console.print(
        "\n[bold yellow]⚠  DISCLAIMER:[/bold yellow] "
        "[dim]This system is for educational purposes only. "
        "Always consult a qualified doctor for medical advice.[/dim]\n"
    )


# ── Collect Patient Info ─────────────────────

def collect_patient_info(wm: WorkingMemory):
    console.print("[bold cyan]── Patient Information ──────────────────[/bold cyan]")

    name = Prompt.ask("  Patient name", default="Anonymous")
    age  = Prompt.ask("  Age")
    temp = Prompt.ask("  Body temperature (°F)", default="Unknown")
    days = Prompt.ask("  How many days have symptoms lasted?", default="1")

    wm.set_patient_info("name", name)
    wm.set_patient_info("age", age)
    wm.set_patient_info("temperature_f", temp)
    wm.set_patient_info("illness_duration_days", days)

    console.print()


# ── Display Symptom Menu ─────────────────────

def display_symptom_menu(symptom_labels: dict) -> list:
    """Show all available symptoms in a simple numbered list."""
    console.print("[bold cyan]── Available Symptoms ───────────────────[/bold cyan]")
    console.print("[dim]Enter symptom numbers separated by commas (e.g. 1,3,7,12)[/dim]\n")

    symptoms_list = list(symptom_labels.items())  # [(key, display), ...]

    for i, (key, label) in enumerate(symptoms_list, 1):
        console.print(f"  [dim]{i:>2}.[/dim]  {label}")

    console.print()
    return symptoms_list


# ── Collect Symptoms ─────────────────────────

def collect_symptoms(wm: WorkingMemory, symptom_labels: dict):
    symptoms_list = display_symptom_menu(symptom_labels)

    while True:
        raw = Prompt.ask(
            "  [bold green]Enter symptom numbers[/bold green]"
        ).strip()

        if not raw:
            console.print("[red]  Please enter at least one symptom number.[/red]")
            continue

        selected_indices = []
        valid = True

        for part in raw.split(","):
            part = part.strip()
            if not part.isdigit():
                console.print(f"[red]  '{part}' is not a valid number. Try again.[/red]")
                valid = False
                break
            idx = int(part) - 1
            if idx < 0 or idx >= len(symptoms_list):
                console.print(f"[red]  Number {int(part)} is out of range. Try again.[/red]")
                valid = False
                break
            selected_indices.append(idx)

        if not valid:
            continue

        # Add selected symptoms to working memory
        selected_symptoms = []
        for idx in selected_indices:
            key, label = symptoms_list[idx]
            wm.add_symptom(key)
            selected_symptoms.append(label)

        # Confirm selection
        console.print("\n[bold cyan]── You selected these symptoms: ─────────[/bold cyan]")
        for s in selected_symptoms:
            console.print(f"  [green]✓[/green]  {s}")

        console.print()
        confirm = Confirm.ask("  Confirm and run diagnosis?", default=True)

        if confirm:
            break
        else:
            # Let them re-enter
            wm.clear_symptoms()
            console.print("\n[yellow]  Cleared. Please re-enter your symptoms.[/yellow]\n")


# ── Display Results ──────────────────────────

def display_results(results: list, wm: WorkingMemory):
    if not results:
        console.print(Panel(
            "[bold red]No diagnosis could be made.[/bold red]\n"
            "[dim]Too few or unrecognized symptoms were entered.\n"
            "Please consult a doctor directly.[/dim]",
            border_style="red",
            title="Result"
        ))
        return

    console.print()
    console.print(Panel(
        f"[bold cyan]Diagnosis Results for: "
        f"[white]{wm.get_patient_info('name', 'Patient')}[/white][/bold cyan]\n"
        f"[dim]Age: {wm.get_patient_info('age', 'N/A')}  |  "
        f"Temp: {wm.get_patient_info('temperature_f', 'N/A')}°F  |  "
        f"Duration: {wm.get_patient_info('illness_duration_days', 'N/A')} day(s)[/dim]",
        border_style="cyan",
        title="🏥 Patient Report"
    ))

    # ── Results table ────────────────────────
    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        title="[bold]Ranked Diagnoses[/bold]",
        title_style="bold white"
    )
    table.add_column("Rank",        style="dim",        width=6)
    table.add_column("Disease",     style="bold white", width=28)
    table.add_column("Confidence",  style="cyan",       width=12)
    table.add_column("Likelihood",  width=22)
    table.add_column("Severity",    width=12)

    for i, r in enumerate(results, 1):
        rank_str = f"#{i}"
        bar_len  = int(r.confidence / 5)
        bar      = "█" * bar_len + "░" * (20 - bar_len)
        sev_style = SEV_STYLE.get(r.severity, "white")
        conf_str  = f"{r.confidence:.1f}%"

        table.add_row(
            rank_str,
            r.display_name,
            conf_str,
            bar,
            Text(r.severity.upper(), style=sev_style)
        )

    console.print(table)

    # ── Top diagnosis detail ─────────────────
    top = results[0]
    sev_style = SEV_STYLE.get(top.severity, "white")

    console.print()
    console.print(Panel(
        f"[bold white]{top.display_name}[/bold white]  "
        f"[cyan]({top.confidence:.1f}% confidence)[/cyan]\n\n"
        f"[dim]{top.description}[/dim]\n\n"
        f"[bold]Severity:[/bold] [{sev_style}]{top.severity.upper()}[/{sev_style}]\n\n"
        f"[bold yellow]Recommended Action:[/bold yellow]\n"
        f"  {top.recommended_action}",
        border_style="green",
        title="[bold green]Top Diagnosis[/bold green]",
        padding=(1, 2)
    ))

    # ── Ask to show explanation ──────────────
    console.print()
    show_exp = Confirm.ask(
        "  Show detailed explanation (which rules fired and why)?",
        default=True
    )

    if show_exp:
        display_explanation(top, wm)


# ── Display Explanation ──────────────────────

def display_explanation(result, wm: WorkingMemory):
    console.print()
    console.print(Panel(
        f"[bold cyan]Why was [white]{result.display_name}[/white] diagnosed?[/bold cyan]",
        border_style="cyan",
        title="🔍 Explanation"
    ))

    exp = ExplanationModule(result, wm.get_all_symptoms())

    console.print(f"\n  [bold]Rules that fired ({len(result.fired_rules)}):[/bold]\n")

    for i, rule in enumerate(result.fired_rules, 1):
        console.print(
            f"  [bold cyan][{rule.rule_id}][/bold cyan]  "
            f"[yellow]{rule.explanation}[/yellow]"
        )
        console.print(
            f"         Matched symptoms : [green]{', '.join(rule.matched_conditions)}[/green]"
        )
        console.print(
            f"         Confidence added : [cyan]+{rule.confidence_boost}[/cyan]"
        )
        console.print()

    console.print(
        f"  [bold]All contributing symptoms:[/bold] "
        f"[green]{', '.join(result.matched_symptoms)}[/green]"
    )
    console.print()


# ── Main Loop ────────────────────────────────

def main():
    symptom_labels = load_symptom_labels()
    kb = KnowledgeBase()

    while True:
        print_header()

        wm = WorkingMemory()

        # Step 1: Patient info
        collect_patient_info(wm)

        # Step 2: Collect symptoms
        collect_symptoms(wm, symptom_labels)

        # Step 3: Run inference
        console.print("\n[bold cyan]  Running diagnosis...[/bold cyan]\n")
        engine = InferenceEngine(kb, wm)
        results = engine.run()

        # Step 4: Display results
        display_results(results, wm)

        # Step 5: Ask to diagnose another patient
        console.print()
        again = Confirm.ask("  Diagnose another patient?", default=False)
        if not again:
            console.print(
                "\n[bold cyan]  Thank you for using the Medical Expert System. "
                "Stay healthy! 🏥[/bold cyan]\n"
            )
            break


if __name__ == "__main__":
    main()