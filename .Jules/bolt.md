## 2024-05-24 - Faster Queue Polling
**Learning:** In high-frequency polling loops (like CustomTkinter's `after` events running at ~16ms), the EAFP pattern `try: queue.get_nowait() except queue.Empty:` is surprisingly slower than `if not queue.empty(): queue.get_nowait()`. Raising and catching the exception thousands of times a second adds unnecessary overhead when the queue is frequently empty.
**Action:** Use `if not queue.empty():` check before `get_nowait()` in tight UI polling loops.

## 2024-06-12 - Fast Theme Token Resolution
**Learning:** The UI extensively calls helper functions like `get_color(path)` and `get_font(type)` to resolve design tokens. Deep dictionary lookups `TOKENS.get(...)` coupled with string parsing (`path.split('.')`) multiple times per widget creation and during hover/focus events introduces measurable latency in the main UI thread.
**Action:** Apply `@functools.lru_cache` to UI styling helper functions (`get_color`, `get_font`, `get_radius`, `parse_border`) to avoid repetitive string manipulations and dict lookups.

## 2024-06-25 - Avoid Dynamic Event Colors
**Learning:** Computing visual effect states (like string hex code lighten/darken math in `apply_click_animation`) dynamically *inside* event handler callbacks like `on_click(_)` introduces measurable string manipulation latency on the main UI thread during every interaction.
**Action:** Precompute standard event colors in the closure scope of effect binders instead of computing them on the fly during the interaction event itself.
