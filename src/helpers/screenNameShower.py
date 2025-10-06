from psychopy import visual

def _corner_pos(win, corner="bottom-right", margin=30, units=None):
    """
    Compute a corner position for the given window and units.
    margin is in the window's units:
      - 'pix': pixels
      - 'norm': ~[-1..1]
      - 'height': y ~[-0.5..0.5], x scales with aspect
    """
    units = units or getattr(win, "units", "pix")
    w, h = win.size  # in pixels

    if units == "pix":
        half_w, half_h = w/2, h/2
        x_right  =  half_w - margin
        x_left   = -half_w + margin
        y_top    =  half_h - margin
        y_bottom = -half_h + margin
    elif units == "norm":
        # corners at ±1; a margin like 0.05 works nicely
        x_right, x_left =  1 - margin, -1 + margin
        y_top, y_bottom =  1 - margin, -1 + margin
    elif units == "height":
        # y in [-0.5..0.5], x scales with aspect = w/h
        aspect = float(w)/float(h)
        x_right, x_left =  (aspect/2 - margin), -(aspect/2 - margin)
        y_top, y_bottom =  (0.5 - margin), -(0.5 - margin)
    else:
        # Fallback: treat like norm
        x_right, x_left =  1 - margin, -1 + margin
        y_top, y_bottom =  1 - margin, -1 + margin

    if corner == "bottom-right": return (x_right,  y_bottom)
    if corner == "bottom-left":  return (x_left,   y_bottom)
    if corner == "top-right":    return (x_right,  y_top)
    if corner == "top-left":     return (x_left,   y_top)
    return (x_right, y_bottom)


def show_screen_name(
    window,
    name,                      # e.g., "A" or "B"
    *,
    corner="bottom-right",
    margin=30,                 # 'pix' windows: pixels; 'norm': 0.05-ish; 'height': 0.03–0.05
    tag_size=40,               # square size (in window units)
    text_height=28,            # text height inside the square
    bg_color="black",
    text_color="#F5F5DC",
    bg_opacity=1.0,
    flip=False
):
    """
    Draws a small labeled tag in the chosen corner of the window.
    Does NOT clear the screen; you can call it before a single flip.

    Tip: set flip=False when composing with other draw calls and
    call window.flip() once at the end.
    """
    # Convert tag_size / margin defaults for non-pixel units
    units = getattr(window, "units", "pix")
    if units == "norm" and isinstance(tag_size, (int, float)) and tag_size > 1:
        # Provide a sensible default if user passed pixel-like sizes
        tag_size = 0.12
        text_height = 0.08
        if margin == 30: margin = 0.05
    if units == "height" and isinstance(tag_size, (int, float)) and tag_size > 1:
        tag_size = 0.08
        text_height = 0.06
        if margin == 30: margin = 0.035

    pos = _corner_pos(window, corner=corner, margin=margin)

    # Tag background (square)
    tag_rect = visual.Rect(
        win=window,
        width=tag_size,
        height=tag_size,
        fillColor=bg_color,
        lineColor=None,
        pos=pos,
        opacity=bg_opacity
    )
    tag_rect.draw()

    # Label
    label = visual.TextStim(
        win=window,
        text=str(name),
        color=text_color,
        height=text_height,
        pos=pos
    )
    label.draw()

    if flip:
        window.flip()
