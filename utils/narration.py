# utils/narration.py
import sys, time, select, termios, tty, contextlib
from textwrap import fill

# Global toggles
IMMERSION = True        # your existing “allow immersion?” choice
SKIP_ALL = False        # set when user pressed 'S' at the very start
FAST_FORWARD = False    # set when user hits Enter during animation; cleared at the next prompt

# Terminal helpers (macOS/Linux)
@contextlib.contextmanager
def raw_stdin():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)   # immediately deliver keystrokes (no line buffering)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def enter_pressed_nonblocking():
    """Return True iff an Enter keypress is available right now; consume it."""
    if not sys.stdin.isatty():
        return False
    r, _, _ = select.select([sys.stdin], [], [], 0)
    if not r:
        return False
    ch = sys.stdin.read(1)
    # Swallow a full '\r\n' sequence if terminal sends CRLF
    if ch == '\r':
        # try to consume '\n' if present
        r2, _, _ = select.select([sys.stdin], [], [], 0)
        if r2:
            _ = sys.stdin.read(1)
        return True
    return ch == '\n'

def set_skip_all(value: bool):
    global SKIP_ALL
    SKIP_ALL = bool(value)

def reset_fast_forward():
    global FAST_FORWARD
    FAST_FORWARD = False

def _write_typewriter(text: str, char_delay: float = 0.02):
    """Typewriter effect with mid-stream fast-forward on Enter."""
    global FAST_FORWARD
    if SKIP_ALL or FAST_FORWARD or not IMMERSION or char_delay <= 0:
        sys.stdout.write(text)
        sys.stdout.flush()
        return

    with raw_stdin():
        for i, ch in enumerate(text):
            sys.stdout.write(ch)
            sys.stdout.flush()
            # if Enter is hit, fast-forward remainder of this paragraph and all subsequent ones
            if enter_pressed_nonblocking():
                FAST_FORWARD = True
                remaining = text[i+1:]
                sys.stdout.write(remaining)
                sys.stdout.flush()
                return
            time.sleep(char_delay)

def _wrap(text: str, width: int = 78) -> str:
    return fill(text, width=width)

def narrate(entries, default_delay: float = 1.0, char_delay: float = 0.02, width: int = 78):
    """
    Print a sequence of narrative paragraphs.
    entries: str OR flat [text, delay, text, delay, ...]
    """
    # Normalize to flat list of pairs
    if isinstance(entries, str):
        seq = [(entries, default_delay)]
    else:
        if len(entries) % 2 != 0:
            raise ValueError("entries must be a flat [text, delay, text, delay, ...] list")
        it = iter(entries)
        seq = [(t, d) for t, d in zip(it, it)]

    for idx, (text, delay) in enumerate(seq):
        # Draw wrapped text with typewriter effect
        paragraph = _wrap(text, width=width)
        _write_typewriter(paragraph, char_delay=char_delay)
        sys.stdout.write("\n")  # end of paragraph
        sys.stdout.flush()

        # Respect delay unless we’re skipping
        if SKIP_ALL or FAST_FORWARD or not IMMERSION:
            continue
        # small end-of-paragraph pause
        time.sleep(max(0.0, delay))

def print_wrapped(text: str, newline_delay: float = 1.0, **kw):
    """
    Backwards-compatible wrapper. You can start migrating callsites to 'narrate'
    with entries lists; this stays as a thin shim.
    """
    narrate(text, default_delay=newline_delay, **kw)

def prompt_input(prompt: str = "> "):
    """
    Use this instead of built-in input() to correctly reset fast-forward at menus.
    """
    # Any time we reach a real prompt, stop fast-forwarding.
    reset_fast_forward()
    # You can still typewriter the prompt itself if you want
    _write_typewriter(prompt, char_delay=0.0)  # no animation; instant
    return input()
