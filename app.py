"""
Right Care Now — triage-aware ER / urgent care / telehealth router.

Rule-based only: maps a fixed, clinician-reviewable symptom checklist to a
severity tier. This is NOT a diagnostic model, and any red-flag symptom
always wins, regardless of what else is selected — uncertainty always
resolves toward MORE care, never less.
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# --- Mock data -------------------------------------------------------------
# In production this would come from hospitals' published ED wait-time feeds
# and a maps/geolocation API, not hardcoded values.

FACILITIES = {
    "red": [
        {"name": "Harborview General — Emergency Dept.", "wait": "12 min", "dist": "1.4 mi"},
        {"name": "St. Aldric Medical Center — ER", "wait": "28 min", "dist": "2.1 mi"},
        {"name": "Call 911 if you cannot get there safely", "wait": "—", "dist": "—"},
    ],
    "amber": [
        {"name": "Northside Urgent Care", "wait": "22 min", "dist": "0.9 mi"},
        {"name": "CareNow Clinic — Main St.", "wait": "35 min", "dist": "1.6 mi"},
        {"name": "Harborview General — ER (backup option)", "wait": "55 min", "dist": "1.4 mi"},
    ],
    "green": [
        {"name": "Telehealth visit — same-day", "wait": "~10 min", "dist": "From home"},
        {"name": "Your primary care office", "wait": "Call ahead", "dist": "varies"},
        {"name": "Northside Urgent Care (if it worsens)", "wait": "22 min", "dist": "0.9 mi"},
    ],
    "none": [],
}

COPY = {
    "red": {
        "title": "Go to the ER now",
        "sub": "What you selected can be a sign of a medical emergency.",
        "why": "One or more answers matched warning signs — like chest pain, trouble "
               "breathing, or sudden weakness — that always route to emergency care, "
               "regardless of anything else selected.",
    },
    "amber": {
        "title": "Urgent care today",
        "sub": "This looks like something that needs attention soon, but is not an emergency.",
        "why": "What you selected typically needs same-day medical care. If anything "
               "changes or gets worse, treat it as an emergency and go to the ER instead.",
    },
    "green": {
        "title": "Telehealth or your own doctor",
        "sub": "This looks manageable without an in-person urgent visit.",
        "why": "What you selected is commonly handled by a telehealth visit, a nurse "
               "line, or your regular doctor. If symptoms worsen, move up to urgent "
               "care or the ER.",
    },
    "none": {
        "title": "Tell us a bit more",
        "sub": "Select at least one symptom so we can point you the right way.",
        "why": "If nothing quite fits and you're still concerned, a nurse line or "
               "urgent care is a safe default.",
    },
}


def determine_tier(selected_tiers):
    """Conservative priority: red beats amber beats green beats none."""
    if "red" in selected_tiers:
        return "red"
    if "amber" in selected_tiers:
        return "amber"
    if "green" in selected_tiers:
        return "green"
    return "none"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected = request.form.getlist("symptom")   # e.g. ['red', 'amber']
        self_harm = request.form.get("self_harm") == "yes"

        tier = determine_tier(selected)

        return render_template(
            "result.html",
            tier=tier,
            copy=COPY[tier],
            facilities=FACILITIES[tier],
            self_harm=self_harm,
        )

    return render_template("index.html")


if __name__ == "__main__":
    # debug=True is for local development only — turn off before any real deployment
    app.run(debug=True)
