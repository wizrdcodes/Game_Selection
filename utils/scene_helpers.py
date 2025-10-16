# utils/scene_helpers.py
import functools
from .helper_functions import has_seen_intro, remember_intro
from .io_helpers import print_wrapped, narrate

def _is_number_like(x: object) -> bool:
    if isinstance(x, (int, float)):
        return True
    if isinstance(x, str):
        s = x.strip()
        # simple numeric string check: 123 or 123.45
        if s.replace('.', '', 1).isdigit():
            return True
    return False

def _coerce_delay(x: object, default: float = 1.0) -> float:
    if x is None:
        return float(default)
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip()
        try:
            return float(s)
        except ValueError:
            return float(default)
    return float(default)

def _print_block(flat_list, *, default_delay: float = 1.0, scene_key: str | None = None):
    """
    Accepts a flat list where items can be:
      ["text", 1.2, "text2", "0.5", "text3", ...]
    If an item is a string and the NEXT item is number-like, the next item is used as its delay.
    Otherwise the default_delay is used.
    """
    if not flat_list:
        return
    normalized: list[str | float] = []
    i = 0
    n = len(flat_list)
    while i < n:
        text = flat_list[i]
        if not isinstance(text, str):
            text = str(text)
        if i + 1 < n and _is_number_like(flat_list[i + 1]):
            delay = _coerce_delay(flat_list[i + 1], default_delay)
            i += 2
        else:
            delay = default_delay
            i += 1
        normalized.extend([text, delay])
    narrate(normalized, default_delay=default_delay)

def _run_prelude(item):
    """
    Allowed forms:
      - callable() -> result
      - (fn,) -> fn()
      - (fn, args) -> fn(*args)
      - (fn, args, kwargs) -> fn(*args, **kwargs)
    If a prelude returns True, the scene entry is aborted.
    """
    if callable(item):
        return item()
    if not isinstance(item, tuple):
        raise TypeError(f"Invalid prelude action: {item!r}")
    if len(item) == 1:
        (fn,) = item
        return fn()
    if len(item) == 2:
        fn, args = item
        return fn(*args)
    fn, args, kwargs = item
    return fn(*args, **kwargs)

def go_to(scene_fn, **kwargs):
    """Handoff to a scene without re-running preludes/narration."""
    return scene_fn(only_options=True, **kwargs)

def scene_intro(entries, return_entries=None, preludes=None):
    """
    Decorator for scene functions.

    - entries:         flat list of text and optional numeric delays (default 1s if omitted)
                       OR a callable returning such a list (or nested lists/callables).
    - return_entries:  same as entries, used when intro has been seen (revisit).
    - preludes:        list of prelude actions run BEFORE intro text on real movement.
                       Each can be a callable or tuple accepted by _run_prelude.
                       If any returns True, scene entry is aborted.

    Wrapper understands:
      - force_intro=True          -> print entries, skip return_entries logic
      - only_options=True         -> suppress narration AND skip preludes (silent resume)
      - suppress_narration=True   -> same effect as only_options=True
    """
    def decorator(fn):
        key = fn.__name__.replace("scene_", "")

        @functools.wraps(fn)
        def wrapper(*args, force_intro=False, **kwargs):
            # Peek (do NOT pop) so the scene body can still branch on these flags
            only_options = bool(kwargs.get("only_options", False))
            suppress_narration = bool(kwargs.get("suppress_narration", False))
            suppress = only_options or suppress_narration

            # 1) Preludes only on real movement (not forced intros or silent resumes)
            if preludes and not force_intro and not suppress:
                for item in preludes:
                    prelude_result = _run_prelude(item)
                    if prelude_result:
                        return prelude_result # prelude handled (e.g., attack, slip, redirect)

            # 2) Resolve dynamic narration blocks (supports callables and lists of callables)
            def _resolve_block(block):
                if block is None:
                    return []
                if callable(block):
                    return _resolve_block(block())
                if isinstance(block, (list, tuple)):
                    out = []
                    for el in block:
                        out.extend(_resolve_block(el))
                    return out
                # assume atom (str/number)
                return [block]

            entries_block = _resolve_block(entries)
            return_block  = _resolve_block(return_entries)

            # 3) Narration (intro vs revisit) unless suppressed
            if not suppress:
                seen = has_seen_intro(key)
                if force_intro or not seen:
                    if entries_block:
                        _print_block(entries_block, default_delay=1.0, scene_key=key)
                    if not seen:
                        remember_intro(key)
                elif return_block:
                    _print_block(return_block, default_delay=1.0, scene_key=key)

            # 4) Hand control to the scene body (flags still available in kwargs)
            return fn(*args, **kwargs)

        return wrapper
    return decorator

