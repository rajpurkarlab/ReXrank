#!/usr/bin/env python3
"""Manually mark a ReXGroundingCT challenge user's email as verified.

Use this when someone can't receive the Firebase verification email
(e.g. it's blocked, or they exhausted the resend button).

SETUP (one-time)
  1. Firebase console -> Project settings (gear) -> Service accounts ->
     "Generate new private key" -> save the downloaded JSON next to this
     file as  serviceAccountKey.json
     *** KEEP IT PRIVATE — it grants full admin access. Do NOT commit it. ***
  2. pip install firebase-admin

USAGE
  python verify_user.py someone@example.com
  python verify_user.py someone@example.com --key /path/to/serviceAccountKey.json
"""
import argparse
import os
import sys

import firebase_admin
from firebase_admin import auth, credentials

DEFAULT_KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "serviceAccountKey.json")


def main():
    ap = argparse.ArgumentParser(description="Mark a Firebase Auth user's email as verified.")
    ap.add_argument("email", help="the user's email address")
    ap.add_argument("--key", default=DEFAULT_KEY, help="path to the Firebase service-account JSON")
    args = ap.parse_args()

    if not os.path.isfile(args.key):
        sys.exit(f"Service-account key not found at {args.key}. See the setup notes in this file.")

    firebase_admin.initialize_app(credentials.Certificate(args.key))

    try:
        user = auth.get_user_by_email(args.email)
    except auth.UserNotFoundError:
        sys.exit(f"No account found for {args.email} (they may not have signed up, or typo'd the email).")

    if user.email_verified:
        print(f"{args.email} is already verified (uid {user.uid}). Nothing to do.")
        return

    auth.update_user(user.uid, email_verified=True)
    print(f"Verified {args.email} (uid {user.uid}). They can now log in.")


if __name__ == "__main__":
    main()
