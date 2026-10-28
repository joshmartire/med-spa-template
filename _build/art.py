# -*- coding: utf-8 -*-
"""Drawn artwork: one flat graphic language in the palette's colours (classes k-a accent, k-2 field 2, k-3 field 3,
k-i ink, k-p paper, plus tonal steps k-3l / k-3d / k-2d defined in main.css). Used where the clinic has no photograph
yet. Every drawing is a self-contained 400x400 square with its own background, built from flat shapes: no outlines,
no gradients, no shadows. The client's own photos (config hero_photo, category_photos) replace the drawings in the
big picture slots."""
import math


def _svg(inner, label=None, cls="art"):
    a11y = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return f'<svg class="{cls}" viewBox="0 0 400 400" preserveAspectRatio="xMidYMid slice" {a11y}>{inner}</svg>'


def _bg(c):
    return f'<rect class="{c}" x="0" y="0" width="400" height="400"/>'


def _ring(cx, cy, r, n, pr, cls, start=0):
    out = ""
    for i in range(n):
        t = math.radians(start + i * 360 / n)
        out += f'<circle class="{cls}" cx="{cx + r * math.cos(t):.1f}" cy="{cy + r * math.sin(t):.1f}" r="{pr}"/>'
    return out


def _peony(a, b, c, centre, leaf, bg):
    leaves = (_bg(bg) + f'<ellipse class="{leaf}" cx="304" cy="318" rx="96" ry="44" transform="rotate(-38 304 318)"/>'
              f'<ellipse class="{leaf}" cx="94" cy="304" rx="82" ry="38" transform="rotate(32 94 304)"/>')
    petals = (_ring(200, 190, 112, 9, 70, a, 10) + _ring(200, 190, 66, 8, 54, b, 30)
              + f'<circle class="{a}" cx="200" cy="190" r="62"/>' + _ring(200, 190, 34, 6, 28, b, 0)
              + f'<circle class="{c}" cx="200" cy="190" r="26"/>' + _ring(200, 190, 13, 6, 5, centre, 15) + f'<circle class="{centre}" cx="200" cy="190" r="6"/>')
    return leaves + petals


def peony(label=None, cls="art"):
    """The brand motif: a peony from above, rings of round petals and two leaves, on the deep field."""
    return _svg(_peony("k-a", "k-3", "k-p", "k-2", "k-2", "k-3"), label, cls)


def peony_tonal(label=None, cls="art"):
    """The hero square: the same peony in tones of the deep colour, so light type reads cleanly across it."""
    return _svg(_peony("k-3l", "k-3d", "k-a", "k-3", "k-3d", "k-3"), label, cls)


def vial(label=None, cls="art"):
    s = (_bg("k-3") + '<rect class="k-2d" x="0" y="318" width="400" height="82"/>'
         '<rect class="k-2" x="152" y="52" width="96" height="56" rx="12"/>'
         '<rect class="k-2d" x="142" y="100" width="116" height="28" rx="8"/>'
         '<rect class="k-p" x="164" y="124" width="72" height="30"/>'
         '<rect class="k-p" x="118" y="146" width="164" height="214" rx="36"/>'
         '<path class="k-a" d="M118 236 H282 V324 A36 36 0 0 1 246 360 H154 A36 36 0 0 1 118 324Z"/>'
         '<rect class="k-2" x="146" y="172" width="108" height="42" rx="8"/>'
         '<circle class="k-p" cx="240" cy="290" r="11"/><circle class="k-p" cx="212" cy="320" r="7"/>')
    return _svg(s, label, cls)


def lips(label=None, cls="art"):
    s = (_bg("k-2") + '<circle class="k-2d" cx="200" cy="210" r="156"/>'
         '<path class="k-a" d="M54 206 C96 156 136 124 170 140 C184 146 192 156 200 156 C208 156 216 146 230 140 C264 124 304 156 346 206 C300 212 252 216 200 216 C148 216 100 212 54 206Z"/>'
         '<path class="k-3" d="M54 206 C100 212 148 218 200 218 C252 218 300 212 346 206 C312 268 262 298 200 298 C138 298 88 268 54 206Z"/>'
         '<ellipse class="k-p" cx="246" cy="252" rx="34" ry="11" opacity=".55"/>')
    return _svg(s, label, cls)


def drop(label=None, cls="art"):
    s = (_bg("k-p") + '<circle class="k-2" cx="200" cy="300" r="96"/>'
         '<path class="k-a" d="M200 36 C200 36 92 172 92 250 C92 312 140 356 200 356 C260 356 308 312 308 250 C308 172 200 36 200 36Z"/>'
         '<path class="k-3" d="M308 250 C308 312 260 356 200 356 C162 356 128 338 108 308 C190 330 268 300 300 214 C305 226 308 238 308 250Z"/>'
         '<ellipse class="k-p" cx="156" cy="232" rx="20" ry="40" transform="rotate(18 156 232)"/>')
    return _svg(s, label, cls)


def roller(label=None, cls="art"):
    dots = "".join(f'<circle class="k-p" cx="{x}" cy="{y}" r="5"/>' for x in range(124, 290, 24) for y in (112, 140, 168))
    s = (_bg("k-p") + '<rect class="k-2" x="0" y="0" width="400" height="70"/>'
         '<rect class="k-a" x="96" y="88" width="208" height="104" rx="52"/>' + dots +
         '<rect class="k-3d" x="190" y="186" width="20" height="40"/>'
         '<rect class="k-3" x="176" y="222" width="48" height="150" rx="24"/>'
         '<rect class="k-p" x="190" y="246" width="20" height="54" rx="10" opacity=".5"/>')
    return _svg(s, label, cls)


def jar(label=None, cls="art"):
    s = (_bg("k-a") + '<circle class="k-p" cx="200" cy="222" r="150"/>'
         '<rect class="k-3" x="100" y="100" width="200" height="62" rx="16"/>'
         '<rect class="k-3d" x="100" y="146" width="200" height="16"/>'
         '<rect class="k-2" x="88" y="158" width="224" height="186" rx="40"/>'
         '<rect class="k-p" x="88" y="216" width="224" height="68"/>'
         '<circle class="k-3" cx="200" cy="250" r="17"/>')
    return _svg(s, label, cls)


def mirror(label=None, cls="art"):
    s = (_bg("k-a") + '<rect class="k-2" x="0" y="262" width="400" height="138"/>'
         '<rect class="k-3" x="184" y="230" width="32" height="150" rx="16"/>'
         '<circle class="k-3" cx="200" cy="160" r="128"/>'
         '<circle class="k-p" cx="200" cy="160" r="104"/>'
         '<path class="k-a" d="M128 112 a104 104 0 0 1 120 -50 L120 190 a104 104 0 0 1 8 -78Z"/>')
    return _svg(s, label, cls)


def beam(label=None, cls="art"):
    rays = "".join(f'<rect class="k-p" x="{200 - w / 2}" y="{y}" width="{w}" height="12" rx="6"/>' for y, w in ((206, 40), (230, 76), (254, 112), (278, 148)))
    s = (_bg("k-a") + '<rect class="k-2" x="0" y="302" width="400" height="98"/>'
         '<rect class="k-3" x="150" y="40" width="100" height="134" rx="24"/>'
         '<rect class="k-3d" x="164" y="164" width="72" height="32" rx="8"/>' + rays +
         '<circle class="k-a" cx="200" cy="90" r="18"/>'
         '<rect class="k-2d" x="70" y="334" width="260" height="16" rx="8"/>')
    return _svg(s, label, cls)


def sun(label=None, cls="art"):
    rays = "".join(f'<rect class="k-a" x="194" y="30" width="12" height="56" rx="6" transform="rotate({i * 30} 200 200)"/>' for i in range(12))
    s = (_bg("k-2") + rays + '<circle class="k-3" cx="200" cy="200" r="92"/>'
         '<circle class="k-a" cx="174" cy="178" r="16"/><circle class="k-a" cx="230" cy="206" r="11"/><circle class="k-a" cx="190" cy="236" r="8"/><circle class="k-p" cx="218" cy="166" r="6"/>')
    return _svg(s, label, cls)


def waves(label=None, cls="art"):
    s = (_bg("k-2") + "".join(f'<path class="{c}" d="M0 {y} C80 {y - 44} 140 {y - 44} 200 {y} C260 {y + 44} 320 {y + 44} 400 {y} V400 H0Z"/>'
                              for y, c in ((150, "k-a"), (220, "k-3"), (290, "k-p"))))
    return _svg(s, label, cls)


def contour(label=None, cls="art"):
    s = (_bg("k-a") + '<path class="k-3" d="M120 30 C150 120 108 170 116 236 C124 300 180 340 172 400 H0 V30Z"/>'
         '<path class="k-2" d="M290 0 C262 90 300 150 296 220 C292 290 246 330 256 400 H400 V0Z"/>'
         '<circle class="k-p" cx="208" cy="186" r="26"/>')
    return _svg(s, label, cls)


ART = {"peony": peony, "peony_tonal": peony_tonal, "vial": vial, "lips": lips, "drop": drop, "roller": roller, "jar": jar,
       "mirror": mirror, "beam": beam, "sun": sun, "waves": waves, "contour": contour}

CAT_ART = {"injectables": "vial", "skin": "drop", "laser": "beam"}


def draw(key, label=None, cls="art"):
    return ART[key](label, cls)
