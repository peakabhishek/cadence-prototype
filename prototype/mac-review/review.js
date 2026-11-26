/* Cadence Mac: "Review held changes" prototype (cadence#58). Synthetic data only; nothing is saved.
   States: ?state=today|one|many|undo-keep|undo-use|resolved|loading|error|midnight|closed  (&frame=1 hides the demo bar). */
(function () {
  "use strict";
  var P = {
    cloud: '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 11 3.5 3.5 0 0 0 7 18z"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    x: '<path d="M6 6l12 12M18 6L6 18"/>',
    laptop: '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    phone: '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
    alert: '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.5v.01"/>',
    sync: '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.5 4.5L20 16"/><path d="M20 20v-4h-4"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
  };
  function ic(n, s, sw, cls) {
    return '<svg class="ic ' + (cls || "") + '" width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' + (sw || 1.75) +
      '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + P[n] + "</svg>";
  }
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

  /* Synthetic held entries. kind "choice" = too old or lost the field-by-field compare (two buttons);
     kind "update" = unreadable or newer schemaVersion (no buttons). Each choice row names the ONE field the
     phone value would set and the Mac's current value. */
  var ALL = [
    { id: "e1", kind: "choice", reason: "too_old", goal: "Read one paper", chg: "Focus on 18 Nov: 30 min logged", mac: "Mac has 20 min", date: "18 Nov",
      keep: "Keep Mac’s version for Read one paper: keeps 20 min on 18 Nov and drops the phone’s 30 min",
      use: "Use phone’s version for Read one paper: sets 30 min logged on 18 Nov, replacing the Mac’s 20 min" },
    { id: "e2", kind: "choice", reason: "lost", goal: "Write the weekly review", chg: "Time box: 60 min", mac: "Mac has 45 min", date: "25 Nov",
      keep: "Keep Mac’s version for Write the weekly review: keeps the 45 min time box and drops the phone’s 60 min",
      use: "Use phone’s version for Write the weekly review: sets the time box to 60 min, replacing the Mac’s 45 min" },
    { id: "e3", kind: "update", reason: "unreadable", date: "24 Nov" },
    { id: "e4", kind: "choice", reason: "too_old", goal: "Gym", chg: "Name: “Gym, legs day”", mac: "Mac has “Gym”", date: "19 Nov",
      keep: "Keep Mac’s version for Gym: keeps the name Gym and drops the phone’s name Gym, legs day",
      use: "Use phone’s version for Gym: renames it to Gym, legs day" },
    { id: "e5", kind: "choice", reason: "too_old", goal: "Call the bank", chg: "Added to 17 Nov", mac: "Mac doesn’t have it", date: "17 Nov",
      keep: "Keep Mac’s version for Call the bank: 17 Nov stays without it and the phone’s add is dropped",
      use: "Use phone’s version for Call the bank: adds it to 17 Nov" },
    { id: "e6", kind: "update", reason: "schema", date: null },
    { id: "e7", kind: "choice", reason: "lost", goal: "Plan Friday’s demo", chg: "Time box: 50 min", mac: "Mac has 25 min", date: "26 Nov",
      keep: "Keep Mac’s version for Plan Friday’s demo: keeps the 25 min time box and drops the phone’s 50 min",
      use: "Use phone’s version for Plan Friday’s demo: sets the time box to 50 min, replacing the Mac’s 25 min" }
  ];
  function pick(ids) { return ids.map(function (id) { return ALL.filter(function (e) { return e.id === id; })[0]; }); }

  var GOALS = [["Write the weekly review", "30 / 45 min", false], ["Read one paper", "30 / 30 min", true], ["Gym", "Not yet", false], ["Plan Friday’s demo", "0 / 25 min", false]];
  var S = { held: pick(["e1", "e2", "e3"]), open: false, loading: false, errors: {}, pending: null, midnight: false, failNext: false, focusAfter: null };
  var toastTimer = null;

  function noteText(n) {
    return n === 1 ? "1 change from your phone wasn’t applied, to avoid overwriting newer edits."
      : n + " changes from your phone weren’t applied, to avoid overwriting newer edits.";
  }

  function renderToday() {
    var n = S.held.length;
    var day = S.midnight ? "Saturday 28 Nov · Today starts with a fresh list." : "Friday 27 Nov · What matters today?";
    var h = '<h1 id="today-title">' + (S.midnight ? "Good morning." : "Good evening.") + '</h1><p class="sub">' + day + "</p>";
    if (n) {
      h += '<div class="note" role="status">' + ic("cloud", 16) + '<span class="txt">' + noteText(n) + "</span>" +
        '<button type="button" class="linkbtn" data-act="review" aria-haspopup="dialog" aria-label="Review ' + n + (n === 1 ? " held change" : " held changes") + '">Review</button></div>';
    }
    var goals = S.midnight ? [] : GOALS;
    h += '<div class="lbl"><span>Goals</span><span>' + goals.length + " of 6</span></div>";
    goals.forEach(function (g, i) {
      h += '<div class="g"><span class="n' + (g[2] ? " hit" : "") + '">' + (g[2] ? ic("check", 14, 2.4) : i + 1) + '</span><span class="tt">' + esc(g[0]) + '</span><span class="bx">' + g[1] + "</span></div>";
    });
    h += '<button type="button" class="addg">' + ic("plus", 18, 2) + "Add a goal</button>";
    h += '<div class="foot">' + ic("check", 14) + "Saved · OneDrive folder</div>";
    document.getElementById("today").innerHTML = h;
  }

  function rowHtml(e) {
    if (e.kind === "update") {
      var title = e.reason === "schema" ? "Changes from a newer Cadence on your phone" : "A change from your phone";
      var meta = e.reason === "schema" ? "From your phone · Made by a newer version of Cadence" : "From your phone on " + e.date + " · This Mac can’t read it yet";
      return '<li class="row" data-id="' + e.id + '"><span class="gn">' + title + '</span><span class="meta">' + ic("phone", 13) + meta + "</span>" +
        '<span class="upd">' + ic("laptop", 16) + "Update Cadence on this Mac to apply this.</span></li>";
    }
    var why = e.reason === "too_old" ? "More than 7 days old" : "Your Mac changed this later";
    var err = S.errors[e.id] ? '<div class="err" role="alert">' + ic("alert", 16) + '<span class="t">Couldn’t save your choice, so this change is still held. Check that your OneDrive folder is available.</span>' +
      '<button type="button" class="btn text" data-act="retry" data-id="' + e.id + '" aria-label="Try again: ' + esc(S.errors[e.id] === "keep" ? e.keep : e.use) + '">Try again</button></div>' : "";
    return '<li class="row" data-id="' + e.id + '"><span class="gn">' + esc(e.goal) + '</span>' +
      '<span class="chg">' + esc(e.chg) + ' <span class="mac">(' + esc(e.mac) + ")</span></span>" +
      '<span class="meta">' + ic("phone", 13) + "From your phone on " + e.date + " · " + why + "</span>" + err +
      '<div class="acts"><button type="button" class="btn primary" data-act="keep" data-id="' + e.id + '" aria-label="' + esc(e.keep) + '">Keep Mac’s version</button>' +
      '<button type="button" class="btn outline" data-act="use" data-id="' + e.id + '" aria-label="' + esc(e.use) + '">Use phone’s version</button></div></li>';
  }

  function renderSheet() {
    var root = document.getElementById("sheet-root");
    if (!S.open) { root.innerHTML = ""; return; }
    var n = S.held.length, choices = S.held.filter(function (e) { return e.kind === "choice"; }).length;
    var body;
    if (S.loading) {
      body = '<div class="list" aria-busy="true"><p class="loading-line">' + ic("sync", 16, 1.75, "spin") + "Reading held changes…</p>" +
        [1, 2, 3].map(function () { return '<div class="row" aria-hidden="true"><div class="skel" style="width:38%"></div><div class="skel" style="width:72%"></div><div class="skel" style="width:46%"></div></div>'; }).join("") + "</div>";
    } else {
      body = '<ul class="list" role="list" aria-label="Held changes">' + S.held.map(rowHtml).join("") + "</ul>";
    }
    var sub = S.loading ? "Your Mac didn’t apply some changes from your phone, to avoid overwriting newer edits."
      : (n === 1 ? "Your Mac didn’t apply this change, to avoid overwriting newer edits." : "Your Mac didn’t apply these " + n + " changes, to avoid overwriting newer edits.") + " Nothing changes until you choose.";
    root.innerHTML = '<div class="scrim" data-act="scrim"><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="sh-title" aria-describedby="sh-sub" tabindex="-1">' +
      '<div class="sh-head"><div class="hd"><h2 id="sh-title">Held changes from your phone</h2><p id="sh-sub">' + sub + "</p></div>" +
      '<button type="button" class="closex" data-act="close" aria-label="Close. Every change stays held.">' + ic("x", 20, 2) + "</button></div>" + body +
      '<div class="sh-foot"><span class="hint">Closing keeps every change held.</span>' +
      (!S.loading && choices > 1 ? '<button type="button" class="btn outline" data-act="keepall" aria-label="Keep Mac’s version for all ' + choices + ' changes you can choose. The phone changes are dropped.">Keep Mac’s version for all</button>' : "") +
      '<button type="button" class="btn text" data-act="close" aria-label="Close. Every change stays held.">Close</button></div></div></div>';
  }

  function render() { renderToday(); renderSheet(); }

  function showToast(text, onUndo) {
    var t = document.getElementById("toast");
    t.innerHTML = '<span class="t-ico">' + ic("check", 16, 2.2) + "</span><span>" + esc(text) + '</span><button type="button" class="btn text" data-act="undo">Undo</button>';
    t.hidden = false;
    clearTimeout(toastTimer);
    if (!FRAME) toastTimer = setTimeout(commit, 5000);
  }
  function hideToast() { var t = document.getElementById("toast"); t.hidden = true; t.innerHTML = ""; clearTimeout(toastTimer); }

  /* The choice is written when the 5-second Undo ends (or when another choice starts). Until then the entry is
     still held on disk, so quitting the app inside the 5 seconds leaves it held. */
  function commit() {
    var p = S.pending; S.pending = null; hideToast();
    if (!p) return;
    if (S.failNext) { // demo: the save fails, the entries come back, still held, with retry copy
      S.failNext = false;
      p.items.forEach(function (it) { S.held.splice(Math.min(it.index, S.held.length), 0, it.e); S.errors[it.e.id] = p.choice; });
      S.open = true; render();
    }
  }
  function choose(choice, ids) {
    if (S.pending) commit();
    var items = [];
    ids.forEach(function (id) {
      var i = S.held.findIndex(function (e) { return e.id === id; });
      if (i >= 0) { items.push({ e: S.held[i], index: i }); delete S.errors[id]; }
    });
    items.slice().reverse().forEach(function (it) { S.held.splice(it.index, 1); });
    S.pending = { choice: choice, items: items };
    if (!S.held.length) S.open = false;
    render();
    var what = items.length === 1 ? items[0].e.goal : items.length + " changes";
    showToast((choice === "keep" ? "Kept your Mac’s version for " : "Used your phone’s version for ") + what + ".");
  }
  function undo() {
    var p = S.pending; S.pending = null; hideToast();
    if (!p) return;
    p.items.forEach(function (it) { S.held.splice(Math.min(it.index, S.held.length), 0, it.e); });
    render();
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-act]"); if (!b) return;
    var a = b.getAttribute("data-act"), id = b.getAttribute("data-id");
    if (a === "scrim" && ev.target !== b) return;
    if (a === "review") { S.open = true; S.loading = true; render(); setTimeout(function () { S.loading = false; render(); focusSheet(); }, 700); }
    else if (a === "close" || a === "scrim") { S.open = false; render(); var r = document.querySelector('[data-act="review"]'); if (r) r.focus(); }
    else if (a === "keep" || a === "use") choose(a, [id]);
    else if (a === "retry") choose(S.errors[id], [id]);
    else if (a === "keepall") choose("keep", S.held.filter(function (e) { return e.kind === "choice"; }).map(function (e) { return e.id; }));
    else if (a === "undo") undo();
  });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && S.open) { S.open = false; render(); } });
  function focusSheet() { var s = document.querySelector(".sheet"); if (s) s.focus(); }

  /* ---------- states (frames and demo bar) ---------- */
  var q = new URLSearchParams(location.search);
  var FRAME = q.get("frame") === "1";
  if (FRAME) document.body.classList.add("frame");
  function annot(title, text) { var a = document.getElementById("annot"); a.innerHTML = "<b>" + title + "</b>" + text; a.hidden = false; }
  function setState(st) {
    hideToast(); document.getElementById("annot").hidden = true;
    S = { held: pick(["e1", "e2", "e3"]), open: false, loading: false, errors: {}, pending: null, midnight: false, failNext: false };
    if (st === "one") { S.held = pick(["e1"]); S.open = true; }
    if (st === "many") { S.held = pick(["e1", "e2", "e3", "e4", "e5", "e6", "e7"]); S.open = true; }
    if (st === "undo-keep" || st === "undo-use") { S.open = true; render(); choose(st === "undo-keep" ? "keep" : "use", ["e1"]); return; }
    if (st === "resolved") { S.held = pick(["e1"]); S.open = true; render(); choose("keep", ["e1"]); return; }
    if (st === "loading") { S.open = true; S.loading = true; }
    if (st === "error") { S.open = true; S.errors = { e1: "keep" }; }
    if (st === "midnight") { S.open = true; S.midnight = true;
      annot("Day boundary (annotation, not UI)", "Sheet opened at 23:58 IST on Fri 27 Nov; now 00:03 IST on Sat 28 Nov. Today moved to the new day; the sheet’s rows, dates and count are unchanged and nothing resolved by itself. Dates are always absolute (“on 18 Nov”), never “yesterday” or “8 days ago”."); }
    if (st === "closed") { annot("Closed without choosing (annotation, not UI)", "Close, Esc or a click outside the sheet. All 3 changes stay held, so the note keeps the same count."); }
    render();
    if (st === "many" && FRAME) { var l = document.querySelector(".list"); if (l) l.scrollTop = 150; }
  }
  var STATES = [["today", "1 Today"], ["one", "2 One"], ["many", "3 Many"], ["undo-keep", "4 Undo keep"], ["undo-use", "5 Undo use"], ["resolved", "6 Resolved"],
    ["loading", "7 Loading"], ["error", "8 Error"], ["midnight", "9 Midnight"], ["closed", "10 Closed"]];
  var demo = document.getElementById("demo");
  demo.innerHTML = "<b>Demo states (synthetic data)</b>" + STATES.map(function (s) { return '<button type="button" data-st="' + s[0] + '">' + s[1] + "</button>"; }).join("") +
    '<button type="button" data-st="fail">Make the next save fail</button>';
  demo.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-st]"); if (!b) return; ev.stopPropagation();
    var st = b.getAttribute("data-st");
    if (st === "fail") { S.failNext = true; b.textContent = "Next save will fail"; return; }
    history.replaceState(null, "", "?state=" + st); setState(st);
  });
  window.__setState = setState;
  setState(q.get("state") || "today");
})();
