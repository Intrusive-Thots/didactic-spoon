import customtkinter as ctk

from ui.components.factory import get_color, get_font, get_radius

class AboutPage(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("About LeagueLoop")
        self.geometry("460x380")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=get_color("colors.background.app"))
        
        self.update_idletasks()
        try:
            x = master.winfo_rootx() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
            y = master.winfo_rooty() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
            self.geometry(f"+{int(x)}+{int(y)}")
        except Exception:
            pass
            
        self._setup_ui()
        self.focus_force()

    def _setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="#0A1428", corner_radius=0, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="ⓘ  INFO & ABOUT",
            font=("Beaufort for LOL", 16, "bold"),
            text_color="#C8AA6E",
        ).pack(side="left", padx=16, pady=16)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            body, 
            text="LeagueLoop is a companion overlay application designed to automate\n"
                 "and streamline League of Legends lobbies and matchmaking.",
            font=get_font("body"),
            text_color=get_color("colors.text.primary"),
            justify="left"
        ).pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(
            body, 
            text="How it works:\n"
                 "It interfaces directly with the official League Client Update (LCU) API\n"
                 "to safely read client state and send lobby commands automatically,\n"
                 "bypassing manual clicks without modifying game files.",
            font=get_font("body"),
            text_color=get_color("colors.text.muted"),
            justify="left"
        ).pack(anchor="w", pady=(0, 16))

        disclaimer_frame = ctk.CTkFrame(body, fg_color=get_color("colors.background.card"), corner_radius=get_radius("md"))
        disclaimer_frame.pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(
            disclaimer_frame, 
            text="LEGAL & LIABILITY WAIVER",
            font=get_font("caption", "bold"),
            text_color="#e81123",
        ).pack(anchor="w", padx=12, pady=(12, 4))
        
        ctk.CTkLabel(
            disclaimer_frame, 
            text="LeagueLoop was created under Riot Games' policy using assets\n"
                 "owned by Riot Games. Riot Games does not endorse or sponsor\n"
                 "this project. Furthermore, the creator is NOT liable for any\n"
                 "account suspensions, spontaneous PC combustion, or emotional\n"
                 "damage incurred while using this software. Use entirely at\n"
                 "your own risk.",
            font=get_font("caption"),
            text_color=get_color("colors.text.muted"),
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 12))

        footer = ctk.CTkFrame(body, fg_color="transparent")
        footer.pack(fill="x", side="bottom")

        ctk.CTkLabel(
            footer, text="Made by Malcolm Hopper",
            font=get_font("body", "bold"),
            text_color="#C8AA6E",
        ).pack(side="left")

        ctk.CTkLabel(
            footer, text="Banned.Malcolm@gmail.com",
            font=get_font("body", "bold"),
            text_color="#4B5E73",
        ).pack(side="right")
