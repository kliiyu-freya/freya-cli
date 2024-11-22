import click
import re

from freya_cli.composer import run_compose, stop_compose, restart_compose
from freya_cli.package_manager import PackageManager, Package

package_manager = PackageManager()

@click.group()
def cli():
    """Freya CLI main group."""
    pass

@click.command(name="run")
def run():
    """Run Freya."""
    click.echo("Starting Freya...")
    run_compose()
    
@click.command(name="stop")
def stop():
    """Stop Freya."""
    click.echo("Stopping Freya...")
    stop_compose()
    
@click.command(name="restart")
def restart():
    """Restart Freya."""
    click.echo("Restarting Freya...")
    restart_compose()
    
@click.command(name="version")
def version():
    """Display the version of the Freya CLI."""
    click.echo("Freya CLI version 0.1.0")

@click.command(name="status")
def status(status):
    """Display the status of the Freya CLI."""
    if status:
        click.echo("Freya CLI is up and running. All systems go!")

@click.command(name="install")
@click.argument('package_name', type=str, required=True)
def install(package_name: str):
    """Install a package. 'freya install <name>:<version>'"""
    name = package_name.split(":")[0]
    
    no_version_specified = lambda: (click.echo("No version specified, installing latest version."), "latest")[1]
    
    try:
        version = package_name.split(":")[1]
    except IndexError:
        version = no_version_specified()
    if version.strip() == "": 
        version = no_version_specified()
    if not re.match(r'^[a-zA-Z0-9.]+$', version):
        version = no_version_specified()
    
    click.echo(f"Installing package: {name}, version: {version}")

    package = Package(name, version)
    output = package_manager.add_package(package=package)
    click.echo(output)
    
@click.command(name="uninstall")
@click.argument('package_name', type=str, required=True)
def uninstall(package_name: str):
    """Uninstall a package. uninstall <name>"""
    click.echo(f"Uninstalling package: {package_name}")
    output = package_manager.remove_package(package_name)
    click.echo(output)
    
@click.command(name="list")
def list():
    """List all installed packages."""
    click.echo("Listing all installed packages...")
    package_manager.list_packages()

# Register commands with the group
cli.add_command(run)
cli.add_command(stop)
cli.add_command(restart)
cli.add_command(version)
cli.add_command(status)
cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(list)

if __name__ == '__main__':
    cli()
