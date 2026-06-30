"""
MedScribe CLI - Command-line client for the MedScribe API.

Usage:
    python medscribe_cli.py health
    python medscribe_cli.py upload <path_to_image>
    python medscribe_cli.py records
"""

import argparse
import sys
import json
import requests

DEFAULT_BASE_URL = "https://medscribe-deploy.onrender.com"


def cmd_health(args):
    """Check API health status."""
    url = f"{args.base_url}/health"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        print(json.dumps(resp.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach {url}\n{e}", file=sys.stderr)
        sys.exit(1)


def cmd_upload(args):
    """Upload a prescription/lab report image for OCR + extraction."""
    url = f"{args.base_url}/upload"
    try:
        with open(args.file, "rb") as f:
            files = {"file": (args.file, f)}
            print(f"Uploading {args.file} to {url} ...")
            resp = requests.post(url, files=files, timeout=120)
        if resp.status_code == 200:
            print("Success:")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"Server returned status {resp.status_code}:")
            print(resp.text)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: request failed\n{e}", file=sys.stderr)
        sys.exit(1)


def cmd_records(args):
    """List all processed medical records."""
    url = f"{args.base_url}/records"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        records = resp.json()
        if not records:
            print("No records found.")
        else:
            print(json.dumps(records, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach {url}\n{e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="MedScribe CLI - interact with the MedScribe API from your terminal."
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base URL (default: {DEFAULT_BASE_URL})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_health = subparsers.add_parser("health", help="Check API health status")
    p_health.set_defaults(func=cmd_health)

    p_upload = subparsers.add_parser("upload", help="Upload a prescription/lab report image")
    p_upload.add_argument("file", help="Path to image file (jpg, png, or pdf)")
    p_upload.set_defaults(func=cmd_upload)

    p_records = subparsers.add_parser("records", help="List all processed records")
    p_records.set_defaults(func=cmd_records)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()