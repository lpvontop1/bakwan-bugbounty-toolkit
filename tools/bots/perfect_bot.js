/* Bakwan perfect bot v4 — in-page via BFB_DEBUG hook.
 * Reads B.sched (seeded note schedule), taps each circle at its exact
 * perfect time using BFB_DEBUG.tap(). Skips bombs + skill shapes.
 * Install: agent-browser eval "<file content>"
 * Start:   __KB.start()   Stop: __KB.stop()   Status: __KB.status()  */
(function () {
  if (window.__KB) { return; }
  const D = () => window.BFB_DEBUG;
  window.__KB = {
    running: false, iv: null, fired: 0, judged: { perfect: 0, great: 0, good: 0, ok: 0, miss: 0, bomb: 0, other: 0 },
    log: [],
    start(maxMs) {
      if (this.running) return 'already running';
      this.running = true; this.fired = 0;
      const self = this; const t0 = Date.now();
      this.iv = setInterval(function () {
        try {
          const d = D(); if (!d || !d.B || !d.B.sched || !d.B.m) return;
          const B = d.B;
          if (B.ended) { self.stop(); return; }
          if (maxMs && Date.now() - t0 > maxMs) { self.stop(); return; }
          const t = d.serverNow() - B.m.startAt;
          const l = d.L();
          const objs = B.sched.objs;
          objs.sort(function (p, q) { return p.a - q.a; });   // tap() breaks on o.a > t — MUST be sorted
          for (let i = 0; i < objs.length; i++) {
            const o = objs[i];
            if (o.k !== 'c' || B.done[o.id]) continue;
            const dt = o.h - t;
            if (dt > 60) continue;                   // not yet time (NO break — sched may be unsorted)
            if (dt < -450) continue;                 // expired
            const x = l.left + (o.x - 0.14) / 0.72 * (l.right - l.left);
            const y = l.top + (o.y - 0.30) / 0.48 * (l.bottom - l.top);
            d.tap(x, y);
            self.fired++; self.log.push({ id: o.id, off: Math.round(t - o.h) });
            if (self.log.length > 400) self.log.shift();
          }
          // harvest judgements
          const L = B.L;
          if (L) {
            self.judged.perfect = L.perfects || 0; self.judged.hits = L.hits || 0;
            self.judged.combo = L.combo || 0; self.judged.bomb = L.bombed || 0;
          }
        } catch (e) { self.err = String(e && e.message); }
      }, 8);
      return 'started';
    },
    stop() { this.running = false; if (this.iv) clearInterval(this.iv); this.iv = null; return 'stopped'; },
    status() {
      const d = D(); const B = d && d.B;
      return JSON.stringify({
        running: this.running, fired: this.fired, judged: this.judged,
        ended: B ? B.ended : null, err: this.err || null,
        board: B && B.L ? { dealt: B.L.dealt, hits: B.L.hits, perfects: B.L.perfects, combo: B.L.combo, bombed: B.L.bombed } : null
      });
    }
  };
  return 'installed';
})();
