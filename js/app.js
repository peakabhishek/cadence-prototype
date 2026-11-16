/* Cadence laptop prototype. The product saves to a OneDrive folder; this prototype still uses localStorage. No network calls. */
(function () {
  "use strict";

  const STORE_KEY = "cadence-prototype-v1";
  const DEFAULT_TODAY = "2026-11-12";
  const EXAMPLE_TODAY = "2026-11-15";
  const GRACE_MS = 10000;
  const DEMO_RATIO = 60;
  const DURS = [
    { min: 25, label: "Short" },
    { min: 50, label: "Deep" },
    { min: 90, label: "Long" },
  ];
  const AP = "\u2019";
  const EN = "\u2013";
  const EM = "\u2014";
  const MD = "\u00b7";

  const ICONS = {
    today: '<path d="M7 14h10l-1.3 6.2a1 1 0 0 1-1 .8H9.3a1 1 0 0 1-1-.8z"/><path d="M12 14V9"/><path d="M12 10.5c0-2.6 1.8-4.5 4.5-4.5 0 2.6-1.9 4.5-4.5 4.5z"/><path d="M12 9c0-2-1.4-3.5-3.5-3.5 0 2 1.4 3.5 3.5 3.5z"/>',
    focus: '<circle cx="12" cy="13" r="7.5"/><path d="M12 9.5V13l2.4 1.6"/><path d="M10 3h4"/>',
    week: '<path d="M5 19V12"/><path d="M10 19V7"/><path d="M15 19v-9"/><path d="M20 19v-5"/>',
    device: '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/>',
    plus: '<path d="M12 6v12M6 12h12"/>',
    check: '<path d="M6 12.5l4 4 8-9"/>',
    tab: '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3 9h18"/><path d="M14 14h4m0 0-1.6-1.6M18 14l-1.6 1.6"/>',
    hand: '<path d="M8 12V6.5a1.5 1.5 0 0 1 3 0V11"/><path d="M11 10V5a1.5 1.5 0 0 1 3 0v6"/><path d="M14 10.5V7a1.5 1.5 0 0 1 3 0v6.5c0 3.6-2.4 6.5-6 6.5-2.3 0-3.6-1-4.8-2.8L4.6 14.6a1.5 1.5 0 0 1 2.4-1.8L8 14"/>',
    sunrise: '<path d="M4 18h16"/><path d="M7.5 18a4.5 4.5 0 0 1 9 0"/><path d="M12 7v3M5.6 11.6l1.6 1.2M18.4 11.6l-1.6 1.2"/>',
    sun: '<circle cx="12" cy="12" r="3.8"/><path d="M12 3.5v2M12 18.5v2M3.5 12h2M18.5 12h2M6 6l1.4 1.4M16.6 16.6 18 18M6 18l1.4-1.4M16.6 7.4 18 6"/>',
    moon: '<path d="M18.5 14.5A7 7 0 0 1 9.5 5.5a7 7 0 1 0 9 9z"/>',
    install: '<rect x="4" y="4" width="16" height="13" rx="2.5"/><path d="M12 8v5m0 0-2.2-2.2M12 13l2.2-2.2"/><path d="M8 20h8"/>',
    bell: '<path d="M6.2 9.2a5.8 5.8 0 0 1 11.6 0c0 6.2 2.2 6.8 2.2 8.6H4c0-1.8 2.2-2.4 2.2-8.6z"/><path d="M10 18.8a2 2 0 0 0 4 0"/>',
    close: '<path d="M7 7l10 10M17 7 7 17"/>',
    lock: '<rect x="6" y="11" width="12" height="10" rx="2"/><path d="M8.5 11V8.2a3.5 3.5 0 0 1 7 0V11"/>',
    folder: '<path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H9l1.8 2H18.5A2.5 2.5 0 0 1 21 9.5v7A2.5 2.5 0 0 1 18.5 19h-13A2.5 2.5 0 0 1 3 16.5z"/>',
  };

  function ic(name, size, sw) {
    size = size || 18;
    sw = sw || 1.75;
    const p = ICONS[name] || "";
    return '<svg class="ic" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' + sw + '" stroke-linecap="round" stroke-linejoin="round">' + p + "</svg>";
  }
  function ring(size) {
    size = size || 16;
    return '<svg class="ic" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="7.5" stroke-dasharray="3.2 2.6"/></svg>';
  }
  const LEAFMARK = '<svg width="20" height="22" viewBox="0 0 20 22" aria-hidden="true"><path d="M10 21V12" stroke="#1B5E3B" stroke-width="1.8" stroke-linecap="round"/><path d="M10 13 C4 11 1.5 7 3 2.5 C6 1.5 9 3 10 6 C11 3 14 1.5 17 2.5 C18.5 7 16 11 10 13Z" fill="#1B5E3B"/><path d="M10 12V6" stroke="#E6EEE3" stroke-width="1" stroke-linecap="round" opacity=".7"/></svg>';

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function plant(stage, width) {
    const src = (window.PLANTS && window.PLANTS[stage]) || ("plants/" + stage + ".svg");
    const w = width ? 'width="' + width + '" style="width:' + width + 'px"' : "";
    return '<img class="plant" src="' + src + '" alt="money plant, ' + stage + '" ' + w + ">";
  }

  const GROW_STAGES = ["sprout", "early", "mid", "full"];

  function growingPlant(progress, width) {
    width = width || 480;
    const layers = GROW_STAGES.map(function (st) {
      return '<img class="plant-stage" data-stage="' + st + '" src="' + ((window.PLANTS && window.PLANTS[st]) || ("plants/" + st + ".svg")) + '" alt="" width="' + width + '">';
    }).join("");
    return '<div class="plant-grow" id="sess-plant" style="width:' + width + 'px" aria-label="money plant, sprout"><div class="plant-sway">' + layers + "</div></div>";
  }

  function sessionGrowProgress(ses) {
    if (!ses || ses.phase === "grace") return 0;
    const planned = ses.plannedMinutes * 60;
    const graceSec = GRACE_MS / 1000;
    const liveTotal = Math.max(1, planned - graceSec);
    const liveLeft = Math.max(0, ses.remainingSec);
    return Math.max(0, Math.min(1, (liveTotal - liveLeft) / liveTotal));
  }

  function patchGrowingPlant(progress) {
    const wrap = document.getElementById("sess-plant");
    if (!wrap) return;
    if (progress == null) progress = sessionGrowProgress(state.session);
    progress = Math.max(0, Math.min(1, progress));
    const stages = wrap.querySelectorAll(".plant-stage");
    const n = GROW_STAGES.length - 1;
    const x = progress * n;
    const i = Math.min(n, Math.floor(x + 1e-9));
    const f = x - i;
    for (let idx = 0; idx < stages.length; idx++) {
      let op = 0, sc = 0.94;
      if (idx === i && i === n) {
        op = 1; sc = 1;
      } else if (idx === i) {
        op = 1 - f;
        sc = 0.96 + 0.04 * (1 - f);
      } else if (idx === i + 1) {
        op = f;
        sc = 0.96 + 0.04 * f;
      }
      stages[idx].style.opacity = String(op);
      stages[idx].style.transform = "scale(" + sc.toFixed(4) + ")";
    }
    wrap.setAttribute("data-progress", progress.toFixed(3));
    const current = GROW_STAGES[Math.min(n, Math.round(x))];
    wrap.setAttribute("aria-label", "money plant, " + current);
  }

  function parseYMD(ymdStr) {
    const p = ymdStr.split("-").map(Number);
    return new Date(p[0], p[1] - 1, p[2]);
  }
  function ymd(dt) {
    const y = dt.getFullYear();
    const m = String(dt.getMonth() + 1).padStart(2, "0");
    const d = String(dt.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + d;
  }
  function startOfWeek(date) {
    const d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const day = d.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    d.setDate(d.getDate() + diff);
    return d;
  }
  function addDays(date, n) {
    const d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    d.setDate(d.getDate() + n);
    return d;
  }
  function sameDay(a, b) {
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
  }
  function fmtDayLong(dt) {
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return days[dt.getDay()] + " " + dt.getDate() + " " + months[dt.getMonth()];
  }
  function fmtDayShort(dt) {
    return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][dt.getDay()];
  }
  function fmtDateShort(dt) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return dt.getDate() + " " + months[dt.getMonth()];
  }
  function fmtWeekRange(mon, sun) {
    return "Mon " + mon.getDate() + " " + EN + " Sun " + sun.getDate() + " " + fmtDateShort(sun).split(" ")[1];
  }
  function fmtTime(dt) {
    const h = dt.getHours();
    const m = dt.getMinutes();
    const am = h < 12;
    const h12 = h % 12 || 12;
    return h12 + ":" + String(m).padStart(2, "0") + " " + (am ? "AM" : "PM");
  }
  function fmtMins(m) {
    m = Math.round(m);
    if (m <= 0) return "0m";
    const h = Math.floor(m / 60);
    const r = m % 60;
    if (h && r) return h + "h " + r + "m";
    if (h) return h + "h";
    return r + "m";
  }
  function fmtClock(totalSec) {
    totalSec = Math.max(0, Math.round(totalSec));
    const m = Math.floor(totalSec / 60);
    const s = totalSec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }
  function parseBox(str) {
    if (!str) return null;
    const t = String(str).trim().toLowerCase().replace(/,/g, " ");
    if (!t) return null;
    let hours = 0, mins = 0;
    const hm = t.match(/(\d+(?:\.\d+)?)\s*h/);
    const mm = t.match(/(\d+)\s*m/);
    if (hm) hours = parseFloat(hm[1]);
    if (mm) mins = parseInt(mm[1], 10);
    if (!hm && !mm) {
      const n = parseFloat(t);
      if (!isFinite(n) || n <= 0) return null;
      return n >= 10 ? Math.round(n) : Math.round(n * 60);
    }
    const total = Math.round(hours * 60 + mins);
    return total > 0 ? total : null;
  }
  function fmtBox(mins) {
    if (!mins) return "";
    return fmtMins(mins);
  }
  function protoNow() {
    const real = new Date();
    const d = parseYMD(state.protoDate);
    d.setHours(real.getHours(), real.getMinutes(), real.getSeconds(), real.getMilliseconds());
    return d;
  }
  function combineDateTime(ymdStr, hours, minutes) {
    const d = parseYMD(ymdStr);
    d.setHours(hours, minutes, 0, 0);
    return d;
  }

  let storageAvailable = true;

  function probeStorage() {
    try {
      const k = "__cadence_probe__";
      localStorage.setItem(k, "1");
      localStorage.removeItem(k);
      storageAvailable = true;
    } catch (e) {
      storageAvailable = false;
    }
  }
  function loadStore() {
    if (!storageAvailable) return null;
    try {
      const raw = localStorage.getItem(STORE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }
  // Simulated save status only. The prototype still writes to localStorage, not a OneDrive file.
  let saveFlashTimer = null;
  function flashSaving() {
    state.saveStatus = "saving";
    if (saveFlashTimer) clearTimeout(saveFlashTimer);
    saveFlashTimer = setTimeout(function () {
      state.saveStatus = "saved";
      saveFlashTimer = null;
      if (state.view !== "session") render();
    }, 700);
  }

  function saveStore() {
    if (state.useAnyway && !storageAvailable) return true;
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(snapshot()));
      state.saveFailed = false;
    state.saveStatus = "saved";
      flashSaving();
      return true;
    } catch (e) {
      state.saveFailed = true;
      return false;
    }
  }
  function snapshot() {
    return {
      version: 1,
      goals: state.goals,
      sessions: state.sessions,
      protoDate: state.protoDate,
      demoSpeed: state.demoSpeed,
      notifDismissed: state.notifDismissed,
      idSeq: state.idSeq,
    };
  }
  function uid(prefix) {
    state.idSeq = (state.idSeq || 0) + 1;
    return (prefix || "id") + state.idSeq;
  }

  let _exSeq = 0;
  function exampleSess(goalId, planned, day, hh, mm, status, reason, elapsed) {
    _exSeq += 1;
    const start = combineDateTime(day, hh, mm);
    const used = status === "finished" ? planned : (elapsed || 0);
    const end = new Date(start.getTime() + used * 60000);
    const names = { g1: "Write the weekly review", g2: "Deep work on the stack", g3: "Gym" };
    return {
      id: "ex" + _exSeq,
      goalId: goalId,
      goalName: names[goalId],
      plannedMinutes: planned,
      startedAt: start.toISOString(),
      endedAt: end.toISOString(),
      status: status,
      reason: reason || null,
      elapsedMinutes: used,
    };
  }
  function exampleData() {
    _exSeq = 0;
    const goals = [
      { id: "g1", name: "Write the weekly review", boxMinutes: 60 },
      { id: "g2", name: "Deep work on the stack", boxMinutes: 120 },
      { id: "g3", name: "Gym", boxMinutes: null },
    ];
    const sessions = [
      exampleSess("g1", 25, "2026-11-09", 8, 30, "finished"),
      exampleSess("g2", 50, "2026-11-09", 10, 0, "withered", "left-tab", 22),
      exampleSess("g1", 25, "2026-11-10", 8, 0, "finished"),
      exampleSess("g2", 50, "2026-11-10", 9, 30, "finished"),
      exampleSess("g1", 25, "2026-11-12", 8, 40, "finished"),
      exampleSess("g2", 50, "2026-11-12", 11, 18, "withered", "left-tab", 23),
      exampleSess("g2", 50, "2026-11-12", 14, 10, "finished"),
      exampleSess("g3", 25, "2026-11-12", 18, 5, "finished"),
      exampleSess("g3", 25, "2026-11-13", 8, 0, "finished"),
      exampleSess("g3", 50, "2026-11-14", 10, 0, "withered", "gave-up", 20),
      exampleSess("g3", 25, "2026-11-15", 18, 0, "finished"),
    ];
    return { goals: goals, sessions: sessions };
  }

  function namedGoals() {
    return state.goals.filter(function (g) { return g.name && g.name.trim(); });
  }
  function weekBounds(date) {
    const mon = startOfWeek(date);
    const sun = addDays(mon, 6);
    return { mon: mon, sun: sun };
  }
  function sessionDate(sess) {
    return new Date(sess.startedAt);
  }
  function inWeek(sess, mon, sun) {
    const d = sessionDate(sess);
    const day = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    return day >= mon && day <= sun;
  }
  function isFinished(sess) {
    return sess.status === "finished";
  }
  function finishedMins(sess) {
    return isFinished(sess) ? (sess.plannedMinutes || sess.elapsedMinutes || 0) : 0;
  }

  function weekStats() {
    const today = parseYMD(state.protoDate);
    const bounds = weekBounds(today);
    const mon = bounds.mon;
    const sun = bounds.sun;
    const sessions = state.sessions.filter(function (s) {
      return inWeek(s, mon, sun) && s.status !== "cancelled";
    });
    const goals = namedGoals();
    const finished = sessions.filter(isFinished);
    const withered = sessions.filter(function (s) { return s.status === "withered"; });
    const totalMins = finished.reduce(function (a, s) { return a + finishedMins(s); }, 0);
    const buckets = { morning: 0, afternoon: 0, evening: 0 };
    finished.forEach(function (s) {
      const h = sessionDate(s).getHours();
      if (h < 12) buckets.morning += finishedMins(s);
      else if (h < 17) buckets.afternoon += finishedMins(s);
      else buckets.evening += finishedMins(s);
    });
    const byGoal = goals.map(function (g) {
      const gs = sessions.filter(function (s) { return s.goalId === g.id; });
      const fin = gs.filter(isFinished);
      const wth = gs.filter(function (s) { return s.status === "withered"; });
      const mins = fin.reduce(function (a, s) { return a + finishedMins(s); }, 0);
      const todayFin = fin.filter(function (s) { return ymd(sessionDate(s)) === state.protoDate; });
      const todayW = wth.filter(function (s) { return ymd(sessionDate(s)) === state.protoDate; });
      const todayMins = todayFin.reduce(function (a, s) { return a + finishedMins(s); }, 0);
      const boxed = g.boxMinutes != null && g.boxMinutes > 0;
      const weekEnded = today >= sun;
      let hit, kind, badgeText;
      if (boxed) {
        hit = mins >= g.boxMinutes;
        if (hit) {
          kind = "met";
          badgeText = "Box met" + (weekEnded ? " " + MD + " hit" : "");
        } else if (!weekEnded) {
          kind = "prog";
          badgeText = fmtMins(g.boxMinutes - mins) + " to go";
        } else {
          kind = "short";
          badgeText = "Box not met " + MD + " not hit";
        }
      } else {
        hit = fin.length >= 1;
        if (hit) {
          kind = "hit";
          badgeText = weekEnded ? "Hit " + MD + " session finished" : "Hit";
        } else {
          kind = "not";
          badgeText = "Not yet";
        }
      }
      return { goal: g, sessions: gs, fin: fin, wth: wth, mins: mins, todayMins: todayMins, todayW: todayW.length, boxed: boxed, hit: hit, kind: kind, badgeText: badgeText, weekEnded: weekEnded };
    });
    const hits = byGoal.filter(function (x) { return x.hit; }).length;
    const days = [];
    for (let i = 0; i < 7; i++) {
      const d = addDays(mon, i);
      const key = ymd(d);
      const isAhead = d > today;
      const daySess = sessions.filter(function (s) { return ymd(sessionDate(s)) === key; });
      const dayFin = daySess.filter(isFinished);
      const mins = dayFin.reduce(function (a, s) { return a + finishedMins(s); }, 0);
      days.push({ date: d, key: key, isAhead: isAhead, sessions: daySess, mins: mins, isToday: key === state.protoDate });
    }
    return { mon: mon, sun: sun, today: today, sessions: sessions, finished: finished, withered: withered, totalMins: totalMins, buckets: buckets, byGoal: byGoal, hits: hits, goals: goals, days: days };
  }

  function todaySessions() {
    return state.sessions
      .filter(function (s) { return ymd(sessionDate(s)) === state.protoDate && s.status !== "cancelled"; })
      .sort(function (a, b) { return new Date(a.startedAt) - new Date(b.startedAt); });
  }

  const state = {
    view: "today",
    goals: [],
    sessions: [],
    protoDate: DEFAULT_TODAY,
    demoSpeed: true,
    notifDismissed: false,
    notifDenied: false,
    storageBlocked: false,
    useAnyway: false,
    saveFailed: false,
    saveStatus: "saved",
    idSeq: 0,
    selectedGoalId: null,
    selectedDur: 25,
    session: null,
    endInfo: null,
    addingBoxFor: null,
  };

  let tickTimer = null;

  function defaultState() {
    state.view = "today";
    state.goals = [];
    state.sessions = [];
    state.protoDate = DEFAULT_TODAY;
    state.demoSpeed = true;
    state.notifDismissed = false;
    state.saveFailed = false;
    state.idSeq = 0;
    state.selectedGoalId = null;
    state.selectedDur = 25;
    state.session = null;
    state.endInfo = null;
    state.addingBoxFor = null;
  }

  function hydrate() {
    probeStorage();
    if (!storageAvailable) {
      state.storageBlocked = true;
      defaultState();
      return;
    }
    const data = loadStore();
    defaultState();
    if (data && data.version === 1) {
      state.goals = data.goals || [];
      state.sessions = data.sessions || [];
      state.protoDate = data.protoDate || DEFAULT_TODAY;
      state.demoSpeed = data.demoSpeed !== false;
      state.notifDismissed = !!data.notifDismissed;
      state.idSeq = data.idSeq || 0;
    }
  }

  function chrome(title) {
    return '<div class="chrome"><div class="lights"><i></i><i></i><i></i></div><div class="url">' + ic("device", 14) + " Cadence " + MD + " " + esc(title) + '</div><button class="inst" type="button" data-act="install" title="This is a prototype">' + ic("install", 15) + " Install Cadence</button></div>";
  }
  function wordmark() {
    return '<div class="word cad">' + LEAFMARK + "Cadence</div>";
  }
  function demoToggle() {
    const on = state.demoSpeed;
    return '<button type="button" class="demo ' + (on ? "on" : "") + '" data-act="toggle-demo" aria-pressed="' + (on ? "true" : "false") + '" title="When on, a 25-minute session runs in about 25 seconds. The 10-second cancel stays real."><span>Demo speed</span><span class="sw" aria-hidden="true"><b></b></span><span class="hint">' + (on ? "on " + MD + " 25 min in ~25s" : "off " + MD + " real time") + "</span></button>";
  }
  function tabs(active, right) {
    const items = [["today", "Today", "today"], ["focus", "Focus", "pick"], ["week", "Week", "week"]];
    const t = items.map(function (it) {
      const k = it[0], v = it[1], view = it[2];
      const on = (k === "today" && (active === "today" || active === "grove")) || (k === "focus" && (active === "pick" || active === "session" || active === "end")) || (k === "week" && active === "week");
      return '<button type="button" class="' + (on ? "on" : "") + '" data-act="nav" data-view="' + view + '">' + ic(k, 19) + v + "</button>";
    }).join("");
    return '<div class="lbar">' + wordmark() + '<div class="ltabs">' + t + '</div><div class="rightmeta">' + demoToggle() + '<div class="date">' + (right || esc(fmtDayLong(parseYMD(state.protoDate)))) + "</div></div></div>";
  }
  function focusTop(right) {
    return '<div class="lbar" style="position:absolute;left:64px;right:64px;top:0;z-index:4">' + wordmark() + '<div class="rightmeta">' + demoToggle() + '<div class="date" style="font-size:16px">' + (right || "") + "</div></div></div>";
  }
  function panes(a, b) {
    return '<div class="pane" style="left:' + a + 'px"></div><div class="pane" style="left:' + b + 'px"></div>';
  }
  function badge(kind, text) {
    const icon = (kind === "met" || kind === "hit") ? ic("check", 13) : ring(14);
    return '<span class="badge b-' + kind + '"><span class="dotc">' + icon + "</span>" + esc(text) + "</span>";
  }
  function pbar(done, box) {
    if (!box) return "";
    if (done >= box) {
      const left = (box / done) * 100;
      return '<div class="pbar over"><i style="width:100%"></i><span class="boxmark" style="left:' + left.toFixed(1) + '%"></span></div>';
    }
    const pct = (done / box) * 100;
    return '<div class="pbar"><i style="width:' + pct.toFixed(1) + '%"></i><span class="gap" style="left:' + pct.toFixed(1) + '%;right:0"></span></div>';
  }
  function saveStatusHtml() {
    if (state.saveStatus === "saving") {
      return '<span class="save-status saving">' + ic("folder", 14) + " Saving…</span>";
    }
    return '<span class="save-status saved">' + ic("check", 14) + " Saved " + MD + " OneDrive folder</span>";
  }
  function honestFoot() {
    return ic("folder", 15) + " Saved on this laptop, in your OneDrive folder. Friday can read your goals and scorecard.";
  }
  function footline(right) {
    return '<div class="footline">' + saveStatusHtml() + '<span class="links"><button type="button" class="btn text" data-act="load-example" style="height:auto;font-size:13.5px">Load example week</button><button type="button" class="reset" data-act="reset" style="font-size:13.5px;color:var(--text-muted)">Reset prototype</button>' + (right ? "<span>" + right + "</span>" : "") + "</span></div>";
  }

  function viewToday() {
    const named = namedGoals();
    const empty = named.length === 0;
    const stats = weekStats();
    const todayS = todaySessions();
    const list = state.goals.length ? state.goals : [{ id: "tmp-first", name: "", boxMinutes: null }];
    const labelL = named.length <= 1 && empty ? "Goal" : "Goals";
    let ghtml = '<div class="lbls"><span class="label">' + labelL + '</span><span class="label" style="text-align:right">Weekly time box ' + MD + " optional</span></div>";
    list.forEach(function (g, i) {
      const isPh = !g.name;
      const adding = state.addingBoxFor === g.id;
      const hasBox = g.boxMinutes != null && g.boxMinutes > 0;
      let tb;
      if (hasBox || adding || isPh) {
        const val = hasBox ? fmtBox(g.boxMinutes) : "";
        const ph = isPh || !hasBox ? "e.g. 2h" : "";
        tb = '<div class="field tb tab ' + (isPh && !val ? "ph" : "") + '"><input data-act="edit-box" data-id="' + g.id + '" value="' + esc(val) + '" placeholder="' + ph + '" aria-label="Weekly time box"></div>';
      } else {
        tb = '<button type="button" class="addtb" data-act="add-box" data-id="' + g.id + '">Add time box</button>';
      }
      const remove = isPh ? "" : '<button type="button" class="row-x" data-act="remove-goal" data-id="' + g.id + '" aria-label="Remove goal">&times;</button>';
      ghtml += '<div class="grow"><div class="field ' + (isPh ? "ph focus" : "") + '"><span class="num">' + (i + 1) + '</span><input data-act="edit-goal" data-id="' + g.id + '" value="' + esc(g.name || "") + '" placeholder="A goal for today" aria-label="Goal ' + (i + 1) + '">' + remove + "</div>" + tb + "</div>";
    });
    if ((named.length >= 1 || empty) && (state.goals.length < 8)) {
      ghtml += '<button type="button" class="btn text" style="align-self:flex-start;margin-top:2px" data-act="add-goal">' + ic("plus", 20) + " Add a goal</button>";
    }
    if (named.length >= 3) {
      ghtml += '<div class="enough">' + ic("check", 18) + " Three goals " + EM + " plenty for one day.</div>";
    }
    const rule = empty
      ? '<div class="rulebox" style="margin-top:28px">' + ic("check", 18) + "<div>Sessions are saved on this laptop, in your OneDrive folder. A plant grows when you finish, and withers if you leave or give up " + EM + " except in the first 10 seconds.</div></div>"
      : '<div class="rulebox" style="margin-top:10px">' + ic("check", 18) + "<div><b>Time box:</b> hit when finished sessions reach it. <b>No time box:</b> hit when one session is finished. Withered sessions don" + AP + "t count.</div></div>";
    const sub = empty ? "Add a goal to begin " + EM + " something you want to sit with." : "What matters today?";
    const foot = honestFoot();

    let right;
    if (empty) {
      right = '<div class="stageR" style="flex:1"><div class="glow"></div><div class="sill"></div>' + plant("sprout", 300) + '</div><p class="cap" style="font-size:15px;text-align:center;padding:16px 0 18px;color:var(--text-muted)">Your first plant starts as a seedling. It grows when you finish a session.</p>';
    } else {
      const todayD = parseYMD(state.protoDate);
      const mon = stats.mon;
      let rangeLabel;
      if (sameDay(todayD, mon) && todayS.length === 0) {
        rangeLabel = "This week so far";
      } else if (todayS.length === 0 && todayD > mon) {
        const yest = addDays(todayD, -1);
        rangeLabel = "This week so far " + MD + " " + fmtDayShort(mon) + " " + EN + " " + fmtDayShort(yest);
      } else {
        rangeLabel = "This week so far " + MD + " " + fmtDayShort(mon) + " " + EN + " " + fmtDayShort(todayD);
      }
      const so = stats.byGoal.map(function (g) {
        if (g.boxed) {
          return '<div class="wsrow"><span class="n">' + esc(g.goal.name) + '</span><span class="v tab">' + fmtMins(g.mins) + " / " + fmtMins(g.goal.boxMinutes) + " box</span>" + pbar(g.mins, g.goal.boxMinutes) + "</div>";
        }
        return '<div class="wsrow"><span class="n">' + esc(g.goal.name) + ' <span class="v" style="font-weight:500">' + MD + " no time box</span></span>" + badge(g.kind, g.badgeText) + "</div>";
      }).join("");
      const sillMsg = todayS.length
        ? '<p class="cap" style="font-size:15px;text-align:center;padding:16px 0 18px;color:var(--text-muted)"><button type="button" class="btn text" data-act="nav" data-view="grove" style="font-size:15px">See today' + AP + "s grove</button></p>"
        : '<p class="cap" style="font-size:15px;text-align:center;padding:16px 0 18px;color:var(--text-muted)">Today' + AP + "s sill is empty. Your first plant grows here.</p>";
      right = '<div class="panel" style="padding:22px 26px 24px;position:relative;z-index:3;width:520px"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="label">' + rangeLabel + '</span><span class="cap">Finished sessions only</span></div><div class="wsofar">' + so + '</div></div><div class="stageR"><div class="glow"></div><div class="sill"></div>' + plant("sprout", 270) + "</div>" + sillMsg;
    }
    const dialog = "";
    return '<div class="win">' + dialog + chrome("Today") + '<div class="light"></div>' + panes(900, 1130) + '<div class="lap">' + tabs("today") + '<div class="l1 ' + (empty ? "l0" : "") + '"><div class="panel left"><h1 class="title" style="font-size:44px">Good morning.</h1><p class="sub" style="font-size:19px">' + sub + '</p><div class="goals" style="margin-top:28px">' + ghtml + "</div>" + rule + '<div style="margin-top:auto"><button class="btn primary" style="height:58px" data-act="nav" data-view="pick"' + (named.length ? "" : " disabled") + '>Start focusing</button><div class="foot" style="margin-top:8px">' + foot + "</div></div></div><div class=\"right\">" + right + "</div></div>" + footline() + "</div></div>";
  }

  function sessionCard(sess) {
    const st = sess.status === "withered" ? "withered" : "full";
    const t = fmtTime(new Date(sess.startedAt));
    const found = state.goals.find(function (x) { return x.id === sess.goalId; });
    const g = sess.goalName || (found && found.name) || "Goal";
    let d = sess.plannedMinutes + " min";
    if (sess.status === "withered") {
      const left = sess.elapsedMinutes || 0;
      const leftLabel = left < 1 ? "<1 min" : Math.round(left) + " min";
      d = sess.plannedMinutes + " min " + MD + " left at " + leftLabel;
    }
    const o = sess.status === "withered" ? "Left" : "Grew";
    return '<div class="pot ' + (sess.status === "withered" ? "w" : "") + '">' + plant(st) + '<div class="t tab">' + t + '</div><div class="g">' + esc(g) + '</div><div class="d tab">' + d + '</div><div class="o"><i></i>' + o + "</div></div>";
  }

  function viewPick() {
    const named = namedGoals();
    if (!named.length) return viewToday();
    if (!state.selectedGoalId || !named.some(function (g) { return g.id === state.selectedGoalId; })) {
      state.selectedGoalId = named[0].id;
    }
    const stats = weekStats();
    const todayS = todaySessions();
    const todayFin = todayS.filter(isFinished);
    const todayW = todayS.filter(function (s) { return s.status === "withered"; });
    const todayMins = todayFin.reduce(function (a, s) { return a + finishedMins(s); }, 0);
    const cards = named.map(function (g) {
      const gs = stats.byGoal.find(function (x) { return x.goal.id === g.id; });
      let meta;
      if (g.boxMinutes) {
        meta = fmtMins(g.boxMinutes) + " box " + MD + " " + fmtMins(gs ? gs.mins : 0) + " finished this week";
      } else {
        meta = "No time box " + MD + " one finished session hits it";
      }
      const sel = g.id === state.selectedGoalId;
      const b = gs ? badge(gs.kind, gs.badgeText) : "";
      return '<button type="button" class="gcard ' + (sel ? "sel" : "") + '" data-act="pick-goal" data-id="' + g.id + '"><span class="r">' + (sel ? ic("check", 14) : "") + '</span><div><div class="g">' + esc(g.name) + '</div><div class="m">' + meta + "</div></div>" + b + "</button>";
    }).join("");
    const durs = DURS.map(function (d) {
      const sel = d.min === state.selectedDur;
      return '<button type="button" class="dur ' + (sel ? "sel" : "") + '" data-act="pick-dur" data-min="' + d.min + '"><b class="tab">' + d.min + "<small>min</small></b><span>" + d.label + "</span></button>";
    }).join("");
    const goal = named.find(function (g) { return g.id === state.selectedGoalId; });
    const gs = stats.byGoal.find(function (x) { return x.goal.id === goal.id; });
    const start = protoNow();
    const end = new Date(start.getTime() + state.selectedDur * 60000);
    let would = "";
    if (goal.boxMinutes) {
      const next = (gs ? gs.mins : 0) + state.selectedDur;
      would = "Would bring it to " + fmtMins(next) + " / " + fmtMins(goal.boxMinutes);
    }
    const summary = "<b>" + esc(goal.name) + "</b> " + MD + " " + state.selectedDur + " min " + MD + " ends " + fmtTime(end);
    const pots = todayS.map(sessionCard).join("");
    const tallyChip = todayW.length ? '<span class="chip w">' + todayW.length + " withered</span>" : "";
    const deskPots = todayS.length
      ? '<div style="position:relative;padding-bottom:30px"><div class="sill" style="top:auto;bottom:118px;left:-40px;right:-40px;height:24px"></div><div class="pots2">' + pots + "</div></div>"
      : '<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end"><div class="stageR" style="width:100%"><div class="glow"></div><div class="sill"></div>' + plant("sprout", 220) + '</div><p class="cap" style="padding:16px 0 24px">No sessions yet today.</p></div>';
    return '<div class="win">' + chrome("Focus") + '<div class="light"></div>' + panes(260, 480) + '<div class="lap">' + tabs("pick", fmtDayLong(parseYMD(state.protoDate)) + " " + MD + " " + fmtTime(protoNow())) + '<div class="l2"><div class="desk"><span class="label">Today so far</span><div class="tally" style="margin-top:4px"><span class="big tab" style="font-size:44px">' + fmtMins(todayMins) + '</span><span class="lbl">focused</span>' + tallyChip + '</div><div style="flex:1"></div>' + deskPots + '</div><div class="panel sheet"><h1 class="title" style="font-size:34px">What will you sit with?</h1><div class="gcards" style="margin-top:20px">' + cards + '</div><div class="label" style="margin-top:24px">For how long?</div><div class="durs">' + durs + '</div><div style="margin-top:auto"><div class="rulebox" style="margin-bottom:14px;justify-content:space-between;align-items:center"><span>' + summary + '</span><span class="cap" style="font-size:14px">' + would + '</span></div><button class="btn primary" style="height:60px;font-size:18px" data-act="start">Start</button><p class="cap" style="text-align:center;margin-top:12px;font-size:14px">You can cancel in the first 10 seconds ' + EM + " no plant will wither.</p></div></div></div>" + footline() + "</div></div>";
  }

  function notifBanner() {
    if (!state.notifDenied || state.notifDismissed) return "";
    return '<div class="banner" role="status"><div class="ico">' + ic("bell", 18) + '</div><div class="bbody"><div class="bt">Cadence can' + AP + 't ping you when this session ends.</div><div class="bm">The session itself is fine. To allow notifications, click the lock icon in the address bar, then switch notifications on.</div></div><button class="dismiss" type="button" data-act="dismiss-notif" aria-label="Dismiss">' + ic("close", 16) + " Dismiss</button></div>";
  }

  function viewSession() {
    const ses = state.session;
    if (!ses) return viewPick();
    const inGrace = ses.phase === "grace";
    const remaining = ses.remainingSec;
    const planned = ses.plannedMinutes * 60;
    const elapsed = planned - remaining;
    const started = new Date(ses.startedAt);
    const ends = new Date(started.getTime() + ses.plannedMinutes * 60000);
    const timer = fmtClock(remaining);
    const of = inGrace
      ? "of " + fmtClock(planned) + " " + MD + " started " + fmtTime(started)
      : "remaining of " + fmtClock(planned) + " " + MD + " ends " + fmtTime(ends);
    const graceLeft = Math.max(0, Math.ceil((GRACE_MS - (performance.now() - ses.graceOrigin)) / 1000));
    const gracePct = Math.min(100, ((performance.now() - ses.graceOrigin) / GRACE_MS) * 100);
    const progressPct = Math.min(100, (elapsed / planned) * 100);
    const growP = sessionGrowProgress(ses);
    let ctl;
    if (inGrace) {
      ctl = '<div style="margin-top:30px;display:flex;align-items:center;gap:14px"><div class="lprog" style="width:200px;margin:0;height:5px"><i style="width:' + gracePct + '%;background:var(--text-muted);opacity:.6"></i></div><span id="grace-label" style="font-size:17px;font-weight:600;color:var(--text)" class="tab">' + graceLeft + 's to cancel freely</span></div><div class="btnrow" style="margin-top:20px"><button class="btn outline" style="height:56px;font-size:18px;padding:0 40px" data-act="cancel">Cancel</button></div><div class="note">' + ic("check", 17) + " No plant will wither</div>";
    } else {
      ctl = '<div class="lprog"><i id="sess-bar" style="width:' + progressPct.toFixed(1) + '%"></i></div><div class="btnrow"><button class="btn outline" style="height:52px;font-size:17px;padding:0 30px;color:var(--text-muted)" data-act="give-up">Give up</button></div><div class="note" style="margin-top:6px">' + ic("tab", 17) + " Leaving this tab also ends the session.</div>";
    }
    const banner = notifBanner();
    const bannerWrap = banner ? '<div style="margin-bottom:22px">' + banner + "</div>" : "";
    return '<div class="win">' + chrome("Focusing") + '<div class="light"></div>' + panes(240, 470) + '<div class="lap" style="padding:0">' + focusTop() + '<div class="split"><div class="sill" style="left:0;right:0;bottom:64px;height:28px"></div><div class="stagecol"><div class="glow"></div>' + growingPlant(growP, 480) + '</div><div class="info">' + bannerWrap + '<div class="eyebrow">Focusing on</div><div class="gname">' + esc(ses.goalName) + '</div><div class="bigtimer tab" id="sess-timer">' + timer + '</div><div class="lap-of tab" id="sess-of">' + of + "</div>" + ctl + "</div></div></div></div>";
  }

  function viewEnd() {
    const info = state.endInfo;
    if (!info) return viewToday();
    if (info.status === "finished") return viewHealthy(info);
    return viewWithered(info);
  }

  function viewHealthy(info) {
    const stats = weekStats();
    const gs = stats.byGoal.find(function (x) { return x.goal.id === info.goalId; });
    const ended = new Date(info.endedAt);
    let mini = "";
    if (gs && gs.boxed && !state.saveFailed) {
      mini = '<div class="mini"><div class="row"><span>' + esc(info.goalName) + '</span><span class="v tab">' + fmtMins(gs.mins) + " / " + fmtMins(gs.goal.boxMinutes) + ' box</span></div><div style="margin:12px 0 10px">' + pbar(gs.mins, gs.goal.boxMinutes) + '</div><div class="row"><span class="v">+' + fmtMins(info.plannedMinutes) + " this session</span>" + badge(gs.kind, gs.badgeText + (gs.kind === "prog" ? " this week" : "")) + "</div></div>";
    } else if (gs && !state.saveFailed) {
      mini = '<div class="mini"><div class="row"><span>' + esc(info.goalName) + "</span>" + badge(gs.kind, gs.badgeText) + '</div><div class="row" style="margin-top:10px"><span class="v">No time box ' + MD + " " + fmtMins(gs.mins) + " finished this week</span></div></div>";
    }
    const sub = state.saveFailed
      ? "It will join today" + AP + "s grove once this session is saved."
      : "It joins today" + AP + "s grove.";
    const alert = state.saveFailed
      ? '<div class="alert" role="alert"><h2>We couldn' + AP + 't save this session.</h2><p>The plant is still here. Try saving again ' + EM + " nothing has been thrown away.</p></div>"
      : mini;
    const actions = state.saveFailed
      ? '<div class="btnrow"><button class="btn primary" style="height:56px" data-act="retry-save">Try saving again</button><button class="btn outline" style="height:56px" data-act="nav" data-view="grove">See today' + AP + "s grove</button></div>"
      : '<div class="btnrow"><button class="btn primary" style="height:56px" data-act="nav" data-view="grove">See today' + AP + 's grove</button><button class="btn outline" style="height:56px" data-act="nav" data-view="pick">Start another</button></div>';
    return '<div class="win">' + chrome("Session finished") + '<div class="light"></div>' + panes(240, 470) + '<div class="lap" style="padding:0">' + focusTop() + '<div class="split"><div class="sill" style="left:0;right:0;bottom:64px;height:28px"></div><div class="stagecol"><div class="glow"></div>' + plant("full", 480) + '</div><div class="info" style="padding-right:64px"><div class="endtitle">This plant is yours.</div><div class="endmeta tab">' + esc(info.goalName) + " " + MD + " " + info.plannedMinutes + " minutes " + MD + " finished " + fmtTime(ended) + '</div><div class="endsub2">' + sub + "</div>" + alert + actions + "</div></div></div></div>";
  }

  function viewWithered(info) {
    const reason = info.reason === "gave-up" ? "You gave up." : "You left the tab.";
    const icon = info.reason === "gave-up" ? ic("hand", 18) : ic("tab", 18);
    const started = new Date(info.startedAt);
    const ended = new Date(info.endedAt);
    const left = Math.round(info.elapsedMinutes || 0);
    const g = state.goals.find(function (x) { return x.id === info.goalId; });
    const boxNote = (g && g.boxMinutes)
      ? "Withered time doesn" + AP + "t count toward hours or the " + fmtMins(g.boxMinutes) + " box."
      : "Withered time doesn" + AP + "t count toward hours.";
    return '<div class="win wpage">' + chrome("Session ended") + '<div class="light"></div>' + panes(240, 470) + '<div class="lap" style="padding:0">' + focusTop() + '<div class="split"><div class="sill" style="left:0;right:0;bottom:64px;height:28px"></div><div class="stagecol"><div class="glow"></div>' + plant("withered", 480) + '</div><div class="info" style="padding-right:64px"><div class="endtitle">This plant withered.</div><div class="endmeta tab">' + esc(info.goalName) + " " + MD + " " + info.plannedMinutes + "-minute session<br>Started " + fmtTime(started) + " " + MD + " ended " + fmtTime(ended) + ", after " + left + ' min</div><div class="reason2">' + icon + reason + '</div><div class="endsub2">It' + AP + "s still in today" + AP + "s grove " + EM + ' an honest record.</div><div class="note">' + ring(17) + " " + boxNote + '</div><div class="btnrow"><button class="btn primary" style="height:56px" data-act="nav" data-view="pick">Try again</button><button class="btn outline" style="height:56px" data-act="nav" data-view="grove">See today' + AP + "s grove</button></div></div></div></div></div>";
  }

  function viewGrove() {
    const todayS = todaySessions();
    const stats = weekStats();
    const todayFin = todayS.filter(isFinished);
    const todayW = todayS.filter(function (s) { return s.status === "withered"; });
    const todayMins = todayFin.reduce(function (a, s) { return a + finishedMins(s); }, 0);
    const empty = todayS.length === 0;
    const side = stats.byGoal.map(function (g) {
      if (g.boxed) {
        const todayBit = g.todayMins ? fmtMins(g.todayMins) + " today" : "none today";
        const w = g.todayW ? ", " + g.todayW + " withered" : "";
        return '<div class="gst"><div class="top2"><span class="n">' + esc(g.goal.name) + "</span>" + badge(g.kind, g.badgeText) + '</div><div style="margin-top:12px">' + pbar(g.mins, g.goal.boxMinutes) + '</div><div class="v tab">' + fmtMins(g.mins) + " / " + fmtMins(g.goal.boxMinutes) + " box " + MD + " " + todayBit + w + "</div></div>";
      }
      const line = g.todayMins
        ? "No time box " + MD + " one session finished today (" + fmtMins(g.todayMins) + ")"
        : (g.mins ? "No time box " + MD + " " + fmtMins(g.mins) + " finished this week" : "No time box " + MD + " no finished session this week");
      return '<div class="gst"><div class="top2"><span class="n">' + esc(g.goal.name) + "</span>" + badge(g.kind, g.badgeText) + '</div><div class="v tab" style="margin-top:10px">' + line + "</div></div>";
    }).join("");
    let tallyNum, tallyLbl;
    if (empty) {
      tallyNum = "0m";
      tallyLbl = "focused " + MD + " no sessions yet";
    } else {
      tallyNum = fmtMins(todayMins);
      tallyLbl = todayW.length ? "focused " + MD + " " + todayW.length + " withered" : "focused";
    }
    const sill = empty
      ? '<div class="empty-sill">' + plant("empty", 240) + '<div class="sill" style="position:relative;left:0;right:0;bottom:auto;top:auto;height:24px;width:100%"></div><p class="cap" style="font-size:15px;text-align:center;padding:20px 0 18px;position:relative;z-index:2">Today' + AP + "s sill is empty. Start a session when you" + AP + "re ready.</p></div>"
      : '<div class="sill" style="bottom:118px;left:0;right:0;top:auto;height:24px"></div><div class="pots4">' + todayS.map(sessionCard).join("") + "</div>";
    const timeBit = todayS.length ? " " + MD + " " + fmtTime(protoNow()) : "";
    return '<div class="win">' + chrome("Today") + '<div class="light"></div>' + panes(560, 800) + '<div class="lap">' + tabs("grove", fmtDayLong(parseYMD(state.protoDate)) + timeBit) + '<div class="l7 ' + (empty ? "l7e" : "") + '"><div class="sillp"><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><h1 class="title" style="font-size:40px">Today' + AP + 's grove</h1><div class="tally" style="margin-top:12px"><span class="big tab" style="font-size:60px">' + tallyNum + '</span><span class="lbl" style="font-size:20px">' + tallyLbl + '</span></div></div><button class="btn primary" style="width:auto;padding:0 26px;height:50px" data-act="nav" data-view="pick">Start a session</button></div>' + sill + '</div><div class="panel gside"><span class="label">Goals this week, as of today</span>' + side + '<div class="rulebox" style="margin-top:auto">' + ic("check", 18) + "<div><b>Time box:</b> hit only when the box is met. <b>No time box:</b> hit when one session is finished. Hours count only finished sessions.</div></div></div></div>" + footline() + "</div></div>";
  }

  function shortName(n) {
    const low = n.toLowerCase();
    if (low.indexOf("write") === 0 || low.indexOf("review") !== -1) return "Review";
    if (low.indexOf("deep") === 0) return "Deep work";
    return n.split(" ")[0];
  }

  function viewWeek() {
    const stats = weekStats();
    const empty = stats.sessions.length === 0;
    const weekEnded = stats.today >= stats.sun;
    const dots = stats.byGoal.map(function (g) {
      return '<i class="' + (g.hit ? "" : "no") + '">' + (g.hit ? ic("check", 13) : "") + "</i>";
    }).join("");
    const nGoals = stats.goals.length;
    const hitLine = nGoals ? (stats.hits + " of " + nGoals + " goals hit") : "No goals yet";
    let status;
    if (empty) {
      status = '<div style="font-size:15px;margin-top:12px;line-height:1.4;color:var(--text-muted)">No finished sessions this week yet.</div>';
    } else {
      const bits = [];
      const short = [];
      stats.byGoal.forEach(function (g) {
        if (g.kind === "met") bits.push(shortName(g.goal.name) + " box met.");
        else if (g.kind === "hit") bits.push(shortName(g.goal.name) + " hit.");
        else if (g.kind === "short") short.push('<span style="color:var(--wither-ink);font-weight:700">' + esc(shortName(g.goal.name)) + " " + fmtMins(g.goal.boxMinutes - g.mins) + " short of its " + fmtMins(g.goal.boxMinutes) + " box.</span>");
      });
      status = '<div style="font-size:15px;margin-top:12px;line-height:1.4">' + esc(bits.join(" ")) + (short.length ? "<br>" + short.join("<br>") : "") + "</div>";
    }
    const cap = stats.finished.length + " plant" + (stats.finished.length === 1 ? "" : "s") + " grew " + MD + " " + stats.withered.length + " withered";
    const cards = stats.byGoal.map(function (g) {
      if (g.boxed) {
        let why;
        if (g.hit) why = "Finished sessions reached the box (+" + fmtMins(g.mins - g.goal.boxMinutes) + " over).";
        else if (g.mins === 0) why = "No finished sessions yet this week.";
        else why = '<b style="color:var(--wither-ink)">' + fmtMins(g.goal.boxMinutes - g.mins) + " short.</b> " + g.wth.length + " withered session" + (g.wth.length === 1 ? "" : "s") + " didn" + AP + "t count.";
        return '<div class="gc3 ' + (g.kind === "short" ? "short" : "") + '"><span class="n">' + esc(g.goal.name) + "</span><div>" + badge(g.kind, g.badgeText) + '</div><div class="num2 tab">' + fmtMins(g.mins) + " <small>/ " + fmtMins(g.goal.boxMinutes) + ' box</small></div><div style="margin-top:14px">' + pbar(g.mins, g.goal.boxMinutes) + '</div><div class="why">' + why + "</div></div>";
      }
      const why = "No box: hit once one session is finished. Needed 1 " + MD + " has " + g.fin.length + ".";
      const pills = g.fin.length ? '<div class="pills">' + g.fin.map(function () { return "<span></span>"; }).join("") + "</div>" : "";
      const noBoxNum = (g.mins > 0 && g.mins < 120) ? (Math.round(g.mins) + "m") : fmtMins(g.mins);
      return '<div class="gc3"><span class="n">' + esc(g.goal.name) + ' <span style="font-weight:500;color:var(--text-muted)">' + MD + " no time box</span></span><div>" + badge(g.kind, g.badgeText) + '</div><div class="num2 tab">' + noBoxNum + " <small>finished" + (g.fin.length ? " " + MD + " " + g.fin.length + " session" + (g.fin.length === 1 ? "" : "s") : "") + "</small></div>" + pills + '<div class="why">' + why + "</div></div>";
    }).join("");
    const maxB = Math.max(stats.buckets.morning, stats.buckets.afternoon, stats.buckets.evening, 1);
    const anyB = stats.buckets.morning + stats.buckets.afternoon + stats.buckets.evening;
    const tcols = [
      ["Morning", stats.buckets.morning, "sunrise"],
      ["Afternoon", stats.buckets.afternoon, "sun"],
      ["Evening", stats.buckets.evening, "moon"],
    ].map(function (row) {
      const name = row[0], mins = row[1], icn = row[2];
      const best = anyB && mins === maxB && mins > 0;
      const h = anyB ? Math.max(22, Math.round((mins / maxB) * 118)) : 22;
      const bg = anyB ? "" : "background:var(--track)";
      return '<div class="tcol ' + (best ? "best" : "") + '"><div class="b" style="height:' + h + "px;" + bg + '"></div><div class="n" style="font-size:15px">' + ic(icn, 17) + name + '</div><div class="v tab" style="font-size:14px">' + (anyB ? fmtMins(mins) : EM) + "</div></div>";
    }).join("");
    const bestName = !anyB ? null : ["morning", "afternoon", "evening"].sort(function (a, b) { return stats.buckets[b] - stats.buckets[a]; })[0];
    const bestTitle = bestName ? "Best time: " + bestName + "s" : "Best time";
    const bestCap = anyB
      ? "Mornings before noon " + MD + " afternoons noon" + EN + "5 PM " + MD + " evenings after 5 PM"
      : "We" + AP + "ll see your best time after a few sessions.";
    const weighted = stats.days.some(function (d) { return d.sessions.length >= 3; });
    const cols = stats.days.map(function (d) {
      if (d.isAhead) {
        return '<div class="d7"><div class="st rest"><span class="rest" style="font-size:14px;width:100%;text-align:center">Ahead</span></div><div class="dn">' + fmtDayShort(d.date) + '</div><div class="dd tab">' + fmtDateShort(d.date) + '</div><div class="dm z">' + EM + "</div></div>";
      }
      if (d.sessions.length === 0) {
        if (!empty && !d.isToday) {
          return '<div class="d7"><div class="st rest"><span class="rest" style="font-size:14px;width:100%;text-align:center">Rest day</span></div><div class="dn">' + fmtDayShort(d.date) + '</div><div class="dd tab">' + fmtDateShort(d.date) + '</div><div class="dm z">' + EM + "</div></div>";
        }
        return '<div class="d7"><div class="st">' + plant("empty") + '</div><div class="dn">' + fmtDayShort(d.date) + '</div><div class="dd tab">' + fmtDateShort(d.date) + '</div><div class="dm z">' + EM + "</div></div>";
      }
      const pl = d.sessions.map(function (s) { return plant(s.status === "withered" ? "withered" : "full"); }).join("");
      const mm = d.mins > 0 ? fmtMins(d.mins) : "0m";
      const z = d.mins > 0 ? "" : "z";
      return '<div class="d7"><div class="st">' + pl + '</div><div class="dn">' + fmtDayShort(d.date) + '</div><div class="dd tab">' + fmtDateShort(d.date) + '</div><div class="dm tab ' + z + '">' + mm + "</div></div>";
    }).join("");
    const groveCap = empty
      ? "Your first week starts here. " + fmtDayShort(addDays(stats.today, 1)) + " to Sunday are still ahead."
      : "Withered sessions stay visible. Hours count only finished sessions.";
    const footNote = empty ? "first week, no sessions yet" : (weekEnded ? "a full week shown so every day has data" : "");
    const heroNum = empty ? "0m" : fmtMins(stats.totalMins);
    return '<div class="win">' + chrome("Week") + '<div class="light" style="opacity:.7"></div><div class="lap">' + tabs("week", fmtWeekRange(stats.mon, stats.sun)) + '<div class="l8"><div class="panel hero2"><span class="label">This week</span><div class="big tab">' + heroNum + '</div><div style="font-size:20px;font-weight:600;margin-top:6px">focused</div><div class="hitline"><span class="dots">' + (nGoals ? dots : "") + "</span><b>" + hitLine + "</b></div>" + status + '<div class="cap" style="font-size:14px;margin-top:auto">' + cap + '</div></div><div class="panel" style="padding:22px 24px 22px"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px"><h2 class="disp" style="font-size:23px;font-weight:600">Goals</h2><span class="cap" style="font-size:14px">With a box: hit only when the box is met. No box: hit when one session is finished.</span></div><div class="gcards3">' + (cards || '<p class="cap">Add a goal on Today to see it here.</p>') + '</div></div><div class="panel" style="padding:22px 26px;display:flex;flex-direction:column"><h2 class="disp" style="font-size:23px;font-weight:600">' + bestTitle + '</h2><div class="times">' + tcols + '</div><p class="cap" style="font-size:14px;margin-top:16px">' + bestCap + '</p></div><div class="panel" style="padding:22px 26px 18px;display:flex;flex-direction:column"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="disp" style="font-size:23px;font-weight:600">This week' + AP + 's grove</h2><div class="legend" style="font-size:14px"><span><i></i>' + stats.finished.length + ' grew</span><span class="w"><i></i>' + stats.withered.length + " withered</span></div></div><div class=\"wk7 " + (weighted ? "weighted" : "") + '">' + cols + '</div><p class="cap" style="font-size:14px;margin-top:12px">' + groveCap + "</p></div></div>" + footline(footNote ? "Example data " + MD + " " + footNote : "") + "</div></div>";
  }

  const root = document.getElementById("app");

  function render() {
    let html;
    switch (state.view) {
      case "grove": html = viewGrove(); break;
      case "pick": html = viewPick(); break;
      case "session": html = viewSession(); break;
      case "end": html = viewEnd(); break;
      case "week": html = viewWeek(); break;
      default: html = viewToday();
    }
    root.innerHTML = '<div class="stage" id="stage">' + html + "</div>";
    scaleStage();
    if (state.view === "session") patchGrowingPlant();
    if (state._focusSel) {
      const el = root.querySelector(state._focusSel);
      if (el && el.focus) {
        el.focus();
        if (state._focusCaret != null && el.setSelectionRange) {
          try { el.setSelectionRange(state._focusCaret, state._focusCaret); } catch (err) {}
        }
      }
      state._focusSel = null;
    }
  }

  function scaleStage() {
    const stage = document.getElementById("stage");
    if (!stage) return;
    const s = Math.min(window.innerWidth / 1440, window.innerHeight / 900);
    stage.style.transform = s < 0.999 ? "scale(" + s + ")" : "";
  }

  function speedFactor() {
    return state.demoSpeed ? DEMO_RATIO : 1;
  }

  function startSession() {
    const goal = namedGoals().find(function (g) { return g.id === state.selectedGoalId; });
    if (!goal) return;
    const started = protoNow();
    state.session = {
      goalId: goal.id,
      goalName: goal.name,
      plannedMinutes: state.selectedDur,
      startedAt: started.toISOString(),
      remainingSec: state.selectedDur * 60,
      phase: "grace",
      graceOrigin: performance.now(),
      lastTick: performance.now(),
    };
    state.view = "session";
    maybeAskNotifs();
    render();
    startTicker();
  }

  function maybeAskNotifs() {
    if (!("Notification" in window)) return;
    if (Notification.permission === "denied") {
      state.notifDenied = true;
    } else if (Notification.permission === "default" && !state.notifDismissed) {
      try {
        Notification.requestPermission().then(function (p) {
          if (p !== "granted") {
            state.notifDenied = true;
            if (state.view === "session") render();
          }
        });
      } catch (err) {}
    }
  }

  function startTicker() {
    stopTicker();
    tickTimer = setInterval(onTick, 100);
  }
  function stopTicker() {
    if (tickTimer) clearInterval(tickTimer);
    tickTimer = null;
  }

  function onTick() {
    const ses = state.session;
    if (!ses || state.view !== "session") {
      stopTicker();
      return;
    }
    const now = performance.now();
    const dt = now - ses.lastTick;
    ses.lastTick = now;
    if (ses.phase === "grace") {
      if (now - ses.graceOrigin >= GRACE_MS) {
        ses.phase = "live";
        if (document.hidden) {
          endSession("withered", "left-tab");
          return;
        }
        // remainingSec already accounts for the 10 real seconds of grace
        render();
        return;
      }
      ses.remainingSec = Math.max(0, ses.plannedMinutes * 60 - (now - ses.graceOrigin) / 1000);
      patchSessionClock();
      return;
    }
    ses.remainingSec -= (dt / 1000) * speedFactor();
    if (ses.remainingSec <= 0) {
      ses.remainingSec = 0;
      endSession("finished");
      return;
    }
    patchSessionClock();
  }

  function patchSessionClock() {
    const ses = state.session;
    if (!ses) return;
    const timerEl = document.getElementById("sess-timer");
    const graceEl = document.getElementById("grace-label");
    const bar = document.getElementById("sess-bar");
    if (timerEl) timerEl.textContent = fmtClock(ses.remainingSec);
    if (ses.phase === "grace") {
      const graceLeft = Math.max(0, Math.ceil((GRACE_MS - (performance.now() - ses.graceOrigin)) / 1000));
      if (graceEl) graceEl.textContent = graceLeft + "s to cancel freely";
      const barG = document.querySelector(".lprog i");
      if (barG) barG.style.width = Math.min(100, ((performance.now() - ses.graceOrigin) / GRACE_MS) * 100) + "%";
    } else if (bar) {
      const planned = ses.plannedMinutes * 60;
      const elapsed = planned - ses.remainingSec;
      bar.style.width = Math.min(100, (elapsed / planned) * 100).toFixed(1) + "%";
    }
    patchGrowingPlant();
  }

  function cancelGrace() {
    state.session = null;
    stopTicker();
    state.view = "pick";
    render();
  }

  function endSession(status, reason) {
    const ses = state.session;
    if (!ses) return;
    stopTicker();
    const planned = ses.plannedMinutes * 60;
    const elapsedSec = Math.max(0, planned - ses.remainingSec);
    const elapsedMin = elapsedSec / 60;
    const started = new Date(ses.startedAt);
    const ended = new Date(started.getTime() + elapsedSec * 1000);
    const rec = {
      id: uid("s"),
      goalId: ses.goalId,
      goalName: ses.goalName,
      plannedMinutes: ses.plannedMinutes,
      startedAt: ses.startedAt,
      endedAt: ended.toISOString(),
      status: status,
      reason: reason || null,
      elapsedMinutes: status === "finished" ? ses.plannedMinutes : elapsedMin,
    };
    state.session = null;
    state.endInfo = rec;
    if (status !== "cancelled") {
      state.sessions.push(rec);
      const ok = saveStore();
      if (!ok && status === "finished") {
        state.saveFailed = true;
        state.sessions = state.sessions.filter(function (s) { return s.id !== rec.id; });
      }
    }
    state.view = "end";
    if (status === "finished" && !state.saveFailed && "Notification" in window && Notification.permission === "granted") {
      try { new Notification("Cadence", { body: "This plant is yours. " + rec.goalName + " finished." }); } catch (err) {}
    }
    render();
  }

  function onVisibility() {
    if (!document.hidden) return;
    if (state.view !== "session" || !state.session) return;
    if (state.session.phase === "grace") return;
    endSession("withered", "left-tab");
  }

  function onClick(e) {
    const btn = e.target.closest("[data-act]");
    if (!btn) return;
    const act = btn.getAttribute("data-act");
    if (act === "edit-goal" || act === "edit-box") return;
    e.preventDefault();
    if (act === "nav") {
      const view = btn.getAttribute("data-view");
      if (state.view === "session") return;
      if (view === "pick" && !namedGoals().length) {
        state.view = "today";
        render();
        return;
      }
      state.view = view;
      render();
      return;
    }
    if (act === "toggle-demo") {
      state.demoSpeed = !state.demoSpeed;
      saveStore();
      render();
      return;
    }
    if (act === "add-goal") {
      if (state.goals.length >= 8) return;
      if (!state.goals.length) {
        state.goals.push({ id: uid("g"), name: "", boxMinutes: null });
      }
      const g = { id: uid("g"), name: "", boxMinutes: null };
      state.goals.push(g);
      saveStore();
      state._focusSel = 'input[data-act="edit-goal"][data-id="' + g.id + '"]';
      render();
      return;
    }
    if (act === "remove-goal") {
      const id = btn.getAttribute("data-id");
      state.goals = state.goals.filter(function (g) { return g.id !== id; });
      saveStore();
      render();
      return;
    }
    if (act === "add-box") {
      state.addingBoxFor = btn.getAttribute("data-id");
      state._focusSel = 'input[data-act="edit-box"][data-id="' + state.addingBoxFor + '"]';
      render();
      return;
    }
    if (act === "pick-goal") {
      state.selectedGoalId = btn.getAttribute("data-id");
      render();
      return;
    }
    if (act === "pick-dur") {
      state.selectedDur = Number(btn.getAttribute("data-min"));
      render();
      return;
    }
    if (act === "start") { startSession(); return; }
    if (act === "cancel") { cancelGrace(); return; }
    if (act === "give-up") { endSession("withered", "gave-up"); return; }
    if (act === "dismiss-notif") { state.notifDismissed = true; saveStore(); render(); return; }
    if (act === "use-anyway") { state.useAnyway = true; render(); return; }
    if (act === "retry-save") {
      if (state.endInfo) {
        state.sessions.push(state.endInfo);
        const ok = saveStore();
        if (ok) state.saveFailed = false;
        else state.sessions = state.sessions.filter(function (s) { return s.id !== state.endInfo.id; });
      }
      render();
      return;
    }
    if (act === "load-example") {
      const ex = exampleData();
      state.goals = ex.goals;
      state.sessions = ex.sessions;
      state.protoDate = EXAMPLE_TODAY;
      state.idSeq = 100;
      state.view = "week";
      state.selectedGoalId = "g1";
      saveStore();
      render();
      return;
    }
    if (act === "reset") {
      try { localStorage.removeItem(STORE_KEY); } catch (err) {}
      defaultState();
      if (state.storageBlocked) state.useAnyway = true;
      render();
      return;
    }
  }

  function onInput(e) {
    const el = e.target;
    if (!el.getAttribute) return;
    const act = el.getAttribute("data-act");
    if (!act) return;
    const id = el.getAttribute("data-id");
    if (act === "edit-goal") {
      let g = state.goals.find(function (x) { return x.id === id; });
      if (!g && id === "tmp-first") {
        g = { id: uid("g"), name: el.value, boxMinutes: parseBox(document.querySelector('input[data-act="edit-box"][data-id="tmp-first"]') && document.querySelector('input[data-act="edit-box"][data-id="tmp-first"]').value) };
        state.goals = [g];
        saveStore();
        state._focusSel = 'input[data-act="edit-goal"][data-id="' + g.id + '"]';
        state._focusCaret = el.selectionStart;
        render();
        return;
      }
      if (g) {
        g.name = el.value;
        saveStore();
      }
    }
    if (act === "edit-box") {
      const g = state.goals.find(function (x) { return x.id === id; });
      if (g) g._boxRaw = el.value;
    }
  }

  function commitBox(el) {
    const id = el.getAttribute("data-id");
    const g = state.goals.find(function (x) { return x.id === id; });
    if (!g) return;
    g.boxMinutes = parseBox(el.value);
    delete g._boxRaw;
    state.addingBoxFor = null;
    saveStore();
    render();
  }

  function onBlur(e) {
    const el = e.target;
    if (!el.getAttribute) return;
    const act = el.getAttribute("data-act");
    if (act === "edit-box") commitBox(el);
    if (act === "edit-goal") {
      saveStore();
      render();
    }
  }

  function onKey(e) {
    const el = e.target;
    const act = el.getAttribute && el.getAttribute("data-act");
    if (e.key === "Enter" && (act === "edit-box" || act === "edit-goal")) {
      e.preventDefault();
      el.blur();
    }
    if (e.key === "Escape" && state.view === "session" && state.session && state.session.phase === "grace") {
      cancelGrace();
    }
  }

  window.addEventListener("resize", scaleStage);
  document.addEventListener("visibilitychange", onVisibility);
  document.addEventListener("click", onClick);
  document.addEventListener("input", onInput);
  document.addEventListener("focusout", onBlur);
  document.addEventListener("keydown", onKey);

  hydrate();
  render();

  function setSessionProgress(p) {
    stopTicker();
    const ses = state.session;
    if (!ses) return 0;
    p = Math.max(0, Math.min(1, Number(p) || 0));
    const planned = ses.plannedMinutes * 60;
    const graceSec = GRACE_MS / 1000;
    if (p <= 0) {
      ses.phase = "grace";
      ses.remainingSec = planned;
      ses.graceOrigin = performance.now();
      ses.lastTick = performance.now();
      render();
      patchGrowingPlant(0);
      return 0;
    }
    ses.phase = "live";
    ses.remainingSec = (planned - graceSec) * (1 - p);
    ses.lastTick = performance.now();
    if (state.view !== "session") {
      state.view = "session";
    }
    render();
    patchGrowingPlant(p);
    return p;
  }

  window.__cadence = {
    getState: function () { return state; },
    weekStats: weekStats,
    fmtMins: fmtMins,
    setSessionProgress: setSessionProgress,
    sessionGrowProgress: sessionGrowProgress,
    hideTab: function () {
      Object.defineProperty(document, "hidden", { configurable: true, get: function () { return true; } });
      document.dispatchEvent(new Event("visibilitychange"));
    },
    showTab: function () {
      Object.defineProperty(document, "hidden", { configurable: true, get: function () { return false; } });
      document.dispatchEvent(new Event("visibilitychange"));
    },
  };
})();
