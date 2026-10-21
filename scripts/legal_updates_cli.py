"""Run from project root: python -m scripts.legal_updates_cli <command>"""
import argparse
import json
from app.legal_updates.core import (
    register, list_sources, fetch, fetch_all, ingest_local,
    reviews, review_decision, activate, search_approved,
)


def main():
    parser = argparse.ArgumentParser(description="Legal Intelligence legal update manager")
    commands = parser.add_subparsers(dest="cmd", required=True)
    p = commands.add_parser("register")
    for name in ("id", "url", "domain", "jurisdiction", "title"):
        p.add_argument(name)
    commands.add_parser("sources")
    p = commands.add_parser("fetch")
    p.add_argument("id")
    commands.add_parser("fetch-all")
    p = commands.add_parser("ingest-local")
    p.add_argument("id")
    p.add_argument("path")
    commands.add_parser("reviews")
    p = commands.add_parser("decide")
    p.add_argument("id", type=int)
    choice = p.add_mutually_exclusive_group(required=True)
    choice.add_argument("--approve", action="store_true")
    choice.add_argument("--reject", action="store_true")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--notes", required=True)
    p.add_argument("--law-status", default="")
    p.add_argument("--jurisdiction", default="")
    p.add_argument("--publication-date", default="")
    p.add_argument("--effective-date", default="")
    p = commands.add_parser("activate")
    p.add_argument("id", type=int)
    p = commands.add_parser("search")
    p.add_argument("query")
    p.add_argument("--domain", default=None)
    p.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    if args.cmd == "register":
        result = register(args.id, args.url, args.domain, args.jurisdiction, args.title)
    elif args.cmd == "sources":
        result = list_sources()
    elif args.cmd == "fetch":
        result = fetch(args.id)
    elif args.cmd == "fetch-all":
        result = fetch_all()
    elif args.cmd == "ingest-local":
        result = ingest_local(args.id, args.path)
    elif args.cmd == "reviews":
        result = reviews()
    elif args.cmd == "decide":
        result = review_decision(args.id, args.approve, args.reviewer, args.notes,
                                 args.publication_date, args.effective_date,
                                 args.law_status, args.jurisdiction)
    elif args.cmd == "activate":
        result = activate(args.id)
    else:
        result = search_approved(args.query, args.k, args.domain)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
