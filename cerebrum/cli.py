#!/usr/bin/env python3
"""
Cerebrum CLI - Your Personal Knowledge Refinement Tool
"""

import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from cerebrum.core.orchestrator import Orchestrator
from cerebrum.services.llm_service import LLMService
from cerebrum.utils.config import Config

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """🧠 Cerebrum - Personal Knowledge Refinement System"""
    pass


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--vault', '-v', type=click.Path(), help='Vault path (default: current dir)')
@click.option('--verbose', is_flag=True, help='Show detailed processing steps')
def process(input_path, vault, verbose):
    """
    Transform documents into atomic notes with semantic connections.

    Simply point to a file or folder - Cerebrum handles the rest.

    Examples:
        cerebrum process paper.pdf
        cerebrum process inbox/ --vault ~/my-vault
        cerebrum process paper.pdf --verbose
    """
    console.print("\n[bold]🧠 Cerebrum[/bold] [dim]· It just works, beautifully[/dim]\n")

    input_path = Path(input_path)
    vault_path = Path(vault) if vault else Path.cwd()

    # Initialize LLM (quietly unless verbose)
    try:
        if verbose:
            console.print("🔌 Initializing AI...")
        llm = LLMService.create_default()
        if verbose:
            console.print(f"[green]✓[/green] Using {llm.provider} ({llm.model})\n")
        elif not verbose:
            console.print(f"[dim]Using {llm.provider} ({llm.model})[/dim]\n")
    except Exception as e:
        console.print(f"[red]✗[/red] Could not initialize AI: {str(e)}")
        console.print("\n[dim]Need help? Try:[/dim]")
        console.print("  • ollama serve && ollama pull llama3.2")
        console.print("  • export GEMINI_API_KEY=your-key\n")
        return

    # Initialize orchestrator
    orchestrator = Orchestrator(llm, vault_path, verbose=verbose)

    # Process
    if input_path.is_file():
        # Single file
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Processing {input_path.name}...", total=None)

            result = orchestrator.process(input_path)

            progress.update(task, completed=True)

        # Display results with Apple-style simplicity
        if result.success:
            console.print(f"\n[green bold]✓ Done[/green bold] [dim]· {input_path.name}[/dim]\n")

            # Clean, minimal stats
            console.print(f"[bold]{len(result.permanent_notes) + 1}[/bold] atomic notes  [dim]·[/dim]  [bold]{result.links_created}[/bold] connections  [dim]·[/dim]  {result.duration_seconds:.0f}s\n")

            # Show concepts extracted (first 8)
            if result.permanent_notes and verbose:
                console.print("[dim]Concepts extracted:[/dim]")
                for note in result.permanent_notes[:8]:
                    console.print(f"  · {note.metadata.title}")
                if len(result.permanent_notes) > 8:
                    console.print(f"  [dim]· {len(result.permanent_notes) - 8} more[/dim]")
                console.print()
        else:
            console.print(f"\n[red]✗ Failed[/red] [dim]· {input_path.name}[/dim]\n")
            if verbose:
                for error in result.errors:
                    console.print(f"  [dim]·[/dim] {error}")
                console.print()
            else:
                console.print("[dim]Run with --verbose to see details[/dim]\n")

    else:
        # Directory
        pattern = "*.pdf"
        files = list(input_path.glob(pattern))

        if not files:
            console.print(f"[dim]No PDF files found in {input_path}[/dim]\n")
            return

        console.print(f"[dim]Processing {len(files)} files...[/dim]\n")

        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("", total=len(files))

            for file_path in files:
                progress.update(task, description=f"{file_path.name}")
                result = orchestrator.process(file_path)
                results.append(result)
                progress.advance(task)

        # Batch summary - Apple-style clean
        succeeded = sum(1 for r in results if r.success)
        failed = len(results) - succeeded
        total_notes = sum(1 + len(r.permanent_notes) for r in results)
        total_links = sum(r.links_created for r in results)
        total_time = sum(r.duration_seconds for r in results)

        if failed == 0:
            console.print(f"\n[green bold]✓ Done[/green bold] [dim]· {len(results)} files[/dim]\n")
        else:
            console.print(f"\n[yellow bold]⚠ Completed with issues[/yellow bold] [dim]· {succeeded} succeeded, {failed} failed[/dim]\n")

        console.print(f"[bold]{total_notes}[/bold] atomic notes  [dim]·[/dim]  [bold]{total_links}[/bold] connections  [dim]·[/dim]  {total_time:.0f}s\n")


@cli.command()
@click.argument('note_path', type=click.Path(exists=True), required=False)
@click.option('--all', '-a', is_flag=True, help='Analyze entire vault')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.option('--threshold', '-t', default=0.75, help='Similarity threshold')
def link(note_path, all, interactive, threshold):
    """
    Suggest semantic links between notes.

    Examples:
        cerebrum link note.md
        cerebrum link --all --threshold 0.8
        cerebrum link --interactive
    """
    console.print("\n[bold cyan]🔗 Cerebrum Linker[/bold cyan]\n")
    console.print("[yellow]Coming soon![/yellow]\n")


@cli.command()
@click.option('--dashboard', '-d', is_flag=True, help='Generate dashboard')
@click.option('--orphans', is_flag=True, help='Find orphan notes')
def curate(dashboard, orphans):
    """
    Curate and maintain vault health.

    Examples:
        cerebrum curate
        cerebrum curate --dashboard > health.md
        cerebrum curate --orphans
    """
    console.print("\n[bold cyan]🧹 Cerebrum Curator[/bold cyan]\n")
    console.print("[yellow]Coming soon![/yellow]\n")


@cli.command()
@click.option('--recent', '-r', default=30, help='Analyze recent N notes')
@click.option('--tag', help='Filter by tag')
def synthesize(recent, tag):
    """
    Detect patterns and generate emergent insights.

    Examples:
        cerebrum synthesize --recent 30
        cerebrum synthesize --tag neuroscience
    """
    console.print("\n[bold cyan]🔮 Cerebrum Synthesizer[/bold cyan]\n")
    console.print("[yellow]Coming soon![/yellow]\n")


@cli.command()
@click.option('--vault', type=click.Path(), help='Vault path')
def init(vault):
    """Initialize Cerebrum in your vault."""
    console.print("\n[bold cyan]🚀 Initializing Cerebrum[/bold cyan]\n")

    vault_path = Path(vault) if vault else Path.cwd()

    # Create structure
    (vault_path / '.cerebrum').mkdir(exist_ok=True)
    (vault_path / '.cerebrum' / 'templates').mkdir(exist_ok=True)
    (vault_path / '.cerebrum' / 'embeddings.db').touch()

    # Create default config
    config_path = vault_path / '.cerebrum' / 'config.yaml'
    if not config_path.exists():
        Config.create_default(config_path)
        console.print(f"[green]✓[/green] Created config: {config_path}")

    # Create vault structure
    for folder in ['00-Inbox', '03-Permanent', '04-MOCs', '99-Meta']:
        (vault_path / folder).mkdir(exist_ok=True)
        console.print(f"[green]✓[/green] Created folder: {folder}")

    console.print(f"\n[green]✓ Cerebrum initialized in {vault_path}[/green]\n")
    console.print("Next steps:")
    console.print("  1. Review config: .cerebrum/config.yaml")
    console.print("  2. Install Ollama: https://ollama.ai")
    console.print("  3. Pull model: ollama pull llama3.2")
    console.print("  4. Start using: cerebrum distill 00-Inbox/\n")


if __name__ == '__main__':
    cli()
