# UniJudge @ ACM TRUST 2027

Website for **The First Workshop on Universal Judges** (**UniJudge @ ACM TRUST 2027**),
a full-day workshop at ACM TRUST 2027 (Washington, DC, March 7–9, 2027).
Theme: Reliable judging across languages and modalities.

Live site: https://acmtrustunijudge.github.io/

## Editing

Everything is in `index.html`. The settings most likely to change are in the
`<script>` block near the bottom:

- `SUBMIT_URL`: the direct submission link on OpenReview
- `ARR_COMMIT_URL`: the ARR commitment link on OpenReview
- `EMAIL`: the organizer contact address, also used for reviewer interest
- `DATES`, `LEN_FULL`, `LEN_SHORT`, `WORKSHOP_DAY`: dates and page limits
- `ORGANIZERS`: organizer cards (`linkedin` links the name; add `photo: 'images/name.jpg'` for a portrait)

`UniJudge_TRUST2027_CFP.pdf` is the one-page CFP flyer.

To rebuild it, install `reportlab` and `qrcode`, then run
`python scripts/build_cfp.py`. The script reads deadlines, submission links,
organizers, and the contact address from `index.html`; flyer copy and topic
summaries are maintained in the script. It uses Lato fonts from
`/usr/share/fonts/truetype/lato` (override with `--font-dir`).
The default theme is muted navy; `--theme slate` provides a subtle alternative.
Use `--output /path/to/flyer.pdf` to save a separate copy.

For the condensed 1200 x 1200 LinkedIn PNG, install `Pillow` and `qrcode`,
then run `python scripts/build_linkedin.py`. This also reads dates from
`index.html` and uses the same Lato font directory.
