#!/usr/bin/env python3
"""
Cerebrum CLI - Your Personal Knowledge Refinement Tool
"""

import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from cerebrum.agents.distiller import DistillerAgent
from cerebrum.utils.config import Config

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """🧠 Cerebrum - Personal Knowledge Refinement System"""
    pass


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--template', '-t', default='concept', help='Template to use')
@click.option('--auto', '-a', is_flag=True, help='Auto-process without confirmation')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def distill(input_path, template, auto, output):
    """
    Distill knowledge from PDF, Markdown, or text files.

    Examples:
        cerebrum distill paper.pdf
        cerebrum distill inbox/ --auto
        cerebrum distill article.md --template academic
    """
    console.print("\n[bold cyan]🧠 Cerebrum Distiller[/bold cyan]\n")

    input_path = Path(input_path)

    # Load config
    config = Config.load()

    # Initialize agent
    agent = DistillerAgent(config)

    # Process
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        if input_path.is_file():
            task = progress.add_task(f"Processing {input_path.name}...", total=None)
            notes = agent.process_file(input_path, template=template)
            progress.update(task, completed=True)
        else:
            # Process directory
            files = list(input_path.glob('*'))
            task = progress.add_task(f"Processing {len(files)} files...", total=len(files))
            notes = []
            for file in files:
                if file.suffix in ['.pdf', '.md', '.txt']:
                    progress.update(task, description=f"Processing {file.name}...")
                    notes.extend(agent.process_file(file, template=template))
                    progress.advance(task)

    # Display results
    if notes:
        console.print(f"\n[green]✓[/green] Created {len(notes)} atomic notes:\n")
        for note in notes:
            console.print(f"  • [cyan]{note.title}[/cyan]")
            console.print(f"    → {note.file_path}")

        console.print(f"\n[dim]Total processing time: {agent.elapsed_time:.1f}s[/dim]\n")
    else:
        console.print("[yellow]No notes created.[/yellow]")


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
