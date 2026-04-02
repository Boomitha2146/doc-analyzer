"""
Quick smoke-test: run against localhost or your deployed URL.

Usage:
    pip install requests
    python tests/test_api.py --url http://localhost:8000 --key hackathon-key-2024 --file sample.pdf
"""
import argparse
import json
import sys
import requests


def test_health(base_url: str):
    r = requests.get(f"{base_url}/health", timeout=10)
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("✓ Health check passed")


def test_analyze(base_url: str, api_key: str, filepath: str):
    headers = {"X-API-Key": api_key}
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f)}
        r = requests.post(f"{base_url}/analyze", headers=headers, files=files, timeout=60)

    if r.status_code != 200:
        print(f"✗ /analyze failed ({r.status_code}): {r.text}")
        sys.exit(1)

    data = r.json()
    print("\n✓ /analyze succeeded")
    print(f"  File type   : {data['file_type']}")
    print(f"  Summary     : {data['summary'][:120]}…")
    print(f"  Sentiment   : {data['sentiment']['label']} (score={data['sentiment']['score']})")
    print(f"  Persons     : {data['entities'].get('persons', [])}")
    print(f"  Orgs        : {data['entities'].get('organisations', [])}")
    print(f"  Dates       : {data['entities'].get('dates', [])}")
    print(json.dumps(data, indent=2))


def test_auth_rejection(base_url: str):
    r = requests.post(f"{base_url}/analyze", headers={"X-API-Key": "wrong"}, timeout=10)
    assert r.status_code == 403, f"Expected 403, got {r.status_code}"
    print("✓ Auth rejection works correctly")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--key", default="hackathon-key-2024")
    parser.add_argument("--file", required=True, help="Path to PDF/DOCX/image file")
    args = parser.parse_args()

    test_health(args.url)
    test_auth_rejection(args.url)
    test_analyze(args.url, args.key, args.file)
