# Right Care Now

A rule-based (not diagnostic) tool that maps self-reported symptoms to a
severity tier — ER, urgent care, or telehealth — using a conservative
checklist rather than a machine learning model. Any red-flag symptom always
wins, and a self-harm mention always shows crisis resources, regardless of
what else is selected.

## Run it locally

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Project structure

```
right-care-now/
├── app.py                # Flask app + triage logic
├── requirements.txt
├── templates/
│   ├── index.html         # symptom checklist form
│   └── result.html        # recommendation + mock facility list
└── static/
    └── style.css
```

## Important limitations (say this out loud at judging)

- Wait times and facility names are **mock data** — a real version needs a
  live feed of hospital-reported ED wait times plus a maps/geolocation API.
- This is a fixed checklist, not a diagnostic model, by design — it should
  be reviewed by an actual clinician before any real-world use.
- It is not a substitute for calling 911 or professional medical judgment.
