# wheyapp

Tells me when [AGN Roots Grassfed Whey (3 lbs)](https://agnroots.com/products/agn-roots-grass-fed-whey-3-lbs) is back in stock.

## How it works

A GitHub Actions workflow (`.github/workflows/stock-check.yml`) runs every 30 minutes and calls
`check_stock.py`, which reads the store's public Shopify product data
(`/products/<handle>.js`) and looks at each variant's `available` flag.

- **Back in stock:** it opens a GitHub issue labelled `in-stock` that @-mentions me.
  GitHub emails me and pushes a notification to the GitHub mobile app.
- **Still in stock on later runs:** nothing happens, because the open issue means I've already been alerted.
- **Sold out again:** it closes the issue, so the next restock sends a new alert.

## Instant phone notifications (optional)

GitHub email works without any setup. For a louder push notification:

1. Install the [ntfy](https://ntfy.sh) app (iOS/Android) and subscribe to a hard-to-guess topic name,
   e.g. `whey-restock-8f3k2q`. Anyone who knows the name can read it.
2. In this repo, go to **Settings → Secrets and variables → Actions → New repository secret**,
   name it `NTFY_TOPIC` and set the value to that topic name.

## Test it

**Actions → Whey restock check → Run workflow**, tick *Send a test alert now*, then run.
You should get a `[Test]` issue (and an ntfy push if configured). Close it afterwards.

Run the check locally with `python3 check_stock.py`. To watch a different product on a Shopify store, set `PRODUCT_URL`.

## Notes

- Scheduled workflows run only on the repo's **default branch**, and GitHub may delay a scheduled run by a few minutes.
- This repo is private, so each run uses about 1 of the 2,000 free Actions minutes per month.
  Running every 30 minutes uses about 1,500 a month. To check more often, make the repo public
  (Actions minutes are then free) and tighten the `cron` line.
