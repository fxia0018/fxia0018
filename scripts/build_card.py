"""Generate assets/card-dark.svg and assets/card-light.svg.

The left half is a radar whose sweep lights up each upstream project it
passes (flash, ripples, lock-on brackets). The right half types a rotating
tagline, glitches it and shatters it before typing the next one.

update_stats.py later rewrites the two numbers in place (ids n-merged and
n-opened), so this script only needs re-running when the design changes:

    python scripts/build_card.py [merged] [opened]
"""

from __future__ import annotations

import math
import random
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
W, H = 985, 534
CX, CY, R = 210, 262, 150
SWEEP = 6.0  # seconds per radar revolution

THEMES = {
    "dark": dict(
        bg="#120b0c", border="#3a1f22", glow="#e5484d", grid="#e5484d",
        crimson="#e5484d", amber="#f5a524", head="#f7e6c4", text="#e8d9d3",
        dim="#8c7470", blip="#7a2e30",
    ),
    "light": dict(
        bg="#fffaf5", border="#efd6cc", glow="#f28b82", grid="#c9302c",
        crimson="#c9302c", amber="#c26a00", head="#3a1a14", text="#3d2b27",
        dim="#9a7f78", blip="#e3a7a2",
    ),
}

# (label, angle clockwise from east in degrees, radius as a fraction of R)
BLIPS = [
    ("AgentScope", 20, 0.78),
    ("OpenSandbox", 62, 0.55),
    ("WeKnora", 118, 0.80),
    ("ReMe", 160, 0.42),
    ("Dify", 196, 0.70),
    ("logfire", 238, 0.88),
    ("OpenJudge", 282, 0.50),
    ("AI-Infra-Guard", 322, 0.72),
]

TAGLINES = [
    "CS @ Monash '28",
    "building agents that use tools",
    "MCP · RAG · tool use",
    "fixing bugs in agent frameworks",
]


def pt(angle: float, radius: float) -> tuple[float, float]:
    a = math.radians(angle)
    return CX + radius * math.cos(a), CY + radius * math.sin(a)


def f(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def radar(c: dict) -> list[str]:
    out = [
        f'<circle cx="{CX}" cy="{CY}" r="{R + 40}" fill="url(#glow)"/>',
    ]
    for frac, op in ((1.0, 0.55), (0.66, 0.28), (0.33, 0.28)):
        out.append(
            f'<circle cx="{CX}" cy="{CY}" r="{f(R * frac)}" fill="none" '
            f'stroke="{c["grid"]}" stroke-opacity="{op}"/>'
        )
    for a in range(0, 180, 45):
        x1, y1 = pt(a, R)
        x2, y2 = pt(a + 180, R)
        out.append(
            f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
            f'stroke="{c["grid"]}" stroke-opacity="0.14"/>'
        )
    # bezel ticks
    for a in range(0, 360, 5):
        long = a % 30 == 0
        x1, y1 = pt(a, R + 4)
        x2, y2 = pt(a, R + (12 if long else 8))
        out.append(
            f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
            f'stroke="{c["grid"]}" stroke-opacity="{0.6 if long else 0.3}"/>'
        )
    # slow counter-rotating dashed ring
    out.append(
        f'<circle cx="{CX}" cy="{CY}" r="{R + 20}" fill="none" stroke="{c["amber"]}" '
        f'stroke-opacity="0.35" stroke-dasharray="2 10 24 10">'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="360 {CX} {CY}" to="0 {CX} {CY}" dur="40s" repeatCount="indefinite"/></circle>'
    )

    # sweep: a fading trail of thin wedges behind a bright leading edge
    out.append("<g>")
    out.append(
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="0 {CX} {CY}" to="360 {CX} {CY}" dur="{SWEEP}s" repeatCount="indefinite"/>'
    )
    steps = 30
    for k in range(steps):
        a2 = -k * 2.2
        a1 = a2 - 2.4
        x1, y1 = pt(a1, R)
        x2, y2 = pt(a2, R)
        op = 0.42 * (1 - k / steps) ** 1.6
        out.append(
            f'<path d="M{CX},{CY} L{f(x1)},{f(y1)} A{R},{R} 0 0,1 {f(x2)},{f(y2)} Z" '
            f'fill="{c["crimson"]}" fill-opacity="{op:.3f}"/>'
        )
    ex, ey = pt(0, R)
    out.append(
        f'<line x1="{CX}" y1="{CY}" x2="{f(ex)}" y2="{f(ey)}" stroke="{c["amber"]}" '
        f'stroke-width="2"/>'
    )
    out.append("</g>")

    for label, angle, frac in BLIPS:
        out += blip(c, label, angle, frac)

    # centre pulse
    out.append(f'<circle cx="{CX}" cy="{CY}" r="3.5" fill="{c["amber"]}"/>')
    out.append(
        f'<circle cx="{CX}" cy="{CY}" r="4" fill="none" stroke="{c["amber"]}">'
        f'<animate attributeName="r" values="4;26" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/>'
        f"</circle>"
    )
    # caption
    y = CY + R + 52
    out.append(
        f'<circle cx="{CX - 98}" cy="{y - 4}" r="3.5" fill="{c["crimson"]}">'
        f'<animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>'
    )
    out.append(
        f'<text x="{CX - 88}" y="{y}" font-size="11" letter-spacing="2" fill="{c["dim"]}">'
        f"SCANNING UPSTREAM</text>"
    )
    return out


def blip(c: dict, label: str, angle: float, frac: float) -> list[str]:
    x, y = pt(angle, R * frac)
    hit = angle / 360 * SWEEP
    timing = f'begin="{hit:.3f}s" dur="{SWEEP}s" repeatCount="indefinite"'
    out = ["<g>"]
    for delay in (0.0, 0.35):
        out.append(
            f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="none" stroke="{c["amber"]}" stroke-opacity="0">'
            f'<animate attributeName="r" values="4;24;24" keyTimes="0;0.3;1" '
            f'begin="{hit + delay:.3f}s" dur="{SWEEP}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.9;0;0" keyTimes="0;0.3;1" '
            f'begin="{hit + delay:.3f}s" dur="{SWEEP}s" repeatCount="indefinite"/></circle>'
        )
    out.append(
        f'<circle cx="{f(x)}" cy="{f(y)}" r="3.5" fill="{c["blip"]}">'
        f'<animate attributeName="fill" values="{c["amber"]};{c["amber"]};{c["blip"]};{c["blip"]}" '
        f'keyTimes="0;0.12;0.7;1" {timing}/>'
        f'<animate attributeName="r" values="6;3.5;3.5" keyTimes="0;0.35;1" {timing}/></circle>'
    )
    # lock-on brackets
    s, g = 10, 4
    d = " ".join(
        f"M{f(x + sx * s)},{f(y + sy * (s - g))} L{f(x + sx * s)},{f(y + sy * s)} "
        f"L{f(x + sx * (s - g))},{f(y + sy * s)}"
        for sx in (-1, 1)
        for sy in (-1, 1)
    )
    out.append(
        f'<path d="{d}" fill="none" stroke="{c["crimson"]}" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.25;0.4;1" {timing}/></path>'
    )
    left = 90 < angle < 270
    tx = x + (-10 if left else 10)
    anchor = "end" if left else "start"
    out.append(
        f'<text x="{f(tx)}" y="{f(y + 4)}" font-size="11" text-anchor="{anchor}" fill="{c["dim"]}">'
        f'<animate attributeName="fill" values="{c["head"]};{c["head"]};{c["dim"]};{c["dim"]}" '
        f'keyTimes="0;0.2;0.7;1" {timing}/>{escape(label)}</text>'
    )
    out.append("</g>")
    return out


def typed_once(text: str, x: float, y: float, size: int, fill: str, start: float,
               per_char: float, extra: str = "") -> list[str]:
    """Type ``text`` in once and keep it."""
    cw = size * 0.6
    out = []
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        t = start + i * per_char
        out.append(
            f'<text x="{f(x + i * cw)}" y="{y}" font-size="{size}" fill="{fill}" opacity="0"{extra}>'
            f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>{escape(ch)}</text>'
        )
    return out


def taglines(c: dict, x: float, y: float, start: float) -> list[str]:
    """Type each tagline, glitch it, shatter it, then type the next one."""
    size, cw, per_char = 15, 9.0, 0.06
    hold, glitch, shatter, gap = 2.4, 0.3, 0.8, 0.35
    rng = random.Random(7)
    spans = []
    t = 0.0
    for phrase in TAGLINES:
        typed = t + len(phrase) * per_char
        g = typed + hold
        s = g + glitch
        end = s + shatter + gap
        spans.append((phrase, t, g, s, end))
        t = end
    total = t
    timing = f'begin="{start}s" dur="{total:.2f}s" repeatCount="indefinite"'

    def kt(*times: float) -> str:
        return ";".join(f"{min(max(v / total, 0), 1):.4f}" for v in times)

    eps = 0.001
    out = []
    for phrase, t0, g, s, end in spans:
        for i, ch in enumerate(phrase):
            if ch == " ":
                continue
            appear = t0 + (i + 1) * per_char
            cx = x + i * cw + cw / 2
            dx = rng.uniform(-40, 40)
            dy = rng.uniform(18, 46)
            rot = rng.uniform(-160, 160)
            out.append(
                f'<text x="{f(x + i * cw)}" y="{y}" font-size="{size}" fill="{c["text"]}" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{kt(appear - eps, appear, s, s + shatter)};1" {timing}/>'
                f'<animate attributeName="fill" calcMode="discrete" '
                f'values="{c["text"]};{c["crimson"]};{c["amber"]};{c["crimson"]};{c["text"]}" '
                f'keyTimes="0;{kt(g, g + glitch / 3, g + 2 * glitch / 3, s + shatter)}" {timing}/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'values="0 0;0 0;{rng.choice((-2, 2))} 0;0 0;{f(dx)} {f(dy)};0 0;0 0" '
                f'keyTimes="0;{kt(g, g + glitch / 2, s, s + shatter, s + shatter + eps)};1" {timing}/>'
                f'<animateTransform attributeName="transform" type="rotate" additive="sum" '
                f'values="0 {f(cx)} {y - 5};0 {f(cx)} {y - 5};{f(rot)} {f(cx)} {y - 5};0 {f(cx)} {y - 5};0 {f(cx)} {y - 5}" '
                f'keyTimes="0;{kt(s, s + shatter, s + shatter + eps)};1" {timing}/>'
                f"{escape(ch)}</text>"
            )
    # cursor
    xs, keys = [], []
    for phrase, t0, g, s, end in spans:
        for i in range(len(phrase) + 1):
            xs.append(x + i * cw)
            keys.append(t0 + i * per_char)
        xs.append(x)
        keys.append(s + shatter)
    out.append(
        f'<rect x="{x}" y="{y - 13}" width="8" height="16" fill="{c["amber"]}">'
        f'<animate attributeName="x" calcMode="discrete" values="{";".join(f(v) for v in xs)}" '
        f'keyTimes="{";".join(f"{min(k / total, 1):.4f}" for k in keys)}" {timing}/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="0.9s" '
        f'repeatCount="indefinite"/></rect>'
    )
    return out


def fade_in(body: str, start: float, rise: int = 8) -> str:
    return (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{start}s" dur="0.6s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 {rise}" to="0 0" '
        f'begin="{start}s" dur="0.6s" fill="freeze"/>{body}</g>'
    )


def divider(c: dict, y: float, start: float) -> str:
    length = 525
    return (
        f'<line x1="440" y1="{y}" x2="{440 + length}" y2="{y}" stroke="url(#rule)" '
        f'stroke-dasharray="{length}" stroke-dashoffset="{length}">'
        f'<animate attributeName="stroke-dashoffset" from="{length}" to="0" begin="{start}s" '
        f'dur="0.8s" fill="freeze"/></line>'
    )


def right(c: dict, merged: int, opened: int) -> list[str]:
    x = 440
    out = typed_once("natsuki", x, 118, 30, "url(#name)", 0.3, 0.09, ' font-weight="700"')
    out.append(f'<text x="{x}" y="152" font-size="15" fill="{c["amber"]}">❯</text>')
    out += taglines(c, x + 20, 152, 1.0)
    out.append(divider(c, 176, 0.8))
    out.append(fade_in(
        f'<text x="{x}" y="232" font-size="46" font-weight="700" fill="{c["crimson"]}" id="n-merged">{merged}</text>'
        f'<text x="{x}" y="258" font-size="14" letter-spacing="1" fill="{c["text"]}">merged upstream</text>',
        1.1,
    ))
    out.append(fade_in(
        f'<text x="{x + 250}" y="232" font-size="46" font-weight="700" fill="{c["head"]}" id="n-opened">{opened}</text>'
        f'<text x="{x + 250}" y="258" font-size="14" letter-spacing="1" fill="{c["text"]}">PRs opened</text>',
        1.3,
    ))
    out.append(fade_in(
        f'<text x="{x}" y="294" font-size="14" fill="{c["dim"]}">AgentScope · WeKnora · AI-Infra-Guard</text>'
        f'<text x="{x}" y="316" font-size="14" fill="{c["dim"]}">Dify · pydantic/logfire · OpenSandbox</text>',
        1.5,
    ))
    out.append(divider(c, 340, 1.6))
    out.append(fade_in(
        f'<circle cx="{x + 5}" cy="371" r="4" fill="{c["crimson"]}">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="{x + 18}" y="376" font-weight="700" fill="{c["head"]}">Sonar</text>'
        f'<text x="{x + 76}" y="376" font-size="12" fill="{c["dim"]}">live 24/7</text>'
        f'<text x="{x}" y="400" font-size="14" fill="{c["text"]}">price agent over 6 Japanese marketplaces</text>'
        f'<text x="{x}" y="422" font-size="14" fill="{c["dim"]}">470k+ price events tracked</text>',
        1.8,
    ))
    return out


def build(theme: str, merged: int, opened: int) -> str:
    c = THEMES[theme]
    defs = f"""<defs>
  <radialGradient id="glow">
    <stop offset="0" stop-color="{c['glow']}" stop-opacity="0.16"/>
    <stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="rule" x1="0" x2="1">
    <stop offset="0" stop-color="{c['crimson']}" stop-opacity="0.7"/>
    <stop offset="1" stop-color="{c['crimson']}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="name" gradientUnits="userSpaceOnUse" x1="440" y1="0" x2="580" y2="0">
    <stop offset="0" stop-color="{c['head']}"/>
    <stop offset="1" stop-color="{c['amber']}"/>
  </linearGradient>
</defs>"""
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f"font-family=\"ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace\" font-size=\"15\">",
        defs,
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        *radar(c),
        *right(c, merged, opened),
        "</svg>",
    ]
    return "\n".join(body) + "\n"


def current(name: str, default: int) -> int:
    path = ROOT / "assets" / "card-dark.svg"
    if path.exists():
        m = re.search(rf'id="{name}">(\d+)<', path.read_text(encoding="utf-8"))
        if m:
            return int(m.group(1))
    return default


def main() -> None:
    merged = int(sys.argv[1]) if len(sys.argv) > 1 else current("n-merged", 15)
    opened = int(sys.argv[2]) if len(sys.argv) > 2 else current("n-opened", 68)
    for theme in THEMES:
        (ROOT / "assets" / f"card-{theme}.svg").write_text(build(theme, merged, opened), encoding="utf-8")
    print(f"merged={merged} opened={opened}")


if __name__ == "__main__":
    main()
