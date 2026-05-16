#!/usr/bin/env python3
import argparse
from urllib.parse import quote_plus

from invisible_playwright import InvisiblePlaywright

RESULTS_PER_PAGE = 10


def google_search(
    query: str, max_results: int = 10, max_pages: int = 5
) -> list[str]:
    with InvisiblePlaywright() as browser:
        page = browser.new_page()
        urls: list[str] = []

        for page_index in range(max_pages):
            start = page_index * RESULTS_PER_PAGE
            page.goto(
                f"https://www.google.com/search?q={quote_plus(query)}&start={start}",
                wait_until="domcontentloaded",
            )

            if page_index == 0:
                try:
                    page.get_by_role("button", name="Accept all").click(timeout=3000)
                except Exception:
                    pass

            try:
                page.wait_for_load_state("load", timeout=15000)
                page.wait_for_function(
                    "document.readyState === 'complete' && document.querySelector('div#search a h3') !== null",
                    timeout=15000,
                )
            except Exception:
                break

            anchors = page.locator("div#search a:has(h3)")
            count = anchors.count()
            if count == 0:
                break

            added_on_page = 0
            for i in range(count):
                href = anchors.nth(i).get_attribute("href")
                if href and href.startswith("http") and href not in urls:
                    urls.append(href)
                    added_on_page += 1
                if len(urls) >= max_results:
                    return urls

            if added_on_page == 0:
                break

        return urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Google and print result URLs.")
    parser.add_argument('-q', "--query", help="Search query")
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--sites", help="File with sites to include in the search")

    args = parser.parse_args()

    if args.sites != None:
        with open(args.sites,'r') as f:
            for site in f:
                site = site.strip()
                #print(f"Site: {site}\n")
                query = f"{args.query} site:{site}" 
                results = google_search(query, max_results=args.max_results, max_pages=args.max_pages)
                print(f"Found {len(results)} results for {site}:")
                for i, url in enumerate(results, 1):
                    print(f"{i}. {url}")
    else: 
        results = google_search(args.query, max_results=args.max_results, max_pages=args.max_pages)
        print(f"Found {len(results)} results:")
        for i, url in enumerate(results, 1):
            print(f"{i}. {url}")




