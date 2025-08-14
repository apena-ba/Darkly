import os
import signal
import sys
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn

visited = set()
console = Console()


# Ctrl+C handler
def sigint_handler(sig, frame):
    console.print()
    log("Interrupted by user. Exiting", positive=False)
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def log(message, positive=True):
    """Custom logging with colored [+]/[-] and line separation."""
    icon = "[green]+[/]" if positive else "[red]-[/]"
    console.print()  # Blank line before log
    console.print(f"{icon} {message}")


def sanitize_path(url, base_url, dump_dir):
    parsed = urlparse(url)
    path = parsed.path.replace(base_url, "").lstrip("/")
    return os.path.join(dump_dir, path)


def download_file(url, base_url, dump_dir, verbose=False):
    local_path = sanitize_path(url, base_url, dump_dir)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(r.content)
            if verbose:
                log(f"Downloaded: {url}", positive=True)
    except Exception as e:
        log(f"Failed to download {url}: {e}", positive=False)


def collect_files(url, base_url):
    """Recursively collect all file URLs."""
    if url in visited:
        return []
    visited.add(url)

    try:
        r = requests.get(url)
        if r.status_code != 200:
            return []
    except Exception:
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    files = []

    for link in links:
        href = link.get('href')
        if not href or href in ('../', '/'):
            continue
        full_url = urljoin(url, href)
        if full_url.endswith('/'):
            files.extend(collect_files(full_url, base_url))
        else:
            files.append(full_url)

    return files


def validate_or_create_dump_dir(path):
    """Ensure dump directory exists and is writable."""
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
    parser = argparse.ArgumentParser(description="Recursive web directory crawler with rich progress bar.")
    parser.add_argument("url", help="Base URL to start crawling from")
    parser.add_argument("directory", help="Directory where files will be saved (mandatory)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    validate_or_create_dump_dir(args.directory)

    log(f"Starting crawl at: {args.url}", positive=True)

    # Keep spinner until files are collected
    console.print()  # Blank line before spinner
    with Progress(
        SpinnerColumn(),
        "[cyan]Collecting file list...",
        console=console,
    ) as progress:
        task = progress.add_task("", total=None)
        file_list = collect_files(args.url, args.url)
        total_files = len(file_list)
        progress.remove_task(task)  # Stop spinner
        console.print(f"[yellow]{total_files} files found[/]")

    # Download progress bar
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Downloading files", total=total_files)

        for file_url in file_list:
            download_file(file_url, args.url, args.directory, args.verbose)
            progress.update(task, advance=1)

    log("Crawl complete!", positive=True)
    console.print()


if __name__ == "__main__":
    main()
