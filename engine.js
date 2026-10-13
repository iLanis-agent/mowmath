(function (root) {
  "use strict";
  var OVERLAP = 0.85;  // labeled effective deck width after overlap
  var CLIP_L = 1.2;    // labeled litres of clippings per m2
  var BAG_L = 40;      // labeled catcher bag volume, litres

  function round1(x) { return Math.round(x * 10) / 10; }
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }

  function timePlan(areaM2, deckCm, speedMps) {
    if (!(areaM2 > 0) || !(deckCm > 0) || !(speedMps > 0)) return { error: "the lawn, the deck and the pace must be positive" };
    var effW = deckCm / 100 * OVERLAP;
    var minutes = round1(areaM2 / (effW * speedMps * 60));
    var verdict;
    if (minutes <= 20) verdict = "a quick cut";
    else if (minutes <= 45) verdict = "a standard mow";
    else if (minutes <= 90) verdict = "a long mow";
    else verdict = "a half-day mow";
    return { minutes: minutes, verdict: verdict };
  }

  function stripePlan(widthM, deckCm) {
    if (!(widthM > 0) || !(deckCm > 0)) return { error: "the lawn width and the deck must be positive" };
    var widthCm = round1(widthM * 100);
    var passes = Math.ceil(widthCm / deckCm);
    var lastWidth = round1(widthCm - (passes - 1) * deckCm);
    var verdict;
    if (lastWidth === deckCm) verdict = "even stripes";
    else if (lastWidth >= deckCm / 2) verdict = "a tidy last stripe";
    else verdict = "a skinny last stripe";
    return { passes: passes, lastWidth: lastWidth, verdict: verdict };
  }

  function bagPlan(areaM2) {
    if (!(areaM2 > 0)) return { error: "the lawn must be positive" };
    var litres = round1(areaM2 * CLIP_L);
    var fills = Math.max(1, Math.ceil(litres / BAG_L));
    var verdict;
    if (fills <= 3) verdict = "a few empties";
    else if (fills <= 8) verdict = "a steady rhythm";
    else verdict = "a wheelbarrow day";
    return { litres: litres, fills: fills, verdict: verdict };
  }

  function renderTime(r, areaM2, deckCm, speedMps) {
    return "A lawn " + areaM2 + " m2 at " + deckCm + " cm and " + speedMps + " m/s takes "
      + r.minutes + " minutes - " + r.verdict + ".";
  }

  function renderStripe(r, widthM, deckCm) {
    return "A lawn " + widthM + " m wide at a labeled " + deckCm + " cm deck takes "
      + plural(r.passes, "pass", "passes") + " with a last stripe " + r.lastWidth + " cm - " + r.verdict + ".";
  }

  function renderBag(r, areaM2) {
    return "A lawn " + areaM2 + " m2 drops a labeled " + r.litres + " L of clippings - "
      + plural(r.fills, "bag fill") + ", " + r.verdict + ".";
  }

  var api = { timePlan: timePlan, stripePlan: stripePlan, bagPlan: bagPlan, renderTime: renderTime, renderStripe: renderStripe, renderBag: renderBag };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.MowMath = api;
})(this);
