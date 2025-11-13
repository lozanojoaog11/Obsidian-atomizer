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
@click.option('--verbose', is_flag=True, help='Verbose output')
def process(input_path, vault, verbose):
    """
    Process file through complete pipeline (Extract → Classify → Destill → Connect).

    Examples:
        cerebrum process paper.pdf
        cerebrum process inbox/article.md --vault ~/my-vault
        cerebrum process file.pdf --verbose
    """
    console.print("\n[bold cyan]🧠 Cerebrum - Knowledge Refinement Pipeline[/bold cyan]\n")

    input_path = Path(input_path)
    vault_path = Path(vault) if vault else Path.cwd()

    # Initialize LLM
    try:
        console.print("🔌 Initializing LLM service...")
        llm = LLMService.create_default()
        console.print(f"[green]✓[/green] Using {llm.provider} ({llm.model})\n")
    except Exception as e:
        console.print(f"[red]✗ LLM initialization failed:[/red] {str(e)}\n")
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

        # Display results
        if result.success:
            console.print(f"\n[green]✓ Successfully processed {input_path.name}[/green]\n")
            console.print(f"📝 Notes created: {len(result.permanent_notes) + 1}")
            console.print(f"   • 1 literature note")
            console.print(f"   • {len(result.permanent_notes)} permanent notes")
            console.print(f"\n🔗 Links created: {result.links_created}")
            console.print(f"   • Avg links/note: {result.stats.get('avg_links_per_note', 0):.1f}")
            console.print(f"\n⏱️  Time: {result.duration_seconds:.1f}s\n")

            # Show note titles
            if result.permanent_notes:
                console.print("[bold]Permanent notes:[/bold]")
                for note in result.permanent_notes[:10]:  # Show first 10
                    console.print(f"  • [cyan]{note.metadata.title}[/cyan]")
                if len(result.permanent_notes) > 10:
                    console.print(f"  ... and {len(result.permanent_notes) - 10} more\n")
        else:
            console.print(f"\n[red]✗ Processing failed[/red]\n")
            for error in result.errors:
                console.print(f"  • {error}")
            console.print()

    else:
        # Directory
        pattern = "*.pdf"
        files = list(input_path.glob(pattern))

        if not files:
            console.print(f"[yellow]No {pattern} files found in {input_path}[/yellow]\n")
            return

        console.print(f"Found {len(files)} files to process\n")

        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Processing...", total=len(files))

            for file_path in files:
                progress.update(task, description=f"Processing {file_path.name}...")
                result = orchestrator.process(file_path)
                results.append(result)
                progress.advance(task)

        # Batch summary
        succeeded = sum(1 for r in results if r.success)
        failed = len(results) - succeeded
        total_notes = sum(1 + len(r.permanent_notes) for r in results)
        total_links = sum(r.links_created for r in results)
        total_time = sum(r.duration_seconds for r in results)

        console.print(f"\n[green]✓ Batch processing complete[/green]\n")
        console.print(f"📁 Files: {len(results)} processed")
        console.print(f"   • [green]{succeeded} succeeded[/green]")
        if failed > 0:
            console.print(f"   • [red]{failed} failed[/red]")
        console.print(f"\n📝 Notes created: {total_notes}")
        console.print(f"🔗 Links created: {total_links}")
        console.print(f"⏱️  Total time: {total_time:.1f}s\n")


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
