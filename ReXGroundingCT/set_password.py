#!/usr/bin/env python3
"""Manually set a ReXGroundingCT challenge user's password (Admin SDK).

Use this when someone can't receive the Firebase password-reset email
(e.g. their institutional mail server blocks our messages). You set a
temporary password here, then send it to them through another channel
(Slack/Zoom/in person) and tell them to change it after logging in.

SETUP (one-time) — same service-account key as verify_user.py:
  1. Firebase console -> Project settings (gear) -> Service accounts ->
     "Generate new private key" -> save the JSON next to this file as
     serviceAccountKey.json
     *** KEEP IT PRIVATE — it grants full admin access. Do NOT commit it. ***
  2. pip install firebase-admin

USAGE
  # set a specific password
  python set_password.py someone@example.com --password 'TempPass123'

  # or let it generate a strong temporary one and print it
  python set_password.py someone@example.com

  # also mark their email verified (handy if they never got that email either)
  python set_password.py someone@example.com --verify
"""
import argparse
import os
import secrets
import string
import sys

import firebase_admin
from firebase_admin import auth, credentials

DEFAULT_KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "serviceAccountKey.json")


def generate_password(length=14):
    # letters + digits only — avoids shell-quoting headaches when sharing it
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main():
    ap = argparse.ArgumentParser(description="Set a Firebase Auth user's password directly.")
    ap.add_argument("email", help="the user's email address")
    ap.add_argument("--password", help="the new password (min 6 chars). If omitted, a strong one is generated.")
    ap.add_argument("--verify", action="store_true", help="also mark the email as verified.")
    ap.add_argument("--key", default=DEFAULT_KEY, help="path to the Firebase service-account JSON")
    args = ap.parse_args()

    if not os.path.isfile(args.key):
        sys.exit(f"Service-account key not found at {args.key}. See the setup notes in this file.")

    new_password = args.password or generate_password()
    if len(new_password) < 6:
        sys.exit("Password must be at least 6 characters (Firebase requirement).")

    firebase_admin.initialize_app(credentials.Certificate(args.key))

    try:
        user = auth.get_user_by_email(args.email)
    except auth.UserNotFoundError:
        sys.exit(f"No account found for {args.email} (they may not have signed up, or typo'd the email).")

    update = {"password": new_password}
    if args.verify and not user.email_verified:
        update["email_verified"] = True

    auth.update_user(user.uid, **update)

    print(f"Password set for {args.email} (uid {user.uid}).")
    if args.verify:
        print("Email marked verified." if not user.email_verified else "Email was already verified.")
    if not args.password:
        print(f"Temporary password: {new_password}")
    print("Share this with the user privately and ask them to change it after logging in.")


if __name__ == "__main__":
    main()
