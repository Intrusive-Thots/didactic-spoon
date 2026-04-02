import threading
import tkinter as tk
import customtkinter as ctk

from ui.components.factory import get_color, get_font, get_radius, make_input
from ui.ui_shared import CTkTooltip
from core.constants import SPACING_SM, SPACING_MD
<<<<<<< HEAD
=======
from tkinterdnd2 import TkinterDnD, DND_TEXT

class SearchableDropdown(ctk.CTkFrame):
    def __init__(self, master, variable, command=None, **kwargs):
        # Remove pack_propagate to allow fluid width stretching based on expand=True
        super().__init__(master, fg_color="transparent", **kwargs)
        self.variable = variable
        self.command = command
        self._values = []
        self._filtered_values = []
        self._dropdown_frame = None
        
        self.entry = make_input(
            self,
            textvariable=self.variable,
            height=28
        )
        self.entry.pack(side="left", fill="both", expand=True)
        
        self.btn = ctk.CTkButton(
            self, text="▼", width=22, height=28,
            fg_color=get_color("colors.background.card"),
            hover_color=get_color("colors.state.hover"),
            command=self._toggle_dropdown, cursor="hand2",
            )
        self.btn.pack(side="right", fill="y", padx=(2, 0))
        
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<FocusIn>", self._on_focus)
        self.entry.bind("<Escape>", self._close_dropdown)
        
    def configure(self, values=None, **kwargs):
        if values is not None:
            self._values = values
            self._values_lower = [v.lower() for v in values]
            self._filtered_values = values
        super().configure(**kwargs)
        
    def _on_focus(self, event):
        if "name..." in self.variable.get():
            self.variable.set("")
            
    def _on_key(self, event):
        if event.keysym == "Return" and self.command:
            self._close_dropdown()
            self.command()
            return
            
        # ⚡ Bolt: Throttle search filtering and UI dropdown population on rapid keystrokes
        if hasattr(self, "_debounce_timer") and self._debounce_timer is not None:
            self.after_cancel(self._debounce_timer)

        self._debounce_timer = self.after(150, self._perform_search)

    def _perform_search(self):
        val = self.variable.get().lower()
        if hasattr(self, "_values_lower") and len(self._values_lower) == len(self._values):
            self._filtered_values = [v for v, v_lower in zip(self._values, self._values_lower) if val in v_lower]
        else:
            # ⚡ Bolt: Precompute values_lower if missing to prevent .lower() allocations on every keypress
            self._values_lower = [v.lower() for v in self._values]
            self._filtered_values = [v for v, v_lower in zip(self._values, self._values_lower) if val in v_lower]

        if self._dropdown_frame:
            self._populate_dropdown()
        else:
            self._open_dropdown()
            
    def _toggle_dropdown(self):
        if self._dropdown_frame:
            self._close_dropdown()
        else:
            self._filtered_values = self._values
            self._open_dropdown()
            
    def _close_dropdown(self, event=None):
        if self._dropdown_frame:
            try:
                self._dropdown_frame.place_forget()
                self._dropdown_frame.destroy()
            except Exception:
                pass
            self._dropdown_frame = None
            try:
                if hasattr(self, "_click_id"):
                    root = self.winfo_toplevel()
                    root.unbind("<Button-1>", self._click_id)
            except Exception:
                pass
            
    def _open_dropdown(self):
        if self._dropdown_frame: return
        
        root = self.winfo_toplevel()
        # 20% max size calculation
        root_h = root.winfo_height()
        h = max(100, int(root_h * 0.2))
        
        w = self.winfo_width()
        x = self.winfo_rootx() - root.winfo_rootx()
        y = self.winfo_rooty() - root.winfo_rooty() + self.winfo_height() + 2
        
        self._dropdown_frame = ctk.CTkScrollableFrame(
            root, width=w - 5, height=h,
            fg_color=get_color("colors.background.app"),
            border_width=1, border_color=get_color("colors.border.subtle"),
            corner_radius=4
        )
        # Place it floating
        self._dropdown_frame.place(x=x, y=y)
        self._dropdown_frame.lift()
        
        self._populate_dropdown()
        
        # Register global click to close, stored so we can unbind it
        self._click_id = root.bind("<Button-1>", self._check_click_outside, add="+")
        
    def _check_click_outside(self, event):
        if not self._dropdown_frame: return
        try:
            x, y = event.x_root, event.y_root
            fx, fy = self._dropdown_frame.winfo_rootx(), self._dropdown_frame.winfo_rooty()
            fw, fh = self._dropdown_frame.winfo_width(), self._dropdown_frame.winfo_height()
            
            ex, ey = self.winfo_rootx(), self.winfo_rooty()
            ew, eh = self.winfo_width(), self.winfo_height()
            
            in_dropdown = (fx <= x <= fx+fw) and (fy <= y <= fy+fh)
            in_entry = (ex <= x <= ex+ew) and (ey <= y <= ey+eh)
            
            if not in_dropdown and not in_entry:
                self._close_dropdown()
                
                # Unbind the exact callback
                root = self.winfo_toplevel()
                root.unbind("<Button-1>", self._click_id)
        except Exception:
            self._close_dropdown()
        
    def _populate_dropdown(self):
        for w in self._dropdown_frame.winfo_children():
            w.destroy()
            
        if not self._filtered_values:
            lbl = ctk.CTkLabel(self._dropdown_frame, text="No matches", font=get_font("caption"), text_color="gray")
            lbl.pack(pady=4)
            return
            
        # ⚡ Bolt: Apply LICM for faster dropdown population
        hover_color = get_color("colors.state.hover")

        for val in self._filtered_values:
            btn = ctk.CTkButton(
                self._dropdown_frame, text=val,
                fg_color="transparent", anchor="w",
                hover_color=hover_color,
                height=28,
                command=lambda v=val: self._select_val(v), cursor="hand2",
            )
            btn.pack(fill="x", pady=1)
            
    def _select_val(self, val):
        self.variable.set(val)
        self._close_dropdown()
        if self.command:
            self.after(10, self.command)

>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956

class FriendPriorityList(ctk.CTkFrame):
    def __init__(self, master, config, lcu=None, **kw):
        super().__init__(master, fg_color="#0F1A24", corner_radius=8, **kw)

        self.config = config
        self.lcu = lcu

        self._expanded = True
        self._friends_data = []  # Stores LCU friend objects
        self._auto_join_names = {f.get("name", "").lower(): f.get("enabled", True) for f in self.config.get("auto_join_list", [])}
        
        self._build_header()
        self._build_body()

        # Start fetching loop
        if self.lcu:
            self.after(200, self._fetch_lcu_friends_loop)

    def _save_priority_list(self):
        # Convert dictionary back to list of dicts for config
        lst = [{"name": name, "enabled": enabled} for name, enabled in self._auto_join_names.items()]
        self.config.set("auto_join_list", lst)

    def _build_header(self):
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=24)
        self.header.pack(fill="x", padx=SPACING_MD, pady=(SPACING_MD, 0))

        self.lbl_section = ctk.CTkLabel(
            self.header, text="▼  FRIEND LIST",
            font=get_font("caption", "bold"),
            text_color=get_color("colors.text.muted"), anchor="w",
            cursor="hand2"
        )
        self.lbl_section.pack(side="left", padx=2)
        self.lbl_section.bind("<Button-1>", lambda e: self._toggle_collapse())
        self.lbl_section.bind("<Enter>", lambda e: self.lbl_section.configure(text_color=get_color("colors.text.primary")))
        self.lbl_section.bind("<Leave>", lambda e: self.lbl_section.configure(text_color=get_color("colors.text.muted")))

        # Mass Invite button (right-aligned in header)
        self.btn_mass_invite = ctk.CTkButton(
            self.header, text="👥 Invite All", width=80, height=20,
            corner_radius=get_radius("sm"), font=get_font("caption", "bold"),
            fg_color="transparent",
            text_color=get_color("colors.text.muted"),
            hover_color=get_color("colors.state.hover"),
<<<<<<< HEAD
            command=self._on_mass_invite,
        )
        self.btn_mass_invite.pack(side="right")
        CTkTooltip(self.btn_mass_invite, "Invite all online friends (or VIPs) to your lobby")
=======
            text_color="#0F1A24",
            command=self._move_down_global,
            state="disabled", cursor="hand2",
            )
        self.btn_dn_global.pack(side="right", padx=0)
        CTkTooltip(self.btn_dn_global, "Move Down")

        # Global Up Area
        self.btn_up_global = ctk.CTkButton(
            self.header, text="▲", width=20, height=20,
            corner_radius=4,
            font=("Arial", 10), fg_color="transparent",
            hover_color=get_color("colors.state.hover"),
            text_color="#0F1A24",
            command=self._move_up_global,
            state="disabled", cursor="hand2",
            )
        self.btn_up_global.pack(side="right", padx=(0, 2))
        CTkTooltip(self.btn_up_global, "Move Up")
>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956

        # 🔮 Malcolm's Infusion: Export List Area
        self.btn_export = ctk.CTkButton(
            self.header, text="⎘", width=20, height=20,
            corner_radius=4, font=("Arial", 14),
            fg_color="transparent",
            text_color=get_color("colors.text.muted"),
            hover_color=get_color("colors.state.hover"),
            command=self._export_list, cursor="hand2",
            )
        self.btn_export.pack(side="right", padx=(0, 2))
        CTkTooltip(self.btn_export, "Export List to Clipboard")

    def _export_list(self):
        """Copies the active Friend Auto-Join list to the clipboard."""
        if not self._friends_data:
            from ui.components.toast import ToastManager
            ToastManager.get_instance().show("Friend list is empty!", icon="⚠️", theme="error")
            return

        names = [f.get("name", "") for f in self._friends_data if f.get("name", "")]
        export_str = "\n".join(names)

        self.clipboard_clear()
        self.clipboard_append(export_str)
        self.update()

        from ui.components.toast import ToastManager
        ToastManager.get_instance().show(
            "Friend List Copied!",
            icon="📋",
            theme="success",
            confetti=True
        )

    def _build_body(self):
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="x", pady=(SPACING_SM, SPACING_MD), padx=SPACING_MD)

<<<<<<< HEAD
=======
        # Add Input Row
        self.add_row = ctk.CTkFrame(self.body, fg_color="transparent")
        self.add_row.pack(fill="x", pady=(0, SPACING_SM))

        self.var_new_friend = ctk.StringVar()
        self.combo_add = SearchableDropdown(
            self.add_row,
            variable=self.var_new_friend,
            command=self._on_add_friend
            # Removed static width to allow fluid stretching
        )
        self.combo_add.pack(side="left", fill="x", expand=True, padx=(0, 6))
        # Default placeholder setup is handled inside logic

        self.btn_add = ctk.CTkButton(
            self.add_row, text="Add", width=36, height=28,
            font=get_font("body", "bold"),
            fg_color=get_color("colors.accent.primary"),
            hover_color="#005B99",
            text_color="#FFFFFF",
            command=self._on_add_friend, cursor="hand2",
            )
        self.btn_add.pack(side="right")

        # Scrollable list
>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956
        self.scroll = ctk.CTkScrollableFrame(
            self.body, fg_color="transparent", height=200,
            scrollbar_button_color=get_color("colors.text.disabled"),
            scrollbar_button_hover_color=get_color("colors.text.muted"),
            scrollbar_fg_color="transparent",
        )
        try:
            self.scroll._scrollbar.configure(width=6)
        except Exception:
            pass
        self.scroll.pack(fill="both", expand=True)

        self.list_parent = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.list_parent.pack(fill="x")

    def _fetch_lcu_friends_loop(self):
        if not self.winfo_exists() or not self.lcu:
            return

        def task():
            try:
                res = self.lcu.request("GET", "/lol-chat/v1/friends")
                if res and res.status_code == 200:
                    friends = res.json()
                    
                    # Sort active friends to top, then alphabetical
                    def sort_key(f):
                        avail = f.get("availability", "offline")
                        gn = f.get("gameName", "").lower()
                        prio = 1 if avail == "offline" else 0
                        return (prio, gn)
                        
                    friends.sort(key=sort_key)
                    self._friends_data = friends
                    self.after(0, self._render_list)
            except Exception:
                pass
            finally:
                if self.winfo_exists():
                    self.after(5000, self._fetch_lcu_friends_loop)
                    
        threading.Thread(target=task, daemon=True).start()

<<<<<<< HEAD
=======
    def _on_add_friend(self):
        name = self.var_new_friend.get().strip()
        if not name or "name..." in name: return
        
        # Check if already exists using an early-return generator expression
        name_lower = name.lower()
        exists = any(item.get("name", "").lower() == name_lower for item in self._friends_data)
        if not exists:
            self._friends_data.append({"name": name, "enabled": True})
            self._save_priority_list(self._friends_data)
            self._render_list()
        
        self.var_new_friend.set("")

    def _on_dnd_drop(self, event):
        text = event.data
        if not text: return
        names = [n.strip() for n in text.replace('\r', '\n').split('\n') if n.strip()]
        if not names: return
        
        # Use an O(1) set for lookups instead of checking a list in an O(N) loop
        existing_names = {item.get("name", "").lower() for item in self._friends_data}
        added_any = False
        
        for name in names:
            name_lower = name.lower()
            if name_lower not in existing_names:
                self._friends_data.append({"name": name, "enabled": True})
                existing_names.add(name_lower)
                added_any = True
                
        if added_any:
            self._save_priority_list(self._friends_data)
            self._render_list()

>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956
    def _toggle_collapse(self):
        self._expanded = not self._expanded
        if self._expanded:
            self.body.pack(fill="x", pady=(4, 0))
            self.lbl_section.configure(text="▼  FRIEND LIST")
        else:
            self.body.pack_forget()
            self.lbl_section.configure(text="▶  FRIEND LIST")

    def _toggle_auto_join(self, name):
        name_lower = name.lower()
        if name_lower in self._auto_join_names:
            current = self._auto_join_names[name_lower]
            if current:
                self._auto_join_names[name_lower] = False
            else:
                self._auto_join_names[name_lower] = True
        else:
            self._auto_join_names[name_lower] = True
            
        self._save_priority_list()
        self._render_list()

    def _show_context_menu(self, event, friend_name):
        menu = tk.Menu(self, tearoff=0, bg=get_color("colors.background.card"), fg="#F0E6D2")
        
        name_lower = friend_name.lower()
        is_auto = self._auto_join_names.get(name_lower, False)
        
        label = "Disable Auto-Join" if is_auto else "Enable Auto-Join"
        menu.add_command(label=label, command=lambda: self._toggle_auto_join(friend_name))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _get_render_signature(self):
        sig = []
        for f in self._friends_data:
            name = f.get("gameName", "")
            avail = f.get("availability", "offline")
            msg = f.get("availabilityMessage", "Online")
            is_auto = self._auto_join_names.get(name.lower(), False)
            sig.append(f"{name}|{avail}|{msg}|{is_auto}")
        return "|".join(sig)

    def _focus_add_input(self):
        # We don't need to check if it's expanded, because the button is only
        # visible if the list is expanded.
        self.combo_add.entry.focus_set()

    def _render_list(self):
        if not self.winfo_exists(): return
        
        sig = self._get_render_signature()
        if getattr(self, "_last_render_sig", None) == sig:
            return
        self._last_render_sig = sig
        
        for w in self.list_parent.winfo_children():
            w.destroy()
            
<<<<<<< HEAD
        if not self._friends_data:
            lbl = ctk.CTkLabel(self.list_parent, text="Checking friends...", font=get_font("caption"), text_color=get_color("colors.text.muted"))
            lbl.pack(pady=20)
            return

        for item in self._friends_data:
            name = item.get("gameName", "")
            if not name: continue
            
            avail = item.get("availability", "offline")
            status_msg = item.get("availabilityMessage", "Online") if avail != "offline" else "Offline"
            if avail in ("dnd", "away", "chat"):
                if not status_msg: status_msg = avail.capitalize()
                
=======
        lst = self._friends_data
        if not lst:
            # 🔮 Malcolm's Infusion: Interactive Empty State
            empty_btn = ctk.CTkButton(
                self.list_parent,
                text="+\nAdd Friend",
                font=get_font("body", "bold"),
                fg_color="transparent",
                border_width=1,
                border_color=get_color("colors.border.subtle"),
                text_color=get_color("colors.text.muted"),
                hover_color=get_color("colors.background.card"),
                width=180, height=80,
                corner_radius=8,
                command=self._focus_add_input,
                cursor="hand2"
            )
            empty_btn.pack(pady=20)
            return

        # ⚡ Bolt: Apply LICM for faster list rendering
        font_body_bold = get_font("body", "bold")
        color_text_primary = get_color("colors.text.primary")
        color_text_disabled = get_color("colors.text.disabled")
        color_state_success = get_color("colors.state.success")
        color_border_subtle = get_color("colors.border.subtle")
        color_text_muted = get_color("colors.text.muted")
        color_bg_app = get_color("colors.background.app")

        for i, item in enumerate(lst):
>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956
            row = ctk.CTkFrame(self.list_parent, height=44, fg_color="transparent")
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            # Hover Feedback
            def on_enter(e, r=row):
                r.configure(fg_color="#182531")
            def on_leave(e, r=row):
                r.configure(fg_color="transparent")

            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)

            # Auto-Join Dot indicator
            action_frame = ctk.CTkFrame(row, fg_color="transparent", width=20)
            action_frame.pack(side="left", fill="y", padx=(8, 4))
            
            is_auto = self._auto_join_names.get(name.lower(), False)
            dot_color = get_color("colors.state.success") if is_auto else get_color("colors.state.error")
            
            status = ctk.CTkLabel(action_frame, text="●", text_color=dot_color, font=("Arial", 14))
            status.pack(side="left", pady=(10,0))
            CTkTooltip(status, "Auto-Join: ON" if is_auto else "Auto-Join: OFF")

            # Name + Status
            text_frame = ctk.CTkFrame(row, fg_color="transparent")
            text_frame.pack(side="left", expand=True, fill="x")

            lbl_name = ctk.CTkLabel(
<<<<<<< HEAD
                text_frame, text=name,
                font=get_font("body", "bold"),
                text_color=get_color("colors.text.primary") if avail != "offline" else get_color("colors.text.disabled"),
=======
                text_frame, text=item.get("name", ""),
                font=font_body_bold,
                text_color=color_text_primary if enabled else color_text_disabled,
>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956
            )
            lbl_name.pack(anchor="w", pady=(4, 0))

            lbl_sub = ctk.CTkLabel(
                text_frame,
<<<<<<< HEAD
                text=status_msg,
                text_color="#A0A7B0" if avail != "offline" else get_color("colors.text.disabled"),
=======
                text="Active" if enabled else "Ignored",
                text_color="#A0A7B0" if enabled else color_text_disabled,
>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956
                font=("Segoe UI", 10)
            )
            lbl_sub.pack(anchor="w", pady=(0, 4))

<<<<<<< HEAD
            # Bind right click context menu
            def _popup(e, fn=name):
                self._show_context_menu(e, fn)

            row.bind("<Button-3>", _popup)
            text_frame.bind("<Button-3>", _popup)
            lbl_name.bind("<Button-3>", _popup)
            lbl_sub.bind("<Button-3>", _popup)
            status.bind("<Button-3>", _popup)
=======
            # Actions (Right side layout)
            action_frame = ctk.CTkFrame(row, fg_color="transparent")
            action_frame.pack(side="right", fill="y")
            
            # Status Indicator
            status_color = color_state_success if enabled else color_border_subtle
            status = ctk.CTkLabel(action_frame, text="●", text_color=status_color)
            status.pack(side="left", padx=(0, 6))

            btn_del = ctk.CTkButton(
                action_frame, text="✕", width=20, height=20,
                corner_radius=4, font=("Arial", 10), fg_color="transparent",
                hover_color="#e81123", text_color=color_text_muted if not is_selected else color_bg_app,
                command=lambda idx=i: self._remove_item(idx), cursor="hand2",
            )
            btn_del.pack(side="left", padx=(0, 4))
            CTkTooltip(btn_del, "Remove friend")
>>>>>>> 48a56ccccbee3ca92d42a0af9b88293e3b4c3956

    def _on_mass_invite(self):
        """Delegate mass invite to the automation engine via the widget tree."""
        root = self.winfo_toplevel()
        engine = getattr(root, "automation", None)
        if engine:
            import threading
            threading.Thread(target=engine.mass_invite_friends, daemon=True).start()
        else:
            try:
                from ui.components.toast import ToastManager
                ToastManager.get_instance().show("Automation engine not available.", icon="⚠️", theme="error")
            except Exception:
                pass
