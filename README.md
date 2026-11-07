# Google Maps Scraper (Python)

Scrape Google Maps places and reviews from Python. Search a query such as "coffee shops in Singapore", get name, address, rating, review count, website and coordinates for each place, then pull the reviews of any place. There is no browser to drive and no proxy to set up: each page of results is one POST request to the EveryInfra API.

Also covers: best Google Maps scraper, how to scrape Google Maps.

## Quick start

```bash
git clone https://github.com/everyinfra/google-maps-scraper.git
cd google-maps-scraper
pip install -r requirements.txt
export EVERYINFRA_API_KEY=your_key   # get one at everyinfra.com
python main.py search "coffee shops in Singapore" --limit 15 --out places.csv
python main.py reviews "<place url from search>" --out reviews.csv
```

Get an API key: [everyinfra.com/en/docs](https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper#quickstart). Without `--out`, the script prints the first three rows as JSON.

## Price

| Call | Price per 1,000 calls | Rows per call |
|---|---|---|
| [`google_maps_reviews/search`](https://everyinfra.com/en/google-maps-reviews-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper) | $1.39 | 15 in our test |
| [`google_maps_reviews/reviews`](https://everyinfra.com/en/google-maps-reviews-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper) | $1.39 | 20 in our test |

- You pay per call, not per month. Failed calls and empty results are not charged.
- New accounts can claim $1 of trial credit: create an account, star [everyinfra-agent-plugins](https://github.com/everyinfra/everyinfra-agent-plugins) and [seo-skills](https://github.com/everyinfra/seo-skills), then claim it in the console. It is valid for 24 hours and needs no card. See [pricing](https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper).

## What you get

### `search`

| Field | Meaning |
|---|---|
| `name` | Name of the object itself, for account, product and business capabilities. |
| `url` | Link to the record on the platform. |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `description` | Summary or description, usually shorter than text. |
| `address` | Full address, passed through as is. |
| `city` | City name in the platform's language, not normalized. |
| `phone` | Contact phone number, passed through without format normalization. |
| `website` | External website entered by the account or business. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). Convert with rating_scale before comparing across platforms, or the comparison can come out backwards. |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. Present only when the row has a rating. |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `price` | Price as a number without a currency symbol; see currency. |
| `image_url` | Image link. Capabilities with several images may return an image_urls array. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

Also returned, named as on the platform: `place_id`, `categories`, `state`, `postal_code`, `country_code`, `lat`, `lng`, `permanently_closed`.

Full parameter list: [Google Maps search API](https://everyinfra.com/en/google-maps-reviews-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper).

### `reviews`

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. Unique only within one platform; IDs can repeat across platforms. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). Convert with rating_scale before comparing across platforms, or the comparison can come out backwards. |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. Present only when the row has a rating. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). Non-standard strings from the platform are passed through as is, so parse defensively. null means the platform does not disclose it. |
| `url` | Link to the record on the platform. |
| `owner_response` | The business's public reply to this review: text, author_name and posted_at; absent when there is no reply. |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

Also returned, named as on the platform: `reviewer_name`, `reviewer_id`, `reviewer_review_count`, `is_local_guide`, `owner_response_at`, `detailed_rating`, `place_id`, `place_name`.

Full parameter list: [Google Maps reviews API](https://everyinfra.com/en/google-maps-reviews-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper).

## Tested

We ran both commands against the live API before publishing this repository (times in Singapore time, UTC+8).

| Command | Run at (SGT) | Rows | Charged |
|---|---|---|---|
| `search "coffee shops in Singapore" --limit 15` | 2026-11-08 03:36 | 15 | $0.001389 |
| `reviews "<place url from search>"` | 2026-11-08 03:36 | 20 | $0.001389 |

First row of the `search` result (long text cut, author fields left out of this sample):

```json
{
  "place_id": "ChIJuUak_qQZ2jERgdSigpu0ljc",
  "name": "Kurasu Singapore",
  "url": "https://www.google.com/maps/search/?api=1&query=Kurasu%20Singapore&query_place_id=ChIJuUak_qQZ2jERgdSigpu0ljc",
  "category": "Coffee shop",
  "categories": [
    "Coffee shop",
    "Coffee store"
  ],
  "description": "Contemporary cafe & co-working space showcasing specialty coffees & coffee-making equipment.",
  "address": "261 Waterloo St, #01-24, Singapore 180261",
  "city": "Singapore",
  "postal_code": "180261",
  "country_code": "SG",
  "lat": 1.2984136,
  "lng": 103.8519238,
  "website": "http://www.kurasu.sg/",
  "rating": 4.4,
  "review_count": 1214,
  "platform": "google_maps_reviews",
  "rating_scale": 5
}
```

## How it works

Every call is one request. `everyinfra.py` wraps it in about 60 lines of `requests`:

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"platform": "google_maps_reviews", "action": "search", "params": {"keyword": "coffee shops in Singapore"}}'
```

- Slow actions (Instagram `user_posts`, for example) answer with a `job_id`. The script polls `GET /api/v1/jobs/{job_id}` every 5 seconds; polling is free.
- Errors come back as JSON with a code, a message and whether you were charged. A missing parameter returns 422 before any charge.
- The same key also works over MCP for Claude, Cursor and other AI agents: [docs](https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper).

## More

- [Google Maps API on EveryInfra](https://everyinfra.com/en/google-maps-reviews-api?utm_source=github&utm_medium=example_repo&utm_campaign=google-maps-scraper): every Google Maps action, with prices and live health
- Other examples: [instagram-scraper-python](https://github.com/everyinfra/instagram-scraper-python) · [tiktok-trends-api](https://github.com/everyinfra/tiktok-trends-api) · [tiktok-scraper-python](https://github.com/everyinfra/tiktok-scraper-python) · [douyin-api-python](https://github.com/everyinfra/douyin-api-python)

## License

MIT
