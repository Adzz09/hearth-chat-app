import tkinter as tk
from tkinter import messagebox
import pymysql as c

db = c.connect(#DB_CONFIG)
cr = db.cursor()

current_user_id = None
current_chat_user = None
chat_contacts = {}
last_message_count = 0

COLORS = {
    "bg": "#f6efe6",
    "panel": "#efe2d2",
    "panel_alt": "#e4cfb7",
    "sidebar": "#d7bea5",
    "sidebar_hover": "#c8ab8f",
    "accent": "#8b5e3c",
    "accent_hover": "#734b2f",
    "chat_bg": "#fbf6f0",
    "message_sent": "#8b5e3c",
    "message_received": "#eadccf",
    "text_primary": "#3e2a1f",
    "text_secondary": "#6b4e3d",
    "text_light": "#fffaf4",
    "input_bg": "#fffaf4",
    "border": "#cdb296"
}


def app():
    global root, enty_usr, enty_pss, chat_list, message_entry, chat_title, msg_scrollable_frame, msg_canvas

    root = tk.Tk()
    root.geometry("920x640")
    root.minsize(820, 580)
    root.title("Hearth")
    root.configure(bg=COLORS["bg"])

    def make_button(parent, text, command, bg=None, fg=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg or COLORS["accent"],
            fg=fg or COLORS["text_light"],
            activebackground=COLORS["accent_hover"] if bg is None else COLORS["sidebar_hover"],
            activeforeground=fg or COLORS["text_light"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 11),
            padx=16,
            pady=10
        )

    # ---------------- LOGIN ---------------- #
    def login():
        global current_user_id
        usrnm = enty_usr.get()
        password = enty_pss.get()

        if not usrnm or not password:
            messagebox.showerror("Error", "Fill all fields")
            return

        cr.execute("SELECT id FROM users WHERE user_name=%s AND password=%s", (usrnm, password))
        result = cr.fetchone()

        if result:
            current_user_id = result[0]
            load_contacts()
            show_chat_ui()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register():
        usrnm = enty_usr.get()
        password = enty_pss.get()

        if not usrnm or not password:
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            cr.execute("INSERT INTO users (user_name, password) VALUES (%s, %s)", (usrnm, password))
            db.commit()
            messagebox.showinfo("Success", "Registered! Login now.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- DATA ---------------- #
    def load_contacts():
        global chat_contacts
        cr.execute("SELECT id, user_name FROM users WHERE id != %s", (current_user_id,))
        chat_contacts = {name: uid for uid, name in cr.fetchall()}

    # ---------------- CHAT ---------------- #
    def send_message():
        msg = message_entry.get().strip()
        if not msg or current_chat_user is None:
            return

        cr.execute(
            "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
            (current_user_id, current_chat_user, msg)
        )
        db.commit()
        message_entry.delete(0, tk.END)
        load_messages()

    def load_messages():
        global last_message_count

        for widget in msg_scrollable_frame.winfo_children():
            widget.destroy()

        if current_chat_user is None:
            return

        cr.execute(
            "SELECT message, sender_id FROM messages WHERE (sender_id=%s AND receiver_id=%s) "
            "OR (sender_id=%s AND receiver_id=%s) ORDER BY id ASC",
            (current_user_id, current_chat_user, current_chat_user, current_user_id)
        )

        messages = cr.fetchall()
        last_message_count = len(messages)

        for msg, sender in messages:
            frame = tk.Frame(msg_scrollable_frame, bg=COLORS["chat_bg"])
            frame.pack(fill="x", pady=4)

            if sender == current_user_id:
                bubble = tk.Label(
                    frame,
                    text=msg,
                    bg=COLORS["message_sent"],
                    fg=COLORS["text_light"],
                    padx=14,
                    pady=10,
                    wraplength=400,
                    font=("Segoe UI", 11)
                )
                bubble.pack(anchor="e", padx=10)
            else:
                bubble = tk.Label(
                    frame,
                    text=msg,
                    bg=COLORS["message_received"],
                    fg=COLORS["text_primary"],
                    padx=14,
                    pady=10,
                    wraplength=400,
                    font=("Segoe UI", 11)
                )
                bubble.pack(anchor="w", padx=10)

        msg_canvas.update_idletasks()
        msg_canvas.yview_moveto(1.0)

    def auto_refresh():
        if current_chat_user:
            cr.execute(
                "SELECT COUNT(*) FROM messages WHERE (sender_id=%s AND receiver_id=%s) "
                "OR (sender_id=%s AND receiver_id=%s)",
                (current_user_id, current_chat_user, current_chat_user, current_user_id)
            )

            count = cr.fetchone()[0]
            if count != last_message_count:
                load_messages()

        root.after(1000, auto_refresh)

    # ---------------- UI ---------------- #
    def show_chat_ui():
        global chat_title, message_entry, chat_list, msg_scrollable_frame, msg_canvas

        for w in root.winfo_children():
            w.destroy()

        shell = tk.Frame(root, bg=COLORS["bg"])
        shell.pack(fill="both", expand=True, padx=18, pady=18)

        sidebar = tk.Frame(
            shell,
            bg=COLORS["sidebar"],
            width=260,
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Hearth",
            fg=COLORS["text_primary"],
            bg=COLORS["sidebar"],
            font=("Georgia", 24, "bold")
        ).pack(anchor="w", padx=22, pady=(24, 4))

        tk.Label(
            sidebar,
            text="A softer place to chat",
            fg=COLORS["text_secondary"],
            bg=COLORS["sidebar"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=22, pady=(0, 18))

        chat_list = tk.Frame(sidebar, bg=COLORS["sidebar"])
        chat_list.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        for name, uid in chat_contacts.items():
            btn = tk.Button(
                chat_list,
                text="  " + name,
                bg=COLORS["sidebar"],
                fg=COLORS["text_primary"],
                activebackground=COLORS["sidebar_hover"],
                activeforeground=COLORS["text_primary"],
                relief="flat",
                bd=0,
                anchor="w",
                pady=12,
                padx=10,
                cursor="hand2",
                font=("Segoe UI Semibold", 11),
                command=lambda u=uid, n=name: open_chat(u, n)
            )
            btn.pack(fill="x", pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["sidebar_hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["sidebar"]))

        main = tk.Frame(
            shell,
            bg=COLORS["chat_bg"],
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        main.pack(side="right", fill="both", expand=True, padx=(18, 0))

        top_bar = tk.Frame(main, bg=COLORS["panel"], height=76)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        chat_title = tk.Label(
            top_bar,
            text="Choose a conversation",
            bg=COLORS["panel"],
            fg=COLORS["text_primary"],
            font=("Georgia", 18, "bold")
        )
        chat_title.pack(anchor="w", padx=24, pady=(14, 2))

        tk.Label(
            top_bar,
            text="Messages feel better with a little warmth.",
            bg=COLORS["panel"],
            fg=COLORS["text_secondary"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=24)

        global msg_container, bottom
        msg_container = tk.Frame(main, bg=COLORS["chat_bg"])
        msg_container.pack(fill="both", expand=True, padx=12, pady=12)

        msg_canvas = tk.Canvas(msg_container, bg=COLORS["chat_bg"], highlightthickness=0)
        msg_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(msg_container, command=msg_canvas.yview, troughcolor=COLORS["panel"])
        scrollbar.pack(side="right", fill="y")

        msg_canvas.configure(yscrollcommand=scrollbar.set)

        msg_scrollable_frame = tk.Frame(msg_canvas, bg=COLORS["chat_bg"])
        msg_canvas.create_window((0, 0), window=msg_scrollable_frame, anchor="nw")

        msg_scrollable_frame.bind(
            "<Configure>",
            lambda e: msg_canvas.configure(scrollregion=msg_canvas.bbox("all"))
        )

        bottom = tk.Frame(main, bg=COLORS["panel"], padx=12, pady=12)
        bottom.pack_forget()

        entry_shell = tk.Frame(
            bottom,
            bg=COLORS["input_bg"],
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        entry_shell.pack(side="left", fill="x", expand=True, padx=(0, 10))

        message_entry = tk.Entry(
            entry_shell,
            bg=COLORS["input_bg"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            font=("Segoe UI", 12),
            bd=0
        )
        message_entry.pack(fill="x", padx=14, pady=12)
        message_entry.bind("<Return>", lambda e: send_message())

        send_btn = tk.Button(
            bottom,
            text="Send",
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 11),
            padx=20,
            pady=12,
            command=send_message
        )
        send_btn.pack(side="right")

        auto_refresh()

    def open_chat(uid, name):
        global current_chat_user
        current_chat_user = uid
        chat_title.config(text=name)
        bottom.pack(fill="x", pady=(10, 0))
        load_messages()

    # ---------------- LOGIN UI ---------------- #
    def show_login():
        for w in root.winfo_children():
            w.destroy()

        outer = tk.Frame(root, bg=COLORS["bg"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            outer,
            text="Hearth",
            fg=COLORS["accent"],
            bg=COLORS["bg"],
            font=("Georgia", 38, "bold")
        ).pack(pady=(0, 6))

        tk.Label(
            outer,
            text="A warm little space for your messages",
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"],
            font=("Segoe UI", 11)
        ).pack(pady=(0, 18))

        frame = tk.Frame(
            outer,
            bg=COLORS["panel"],
            padx=28,
            pady=28,
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        frame.pack()

        tk.Label(
            frame,
            text="Welcome",
            fg=COLORS["text_primary"],
            bg=COLORS["panel"],
            font=("Georgia", 22, "bold")
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            frame,
            text="Sign in or create an account to continue",
            fg=COLORS["text_secondary"],
            bg=COLORS["panel"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 18))

        tk.Label(
            frame,
            text="Username",
            fg=COLORS["text_secondary"],
            bg=COLORS["panel"],
            font=("Segoe UI Semibold", 10)
        ).pack(anchor="w")

        global enty_usr
        enty_usr = tk.Entry(
            frame,
            font=("Segoe UI", 12),
            bg=COLORS["input_bg"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        enty_usr.pack(fill="x", pady=(6, 14), ipady=9)

        tk.Label(
            frame,
            text="Password",
            fg=COLORS["text_secondary"],
            bg=COLORS["panel"],
            font=("Segoe UI Semibold", 10)
        ).pack(anchor="w")

        global enty_pss
        enty_pss = tk.Entry(
            frame,
            show="*",
            font=("Segoe UI", 12),
            bg=COLORS["input_bg"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        enty_pss.pack(fill="x", pady=(6, 22), ipady=9)

        make_button(frame, "Login", login).pack(fill="x", pady=(0, 10))
        make_button(
            frame,
            "Create account",
            register,
            bg=COLORS["panel_alt"],
            fg=COLORS["text_primary"]
        ).pack(fill="x")

    show_login()
    root.mainloop()


app()
