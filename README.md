# UniJudge @ ACM TRUST 2027

Website for **Universal Judges (UniJudge): Reliable Judging Across Languages and Modalities**,
a full-day workshop at ACM TRUST 2027 (Washington, DC, March 7–9, 2027).

Live site: https://unijudge.github.io/

## Editing

Everything is in `index.html`. The settings most likely to change are in the
`<script>` block near the bottom:

- `SUBMIT_URL`: the CMT/OpenReview submission link (buttons point to the call until it is set)
- `FORM_URL`: the reviewer-volunteer form (falls back to emailing the primary contact)
- `DATES`, `LEN_FULL`, `LEN_SHORT`, `WORKSHOP_DAY`: dates and page limits
- `ORGANIZERS`, `PC`: organizer cards (add `photo: 'images/name.jpg'`) and program committee

`UniJudge_TRUST2027_CFP.pdf` is the one-page CFP linked from the call section.
