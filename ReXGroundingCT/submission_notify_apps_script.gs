/**
 * ReXGroundingCT @ MICCAI 2026 — email the organizer on every submission.
 *
 * The challenge page (challenge.html) POSTs to this Google Apps Script web app
 * right after a submission is saved to Firestore. The script emails the organizer
 * via Gmail (free, no Firebase billing needed). Sends from / to your own Google account.
 *
 * SETUP
 * 1. https://script.google.com → New project → paste this file.
 * 2. Set ORGANIZER_EMAIL below (and optionally add more addresses, comma-separated).
 * 3. Deploy → New deployment → Web app:
 *      - Execute as:     Me
 *      - Who has access: Anyone
 *    Authorize (it needs permission to send mail as you), then copy the Web app URL.
 * 4. Paste that URL into challenge.html as `var EMAIL_HOOK_URL = '...'`.
 * 5. Re-deploy a NEW VERSION whenever you edit this script.
 *
 * Note: this is triggered by the participant's browser, so it's a best-effort
 * notification (a user could block it). For a tamper-proof, server-side trigger,
 * use the Firebase "Trigger Email" extension instead (requires the Blaze plan).
 */

var ORGANIZER_EMAIL = 'MohammedSalimAB@outlook.com';

function doPost(e) {
  var p = (e && e.parameter) ? e.parameter : {};
  var subject = 'New ReXGrounding submission — ' + (p.team || '(unknown team)');
  var body =
      'A new submission was received for the ReXGroundingCT challenge.\n\n' +
      'Team:        ' + (p.team || '') + '\n' +
      'Submitter:   ' + (p.email || '') + '\n' +
      'Phase:       ' + (p.phase || '') + '\n' +
      'Method/run:  ' + (p.method || '') + '\n' +
      'Drive link:  ' + (p.driveLink || '') + '\n' +
      'Time:        ' + (p.date || '') + '\n';
  MailApp.sendEmail(ORGANIZER_EMAIL, subject, body);
  return ContentService.createTextOutput('ok');
}

function doGet() {
  return ContentService.createTextOutput('ReXGroundingCT submission-notify is live.');
}
