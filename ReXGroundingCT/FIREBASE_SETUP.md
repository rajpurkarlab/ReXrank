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
- **Evaluate:** download a submission's Drive folder → run `rexrank_eval.py` → update the
  leaderboard CSV → push. You can update a submission's `status`/`scores` from the console,
  or use the Firebase Admin SDK for a script.
