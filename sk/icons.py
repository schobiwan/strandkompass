# -*- coding: utf-8 -*-
"""Symbole, Logo und Zierelemente als SVG."""

# ------------------------------------------------------------------ Icons
ICON = {
 "bino": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="7" cy="15" r="4"/><circle cx="17" cy="15" r="4"/><path d="M7 11V6.5a2 2 0 0 1 4 0V13M17 11V6.5a2 2 0 0 0-4 0V13M11 13h2"/></svg>',
 "pack": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6V4.5A1.5 1.5 0 0 1 10.5 3h3A1.5 1.5 0 0 1 15 4.5V6"/><rect x="5" y="6" width="14" height="15" rx="4"/><path d="M9 13h6M9 13v3h6v-3"/></svg>',
 "chev": '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 5 5-5"/></svg>',
 "find": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>',
 "pair": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="8" height="12" rx="2"/><rect x="13" y="6" width="8" height="12" rx="2"/></svg>',
 "year": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 "wave": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9c2.2 0 2.2-2 4.5-2S9.8 9 12 9s2.3-2 4.5-2S18.8 9 21 9M3 15c2.2 0 2.2-2 4.5-2s2.3 2 4.5 2 2.3-2 4.5-2 2.3 2 4.5 2"/></svg>',
 "bird": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 14c3.5 0 5.5-1.6 7-4.5C11.4 6.8 13.2 5 16 5c2 0 3.6 1.3 4 3l1.5.6-1.6.9c-.4 4.6-3.8 8.5-9.4 8.5H6.5"/><path d="M9 17.5 7.5 20M12 17.5 11 20"/><circle cx="16.3" cy="8.2" r=".6" fill="currentColor" stroke="none"/></svg>',
 "seas": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4.5h7v15H4zM13 4.5h7v15h-7z"/><path d="M5.5 14c1 0 1-1 2-1s1 1 2 1M14.5 14c1 0 1-1 2-1s1 1 2 1"/></svg>',
 "nord": '<svg viewBox="0 0 16 16" aria-hidden="true"><text x="8" y="11.6" text-anchor="middle" font-size="10" font-weight="700" font-family="sans-serif" fill="currentColor" stroke="none">N</text></svg>',
 "ost": '<svg viewBox="0 0 16 16" aria-hidden="true"><text x="8" y="11.6" text-anchor="middle" font-size="10" font-weight="700" font-family="sans-serif" fill="currentColor" stroke="none">O</text></svg>',
}

def icon_symbols():
    out = []
    for k in ("nord", "ost"):
        inner = ICON[k].split(">", 1)[1].rsplit("</svg>", 1)[0]
        out.append(f'<symbol id="i-{k}" viewBox="0 0 16 16">{inner}</symbol>')
    return "".join(out)

def act_svg(a):
    return f'<svg aria-hidden="true"><use href="#i-{a}"></use></svg>'

SPIRAL = '<path d="M24.59 25.31 L24.59 25.41 L24.58 25.51 L24.56 25.61 L24.53 25.71 L24.49 25.81 L24.44 25.91 L24.39 26.01 L24.32 26.11 L24.24 26.20 L24.16 26.29 L24.06 26.38 L23.96 26.46 L23.85 26.53 L23.73 26.60 L23.60 26.66 L23.47 26.72 L23.33 26.76 L23.18 26.80 L23.02 26.82 L22.87 26.84 L22.70 26.84 L22.54 26.84 L22.37 26.82 L22.19 26.79 L22.02 26.75 L21.85 26.70 L21.67 26.63 L21.50 26.55 L21.33 26.46 L21.16 26.36 L20.99 26.24 L20.83 26.11 L20.67 25.97 L20.53 25.82 L20.38 25.66 L20.25 25.48 L20.12 25.29 L20.01 25.09 L19.90 24.88 L19.81 24.66 L19.72 24.44 L19.65 24.20 L19.60 23.96 L19.55 23.71 L19.53 23.45 L19.51 23.19 L19.51 22.92 L19.53 22.65 L19.57 22.38 L19.62 22.10 L19.69 21.83 L19.77 21.55 L19.87 21.28 L19.99 21.01 L20.13 20.74 L20.28 20.48 L20.45 20.22 L20.64 19.97 L20.85 19.73 L21.07 19.50 L21.31 19.28 L21.56 19.07 L21.83 18.87 L22.11 18.68 L22.41 18.51 L22.72 18.36 L23.04 18.22 L23.37 18.10 L23.71 17.99 L24.06 17.91 L24.43 17.84 L24.79 17.79 L25.17 17.77 L25.55 17.76 L25.93 17.78 L26.32 17.82 L26.71 17.88 L27.09 17.96 L27.48 18.07 L27.86 18.20 L28.24 18.35 L28.62 18.52 L28.99 18.72 L29.35 18.94 L29.70 19.18 L30.04 19.45 L30.36 19.73 L30.68 20.04 L30.98 20.36 L31.26 20.71 L31.53 21.07 L31.78 21.46 L32.01 21.86 L32.21 22.27 L32.40 22.70 L32.57 23.14 L32.71 23.60 L32.82 24.07 L32.91 24.54 L32.98 25.03 L33.01 25.52 L33.02 26.02 L33.01 26.52 L32.96 27.03 L32.89 27.53 L32.79 28.04 L32.65 28.54 L32.49 29.04 L32.30 29.53 L32.09 30.02 L31.84 30.50 L31.57 30.96 L31.26 31.42 L30.94 31.86 L30.58 32.28 L30.20 32.69 L29.79 33.08 L29.36 33.45 L28.91 33.79 L28.43 34.12 L27.94 34.42 L27.42 34.69 L26.89 34.94 L26.34 35.16 L25.77 35.35 L25.19 35.50 L24.60 35.63 L24.00 35.73 L23.39 35.79 L22.77 35.82 L22.15 35.82 L21.53 35.78 L20.90 35.71 L20.27 35.60 L19.65 35.46 L19.03 35.28 L18.42 35.06 L17.82 34.82 L17.22 34.53 L16.64 34.22 L16.08 33.87 L15.53 33.48 L15.00 33.07 L14.49 32.62 L14.00 32.15 L13.54 31.64 L13.10 31.11 L12.69 30.55 L12.31 29.96 L11.95 29.35 L11.63 28.72 L11.35 28.07 L11.09 27.40 L10.88 26.71 L10.70 26.01 L10.56 25.29 L10.45 24.57 L10.39 23.83 L10.37 23.09 L10.38 22.34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>'

LOGO = ('<svg class="logo-defs" aria-hidden="true" focusable="false"><symbol id="logo-mark" viewBox="0 0 48 48">'
        '<circle cx="24" cy="24" r="21" fill="none" stroke="currentColor" stroke-width="2.2"></circle>'
        '<circle cx="24" cy="24" r="17" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" stroke-opacity=".6"></circle>'
        + SPIRAL + '<path d="M24 1.8 26.6 7.4H21.4z" fill="var(--logo-accent)"></path>'
        '</symbol>' + icon_symbols() + '</svg>')

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#33413f"/>'
           '<circle cx="24" cy="25" r="17.5" fill="none" stroke="#f3eee3" stroke-width="2.4"/>'
           '<g color="#f3eee3" transform="translate(0 1)">' + SPIRAL + '</g><path d="M24 4.5 27 10.5H21z" fill="#ef7a5a"/></svg>')

# ------------------------------------------------------------------ Seiten
# Spierentonne (rot-weiß) als kleines Zeichen
BUOY = ('<svg class="buoy" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5 16 17H8z" fill="var(--rust)"/>'
        '<path d="M10.2 9h3.6l1 3.8H9.2z" fill="#fff"/><path d="M5 19.5c1.4 0 1.4-1.2 2.8-1.2s1.4 1.2 2.8 1.2 1.4-1.2 2.8-1.2 1.4 1.2 2.8 1.2 1.4-1.2 2.8-1.2" fill="none" stroke="var(--seen)" stroke-width="1.6" stroke-linecap="round"/></svg>')

# Rippelmarken wie im Watt bei Ebbe
def _ripples():
    import math
    paths = []
    for i in range(7):
        y0 = 18 + i * 15; amp = 3.2 + (i % 3) * .9; ph = i * 1.3; per = 46 + (i % 2) * 10
        pts = " ".join(f"{x:.0f},{y0 + amp * math.sin(x / per + ph) + 1.6 * math.sin(x / 13 + ph * 2):.1f}" for x in range(0, 1441, 12))
        paths.append(f'<polyline points="{pts}"/>')
    return ('<svg class="h6-ripples" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true" focusable="false">' + "".join(paths) + '</svg>')

RIPPLES = _ripples()

# Zeichen vor den beiden Zeilen der Startseiten-Überschrift
