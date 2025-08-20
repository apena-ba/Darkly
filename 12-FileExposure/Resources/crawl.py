import os
import signal
import sys
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn

console = Console()


def log(message, positive=True):
    icon = "[green]+[/]" if positive else "[red]-[/]"
    console.print(f"\n{icon} {message}")


def sigint_handler(sig, frame):
    log("Interrupted by user. Exiting", positive=False)
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def sanitize_path(url, base_url, dump_dir):
    path = urlparse(url).path.replace(base_url, "").lstrip("/")
    return os.path.join(dump_dir, path)


def download_file(url, base_url, dump_dir):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            local_path = sanitize_path(url, base_url, dump_dir)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(r.content)
    except Exception as e:
        log(f"Failed to download {url}: {e}", positive=False)


def collect_files(url, base_url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    files = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href or href in ("../", "/"):
            continue
        full_url = urljoin(url, href)
        files.extend(collect_files(full_url, base_url) if full_url.endswith("/") else [full_url])
    return files


def validate_or_create_dump_dir(path):
    if os.path.exists(path):
        if not os.access(path, os.W_OK):
            log(f"Cannot write to directory: {path}", positive=False)
            sys.exit(1)
    else:
        try:
            os.makedirs(path)
            log(f"Created dump directory: {path}", positive=True)
        except Exception as e:
            log(f"Failed to create directory {path}: {e}", positive=False)
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Recursive web directory crawler")
    parser.add_argument("url", help="Base URL to start crawling from")
    parser.add_argument("directory", help="Directory where files will be saved")
    args = parser.parse_args()

    validate_or_create_dump_dir(args.directory)
    log(f"Starting crawl at: {args.url}\n", positive=True)

    # File pre-loading
    with Progress(SpinnerColumn(), "[cyan]Collecting file list...", console=console) as progress:
        task = progress.add_task("", total=None)
        file_list = collect_files(args.url, args.url)
        progress.remove_task(task)
        console.print(f"[yellow]{len(file_list)} files found[/]")

    # Download progress bar
    with Progress("[progress.description]{task.description}", BarColumn(), "[progress.percentage]{task.percentage:>3.0f}%", console=console) as progress:
        task = progress.add_task("[cyan]Downloading files", total=len(file_list))
        for file_url in file_list:
            download_file(file_url, args.url, args.directory)
            progress.update(task, advance=1)

    log("Crawl complete!\n", positive=True)


if __name__ == "__main__":
    main()
