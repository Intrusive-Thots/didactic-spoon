---
name: Add Toggle Setting
description: Add a new boolean toggle to the sidebar automation panel and persist it in config
---

# Add Toggle Setting

## Steps

### 1. Add the config default
In `config.json`, add your new key with a default value:
```json
"my_new_toggle": false
```

### 2. Add the UI toggle in `ui/app_sidebar.py`
Inside `_setup_ui()`, after the existing toggle rows in the `automation_frame`:

```python
# My New Toggle
self.var_my_toggle = ctk.BooleanVar(value=self.config.get("my_new_toggle", False))
row_new = ctk.CTkFrame(self.automation_frame, fg_color="transparent", height=TOGGLE_ROW_HEIGHT)
row_new.pack(fill="x", padx=SPACING_MD, pady=(0, SPACING_SM))
row_new.pack_propagate(False)
lbl_new = ctk.CTkLabel(row_new, text="My Toggle", font=get_font("body"), width=120, anchor="w", text_color="#F0E6D2")
lbl_new.pack(side="left")
CTkTooltip(lbl_new, "Description of what this toggle does")
self.sw_my_toggle = LolToggle(row_new, variable=self.var_my_toggle, command=self._on_toggle_my_toggle)
self.sw_my_toggle.pack(side="right")
```

### 3. Add the callback
```python
def _on_toggle_my_toggle(self):
    self.config.set("my_new_toggle", self.var_my_toggle.get())
```

### 4. Increase automation_frame height
Increase `height=110` by `+28` for each new toggle row added.

### 5. Use the value in automation
In `services/automation.py`:
```python
if self.config.get("my_new_toggle"):
    # do something
```
