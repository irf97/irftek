# Deploy IrfTek to GitHub Pages (free daily backend, ~5 minutes)

1. Create a new GitHub repository (e.g. `irftek`), public.
2. Upload EVERYTHING in this folder to it — including the hidden `.github` folder
   (easiest: GitHub web → "uploading an existing file" → drag the whole folder contents;
   or unzip and `git init && git add -A && git commit -m init && git push`).
3. Repo → Settings → Pages → Source: "Deploy from a branch" → Branch: main / (root) → Save.
4. Repo → Actions tab → enable workflows → open "daily-feed" → "Run workflow" (manual first run).
5. Wait ~1 min: the workflow commits a fresh `terminal_data.js` next to the app.
6. Open `https://<your-username>.github.io/<repo>/` — the app loads with the committed
   feed instantly (LIVE tag, states pre-set), zero relays needed. Add to Home Screen.

From then on the feed refreshes itself every weekday after US close. The in-app
⟳ refresh still works anytime for intraday data through the relay chain.
Private note: the repo is public by default on free Pages — it contains only the
app, the public universe/calendar, and delayed market data. No account data ever.
