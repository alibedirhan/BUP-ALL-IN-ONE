# -*- coding: utf-8 -*-
import sys
import os
import locale

def ensure_locales():
    """
    Locale strategy:
    - Always force LC_NUMERIC='C' to keep Tk/tk scaling and numeric parsing stable.
    - Prefer Turkish time locale if available, with safe fallbacks.
    """
    # Time/Date locale (best-effort)
    for cand in ('Turkish_Turkey.1254', 'tr_TR.UTF-8', 'tr_TR', ''):
        try:
            if cand:
                locale.setlocale(locale.LC_TIME, cand)
            break
        except Exception:
            continue
    # Numeric must be 'C' (decimal point='.'), otherwise Tk may break on Windows.
    try:
        locale.setlocale(locale.LC_NUMERIC, 'C')
    except Exception as e:
        print(f"[HOOK WARNING] LC_NUMERIC set failed: {e}")

def ensure_stdio_utf8():
    """Make sure stdout/stderr are UTF-8 to avoid encoding crashes in console mode."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"[HOOK WARNING] stdout/stderr encoding setup failed: {e}")

def fix_matplotlib():
    # In bundled GUI apps, use non-interactive backend to avoid backend init issues.
    try:
        import matplotlib
        matplotlib.use('Agg')
    except Exception:
        pass

ensure_locales()
ensure_stdio_utf8()
fix_matplotlib()
print("[HOOK] Runtime hook executed successfully")    
