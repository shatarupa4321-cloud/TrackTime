import customtkinter as ctk
from tkinter import messagebox
import time
import json
import os
from datetime import datetime
# ---------- APP SETTINGS ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
DATA_FILE = "sessions.json"
BG = "#111827"
CARD = "#1F2937"
WHITE = "#F9FAFB"
MUTED = "#9CA3AF"
PURPLE = "#8B5CF6"
GREEN = "#10B981"
BLUE = "#3B82F6"
RED = "#EF4444"
CARD_COLOURS = [
    "#263A5B",
    "#244A3D",
    "#594126",
    "#4B315F",
    "#56313B",
    "#254B50",
]
# ---------- DATA ----------
def load_sessions():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []
def save_sessions():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=4)
sessions = load_sessions()
start_time = None
active_session_name = ""
active_start_datetime = None
active_elapsed_before_pause = 0
# ---------- MAIN WINDOW ----------
app = ctk.CTk()
app.title("Session Tracker")
app.geometry("760x800")
app.minsize(620, 650)
app.configure(fg_color=BG)
# ---------- HEADER ----------
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(fill="x", padx=30, pady=(25, 12))
ctk.CTkLabel(
    header,
    text="SESSION TRACKER",
    font=("Segoe UI", 27, "bold"),
    text_color=WHITE
).pack(anchor="w")
ctk.CTkLabel(
    header,
    text="Track your day, one session at a time.",
    font=("Segoe UI", 13),
    text_color=MUTED
).pack(anchor="w", pady=(5, 0))
# ---------- TIMER CARD ----------
timer_card = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=20
)
timer_card.pack(fill="x", padx=30, pady=10)
ctk.CTkLabel(
    timer_card,
    text="SESSION TIMER",
    font=("Segoe UI", 12, "bold"),
    text_color=MUTED
).pack(pady=(20, 0))
timer_label = ctk.CTkLabel(
    timer_card,
    text="00:00:00",
    font=("Segoe UI", 48, "bold"),
    text_color="#C4B5FD"
)
timer_label.pack(pady=5)
timer_status = ctk.CTkLabel(
    timer_card,
    text="● Ready to start",
    font=("Segoe UI", 12),
    text_color=GREEN
)
timer_status.pack(pady=(0, 20))
# ---------- INPUT CARD ----------
input_card = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=18
)
input_card.pack(fill="x", padx=30, pady=10)
ctk.CTkLabel(
    input_card,
    text="What are you working on?",
    font=("Segoe UI", 14, "bold"),
    text_color=WHITE
).pack(anchor="w", padx=20, pady=(18, 8))
session_input = ctk.CTkEntry(
    input_card,
    placeholder_text="e.g. Python Project, Exercise, Cooking...",
    height=42,
    corner_radius=10,
    border_width=0,
    fg_color="#374151",
    text_color=WHITE,
    placeholder_text_color=MUTED,
    font=("Segoe UI", 12)
)
session_input.pack(fill="x", padx=20, pady=(0, 14))
button_row = ctk.CTkFrame(input_card, fg_color="transparent")
button_row.pack(fill="x", padx=20, pady=(0, 20))
# ---------- SESSION HISTORY HEADER ----------
history_header = ctk.CTkFrame(app, fg_color="transparent")
history_header.pack(fill="x", padx=30, pady=(15, 8))
ctk.CTkLabel(
    history_header,
    text="My Sessions",
    font=("Segoe UI", 20, "bold"),
    text_color=WHITE
).pack(side="left")
total_label = ctk.CTkLabel(
    history_header,
    text="0 sessions",
    font=("Segoe UI", 11),
    text_color="#C4B5FD"
)
total_label.pack(side="right")
# ---------- SCROLLABLE SESSION CARDS ----------
cards_frame = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent",
    corner_radius=12,
    scrollbar_button_color="#4B5563",
    scrollbar_button_hover_color=PURPLE
)
cards_frame.pack(fill="both", expand=True, padx=30, pady=(0, 25))
# ---------- HELPER ----------
def format_duration(seconds):
    seconds = max(0, int(seconds))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
# ---------- TIMER ----------
def update_timer():
    if start_time is not None:
        elapsed = active_elapsed_before_pause + int(time.time() - start_time)
        timer_label.configure(text=format_duration(elapsed))

    app.after(1000, update_timer)
# ---------- ADD SESSION ----------
def add_session():
    name = session_input.get().strip()
    if not name:
        messagebox.showwarning(
            "Missing session",
            "Please enter a session name."
        )
        return
    session = {
        "id": time.time_ns(),
        "name": name,
        "duration_seconds": 0,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start_time": "",
        "end_time": "",
        "colour": CARD_COLOURS[len(sessions) % len(CARD_COLOURS)],
        "manual": True
    }
    sessions.append(session)
    save_sessions()
    session_input.delete(0, "end")
    display_sessions()
# ---------- START TIMER ----------
def start_session():
    global start_time, active_session_name
    global active_start_datetime, active_elapsed_before_pause
    if start_time is not None:
        messagebox.showinfo(
            "Session running",
            "A session is already running."
        )
        return
    name = session_input.get().strip()
    if not name:
        messagebox.showwarning(
            "Missing session",
            "Please enter a session name first."
        )
        return
    active_session_name = name
    start_time = time.time()
    active_start_datetime = datetime.now()
    active_elapsed_before_pause = 0
    timer_label.configure(text="00:00:00")
    timer_status.configure(
        text=f"● In progress: {name}",
        text_color=GREEN
    )
    start_button.configure(state="disabled")
    add_button.configure(state="disabled")
    session_input.configure(state="disabled")
    stop_button.configure(state="normal")
# ---------- STOP AND SAVE ----------
def stop_session():
    global start_time, active_session_name
    global active_start_datetime, active_elapsed_before_pause
    if start_time is None:
        messagebox.showinfo(
            "No active session",
            "Start a session first."
        )
        return
    elapsed = active_elapsed_before_pause + int(time.time() - start_time)
    session = {
        "id": time.time_ns(),
        "name": active_session_name,
        "duration_seconds": elapsed,
        "date": active_start_datetime.strftime("%Y-%m-%d"),
        "start_time": active_start_datetime.strftime("%H:%M:%S"),
        "end_time": datetime.now().strftime("%H:%M:%S"),
        "colour": CARD_COLOURS[len(sessions) % len(CARD_COLOURS)],
        "manual": False
    }
    sessions.append(session)
    save_sessions()
    start_time = None
    active_session_name = ""
    active_start_datetime = None
    active_elapsed_before_pause = 0
    timer_label.configure(text="00:00:00")
    timer_status.configure(
        text="✓ Session saved successfully!",
        text_color=GREEN
    )
    start_button.configure(state="normal")
    add_button.configure(state="normal")
    session_input.configure(state="normal")
    stop_button.configure(state="disabled")
    session_input.delete(0, "end")
    display_sessions()
# ---------- EDIT SESSION NAME ----------
def edit_session(session_id):
    session_to_edit = next(
        (
            session for session in sessions
            if session.get("id") == session_id
        ),
        None
    )
    if session_to_edit is None:
        messagebox.showerror(
            "Error",
            "Session not found."
        )
        return
    dialog = ctk.CTkInputDialog(
        text="Enter the new session name:",
        title="Edit Session"
    )
    new_name = dialog.get_input()
    if new_name is None:
        return
    new_name = new_name.strip()
    if not new_name:
        messagebox.showwarning(
            "Missing name",
            "Session name cannot be empty."
        )
        return
    session_to_edit["name"] = new_name
    save_sessions()
    display_sessions()
    messagebox.showinfo(
        "Success",
        "Session name updated successfully!"
    )
# ---------- DELETE SESSION ----------
def delete_session(session_id):
    if not messagebox.askyesno(
        "Delete session",
        "Are you sure you want to delete this session?"
    ):
        return
    sessions[:] = [
        session for session in sessions
        if session.get("id") != session_id
    ]
    save_sessions()
    display_sessions()
# ---------- DISPLAY COLOURFUL CARDS ----------
def display_sessions():
    for widget in cards_frame.winfo_children():
        widget.destroy()
    total_seconds = sum(
        session.get("duration_seconds", 0)
        for session in sessions
    )
    total_label.configure(
        text=f"{len(sessions)} sessions  •  "
             f"{total_seconds // 3600}h "
             f"{(total_seconds % 3600) // 60}m tracked"
    )
    if not sessions:
        ctk.CTkLabel(
            cards_frame,
            text="No sessions yet.\nAdd your first session above!",
            font=("Segoe UI", 14),
            text_color=MUTED
        ).pack(pady=35)
        return
    for session in reversed(sessions):
        colour = session.get("colour", CARD)
        name = session.get("name", session.get("subject", "Session"))
        duration = session.get("duration_seconds", 0)
        card = ctk.CTkFrame(
            cards_frame,
            fg_color=colour,
            corner_radius=15
        )
        card.pack(fill="x", pady=7, padx=2)
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(14, 4))
        ctk.CTkLabel(
            top_row,
            text=f"●  {name}",
            font=("Segoe UI", 14, "bold"),
            text_color=WHITE,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            top_row,
            text=format_duration(duration),
            font=("Segoe UI", 13, "bold"),
            text_color=WHITE
        ).pack(side="right", padx=(8, 0))
        bottom_row = ctk.CTkFrame(card, fg_color="transparent")
        bottom_row.pack(fill="x", padx=16, pady=(4, 13))
        date_text = session.get("date", "Date unavailable")
        if session.get("manual"):
            detail = f"{date_text}  •  Manually added"
        else:
            detail = (
                f"{date_text}  •  "
                f"Started at {session.get('start_time', '--:--:--')}"
            )
        ctk.CTkLabel(
            bottom_row,
            text=detail,
            font=("Segoe UI", 10),
            text_color="#D1D5DB"
        ).pack(side="left")
        ctk.CTkButton(
            bottom_row,
            text="Edit",
            width=65,
            height=29,
            corner_radius=8,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            font=("Segoe UI", 10, "bold"),
            command=lambda sid=session.get("id"): edit_session(sid)
        ).pack(side="right", padx=(6, 0))
        ctk.CTkButton(
            bottom_row,
            text="Delete",
            width=78,
            height=29,
            corner_radius=8,
            fg_color=RED,
            hover_color="#DC2626",
            font=("Segoe UI", 10, "bold"),
            command=lambda sid=session.get("id"): delete_session(sid)
        ).pack(side="right")
# ---------- BUTTONS ----------
add_button = ctk.CTkButton(
    button_row,
    text="+ Add Session",
    height=42,
    corner_radius=10,
    fg_color=PURPLE,
    hover_color="#7C3AED",
    font=("Segoe UI", 12, "bold"),
    command=add_session
)
add_button.pack(side="left", fill="x", expand=True, padx=(0, 6))
start_button = ctk.CTkButton(
    button_row,
    text="▶ Start",
    height=42,
    corner_radius=10,
    fg_color=GREEN,
    hover_color="#059669",
    font=("Segoe UI", 12, "bold"),
    command=start_session
)
start_button.pack(side="left", fill="x", expand=True, padx=6)
stop_button = ctk.CTkButton(
    button_row,
    text="■ Stop & Save",
    height=42,
    corner_radius=10,
    fg_color=BLUE,
    hover_color="#2563EB",
    font=("Segoe UI", 12, "bold"),
    command=stop_session,
    state="disabled"
)
stop_button.pack(side="left", fill="x", expand=True, padx=(6, 0))
# ---------- RUN ----------
display_sessions()
update_timer()
app.mainloop()
