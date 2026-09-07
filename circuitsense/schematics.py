"""Small schematic render helpers.

Schemdraw is used when it is installed. The fallback strings keep the app usable
in restricted environments.
"""

from __future__ import annotations


def _try_schemdraw(draw_function):
    try:
        import schemdraw
        import schemdraw.elements as elm
    except Exception:
        return None
    return draw_function(schemdraw, elm)


def voltage_divider_svg() -> str | None:
    def draw(schemdraw, elm):
        with schemdraw.Drawing(show=False) as d:
            d += elm.SourceV().label("Vin")
            d += elm.Resistor().right().label("R1")
            d += elm.Dot().label("Vout")
            d += elm.Resistor().down().label("R2")
            d += elm.Ground()
            return d.get_imagedata("svg").decode("utf-8")

    return _try_schemdraw(draw)


def rc_low_pass_svg() -> str | None:
    def draw(schemdraw, elm):
        with schemdraw.Drawing(show=False) as d:
            d += elm.SourceSin().label("Vin")
            d += elm.Resistor().right().label("R")
            d += elm.Dot().label("Vout")
            d += elm.Capacitor().down().label("C")
            d += elm.Ground()
            return d.get_imagedata("svg").decode("utf-8")

    return _try_schemdraw(draw)


def rc_high_pass_svg() -> str | None:
    def draw(schemdraw, elm):
        with schemdraw.Drawing(show=False) as d:
            d += elm.SourceSin().label("Vin")
            d += elm.Capacitor().right().label("C")
            d += elm.Dot().label("Vout")
            d += elm.Resistor().down().label("R")
            d += elm.Ground()
            return d.get_imagedata("svg").decode("utf-8")

    return _try_schemdraw(draw)


def rlc_svg() -> str | None:
    def draw(schemdraw, elm):
        with schemdraw.Drawing(show=False) as d:
            d += elm.SourceSin().label("AC")
            d += elm.Resistor().right().label("R")
            d += elm.Inductor().right().label("L")
            d += elm.Capacitor().right().label("C")
            d += elm.Ground()
            return d.get_imagedata("svg").decode("utf-8")

    return _try_schemdraw(draw)


ASCII_SCHEMATICS = {
    "divider": "Vin -> R1 -> Vout -> R2 -> GND",
    "lowpass": "Vin -> R -> Vout, with C from Vout to GND",
    "highpass": "Vin -> C -> Vout, with R from Vout to GND",
    "rlc": "AC source -> R -> L -> C in series",
}

