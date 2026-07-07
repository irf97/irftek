# Deploying v4 to https://irf97.github.io/irftek/
PRIMARY PATH — Claude pushes for you:
Cut a token at github.com/settings/tokens → "Generate new token (classic)" →
scopes: repo + workflow → expiry 7 days → paste it in chat. Claude updates every
file via the GitHub API, triggers the first 105-name feed, verifies the site,
then reminds you to revoke the token.

FALLBACK — manual (2 min):
repo → Add file → Upload files → drag EVERYTHING in this folder (GitHub shows
"replace" on existing files — correct) → commit. Site serves v4 in ~1 minute.

Note: the 38 new names show "tap ⟳ to unlock" until the first expanded feed
commits (nightly at 21:15 UTC, or immediately when Claude dispatches it).
