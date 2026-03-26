import tkinter as tk
import customtkinter as ctk

from ui.components.factory import get_color, get_font, get_radius
from ui.ui_shared import CTkTooltip
from ui.components.lol_toggle import LolToggle
from core.constants import SPACING_SM, SPACING_MD
from tkinterdnd2 import TkinterDnD, DND_TEXT

class FriendPriorityList(ctk.CTkFrame, TkinterDnD.DnDWrapper):
    def __init__(self, master, config, lcu=None, **kw):
        super().__init__(master, fg_color="#0F1A24", corner_radius=8, **kw)
        self.config = config
        self.lcu = lcu

        self._expanded = True
        self._friends_data = self._get_priority_list()
        
        self._build_header()
        self._build_body()
        self._render_list()

    def _get_priority_list(self):
        return self.config.get("auto_join_list", [])

    def _save_priority_list(self, lst):
        self.config.set("auto_join_list", lst)

    def _build_header(self):
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=24)
        self.header.pack(fill="x", padx=SPACING_MD, pady=(SPACING_MD, 0))

        self.lbl_section = ctk.CTkLabel(
            self.header, text="▼  FRIEND AUTO-JOIN",
            font=get_font("caption", "bold"),
            text_color=get_color("colors.text.muted"), anchor="w",
        )
        self.lbl_section.pack(side="left", padx=2)
        self.lbl_section.bind("<Button-1>", lambda e: self._toggle_collapse())

        # Master Toggle
        self.var_master_enabled = ctk.BooleanVar(value=self.config.get("auto_join_enabled", True))
        def _on_master_toggle():
            self.config.set("auto_join_enabled", self.var_master_enabled.get())
        
        self.sw_master = LolToggle(self.header, variable=self.var_master_enabled, command=_on_master_toggle)
        self.sw_master.pack(side="left", padx=(10, 0))
        CTkTooltip(self.sw_master, "Enable or disable global Friend Auto-Join")

        # Clear All
        self.btn_clear_all = ctk.CTkButton(
            self.header, text="🗑️", width=20, height=20,
            corner_radius=10, font=("Segoe UI", 12),
            fg_color="transparent",
            text_color="#ff4444",
            hover_color="#4d1111",
            command=self._request_clear_all
        )
        self.btn_clear_all.pack(side="right", padx=2)
        CTkTooltip(self.btn_clear_all, "Clear priority list")

        # Refresh LCU friends
        self.btn_refresh = ctk.CTkButton(
            self.header, text="↻", width=20, height=20,
            corner_radius=10, font=("Arial", 14),
            fg_color="transparent",
            text_color=get_color("colors.accent.primary"),
            hover_color=get_color("colors.state.hover"),
            command=self._refresh_lcu_friends
        )
        self.btn_refresh.pack(side="right", padx=(2, 4))
        CTkTooltip(self.btn_refresh, "Load friends from Client")

        # Global Down Area
        self.btn_dn_global = ctk.CTkButton(
            self.header, text="▼", width=20, height=20,
            corner_radius=4,
            font=("Arial", 10), fg_color="transparent",
            hover_color=get_color("colors.state.hover"),
            text_color="#0F1A24",
            command=self._move_down_global,
            state="disabled"
        )
        self.btn_dn_global.pack(side="right", padx=0)

        # Global Up Area
        self.btn_up_global = ctk.CTkButton(
            self.header, text="▲", width=20, height=20,
            corner_radius=4,
            font=("Arial", 10), fg_color="transparent",
            hover_color=get_color("colors.state.hover"),
            text_color="#0F1A24",
            command=self._move_up_global,
            state="disabled"
        )
        self.btn_up_global.pack(side="right", padx=0)

    def _build_body(self):
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="x", pady=(SPACING_SM, SPACING_MD), padx=SPACING_MD)

        # Scrollable list
        self.scroll = ctk.CTkScrollableFrame(
            self.body, fg_color="transparent", height=150,
            scrollbar_button_color=get_color("colors.text.disabled"),
            scrollbar_button_hover_color=get_color("colors.text.muted"),
            scrollbar_fg_color="transparent",
        )
        try:
            self.scroll._scrollbar.configure(width=6)
        except Exception:
            pass
        self.scroll.pack(fill="x")

        self.list_parent = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.list_parent.pack(fill="x")

        # DND
        self.drop_target_register(DND_TEXT)
        self.dnd_bind('<<Drop>>', self._on_dnd_drop)

        # Initial fetch attempt
        self._refresh_lcu_friends()

    def _on_dnd_drop(self, event):
        text = event.data
        if not text: return
        names = [n.strip() for n in text.replace('\r', '\n').split('\n') if n.strip()]
        if not names: return
        
        hidden = self.config.get("hidden_friends", [])
        existing_names = [item.get("name") for item in self._friends_data]
        
        added_any = False
        for name in names:
            if name in hidden:
                hidden.remove(name)
            if name not in existing_names:
                self._friends_data.append({"name": name, "enabled": True})
                added_any = True
                
        if added_any:
            self.config.set("hidden_friends", hidden)
            self._save_priority_list(self._friends_data)
            self._render_list()

    def _toggle_collapse(self):
        self._expanded = not self._expanded
        if self._expanded:
            self.body.pack(fill="x", pady=(4, 0))
            self.lbl_section.configure(text="▼  FRIEND AUTO-JOIN")
        else:
            self.body.pack_forget()
            self.lbl_section.configure(text="▶  FRIEND AUTO-JOIN")

    def _request_clear_all(self):
        if not getattr(self, "_clear_confirm", False):
            self._clear_confirm = True
            orig_text = self.btn_clear_all.cget("text")
            orig_color = self.btn_clear_all.cget("text_color")

            self.btn_clear_all.configure(text="Sure?", text_color="#e81123")

            def reset():
                if self.winfo_exists() and getattr(self, "_clear_confirm", False):
                    self._clear_confirm = False
                    self.btn_clear_all.configure(text=orig_text, text_color=orig_color)

            self.after(2000, reset)
        else:
            self._commit_clear_all()

    def _commit_clear_all(self):
        self._clear_confirm = False
        self.btn_clear_all.configure(text="🗑️", text_color="#ff4444")
        
        hidden = self.config.get("hidden_friends", [])
        for f in self._friends_data:
            name = f.get("name")
            if name and name not in hidden:
                hidden.append(name)
        self.config.set("hidden_friends", hidden)

        self._friends_data = []
        self._save_priority_list(self._friends_data)
        self._render_list()

    def _refresh_lcu_friends(self):
        if hasattr(self, "btn_refresh"):
            self.btn_refresh.configure(text="...")
        if not self.lcu:
            return
        self.after(50, self._do_fetch_friends)

    def _do_fetch_friends(self):
        try:
            res = self.lcu.request("GET", "/lol-chat/v1/friends")
            if res and res.status_code == 200:
                friends = res.json()
                fetched_names = []
                for f in friends:
                    gn = f.get("gameName", "")
                    gt = f.get("gameTag", "")
                    if gn:
                        fetched_names.append(gn)
                
                hidden = self.config.get("hidden_friends", [])
                existing_names = [item.get("name") for item in self._friends_data]
                
                added_any = False
                for name in sorted(fetched_names, key=lambda x: x.lower()):
                    if name not in existing_names and name not in hidden:
                        self._friends_data.append({"name": name, "enabled": False})
                        added_any = True
                
                if added_any:
                    self._save_priority_list(self._friends_data)
                    self._render_list()

        except Exception:
            pass
        finally:
            if hasattr(self, "btn_refresh"):
                self.btn_refresh.configure(text="↻")

    def _render_list(self):
        for w in self.list_parent.winfo_children():
            w.destroy()

        lst = self._friends_data
        
        if not lst:
            lbl = ctk.CTkLabel(self.list_parent, text="No friends configured.\nLoad friends or Drag and Drop them here.", font=get_font("caption"), text_color=get_color("colors.text.muted"))
            lbl.pack(pady=20)
            return

        for i, item in enumerate(lst):
            row = ctk.CTkFrame(self.list_parent, fg_color="transparent", height=28)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            sel_idx = getattr(self, "_selected_index", -1)
            is_selected = (i == sel_idx)

            if is_selected:
                row.configure(fg_color=get_color("colors.accent.primary"))
                lbl_color = get_color("colors.background.app")
            else:
                lbl_color = get_color("colors.text.primary")

            # Toggle
            idx_var = ctk.BooleanVar(value=item.get("enabled", True))
            setattr(self, f"_var_friend_tog_{i}", idx_var) 
            
            def _on_tog(idx=i, var=idx_var):
                self._friends_data[idx]["enabled"] = var.get()
                self._save_priority_list(self._friends_data)

            sw = LolToggle(row, variable=idx_var, command=_on_tog)
            sw.pack(side="left", padx=(6, 10))
            CTkTooltip(sw, "Toggle active state")

            # Name Label
            lbl = ctk.CTkLabel(
                row, text=item.get("name", ""),
                font=get_font("body", "bold"),
                text_color=lbl_color,
                anchor="w"
            )
            lbl.pack(side="left", fill="x", expand=True)

            # Remove ✕
            btn_del = ctk.CTkButton(
                row, text="✕", width=24, height=24,
                corner_radius=4,
                font=("Arial", 12), fg_color="transparent",
                hover_color="#e81123", text_color=get_color("colors.text.muted") if not is_selected else get_color("colors.background.app"),
                command=lambda idx=i: self._remove_item(idx)
            )
            btn_del.pack(side="right", padx=(4, 6))
            CTkTooltip(btn_del, "Hide from layout")

            # Bind clicks
            def _select(event, idx=i):
                self._selected_index = idx
                self._render_list()

            row.bind("<Button-1>", _select)
            lbl.bind("<Button-1>", _select)

        # Update global arrows state
        sel = getattr(self, "_selected_index", -1)
        if hasattr(self, "btn_up_global"):
            if sel > 0:
                self.btn_up_global.configure(state="normal", text_color=get_color("colors.text.muted"))
            else:
                self.btn_up_global.configure(state="disabled", text_color="#0F1A24")
        if hasattr(self, "btn_dn_global"):
            if sel >= 0 and sel < len(lst) - 1:
                self.btn_dn_global.configure(state="normal", text_color=get_color("colors.text.muted"))
            else:
                self.btn_dn_global.configure(state="disabled", text_color="#0F1A24")

    def _move_up_global(self):
        idx = getattr(self, "_selected_index", -1)
        if idx <= 0: return
        self._friends_data[idx], self._friends_data[idx-1] = self._friends_data[idx-1], self._friends_data[idx]
        self._selected_index = idx - 1
        self._save_priority_list(self._friends_data)
        self._render_list()

    def _move_down_global(self):
        idx = getattr(self, "_selected_index", -1)
        if idx == -1 or idx >= len(self._friends_data) - 1: return
        self._friends_data[idx], self._friends_data[idx+1] = self._friends_data[idx+1], self._friends_data[idx]
        self._selected_index = idx + 1
        self._save_priority_list(self._friends_data)
        self._render_list()

    def _remove_item(self, idx):
        friend = self._friends_data.pop(idx)
        name = friend.get("name")
        if name:
            hidden = self.config.get("hidden_friends", [])
            if name not in hidden:
                hidden.append(name)
                self.config.set("hidden_friends", hidden)

        sel = getattr(self, "_selected_index", -1)
        if sel == idx:
            self._selected_index = -1
        elif sel > idx:
            self._selected_index -= 1
                
        self._save_priority_list(self._friends_data)
        self._render_list()
