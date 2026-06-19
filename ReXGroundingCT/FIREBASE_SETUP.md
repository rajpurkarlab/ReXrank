# ReXGroundingCT challenge — Firebase setup

The challenge registration/submission on `challenge.html` runs entirely in the
browser using **Firebase Auth + Firestore** (no server). One-time setup:

## 1. Create the Firebase project
1. Go to https://console.firebase.google.com → **Add project** (e.g. `rexgroundingct`).
2. **Build → Authentication → Get started → Sign-in method → Email/Password → Enable.**
   (Email verification works out of the box; users get a verify link on sign-up.)
3. **Build → Firestore Database → Create database** → Production mode → pick a region.

## 2. Get the web config
1. Project settings (gear icon) → **General → Your apps → Web app** (`</>`) → register an app.
2. Copy the `firebaseConfig` object (apiKey, authDomain, projectId, …).
3. Paste those values into `challenge.html` where it says
   `var firebaseConfig = { apiKey: "PASTE_API_KEY", ... }`.
   (These keys are *meant* to be public in client code — security is enforced by the rules below, not by hiding them.)

## 3. Apply the security rules
1. Firestore → **Rules** tab → paste the contents of `firestore.rules` → **Publish**.

## 4. Authorize the site domain
- Authentication → **Settings → Authorized domains** → add `rexrank.ai`
  (and `rajpurkarlab.github.io` if you also use that URL, and `localhost` for testing).

## 5. (Recommended) Customize the verification email
- Authentication → **Templates → Email address verification** → set the sender name /
  action URL so the link points back to the challenge page.

## Done
Push `challenge.html` to `gh-pages` and registration is live. No server, no database to run.

## Running the challenge (organizer side)
- **See registrations:** Firestore → `teams` collection.
- **See submissions:** Firestore → `submissions` collection (team, driveLink, phase, status).
- **Evaluate:** download a submission's Drive folder → run `rexrank_eval.py` → record scores
  (below). You can update a submission's `status` from the console or via the Admin SDK.

## Leaderboard
The page shows a live leaderboard read from a public `leaderboard` collection.
- The security rules make `leaderboard` **world-readable but client-write-disabled**, so only
  you (via the Firebase console or Admin SDK) can publish results — participants can't write to it.
- To add/update an entry: Firestore → `leaderboard` → add a document with fields:
  `team` (string), `dice` (number), `hitRate` (number), `instanceF1` (number).
  The page sorts by `dice` (descending) and renders rows automatically.
- Republish the rules (`firestore.rules`) so the `leaderboard` block is active.

## Email notification on each submission
After a submission is saved, the page pings a Google Apps Script that emails you.
- Set it up via `submission_notify_apps_script.gs` (instructions in that file): deploy it as a
  web app, then paste its URL into `challenge.html` as `var EMAIL_HOOK_URL = '...'`.
- Until that URL is set, submissions still work — the email step is simply skipped.
- This is a best-effort, browser-triggered notification. For a tamper-proof server-side trigger,
  use the Firebase **"Trigger Email"** extension instead (requires upgrading to the Blaze plan).
