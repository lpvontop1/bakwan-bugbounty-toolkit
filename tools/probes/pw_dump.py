#!/usr/bin/env python3
"""Phase 1: full production state dump after new build deployment."""
import json, time
from bakwan_session import Game

g = Game()
try:
    out = {}
    # 1. bootstrap -> full config
    try:
        bs = g.call('bootstrap')
        out['bootstrap_keys'] = sorted(bs.keys()) if isinstance(bs, dict) else str(bs)[:200]
        if isinstance(bs, dict):
            out['config'] = bs.get('config')
            out['player'] = bs.get('player')
            out['owned'] = bs.get('owned')
            out['dailyLogin'] = bs.get('dailyLogin')
            out['announcement'] = bs.get('announcement')
            out['isAdmin'] = bs.get('isAdmin')
            out['cfgRev'] = bs.get('cfgRev')
            out['relay'] = bs.get('relay')
    except Exception as e:
        out['bootstrap_err'] = str(e)[:300]
    with open('/home/z/my-project/scripts/prod_state.json', 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

    cfg = out.get('config') or {}
    print('=== CONFIG STORE ===')
    print(json.dumps(cfg.get('store'), ensure_ascii=False, indent=1)[:1200])
    print('=== CONFIG DAILY/REWARDS ===')
    print(json.dumps({'daily': cfg.get('daily'), 'rewards': cfg.get('rewards'), 'elo': cfg.get('elo'), 'build': cfg.get('build')}, ensure_ascii=False, indent=1))
    chars = cfg.get('characters') or []
    print('=== CHARACTERS (%d) ===' % len(chars))
    for c in chars:
        print(' -', c.get('id'), c.get('name'), c.get('rarity'), 'HP', (c.get('stats') or {}).get('hp'))
    print('=== ANNOUNCEMENT ===')
    print(str(out.get('announcement'))[:300])
    print('=== PLAYER ===')
    print(json.dumps(out.get('player'), ensure_ascii=False)[:400])

    # 2. inbox (badge "1")
    try:
        ib = g.call('inbox', out.get('cfgRev', 0))
        print('=== INBOX ===')
        print(json.dumps(ib, ensure_ascii=False)[:600])
    except Exception as e:
        print('inbox err:', str(e)[:200])
finally:
    g.close()
