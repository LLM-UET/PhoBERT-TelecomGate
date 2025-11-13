import click

@click.group()
def cli():
    pass

@cli.command()
def segment():
    from .SEGMENT import do_SEGMENT
    do_SEGMENT()

@cli.group()
def download():
    pass

@download.command(name="models")
def download_models():
    from .DOWNLOAD_MODELS import do_DOWNLOAD_MODELS
    do_DOWNLOAD_MODELS()

if __name__ == "__main__":
    cli()
