"""Google Maps scraper in Python: search places, then pull their reviews.

  python main.py search "coffee shops in Singapore" --limit 20 --out places.csv
  python main.py reviews "<place url from search>" --out reviews.csv
"""
import argparse

from everyinfra import call, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="find places for a query")
    s.add_argument("keyword")
    s.add_argument("--country", help="country code for search context, e.g. us, sg")
    s.add_argument("--language", help="result language, e.g. en")
    s.add_argument("--limit", type=int, default=15, help="1-50 places per call")
    s.add_argument("--pages", type=int, default=1, help="follow next_page_token this many pages")
    r = sub.add_parser("reviews", help="reviews of one place")
    r.add_argument("url", help="place url from search results")
    r.add_argument("--pages", type=int, default=1)
    for x in (s, r):
        x.add_argument("--out", help="write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        action, params = "search", {"keyword": a.keyword, "limit": a.limit}
        for k in ("country", "language"):
            if getattr(a, k):
                params[k] = getattr(a, k)
    else:
        action, params = "reviews", {"url": a.url}

    rows, data = [], {}
    for _ in range(a.pages):
        data = call("google_maps_reviews", action, params)
        rows += data.get("results") or []
        token = data.get("next_page_token")
        if not token:
            break
        params["page_token"] = token
    data["results"] = rows
    report(data, a.out)


if __name__ == "__main__":
    main()
