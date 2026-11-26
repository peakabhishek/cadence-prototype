/* Cadence Mac: "Review held changes" prototype (cadence#58). Synthetic data only; nothing is saved.
   States: ?state=today|one|many|undo-keep|undo-use|resolved|loading|error|midnight|closed|upgrade|empty|undo-all  (&frame=1 hides the demo bar). */
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

  /* Synthetic held entries (cadence#58, spec V3 Held end state). Rows are grouped by goal in the sheet.
     kind "session"  = a held add_session: button "Add this session" (adds that one session, deduped by id; never sets a total)
     kind "edit"     = a held edit_goal/add/remove field: "Use phone’s version" (set wording: Field: phone value (Mac has X))
       basis "snapshot" = the Mac that held it had #58 and knows it edited this field after the hold
       basis "nostamp"  = the Mac that held it ran #55 only: it can’t tell which is newer (Tony’s no-stamp wording)
       basis "old"      = more than 7 days old
     kind "update"   = unreadable or newer schemaVersion: no buttons. */
  var ALL = [
    { id: "e1", kind: "session", goal: "Read one paper", line: "Add 30-min session from your phone (18 Nov)", ctx: "Mac’s total for 18 Nov: 20 min", meta: "More than 7 days old",
      keepV: "drops the phone’s 30-min session from 18 Nov", useV: "adds a 30-min session on 18 Nov. The Mac’s own sessions stay as they are", short: "the 30-min session", date: "18 Nov" },
    { id: "e2", kind: "edit", basis: "snapshot", goal: "Focus", chg: "Name: Deep work", mac: "Mac has Focus", meta: "You changed the name on this Mac after this was held", date: "25 Nov",
      keepV: "keeps the name Focus and drops the phone’s name Deep work", useV: "renames it to Deep work, replacing the Mac’s Focus" },
    { id: "e3", kind: "edit", basis: "nostamp", goal: "Write the weekly review", chg: "Time box: 60 min", meta: "Can’t tell which is newer. Mac has 45 min", date: "25 Nov",
      keepV: "keeps the 45 min time box and drops the phone’s 60 min", useV: "sets the time box to 60 min, replacing the Mac’s 45 min" },
    { id: "e4", kind: "edit", basis: "nostamp", goal: "Write the weekly review", chg: "Name: Weekly review", meta: "Can’t tell which is newer. Mac has Write the weekly review", date: "25 Nov",
      keepV: "keeps the name Write the weekly review and drops the phone’s name Weekly review", useV: "renames it to Weekly review, replacing the Mac’s Write the weekly review" },
    { id: "e5", kind: "edit", basis: "old", goal: "Gym", chg: "Name: Gym, legs day", mac: "Mac has Gym", meta: "From your phone on 19 Nov · More than 7 days old", date: "19 Nov",
      keepV: "keeps the name Gym and drops the phone’s name Gym, legs day", useV: "renames it to Gym, legs day, replacing the Mac’s Gym" },
    { id: "e6", kind: "edit", basis: "old", goal: "Call the bank", chg: "Added to 17 Nov", mac: "Mac doesn’t have it", meta: "From your phone on 17 Nov · More than 7 days old", date: "17 Nov",
      keepV: "17 Nov stays without it and the phone’s add is dropped", useV: "adds it to 17 Nov" },
    { id: "e7", kind: "update", reason: "unreadable", date: "24 Nov" },
    { id: "e8", kind: "update", reason: "schema", date: null },
    { id: "e9", kind: "edit", basis: "snapshot", goal: "Plan Friday’s demo", chg: "Time box: 50 min", mac: "Mac has 25 min", meta: "You changed the time box on this Mac after this was held", date: "26 Nov",
      keepV: "keeps the 25 min time box and drops the phone’s 50 min", useV: "sets the time box to 50 min, replacing the Mac’s 25 min" },
    { id: "e10", kind: "edit", basis: "snapshot", goal: "Write the weekly review", chg: "Time box: 60 min", mac: "Mac has 45 min", meta: "You changed the time box on this Mac after this was held", date: "25 Nov",
      keepV: "keeps the 45 min time box and drops the phone’s 60 min", useV: "sets the time box to 60 min, replacing the Mac’s 45 min" }
  ];
  function pick(ids) { return ids.map(function (id) { return ALL.filter(function (e) { return e.id === id; })[0]; }); }
  function gkey(e) { return e.kind === "update" ? "_update" : e.goal; }
  function isChoice(e) { return e.kind !== "update"; }

  var GOALS = [["Write the weekly review", "30 / 45 min", false], ["Read one paper", "30 / 30 min", true], ["Gym", "Not yet", false], ["Plan Friday’s demo", "0 / 25 min", false]];
  var S = { held: pick(["e1", "e2", "e3"]), open: false, loading: false, errors: {}, bulkErr: null, pending: null, midnight: false, failNext: false, upgrade: null };
  var toastTimer = null;

  /* Today note: routine housekeeping (same leaf-wash note, no error colour). */
  function noteText(n) { return n === 1 ? "1 phone change to review" : n + " phone changes to review"; }
  function upgradeText(u) { return u.applied + " phone changes applied" + (u.toReview ? ", " + u.toReview + " to review" : ""); }

  function renderToday() {
    var n = S.held.length;
    var day = S.midnight ? "Saturday 28 Nov · Today starts with a fresh list." : "Friday 27 Nov · What matters today?";
    var h = '<h1 id="today-title">' + (S.midnight ? "Good morning." : "Good evening.") + '</h1><p class="sub">' + day + "</p>";
    var u = S.upgrade;
    if (u) { // shown once, on the first Today view after the upgrade; the counts are what the upgrade did and never change
      h += '<div class="note" role="status">' + ic("check", 16, 2.2) + '<span class="txt">' + upgradeText(u) + "</span>" +
        (u.toReview ? '<button type="button" class="linkbtn" data-act="review" aria-haspopup="dialog" aria-label="Review ' + u.toReview + (u.toReview === 1 ? " held change" : " held changes") + '">Review</button>' : "") +
        '<button type="button" class="linkbtn" data-act="gotit" aria-label="Got it. Hide this note">Got it</button></div>';
    } else if (n) {
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

  function lineHtml(e) {
    if (e.kind === "session") {
      return '<li class="ln" data-id="' + e.id + '"><span class="chg">' + esc(e.line) + ' <span class="mac">· ' + esc(e.ctx) + '</span></span>' +
        '<span class="meta">' + ic("phone", 13) + esc(e.meta) + "</span></li>";
    }
    return '<li class="ln" data-id="' + e.id + '"><span class="chg">' + esc(e.chg) + (e.basis === "snapshot" || e.basis === "old" ? ' <span class="mac">(' + esc(e.mac) + ")</span>" : "") + "</span>" +
      '<span class="meta">' + ic("phone", 13) + esc(e.meta) + "</span></li>";
  }

  function groupHtml(key, rows) {
    var ids = rows.map(function (e) { return e.id; }).join(" ");
    if (key === "_update") {
      return '<li class="grp" data-g="_update"><div class="gh"><span class="gn">Can’t be applied on this Mac yet</span></div><ul class="lns" role="list">' + rows.map(function (e) {
        var title = e.reason === "schema" ? "Changes from a newer Cadence on your phone" : "A change from your phone";
        var meta = e.reason === "schema" ? "From your phone · Made by a newer version of Cadence" : "From your phone on " + e.date + " · This Mac can’t read it yet";
        return '<li class="ln" data-id="' + e.id + '"><span class="chg">' + title + '</span><span class="meta">' + ic("phone", 13) + meta + "</span></li>";
      }).join("") + '</ul><div class="upd">' + ic("laptop", 16) + "Update Cadence on this Mac to apply this.</div></li>";
    }
    var sessionOnly = rows.every(function (e) { return e.kind === "session"; });
    var useLabel = sessionOnly ? (rows.length === 1 ? "Add this session" : "Add these sessions") : "Use phone’s version";
    var kl = "Keep Mac’s version for " + key + ": " + rows.map(function (e) { return e.keepV; }).join("; ");
    var ul = (sessionOnly ? "Add this session to " : "Use phone’s version for ") + key + ": " + rows.map(function (e) { return e.useV; }).join("; ");
    var ch = S.errors[key];
    var err = ch ? '<div class="err" role="alert">' + ic("alert", 16) + '<span class="t">Couldn’t save your choice, so ' + (rows.length === 1 ? "this change is" : "these changes are") + ' still held. Check that your OneDrive folder is available.</span>' +
      '<button type="button" class="btn text" data-act="retry" data-key="' + esc(key) + '" aria-label="Try again: ' + esc(ch === "keep" ? kl : ul) + '">Try again</button></div>' : "";
    return '<li class="grp" data-g="' + esc(key) + '"><div class="gh"><span class="gn">' + esc(key) + '</span>' + (rows.length > 1 ? '<span class="cnt">' + rows.length + " changes</span>" : "") + '</div>' +
      '<ul class="lns" role="list">' + rows.map(lineHtml).join("") + "</ul>" + err +
      '<div class="acts"><button type="button" class="btn primary" data-act="keep" data-key="' + esc(key) + '" aria-label="' + esc(kl) + '">Keep Mac’s version</button>' +
      '<button type="button" class="btn outline" data-act="use" data-key="' + esc(key) + '" aria-label="' + esc(ul) + '">' + useLabel + "</button></div></li>";
  }

  function groups() {
    var order = [], map = {};
    S.held.forEach(function (e) { var k = gkey(e); if (!map[k]) { map[k] = []; order.push(k); } map[k].push(e); });
    order.sort(function (a, b) { return (a === "_update") - (b === "_update"); }); // unreadable and newer-schema group last
    return order.map(function (k) { return [k, map[k]]; });
  }

  function renderSheet() {
    var root = document.getElementById("sheet-root");
    if (!S.open) { root.innerHTML = ""; return; }
    var n = S.held.length, choices = S.held.filter(isChoice).length;
    var body;
    if (S.loading) {
      body = '<div class="list" aria-busy="true"><p class="loading-line">' + ic("sync", 16, 1.75, "spin") + "Reading held changes…</p>" +
        [1, 2, 3].map(function () { return '<div class="grp" aria-hidden="true"><div class="skel" style="width:38%"></div><div class="skel" style="width:72%"></div><div class="skel" style="width:46%"></div></div>'; }).join("") + "</div>";
    } else if (!n) {
      body = '<div class="list"><div class="empty">' + ic("check", 22, 2) + '<p class="e1">No held changes</p><p class="e2">Nothing needs your choice right now.</p></div></div>';
    } else {
      var be = S.bulkErr ? '<div class="err bulk" role="alert">' + ic("alert", 16) + '<span class="t">Couldn’t save your choice, so all ' + choices + ' changes are still held. Check that your OneDrive folder is available.</span>' +
        '<button type="button" class="btn text" data-act="retrybulk" aria-label="Try again: Keep Mac’s version for all ' + choices + ' changes you can choose">Try again</button></div>' : "";
      body = '<div class="list">' + be + '<ul role="list" aria-label="Held changes, grouped by goal">' + groups().map(function (g) { return groupHtml(g[0], g[1]); }).join("") + "</ul></div>";
    }
    var sub = !n && !S.loading ? "Nothing from your phone is held right now." : S.loading ? "Your Mac didn’t apply some changes from your phone, to avoid overwriting newer edits."
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
     still held on disk, so quitting the app inside the 5 seconds leaves it held. "For all" is ONE write. */
  function commit() {
    var p = S.pending; S.pending = null; hideToast();
    if (!p) return;
    if (S.failNext) { // demo: the save fails, the entries come back, still held, with retry copy
      S.failNext = false;
      p.items.forEach(function (it) { S.held.splice(Math.min(it.index, S.held.length), 0, it.e); });
      if (p.bulk) S.bulkErr = true; else p.items.forEach(function (it) { S.errors[gkey(it.e)] = p.choice; });
      S.open = true; render();
    }
  }
  function choose(choice, ids, bulk) {
    if (S.pending) commit();
    var items = [], keys = {};
    ids.forEach(function (id) {
      var i = S.held.findIndex(function (e) { return e.id === id; });
      if (i >= 0) { items.push({ e: S.held[i], index: i }); delete S.errors[gkey(S.held[i])]; keys[gkey(S.held[i])] = 1; }
    });
    S.bulkErr = null;
    items.slice().reverse().forEach(function (it) { S.held.splice(it.index, 1); });
    S.pending = { choice: choice, items: items, bulk: !!bulk };
    if (!S.held.length) S.open = false;
    render();
    var gk = Object.keys(keys), sessions = items.length && items.every(function (it) { return it.e.kind === "session"; });
    var what = gk.length === 1 ? gk[0] : items.length + " changes";
    showToast(choice === "keep" ? "Kept your Mac’s version for " + what + "."
      : sessions ? "Added the " + (items.length === 1 ? "30-min session" : "sessions") + " to " + what + "." : "Used your phone’s version for " + what + ".");
  }
  function idsOf(key) { return S.held.filter(function (e) { return gkey(e) === key; }).map(function (e) { return e.id; }); }
  function undo() {
    var p = S.pending; S.pending = null; hideToast();
    if (!p) return;
    p.items.forEach(function (it) { S.held.splice(Math.min(it.index, S.held.length), 0, it.e); });
    render();
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-act]"); if (!b) return;
    var a = b.getAttribute("data-act"), key = b.getAttribute("data-key");
    if (a === "scrim" && ev.target !== b) return;
    if (a === "review") { S.upgrade = null; S.open = true; S.loading = true; render(); setTimeout(function () { S.loading = false; render(); focusSheet(); }, 700); }
    else if (a === "gotit") { S.upgrade = null; render(); }
    else if (a === "close" || a === "scrim") { S.open = false; render(); var r = document.querySelector('[data-act="review"]'); if (r) r.focus(); }
    else if (a === "keep" || a === "use") choose(a, idsOf(key));
    else if (a === "retry") choose(S.errors[key], idsOf(key));
    else if (a === "retrybulk") choose("keep", S.held.filter(isChoice).map(function (e) { return e.id; }), true);
    else if (a === "keepall") choose("keep", S.held.filter(isChoice).map(function (e) { return e.id; }), true);
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
    S = { held: pick(["e1", "e2", "e3"]), open: false, loading: false, errors: {}, bulkErr: null, pending: null, midnight: false, failNext: false, upgrade: null };
    if (st === "one") { S.held = pick(["e2"]); S.open = true; }
    if (st === "many") { S.held = pick(["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9"]); S.open = true; }
    if (st === "undo-keep") { S.open = true; render(); choose("keep", ["e2"]); return; }
    if (st === "undo-use") { S.open = true; render(); choose("use", ["e1"]); return; }
    if (st === "undo-all") { S.held = pick(["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9"]); S.open = true; render(); choose("keep", S.held.filter(isChoice).map(function (x) { return x.id; }), true); return; }
    if (st === "resolved") { S.held = pick(["e2"]); S.open = true; render(); choose("use", ["e2"]); return; }
    if (st === "loading") { S.open = true; S.loading = true; }
    if (st === "empty") { S.held = []; S.open = true; }
    if (st === "error") { S.open = true; S.errors = { "Focus": "use" }; }
    if (st === "upgrade") { S.held = pick(["e2", "e10", "e9"]); S.upgrade = { applied: 8, toReview: 3 };
      annot("Shown once (annotation, not UI)", "First Today view after the Mac upgrade. The counts are what the upgrade did: 8 applied, 3 held for Review. They don’t change at midnight or while the sheet is open, and the note is replaced by “3 phone changes to review” once this one has been seen."); }
    if (st === "midnight") { S.open = true; S.midnight = true;
      annot("Day boundary (annotation, not UI)", "Sheet opened at 23:58 IST on Fri 27 Nov; now 00:03 IST on Sat 28 Nov. Today moved to the new day; the sheet’s rows, dates and count are unchanged and nothing resolved by itself. Dates are always absolute (“18 Nov”), never “yesterday” or “8 days ago”."); }
    if (st === "closed") { annot("Closed without choosing (annotation, not UI)", "Close, Esc or a click outside the sheet. All 3 changes stay held, so the note keeps the same count."); }
    render();
    if (st === "many" && FRAME) { var l = document.querySelector(".list"); if (l) l.scrollTop = 190; }
  }
  var STATES = [["today", "1 Today"], ["one", "2 One"], ["many", "3 Many (main)"], ["undo-keep", "4 Undo keep"], ["undo-use", "5 Undo add"], ["resolved", "6 Resolved"],
    ["loading", "7 Loading"], ["error", "8 Error"], ["midnight", "9 Midnight"], ["closed", "10 Closed"], ["upgrade", "11 Applied note"], ["empty", "12 Empty"], ["undo-all", "13 Undo for all"]];
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
