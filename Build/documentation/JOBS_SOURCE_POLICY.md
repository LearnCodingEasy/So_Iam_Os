# Job Source Policy

SO_IAM_OS supports API, RSS, manual and opt-in HTML scraping sources.

For HTML scraping the application requires:

- explicit user confirmation that the source permits the intended scraping;
- robots.txt verification;
- rate limiting;
- public HTTP(S) access only;
- no authentication bypass;
- no CAPTCHA/anti-bot bypass;
- no private/loopback/link-local destination access;
- no automatic application submission through a third-party site.

Source-specific terms always take precedence over the generic scraper capability.

The source adapters are intentionally opt-in and disabled until configured.
