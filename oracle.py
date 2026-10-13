import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

OVERLAP = 0.85
CLIP_L = 1.2
BAG_L = 40

def time_plan(areaM2, deckCm, speedMps):
    if not (areaM2 > 0) or not (deckCm > 0) or not (speedMps > 0):
        return {"error": "the lawn, the deck and the pace must be positive"}
    eff_w = deckCm / 100 * OVERLAP
    minutes = round1(areaM2 / (eff_w * speedMps * 60))
    if minutes <= 20: verdict = "a quick cut"
    elif minutes <= 45: verdict = "a standard mow"
    elif minutes <= 90: verdict = "a long mow"
    else: verdict = "a half-day mow"
    return {"minutes": minutes, "verdict": verdict}

def stripe_plan(widthM, deckCm):
    if not (widthM > 0) or not (deckCm > 0):
        return {"error": "the lawn width and the deck must be positive"}
    width_cm = round1(widthM * 100)
    passes = math.ceil(width_cm / deckCm)
    last_width = round1(width_cm - (passes - 1) * deckCm)
    if last_width == deckCm: verdict = "even stripes"
    elif last_width >= deckCm / 2: verdict = "a tidy last stripe"
    else: verdict = "a skinny last stripe"
    return {"passes": passes, "lastWidth": last_width, "verdict": verdict}

def bag_plan(areaM2):
    if not (areaM2 > 0):
        return {"error": "the lawn must be positive"}
    litres = round1(areaM2 * CLIP_L)
    fills = max(1, math.ceil(litres / BAG_L))
    if fills <= 3: verdict = "a few empties"
    elif fills <= 8: verdict = "a steady rhythm"
    else: verdict = "a wheelbarrow day"
    return {"litres": litres, "fills": fills, "verdict": verdict}

def render_time(r, areaM2, deckCm, speedMps):
    return ("A lawn " + fmt(areaM2) + " m2 at " + fmt(deckCm) + " cm and " + fmt(speedMps)
            + " m/s takes " + fmt(r["minutes"]) + " minutes - " + r["verdict"] + ".")

def render_stripe(r, widthM, deckCm):
    return ("A lawn " + fmt(widthM) + " m wide at a labeled " + fmt(deckCm) + " cm deck takes "
            + plural(r["passes"], "pass", "passes") + " with a last stripe " + fmt(r["lastWidth"]) + " cm - " + r["verdict"] + ".")

def render_bag(r, areaM2):
    return ("A lawn " + fmt(areaM2) + " m2 drops a labeled " + fmt(r["litres"]) + " L of clippings - "
            + plural(r["fills"], "bag fill") + ", " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[500,46,1.2],[200,30,1],[1500,53,1.4],[800,40,0.8],[3000,53,1.4],[100,25,1],[50,20,0.5],[6000,60,1.5],[0,46,1.2],[500,0,1.2]]:
    add("timePlan", time_plan, render_time, a)
for a in [[12,46],[10,50],[8,40],[15,46],[5,53],[20,60],[6.5,50],[9.2,46],[0,46],[12,0]]:
    add("stripePlan", stripe_plan, render_stripe, a)
for a in [[500],[100],[1000],[33],[34],[2000],[320],[321],[0],[50]]:
    add("bagPlan", bag_plan, render_bag, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
