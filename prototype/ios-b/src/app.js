(function () {
'use strict';
/* ---------- helpers ---------- */
var AP = '\u2019', MD = '\u2014';
var $ = function (s, r) { return (r || document).querySelector(s); };
function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
var P = {
  sprout: '<path d="M12 21v-8"/><path d="M12 13c0-4-3-6-7-6 0 4 3 6 7 6z"/><path d="M12 11c0-3.5 2.5-5.5 6.5-5.5 0 3.5-2.5 5.5-6.5 5.5z"/>',
  timer: '<circle cx="12" cy="13.5" r="7.5"/><path d="M12 13.5V9.5"/><path d="M9.5 2.5h5"/>',
  plus: '<path d="M12 5v14M5 12h14"/>', check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  cloud: '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 11 3.5 3.5 0 0 0 7 18z"/>',
  cloudoff: '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 11 3.5 3.5 0 0 0 7 18z"/><path d="M3 3l18 18"/>',
  sync: '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.5 4.5L20 16"/><path d="M20 20v-4h-4"/>',
  alert: '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.5v.01"/>',
  laptop: '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>', phone: '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  chev: '<path d="M9 5l7 7-7 7"/>', back: '<path d="M15 5l-7 7 7 7"/>', x: '<path d="M6 6l12 12M18 6L6 18"/>',
  more: '<circle cx="5" cy="12" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="19" cy="12" r="1.4"/>',
  list: '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r=".6"/><circle cx="4.5" cy="12" r=".6"/><circle cx="4.5" cy="18" r=".6"/>'
};
function ic(n, s, sw) { s = s || 18; return '<svg class="ic" width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' + (sw || 1.9) + '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + P[n] + '</svg>'; }
function plant(stage, cls) { return '<img src="' + PLANTS[stage] + '" alt="money plant, ' + stage + '"' + (cls ? ' class="' + cls + '"' : '') + '>'; }

/* ---------- state ---------- */
var LS = 'cadence-ios-b-demo-v1';
var DAY = 'Thursday 26 Nov';
function G(title, box, mins, extra) { return Object.assign({ id: 0, title: title, box: box, mins: mins, done: false, unsynced: false }, extra || {}); }
function fresh() {
  var s = { v: 1, nextId: 20, tab: 'today', plants: 2, mins: 70, sync: 'ok', seq: 0, coachOff: false, parked: [], session: null, end: null, goals: [
    G('Write the weekly review', 45, 30, { id: 1 }), G('Read one paper', 30, 30, { id: 2, done: true }),
    G('Gym', null, 0, { id: 3 }), G('Plan Friday' + AP + 's demo', 25, 0, { id: 4 })] };
  return s;
}
var S; try { S = JSON.parse(localStorage.getItem(LS)); } catch (e) { S = null; }
if (!S || S.v !== 1) S = fresh();
function save() { try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} }
/* transient (not saved) */
var T = { scn: null, sheet: null, alt: null, pick: null, dur: 50, syncing: false, removed: null, movedIn: false, justParked: 0, kb: 0, conflict: null };
var q = new URLSearchParams(location.search);
var FAKEKB = q.has('fakekb');

function list() { return T.alt ? T.alt.goals : S.goals; }
function offlineNow() { return T.scn === 'offline'; }
var MAC_V = { title: 'Read two papers', box: 45 };
function viewGoals() {
  var sc = T.scn, g = list().map(function (x) { return Object.assign({}, x); });
  if (T.alt) return g;
  if (['offline', 'queued', 'macupdate', 'syncheld', 'failed'].indexOf(sc) >= 0) {
    if (g[1]) g[1].unsynced = true;
    if (['offline', 'queued', 'macupdate', 'syncheld'].indexOf(sc) >= 0 && g.length < 6 && !g.some(function (x) { return x.title === 'Call the bank'; })) g.push(G('Call the bank', null, 0, { id: -1, unsynced: true }));
  }
  if (sc === 'conflict' && g[1] && !T.conflict) { g[1].twov = true; }
  if (T.conflict === 'later' && g[1]) g[1].twov = true;
  return g;
}
function isEmptyView() { return viewGoals().length === 0; }

/* ---------- sync line ---------- */
function fmtN(n, one, many) { return n + ' ' + (n === 1 ? one : many); }
function syncInfo() {
  var sc = T.scn, k;
  if (T.syncing) k = 'syncing';
  else if (['offline', 'failed', 'expired', 'queued', 'waiting', 'macupdate', 'clock', 'syncheld', 'syncing', 'loading', 'error'].indexOf(sc) >= 0) k = sc;
  else if (S.sync !== 'ok') k = S.sync;
  else k = 'ok';
  var last = sc === 'newday' ? 'Last synced 12:30 AM' : 'Last synced 9:40 PM';
  var nUns = S.goals.filter(function (g) { return g.unsynced; }).length;
  var M = {
    ok: [ic('check', 14), last, 0, 0], syncing: [ic('sync', 14).replace('class="ic"', 'class="ic spin"'), 'Syncing\u2026', 0, 0],
    offline: [ic('cloudoff', 14), 'Offline', 0, 0], failed: [ic('alert', 14), 'Not synced', 1, 0], expired: [ic('alert', 14), 'Not synced', 1, 0],
    queued: [ic('cloud', 14), (sc === 'queued' ? '2 changes' : fmtN(Math.max(1, nUns), 'change', 'changes')) + ' waiting to upload', 0, 0],
    waiting: [ic('laptop', 14), 'Waiting for your Mac', 0, 0],
    macupdate: [ic('laptop', 14), 'Your Mac needs an update to sync. Your changes are saved here.', 0, 1],
    clock: [ic('timer', 14), 'Phone clock is off. Times are being corrected.', 0, 1],
    syncheld: [ic('cloud', 14), 'Some changes couldn' + AP + 't sync safely. They' + AP + 're saved on this phone.', 0, 1],
    loading: [ic('sync', 14), 'Loading\u2026', 0, 0], error: [ic('alert', 14), 'Not loaded', 1, 0]
  };
  var m = M[k] || M.ok;
  return { kind: k, icon: m[0], text: m[1], warn: m[2], own: m[3] };
}
function statusBtn() {
  var s = syncInfo();
  return '<button class="status' + (s.warn ? ' warn' : '') + (s.own ? ' own' : '') + '" data-act="syncsheet" aria-label="Sync status: ' + esc(s.text) + '">' + s.icon + '<span>' + esc(s.text) + '</span></button>';
}
function tzOn() { var z = ''; try { z = Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) {} return T.scn === 'tz' || (z && z !== 'Asia/Kolkata' && z !== 'Asia/Calcutta' && !q.has('ist')); }

/* ---------- views ---------- */
function nav(left, right, mid) {
  return '<div class="nav"><div style="display:flex">' + (left || '') + '</div>' + (mid ? '<div class="mid">' + mid + '</div>' : '') + '<div style="display:flex;align-items:center">' + (right || '') + '</div></div>';
}
var DOTS = '<button class="navbtn dots" data-act="menu" aria-label="Demo states">' + ic('more', 22) + '</button>';
var PLUS = '<button class="navbtn" data-act="add" aria-label="Add goal"><span class="circ">' + ic('plus', 18, 2.2) + '</span></button>';
function tabs(on) {
  return '<div class="tabs" role="tablist"><button role="tab" aria-selected="' + (on === 'today') + '" class="' + (on === 'today' ? 'on' : '') + '" data-act="tab" data-tab="today">' + ic('list', 24) + 'Today</button>' +
    '<button role="tab" aria-selected="' + (on === 'focus') + '" class="' + (on === 'focus' ? 'on' : '') + '" data-act="tab" data-tab="focus">' + ic('timer', 24) + 'Focus</button></div>';
}
function titleBlock(title) {
  var s = syncInfo(), date = T.scn === 'newday' ? 'Friday 27 Nov' : DAY;
  var line = s.own ? '<span>' + date + '</span><div style="width:100%">' + statusBtn() + '</div>' : '<span>' + date + ' \u00b7</span>' + statusBtn();
  return '<div class="lt"><h1>' + title + '</h1><div class="sub">' + line + '</div>' + (tzOn() ? '<div class="tzh">' + ic('moon', 13) + 'Days follow India time</div>' : '') + '</div>';
}
function banner(kind, title, body, act, actName) {
  var icn = { info: 'cloudoff', warn: 'alert' }[kind];
  return '<div class="banner ' + kind + '" role="status">' + ic(icn, 18) + '<div><b>' + title + '</b>' + (body || '') + '</div>' + (act ? '<button class="act" data-act="' + actName + '">' + act + '</button>' : '') + '</div>';
}
function banners() {
  var sc = T.scn, h = '';
  if (sc === 'offline') h += banner('info', 'You' + AP + 're offline.', ' Changes stay on this phone and sync when you' + AP + 're back.');
  if (sc === 'failed') h += banner('warn', 'Couldn' + AP + 't sync.', ' Your changes are safe on this phone.', 'Try again', 'retrysync');
  if (sc === 'expired') h += banner('warn', 'Sign in again to sync.', ' Your Microsoft sign-in expired. Your changes are safe on this phone.', 'Sign in', 'signin-again');
  return h ? '<div class="stack">' + h + '</div>' : '';
}
function plantStage(n) { return n <= 0 ? 'empty' : n === 1 ? 'early' : n < 4 ? 'mid' : 'full'; }
function fmtMins(m) { var h = Math.floor(m / 60), r = m % 60; return h ? h + 'h ' + (r ? r + 'm' : '').trim() : r + 'm'; }
function goalRow(g) {
  var det = g.box ? (g.mins + ' / ' + g.box + ' min') : (g.done ? 'Done' : 'Not yet');
  var chips = (g.unsynced ? '<span class="us" aria-label="Not synced yet">' + ic('cloudoff', 15) + '</span>' : '') + (g.twov ? '<span class="v2">2 versions</span>' : '');
  var act = g.twov ? ' data-act="conflict-open"' : '';
  return '<div class="swipe" data-id="' + g.id + '"><button class="rm" data-act="remove" data-id="' + g.id + '" aria-label="Remove ' + esc(g.title) + '">Remove</button>' +
    '<div class="row goal"' + act + ' data-id="' + g.id + '"><button class="tickbtn" role="checkbox" aria-checked="' + !!g.done + '" aria-label="Mark ' + esc(g.title) + ' done" data-act="tick" data-id="' + g.id + '"><span class="tick' + (g.done ? ' on' : '') + '">' + (g.done ? ic('check', 14, 2.6) : '') + '</span></button>' +
    '<span class="tt">' + esc(g.title) + chips + '</span><span class="bx">' + det + '</span></div></div>';
}
function parkedBlock(day) {
  if (!S.parked.length || T.alt) return '';
  var open = day.length < 6;
  var rows = S.parked.map(function (p) {
    return '<div class="row' + (T.justParked === p.id ? ' slidein' : '') + '" style="min-height:58px;align-items:center"><span style="width:24px;color:var(--ios-label-2);display:flex;justify-content:center">' + ic('list', 18) + '</span>' +
      '<span class="tt" style="white-space:normal;padding:8px 0">' + esc(p.title) + '<span style="display:block;font-size:0.7647rem;color:var(--ios-label-2)">This goal didn' + AP + 't fit today' + AP + 's 6. It' + AP + 's in Parked.</span></span>' +
      '<button class="pk' + (open ? '' : ' off') + '" data-act="movein" data-id="' + p.id + '" ' + (open ? '' : 'aria-disabled="true"') + '>Move in</button></div>';
  }).join('');
  return '<div class="sec"><span>Parked</span><span>not counted</span></div><div class="grp">' + rows + '</div>' + (open ? '' : '<p class="hint">Remove one of today' + AP + 's goals first.</p>');
}
function coach(day) {
  if (!S.seq || S.coachOff || T.alt) return '';
  var t;
  if (S.seq === 1) t = 'You added \u201cCall the bank\u201d offline, and the day is full. Tap the sync line under the title, then Sync now.';
  else if (S.parked.length && day.length >= 6) t = 'Move in is greyed out while the day has 6 goals. Swipe a goal left to remove it.';
  else if (S.parked.length) t = 'A slot is free, so Move in is on. Tap it.';
  else t = 'The goal moved in. Parked is empty.';
  var n = S.seq === 1 ? 1 : (S.parked.length ? (day.length >= 6 ? 2 : 3) : 4);
  return '<div class="coach"><span style="flex:1"><b>Demo guide ' + n + ' of 4</b>' + t + '</span><button data-act="coach-off" aria-label="Hide demo guide">' + ic('x', 16) + '</button></div>';
}
function viewToday() {
  var day = viewGoals(), n = day.length, empty = n === 0;
  var plants = T.alt ? 0 : S.plants, mins = T.alt ? 0 : S.mins;
  var tally = plants + ' ' + (plants === 1 ? 'plant' : 'plants') + ' \u00b7 ' + fmtMins(mins);
  var showCard = syncInfo().kind === 'ok' && !(S.seq && S.seq < 4 && !T.alt);
  var card = !showCard ? '' : empty ? '<div class="plantcard">' + plant('empty') + '<div class="tx"><b>No plants yet \u00b7 0m</b>Focused today</div></div>'
    : '<div class="plantcard">' + plant(plantStage(plants)) + '<div class="tx"><b>' + tally + '</b>Focused today</div></div>';
  var rows = day.map(goalRow).join('');
  var addRow = n < 6 ? '<button class="row addrow" data-act="add"><span class="pl">' + ic('plus', 20, 2.2) + '</span><span class="tt" style="text-align:left">Add goal</span></button>' : '<button class="row addrow" data-act="add" aria-disabled="true"><span class="pl">' + ic('plus', 20, 2.2) + '</span><span class="tt" style="text-align:left">Add goal</span></button>';
  var six = n >= 6 ? '<p class="hint">Six goals ' + MD + ' plenty for one day.</p>' : '';
  var hint = empty ? '<p class="hint" style="font-size:0.88rem;margin-top:10px;line-height:1.4">' + (T.scn === 'newday' ? 'Today starts with a fresh list. ' : '') + 'Up to 6 goals a day. Focus on one and a money plant grows. Only Give up withers it.</p>' : '';
  var rem = T.removed ? '<div class="removed"><span>Removed ' + esc(T.removed.g.title) + '.</span><button data-act="undo">Undo</button></div>' : '';
  var moved = T.movedIn ? '<p class="hint" style="display:flex;gap:6px;align-items:center;padding-top:10px">' + ic('check', 15) + 'Moved in. Parked is empty.</p>' : '';
  var foot = S.session ? '<button class="runbar" data-act="tab" data-tab="focus">' + ic('timer', 20) + '<span>Focusing on ' + esc(S.session.title) + '</span><span class="t" id="runt">' + mmss(remaining()) + '</span></button>'
    : '<button class="btn pri" data-act="start-pick"' + (empty ? ' disabled' : '') + '>' + ic('timer', 20, 2) + 'Start focusing</button>';
  return '<div class="screen">' + nav(DOTS, PLUS) + titleBlock('Today') +
    '<div class="scroll">' + banners() + card + '<div class="sec"><span>Goals</span><span>' + n + ' of 6</span></div><div class="grp" id="goals">' + rows + addRow + '</div>' + six + hint + rem + moved + parkedBlock(day) + coach(day) + '</div>' +
    '<div class="foot">' + foot + '</div>' + tabs('today') + '</div>';
}
function viewFocus() {
  if (S.session) return viewSession();
  var gs = viewGoals();
  if (T.pick == null || !gs.some(function (g) { return g.id === T.pick; })) { var f = gs.filter(function (g) { return !g.done; })[0] || gs[0]; T.pick = f ? f.id : null; }
  var rows = gs.map(function (g) {
    var on = g.id === T.pick, det = g.box ? (g.mins + ' / ' + g.box + ' min') : (g.done ? 'Done' : 'Not yet');
    return '<button class="row" data-act="pick" data-id="' + g.id + '" role="radio" aria-checked="' + on + '"><span class="tick' + (on ? ' on' : '') + '">' + (on ? ic('check', 14, 2.6) : '') + '</span><span class="tt">' + esc(g.title) + '</span><span class="bx">' + det + '</span></button>';
  }).join('');
  var durs = [[25, '25 min'], [50, '50 min'], [1, '1 min (demo)']].map(function (d) { return '<button class="chip' + (T.dur === d[0] ? ' on' : '') + '" data-act="dur" data-d="' + d[0] + '" role="radio" aria-checked="' + (T.dur === d[0]) + '">' + d[1] + '</button>'; }).join('');
  return '<div class="screen">' + nav(DOTS, '') + titleBlock('Focus') +
    '<div class="scroll">' + banners() + '<div class="plantcard">' + plant('empty') + '<div class="tx"><b>Ready when you are</b>Pick a goal, then grow a plant</div></div>' +
    (gs.length ? '<div class="sec"><span>Pick a goal</span></div><div class="grp" role="radiogroup">' + rows + '</div><div class="sec"><span>Length</span></div><div class="chips" role="radiogroup" style="margin-top:0;padding:0 4px">' + durs + '</div>'
      : '<p class="hint" style="padding-top:18px;font-size:0.94rem">Add a goal on Today first.</p>') +
    '</div><div class="foot"><button class="btn pri" data-act="begin"' + (gs.length ? '' : ' disabled') + '>' + ic('timer', 20, 2) + 'Start focusing</button></div>' + tabs('focus') + '</div>';
}
function remaining() { var s = S.session; return Math.max(0, s.dur * 60000 - (Date.now() - s.startedAt)); }
function mmss(ms) { var t = Math.ceil(ms / 1000), m = Math.floor(t / 60), s = t % 60; return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s; }
function clock12(ms) { var d = new Date(ms), h = d.getHours(), m = d.getMinutes(); return (h % 12 || 12) + ':' + (m < 10 ? '0' : '') + m + ' ' + (h < 12 ? 'AM' : 'PM'); }
function stageFor(p) { return p < 0.08 ? 'sprout' : p < 0.3 ? 'early' : p < 0.95 ? 'mid' : 'full'; }
function viewSession() {
  var s = S.session, p = 1 - remaining() / (s.dur * 60000);
  return '<div class="screen">' + nav('<button class="navbtn back" data-act="tab" data-tab="today">' + ic('back', 20, 2.2) + ' Today</button>', DOTS, 'Focus') +
    '<div class="sill"><div class="p" id="spl">' + plant(stageFor(p)) + '</div><div class="ledge"></div></div>' +
    '<div style="padding:18px 20px 0;text-align:center"><p class="eyebrow">Focusing on</p><h2 style="font-size:1.294rem;font-weight:700;margin-top:3px">' + esc(s.title) + '</h2>' +
    '<div class="timer" id="tm" role="timer" aria-live="off">' + mmss(remaining()) + '</div>' +
    '<p style="font-size:0.882rem;color:var(--ios-label-2)">remaining of ' + String(s.dur).padStart(2, '0') + ':00 \u00b7 ends <span id="ends">' + clock12(s.startedAt + s.dur * 60000) + '</span></p>' +
    '<div class="bar" style="margin:14px 20px 0"><i id="pb" style="width:' + Math.round(p * 100) + '%"></i></div></div>' +
    '<div style="flex:1"></div><div class="foot" style="padding-bottom:calc(var(--ios-safe-bottom) + 14px)"><button class="btn out giveup" data-act="giveup">Give up</button>' +
    '<p style="font-size:0.765rem;color:var(--ios-label-2);text-align:center;margin-top:8px">Your session keeps counting if you switch apps.</p></div></div>';
}
function endView() {
  var e = S.end, fr = e.midnight;
  var grew = e.kind === 'grew';
  var meta = esc(e.title) + ' \u00b7 ' + e.dur + '-minute session<br>Started ' + e.started + ' \u00b7 ended ' + e.ended;
  var body = grew
    ? '<h1 class="endtitle">Grew.</h1><p style="font-size:0.94rem;line-height:1.45;color:var(--ios-label-2);margin-top:8px">' + meta + '</p><p style="font-size:1rem;margin-top:10px">The plant joins today' + AP + 's grove.</p>'
    : '<h1 class="endtitle w">Gave up.</h1><p style="font-size:0.94rem;line-height:1.45;color:var(--ios-label-2);margin-top:8px">' + esc(e.title) + ' \u00b7 gave up at ' + e.kept + ' min<br>Started ' + e.started + ' \u00b7 ended ' + e.ended + '</p><p style="font-size:1rem;margin-top:10px">The plant withered. Only Give up does that.</p>';
  return '<div class="screen">' + nav(DOTS, '', 'Session ended') + '<div class="sill" style="flex:0 1 230px;min-height:140px"><div class="p" style="width:min(150px,45%)">' + plant(grew ? 'full' : 'withered') + '</div><div class="ledge" style="height:16px"></div></div>' +
    '<div style="padding:18px 22px 0">' + body + '</div><div style="flex:1"></div><div class="foot" style="padding-bottom:calc(var(--ios-safe-bottom) + 12px)">' +
    (grew ? '' : '<button class="btn pri" data-act="try-again" style="margin-bottom:10px">Try again</button>') +
    '<button class="btn ' + (grew ? 'pri' : 'out') + '" data-act="go-today">Go to today</button></div></div>';
}
function midnightView() {
  return '<div class="screen">' + nav(DOTS, '', 'Session ended') + '<div class="sill" style="flex:0 1 230px;min-height:140px"><div class="p" style="width:min(150px,45%)">' + plant('full') + '</div><div class="ledge" style="height:16px"></div></div>' +
    '<div style="padding:18px 22px 0"><h1 class="endtitle">Grew.</h1><p style="font-size:0.94rem;line-height:1.45;color:var(--ios-label-2);margin-top:8px">Plan Friday' + AP + 's demo \u00b7 40-minute session<br>Started 11:50 PM Thursday \u00b7 ended 12:30 AM</p>' +
    '<p style="font-size:1rem;margin-top:10px">The plant joins Thursday' + AP + 's grove. A session counts for the day it started.</p>' +
    '<div class="banner info" style="margin-top:14px" role="status">' + ic('moon', 18) + '<div><b>It' + AP + 's Friday now.</b> Today starts with a fresh list.</div></div></div>' +
    '<div style="flex:1"></div><div class="foot" style="padding-bottom:calc(var(--ios-safe-bottom) + 12px)"><button class="btn pri" data-act="go-newday">Go to today</button></div></div>';
}
function sk(w, h, extra) { return '<div class="skel" style="width:' + w + ';height:' + h + 'px;' + (extra || '') + '"></div>'; }
function viewLoading() {
  var rows = [62, 44, 30, 52].map(function (w) { return '<div class="row"><span class="tick" style="border-color:var(--ios-fill)"></span>' + sk(w + '%', 14) + '</div>'; }).join('');
  return '<div class="screen">' + nav(DOTS, '') + titleBlock('Today') + '<div class="scroll" aria-busy="true">' + sk('100%', 120, 'border-radius:12px') +
    '<div class="sec"><span>Goals</span></div><div class="grp">' + rows + '</div></div><div class="foot"><button class="btn pri" disabled>' + ic('timer', 20, 2) + 'Start focusing</button></div>' + tabs('today') + '</div>';
}
function viewError() {
  return '<div class="screen">' + nav(DOTS, '') + titleBlock('Today') + '<div class="scroll"><div class="center"><div style="width:64px;height:64px;border-radius:50%;background:var(--ios-tint-wash);color:var(--ios-tint-strong);display:flex;align-items:center;justify-content:center">' + ic('cloudoff', 30) + '</div>' +
    '<h2 style="font-size:1.294rem;font-weight:700;margin-top:18px">We couldn' + AP + 't load today.</h2><p style="font-size:1rem;line-height:1.4;color:var(--ios-label-2);margin-top:8px">Cadence couldn' + AP + 't reach your goals. Nothing has been lost.</p>' +
    '<button class="btn pri" style="width:200px;margin-top:22px" data-act="retry-load">Try again</button></div></div>' + tabs('today') + '</div>';
}
function viewFirstRun() {
  return '<div class="screen">' + nav(DOTS, '') + '<div class="sill" style="flex:0 1 290px;margin-top:8px"><div class="p" style="width:min(160px,48%)">' + plant('empty') + '</div><div class="ledge"></div><span class="chipmock">MOCKED sign-in</span></div>' +
    '<div style="padding:22px 22px 0"><h1 style="font-size:1.647rem;font-weight:700;letter-spacing:-.02em;line-height:1.15">Grow a plant for every focus session.</h1>' +
    '<p style="font-size:1rem;line-height:1.4;color:var(--ios-label-2);margin-top:10px">Sign in with the Microsoft account that holds your Cadence folder, so this iPhone shares today' + AP + 's goals with your Mac.</p></div><div style="flex:1"></div>' +
    '<div class="foot" style="padding-bottom:calc(var(--ios-safe-bottom) + 10px)"><button class="btn pri" data-act="firstrun-go">Sign in with Microsoft</button><button class="btn txt" data-act="firstrun-go" style="margin-top:4px">Try with demo data</button>' +
    '<p style="font-size:0.765rem;color:var(--ios-label-2);text-align:center;margin-top:4px">Cadence reads and writes one file in your OneDrive folder. Nothing else.</p></div></div>';
}

/* ---------- layer (sheets) ---------- */
function sheetHTML() {
  var sh = T.sheet; if (!sh) return '';
  var scrim = '<div class="scrim" data-act="sheet-close"></div>';
  if (sh.type === 'add') {
    return scrim + '<div class="sheet" role="dialog" aria-label="New goal"><div class="grab"></div><div class="shead"><button class="l" data-act="sheet-close">Cancel</button><b>New goal</b><button class="r" id="addbtn" data-act="add-commit" disabled>Add</button></div>' +
      '<div class="inner"><div class="field"><div class="row"><input id="gtitle" type="text" enterkeyhint="done" autocomplete="off" autocapitalize="sentences" maxlength="60" placeholder="What matters today?" aria-label="Goal"></div>' +
      '<div class="row"><span class="tt">Time box</span><span class="bx" id="tbval">No time box</span></div></div>' +
      '<div class="chips" role="radiogroup" aria-label="Time box">' + [[0, 'No time box'], [15, '15 min'], [25, '25 min'], [30, '30 min'], [45, '45 min'], [60, '60 min']].map(function (c) { return '<button class="chip' + (c[0] === 0 ? ' on' : '') + '" data-act="box" data-b="' + c[0] + '" role="radio" aria-checked="' + (c[0] === 0) + '">' + c[1] + '</button>'; }).join('') + '</div>' +
      '<p class="full" id="addmsg" role="alert" hidden>Today already has 6 goals. Remove one to add this.</p></div></div>';
  }
  if (sh.type === 'sync') {
    var s = syncInfo(), pend = Math.max(S.goals.filter(function (g) { return g.unsynced; }).length, (['queued', 'offline', 'syncing'].indexOf(T.scn) >= 0 ? 2 : 0));
    var busy = s.kind === 'syncing';
    return scrim + '<div class="sheet auto" role="dialog" aria-label="Sync"><div class="grab"></div><div class="inner"><h3 class="stitle">Sync</h3><p class="smuted">' + (busy ? 'Last synced 9:40 PM \u00b7 Syncing ' + fmtN(Math.max(pend, 1), 'change', 'changes') + '\u2026' : esc(s.kind === 'ok' ? 'Last synced 9:40 PM' : s.text)) + '</p>' +
      '<div class="field" style="margin-top:0"><div class="srow">' + ic('phone', 20) + '<span class="tt">This iPhone<span class="src">' + (pend ? fmtN(pend, 'change', 'changes') + ' waiting' : 'Up to date') + '</span></span><span class="status" style="margin:0;padding:0;min-height:0">' + (busy ? ic('sync', 14).replace('class="ic"', 'class="ic spin"') + 'Syncing\u2026' : '') + '</span></div>' +
      '<div class="srow">' + ic('laptop', 20) + '<span class="tt">MacBook<span class="src">Same OneDrive file</span></span><span class="status" style="margin:0;padding:0;min-height:0">' + ic('check', 14) + '9:40 PM</span></div></div>' +
      '<button class="btn out" style="margin-top:14px" data-act="sync-now"' + (busy ? ' disabled' : '') + '>' + ic('sync', 18) + 'Sync now</button></div></div>';
  }
  if (sh.type === 'conflict') {
    return scrim + '<div class="sheet auto" role="dialog" aria-label="Edited on both devices"><div class="grab"></div><div class="inner"><h3 class="stitle">Edited on both devices</h3><p class="smuted" style="margin-bottom:0">Nothing is lost. Choose which version to keep.</p>' +
      '<div class="ccard"><div class="w">' + ic('laptop', 15) + 'On your Mac \u00b7 8:12 PM</div><div class="n">Read two papers</div><div class="m">Time box 45 min</div></div>' +
      '<div class="ccard sel"><div class="w">' + ic('phone', 15) + 'On this iPhone \u00b7 8:20 PM, made offline</div><div class="n">Read one paper</div><div class="m">Time box 30 min</div></div>' +
      '<div class="btnrow"><button class="btn out" data-act="keep-mac">Keep Mac version</button><button class="btn pri" data-act="keep-phone">Keep iPhone version</button></div>' +
      '<button class="btn txt" style="margin:2px auto 0;width:auto;padding:0 16px" data-act="decide-later">Decide later</button></div></div>';
  }
  if (sh.type === 'giveup') {
    return scrim + '<div class="sheet auto" role="alertdialog" aria-label="Give up"><div class="grab"></div><div class="inner"><h3 class="stitle">Give up this session?</h3><p class="smuted">The plant will wither. Only Give up does that. The minutes before now are not counted.</p>' +
      '<button class="btn out giveup" data-act="giveup-yes">Give up</button><button class="btn pri" style="margin-top:10px" data-act="sheet-close">Keep going</button></div></div>';
  }
  if (sh.type === 'menu') {
    var R = function (k, label, hint, on) { return '<button class="mrow" data-act="scn" data-k="' + k + '"><span class="tt">' + label + '</span>' + (hint ? '<span class="k">' + hint + '</span>' : '') + (on ? '<span class="ok">' + ic('check', 18, 2.4) + '</span>' : '') + '</button>'; };
    var cur = T.scn;
    return scrim + '<div class="sheet menu" role="dialog" aria-label="Demo states"><div class="grab"></div><div class="shead"><span class="l" style="visibility:hidden">x</span><b>Demo states</b><button class="r" data-act="sheet-close">Done</button></div><div class="inner" style="padding-bottom:calc(var(--ios-safe-bottom) + 16px)">' +
      '<p class="hint" style="padding-top:0">Prototype only. These switch the screen into each state for review. Data here is fake.</p>' +
      '<div class="sec">Flows</div><div class="grp">' + R('parked', 'Parked sequence', 'guided') + R('six', '6 goals (limit)', '') + R('midnight', 'Session past midnight IST', '', cur === 'midnight') + R('newday', 'New day, fresh list', '', cur === 'newday') + '</div>' +
      '<div class="sec">First run, loading, error</div><div class="grp">' + R('firstrun', 'First run (sign-in, mocked)', '', cur === 'firstrun') + R('empty', 'Empty today', '', cur === 'empty') + R('loading', 'Loading', '', cur === 'loading') + R('error', 'Error with Try again', '', cur === 'error') + '</div>' +
      '<div class="sec">Sync</div><div class="grp">' + R('offline', 'Offline', '', cur === 'offline') + R('syncing', 'Syncing', '', cur === 'syncing') + R('queued', '2 changes waiting to upload', '', cur === 'queued') + R('waiting', 'Waiting for your Mac', '', cur === 'waiting') +
      R('macupdate', 'Mac needs update', '', cur === 'macupdate') + R('syncheld', 'syncHeld', '', cur === 'syncheld') + R('failed', 'Sync failed', '', cur === 'failed') + R('conflict', 'Edited on both devices', '', cur === 'conflict') + R('expired', 'Sign-in expired', '', cur === 'expired') +
      R('clock', 'Phone clock is off', '', cur === 'clock') + R('tz', 'Days follow India time', '', cur === 'tz') + '</div>' +
      '<div class="sec">Reset</div><div class="grp">' + R('normal', 'Back to normal', '', !cur) + '<button class="mrow danger" data-act="reset"><span class="tt">Reset demo</span></button></div></div></div>';
  }
  return '';
}
function renderLayer() {
  var L = $('#layer'); L.innerHTML = sheetHTML();
  document.getElementById('device').style.setProperty('--kb', (T.sheet && T.sheet.type === 'add' ? (FAKEKB ? 336 : T.kb) : 0) + 'px');
  if (T.sheet && T.sheet.type === 'add' && FAKEKB) L.insertAdjacentHTML('beforeend', '<div class="fakekb" aria-hidden="true">keyboard (test fixture)</div>');
}

/* ---------- render ---------- */
function render() {
  var sc = T.scn, h;
  if (sc === 'firstrun') h = viewFirstRun();
  else if (sc === 'loading') h = viewLoading();
  else if (sc === 'error') h = viewError();
  else if (sc === 'midnight') h = midnightView();
  else if (S.end && S.tab === 'focus') h = endView();
  else if (S.tab === 'focus') h = viewFocus();
  else h = viewToday();
  var scr = $('#app .scroll'), top = scr ? scr.scrollTop : 0;
  $('#app').innerHTML = h;
  scr = $('#app .scroll'); if (scr) scr.scrollTop = top;
  if (T.auto && scr) { scr.scrollTop = scr.scrollHeight; T.auto = false; }
  var t = sc === 'tz' ? '5:11' : (sc === 'midnight' || sc === 'newday') ? '12:30' : '9:41';
  $('#simsb').innerHTML = '<span>' + t + '</span><span class="r"><svg width="18" height="12" viewBox="0 0 18 12" fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg><svg width="27" height="13" viewBox="0 0 27 13" fill="none"><rect x=".5" y=".5" width="23" height="12" rx="3.5" stroke="currentColor" opacity=".4"/><rect x="2" y="2" width="17" height="9" rx="2" fill="currentColor"/></svg></span>';
  save();
}
function rerenderAll() { render(); renderLayer(); }

/* ---------- actions ---------- */
function findGoal(id) { return list().filter(function (g) { return g.id === id; })[0]; }
function openSheet(type) { T.sheet = { type: type }; renderLayer(); if (type === 'add') { var i = $('#gtitle'); if (viewGoals().length >= 6) { var m = $('#addmsg'); if (m) m.hidden = false; if (i) { i.disabled = true; } } else if (i) i.focus(); } }
function closeSheet() { T.sheet = null; renderLayer(); }
function toast() {}
var box = 0;
function commitAdd() {
  var i = $('#gtitle'); if (!i) return; var title = i.value.trim(); if (!title) return;
  if (viewGoals().length >= 6) { var m = $('#addmsg'); if (m) { m.hidden = false; } return; }
  list().push(G(title, box || null, 0, { id: S.nextId++, unsynced: offlineNow() }));
  T.removed = null; T.movedIn = false; closeSheet(); render();
}
function startSync() {
  T.sheet = null; renderLayer(); T.syncing = true; render();
  setTimeout(function () {
    T.syncing = false; var sc = T.scn;
    if (S.seq === 1) { parkMove(); T.auto = true; }
    if (sc === 'queued' || sc === 'waiting' || sc === 'failed' || sc === 'syncing' || !sc) { T.scn = null; S.goals.forEach(function (g) { g.unsynced = false; }); S.sync = 'ok'; }
    render();
  }, 1300);
}
function parkMove() {
  var late = S.goals.filter(function (g) { return g.title === 'Call the bank'; })[0];
  S.goals = S.goals.filter(function (g) { return g !== late; }); S.goals.forEach(function (g) { g.unsynced = false; });
  var mac = G('Morning pages', 15, 0, { id: S.nextId++ });
  var at = S.goals.findIndex(function (g) { return g.title === 'Deep work on the stack'; }); if (at < 0) at = S.goals.length;
  S.goals.splice(at, 0, mac);
  var pid = S.nextId++; S.parked = [{ id: pid, title: 'Call the bank' }]; T.justParked = pid; S.seq = 2; S.sync = 'ok';
}
function endSession(kind) {
  var s = S.session; if (!s) return;
  var now = Date.now(), el = Math.min(now - s.startedAt, s.dur * 60000), kept = Math.floor(el / 60000);
  var g = S.goals.filter(function (x) { return x.id === s.goalId; })[0];
  if (kind === 'grew') {
    if (g) { g.mins += s.dur; if (g.box && g.mins >= g.box) g.done = true; }
    S.plants += 1; S.mins += s.dur;
  }
  S.end = { kind: kind, title: s.title, dur: s.dur, kept: kept, started: clock12(s.startedAt), ended: clock12(kind === 'grew' ? s.startedAt + s.dur * 60000 : now) };
  S.session = null; S.tab = 'focus'; T.sheet = null; render(); renderLayer();
}
function tickSession() {
  if (!S.session) return;
  if (remaining() <= 0) { endSession('grew'); return; }
  var r = remaining(), p = 1 - r / (S.session.dur * 60000);
  var tm = $('#tm'); if (tm) tm.textContent = mmss(r);
  var rt = $('#runt'); if (rt) rt.textContent = mmss(r);
  var pb = $('#pb'); if (pb) pb.style.width = Math.round(p * 100) + '%';
  var sp = $('#spl'); if (sp) { var st = stageFor(p); var img = sp.querySelector('img'); if (img && img.alt.indexOf(st) < 0) sp.innerHTML = plant(st); }
}
function scn(k) {
  T.sheet = null; T.removed = null; T.movedIn = false; T.conflict = null; T.alt = null;
  if (k === 'normal') { T.scn = null; S.goals.forEach(function (g) { g.unsynced = false; }); if (S.seq !== 1) S.sync = 'ok'; }
  else if (k === 'parked') { startParked(); T.scn = null; S.tab = 'today'; }
  else if (k === 'six') { sixGoals(); T.scn = null; S.tab = 'today'; }
  else if (k === 'empty') { T.alt = { goals: [] }; T.scn = 'empty'; S.tab = 'today'; }
  else if (k === 'newday') { T.alt = { goals: [] }; T.scn = 'newday'; S.tab = 'today'; }
  else { T.scn = k; if (k !== 'midnight' && k !== 'firstrun' && k !== 'loading' && k !== 'error') S.tab = 'today'; if (k === 'midnight') S.tab = 'focus'; }
  if (k === 'syncing') { T.sheet = { type: 'sync' }; }
  if (k === 'conflict') { T.sheet = { type: 'conflict' }; }
  rerenderAll();
}
function startParked() {
  S.goals = [G('Write the weekly review', 45, 30, { id: 1 }), G('Read one paper', 30, 30, { id: 2, done: true }), G('Gym', null, 0, { id: 3 }), G('Plan Friday' + AP + 's demo', 25, 0, { id: 4 }),
    G('Deep work on the stack', 60, 20, { id: 5 }), G('Call the bank', null, 0, { id: 6, unsynced: true })];
  S.goals[1].unsynced = true;
  S.parked = []; S.seq = 1; S.coachOff = false; S.sync = 'queued'; S.nextId = 20;
}
function sixGoals() {
  var base = fresh().goals; S.goals = base.concat([G('Morning pages', 15, 15, { id: 5, done: true }), G('Deep work on the stack', 60, 20, { id: 6 })]); S.parked = []; S.seq = 0;
}
function reset() { S = fresh(); T.scn = null; T.sheet = null; T.alt = null; T.removed = null; T.movedIn = false; T.conflict = null; T.pick = null; T.dur = 50; try { localStorage.removeItem(LS); } catch (e) {} rerenderAll(); }

document.addEventListener('click', function (e) {
  var el = e.target.closest('[data-act]'); if (!el || el.disabled) return;
  var a = el.getAttribute('data-act'), id = Number(el.getAttribute('data-id'));
  if (swipeMoved) { swipeMoved = false; if (a !== 'remove') return; }
  switch (a) {
    case 'tab': S.tab = el.getAttribute('data-tab'); render(); break;
    case 'add': openSheet('add'); box = 0; break;
    case 'sheet-close': closeSheet(); break;
    case 'add-commit': commitAdd(); break;
    case 'box': box = Number(el.getAttribute('data-b')); [].forEach.call(document.querySelectorAll('.chips .chip'), function (c) { var on = c === el; c.classList.toggle('on', on); c.setAttribute('aria-checked', on); }); $('#tbval').textContent = box ? box + ' min' : 'No time box'; break;
    case 'tick': { var g = findGoal(id); if (g) { g.done = !g.done; render(); } break; }
    case 'remove': { var arr = list(), i = arr.findIndex(function (x) { return x.id === id; }); if (i >= 0) { T.removed = { g: arr[i], i: i }; arr.splice(i, 1); T.movedIn = false; if (S.parked.length) T.auto = true; render(); } break; }
    case 'undo': if (T.removed) { list().splice(T.removed.i, 0, T.removed.g); T.removed = null; render(); } break;
    case 'movein': { if (list().length >= 6) return; var p = S.parked.filter(function (x) { return x.id === id; })[0]; if (p) { list().push(G(p.title, null, 0, { id: S.nextId++ })); S.parked = S.parked.filter(function (x) { return x !== p; }); S.seq = Math.max(S.seq, 4); T.movedIn = true; T.removed = null; T.auto = true; render(); } break; }
    case 'coach-off': S.coachOff = true; render(); break;
    case 'syncsheet': openSheet('sync'); break;
    case 'sync-now': startSync(); break;
    case 'retrysync': startSync(); break;
    case 'signin-again': T.scn = null; render(); break;
    case 'conflict-open': openSheet('conflict'); break;
    case 'keep-mac': { var g1 = S.goals[1]; if (g1) { g1.title = MAC_V.title; g1.box = MAC_V.box; } T.conflict = 'done'; T.scn = null; closeSheet(); render(); break; }
    case 'keep-phone': T.conflict = 'done'; T.scn = null; closeSheet(); render(); break;
    case 'decide-later': T.conflict = 'later'; T.scn = null; closeSheet(); render(); break;
    case 'menu': openSheet('menu'); break;
    case 'scn': scn(el.getAttribute('data-k')); break;
    case 'reset': reset(); break;
    case 'start-pick': S.tab = 'focus'; T.pick = null; render(); break;
    case 'pick': T.pick = id; render(); break;
    case 'dur': T.dur = Number(el.getAttribute('data-d')); render(); break;
    case 'begin': { var gg = findGoal(T.pick); if (!gg) return; S.session = { goalId: gg.id, title: gg.title, dur: T.dur, startedAt: Date.now() }; S.end = null; render(); break; }
    case 'giveup': openSheet('giveup'); break;
    case 'giveup-yes': endSession('withered'); break;
    case 'go-today': S.end = null; S.tab = 'today'; render(); break;
    case 'try-again': S.end = null; S.tab = 'focus'; render(); break;
    case 'go-newday': T.alt = { goals: [] }; T.scn = 'newday'; S.tab = 'today'; render(); break;
    case 'firstrun-go': T.scn = null; S.tab = 'today'; render(); break;
    case 'retry-load': T.scn = 'loading'; render(); setTimeout(function () { if (T.scn === 'loading') { T.scn = null; render(); } }, 900); break;
  }
});
document.addEventListener('input', function (e) {
  if (e.target.id === 'gtitle') { var b = $('#addbtn'); if (b) b.disabled = !e.target.value.trim(); var m = $('#addmsg'); if (m && !m.hidden && viewGoals().length < 6) m.hidden = true; }
});
document.addEventListener('keydown', function (e) {
  if (e.target.id === 'gtitle' && e.key === 'Enter') { e.preventDefault(); commitAdd(); }
  if (e.key === 'Escape' && T.sheet) closeSheet();
});

/* swipe left to remove */
var swipeMoved = false, sw = null;
document.addEventListener('pointerdown', function (e) {
  var r = e.target.closest('.swipe .row'); if (!r || e.target.closest('.tickbtn')) return;
  sw = { r: r, x: e.clientX, y: e.clientY, base: r.classList.contains('open') ? -96 : 0, dx: 0, lock: null };
});
document.addEventListener('pointermove', function (e) {
  if (!sw) return; var dx = e.clientX - sw.x, dy = e.clientY - sw.y;
  if (sw.lock == null && (Math.abs(dx) > 8 || Math.abs(dy) > 8)) sw.lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
  if (sw.lock !== 'x') return; swipeMoved = true; sw.r.classList.add('drag');
  sw.dx = Math.max(-96, Math.min(0, sw.base + dx)); sw.r.style.transform = 'translateX(' + sw.dx + 'px)';
});
function swEnd() { if (!sw) return; var r = sw.r; r.classList.remove('drag'); if (sw.lock === 'x') { var open = sw.dx < -48; r.classList.toggle('open', open); r.style.transform = open ? 'translateX(-96px)' : ''; setTimeout(function () { swipeMoved = false; }, 60); } sw = null; }
document.addEventListener('pointerup', swEnd); document.addEventListener('pointercancel', swEnd);
document.addEventListener('click', function (e) { if (!e.target.closest('.swipe')) [].forEach.call(document.querySelectorAll('.swipe .row.open'), function (r) { r.classList.remove('open'); r.style.transform = ''; }); }, true);

/* keyboard: keep the add sheet above the iOS keyboard */
if (window.visualViewport) {
  var onVV = function () { var vv = window.visualViewport; T.kb = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop)); if (T.sheet && T.sheet.type === 'add' && !FAKEKB) document.getElementById('device').style.setProperty('--kb', T.kb + 'px'); if (vv.offsetTop) window.scrollTo(0, 0); };
  window.visualViewport.addEventListener('resize', onVV); window.visualViewport.addEventListener('scroll', onVV);
}

/* simulated device on wide screens or ?frame=1 */
var wide = !window.matchMedia('(max-width:500px)').matches;
document.documentElement.classList.toggle('sim', wide || q.has('frame'));
document.documentElement.classList.toggle('wide', wide);
function fit() { if (!wide) return; var s = Math.min(1, (window.innerHeight - 24) / 844); document.getElementById('device').style.transform = 'scale(' + s + ')'; }
window.addEventListener('resize', fit); fit();

setInterval(tickSession, 250);
document.addEventListener('visibilitychange', tickSession); window.addEventListener('pageshow', tickSession); window.addEventListener('focus', tickSession);
if (q.get('scn')) { var k = q.get('scn'); if (k === 'parked' || k === 'six' || k === 'normal') scn(k); else { scn(k); } }
rerenderAll();
tickSession();
window.__cadence = { S: function () { return S; }, T: function () { return T; }, scn: scn };
})();
