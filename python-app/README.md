# Calon PRN Dewan Negeri Johor Ke-16

A small Flask website to browse the candidates and registered-voter counts for
all 56 State Assembly (DUN) seats in the 16th Johor State Election
(polling day **11 July 2026**).

Viewers can:
- Browse the list of all 56 DUN
- Search by constituency name/code **or** candidate name/party
- Open any DUN to see every candidate (with party/coalition) and the total
  registered voters for that seat, plus the 2022 incumbent

## Run

```bash
cd python-app
python -m venv venv           # optional
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Routes

- `/` — the browsable UI (`?q=` search, `?dun=N.01` selects a seat)
- `/api/duns` — JSON of all seats
- `/api/duns/<code>` — JSON for one seat, e.g. `/api/duns/N.01`

## Data

All candidate lists, per-DUN registered voters, and 2022 incumbents live in the
`DATA` list in `app.py`. Edit that list to update figures.

Source: Suruhanjaya Pilihan Raya (SPR), Daftar Pemilih April 2026.
State total registered voters: 2,727,926 across 56 seats · 172 candidates.

> Note: figures are compiled from news reporting of the official SPR roll.
> Verify against the official SPR DPT PDF at https://www.spr.gov.my before
> publishing.
