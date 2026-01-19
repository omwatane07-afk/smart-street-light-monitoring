import serial
import tkinter as tk
from tkinter import ttk
from datetime import datetime

SERIAL_PORT = 'COM7'
BAUD_RATE = 9600

BG_MAIN = "#050813"
CARD_BG = "#101827"
CARD_BORDER = "#2b3a5a"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#9ca3af"
ACCENT_CYAN = "#22d3ee"
IR_YELLOW = "#facc15"
IR_GREEN = "#22c55e"
LED_ON = "#22c55e"
LED_OFF = "#4b5563"
LED_OFF_BORDER = "#f97373"

TITLE_FONT = ("Segoe UI", 26, "bold")
SECTION_TITLE_FONT = ("Segoe UI", 18, "bold")
LABEL_FONT = ("Segoe UI", 14)
BIG_FONT = ("Segoe UI", 32, "bold")

root = tk.Tk()
root.title("Smart Street Light Monitoring System")
root.state("zoomed")
root.configure(bg=BG_MAIN)

title_lbl = tk.Label(root, text="Smart Street Light Monitoring System",
                     font=TITLE_FONT, fg=ACCENT_CYAN, bg=BG_MAIN)
title_lbl.pack(pady=20)

main_card = tk.Frame(root, bg=CARD_BG, bd=2, relief="ridge")
main_card.pack(padx=40, pady=10, fill="both", expand=True)

left_frame = tk.Frame(main_card, bg=CARD_BG)
right_frame = tk.Frame(main_card, bg=CARD_BG)
bottom_frame = tk.Frame(main_card, bg=CARD_BG)

left_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
right_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
bottom_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="nsew")

main_card.grid_rowconfigure(0, weight=3)
main_card.grid_rowconfigure(1, weight=1)
main_card.grid_columnconfigure(0, weight=1)
main_card.grid_columnconfigure(1, weight=1)

# ---------- Lights card ----------
lights_card = tk.Frame(left_frame, bg=CARD_BG, bd=2, relief="ridge",
                       highlightbackground=CARD_BORDER)
lights_card.pack(fill="both", expand=True)

tk.Label(lights_card, text="Street Lights Status",
         font=SECTION_TITLE_FONT, fg=ACCENT_CYAN,
         bg=CARD_BG).pack(anchor="w", padx=25, pady=20)

light_vars = []
light_labels = []

for i in range(8):
    row = tk.Frame(lights_card, bg=CARD_BG)
    row.pack(fill="x", pady=3, padx=20)
    tk.Label(row, text="💡", font=("Segoe UI Emoji", 18),
             bg=CARD_BG, fg="#e5e7eb").pack(side="left")
    tk.Label(row, text=f"Light {i+1}", font=LABEL_FONT,
             bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=10)

    state_var = tk.StringVar(value="OFF")
    pill = tk.Label(row, textvariable=state_var, font=LABEL_FONT,
                    bg=LED_OFF, fg="#ffffff", width=7, padx=10, pady=4)
    pill.pack(side="right")

    light_vars.append(state_var)
    light_labels.append(pill)

# LED current states for flicker-free updates
current_led_states = ["OFF"] * 8

# ---------- IR card ----------
ir_card = tk.Frame(right_frame, bg=CARD_BG, bd=2, relief="ridge",
                   highlightbackground=CARD_BORDER)
ir_card.pack(fill="both", expand=True)

tk.Label(ir_card, text="Traffic Detection (IR Sensors 0 / 1)",
         font=SECTION_TITLE_FONT, fg=ACCENT_CYAN,
         bg=CARD_BG).grid(row=0, column=0, columnspan=4,
                          sticky="w", padx=25, pady=20)

ir_vars = []
ir_labels = []

for idx in range(8):
    r, c = (idx // 4) + 1, idx % 4
    cell = tk.Frame(ir_card, bg=CARD_BG)
    cell.grid(row=r, column=c, padx=15, pady=12)
    tk.Label(cell, text=f"Sensor {idx+1}", font=LABEL_FONT,
             bg=CARD_BG, fg=TEXT_PRIMARY).pack()

    val_var = tk.StringVar(value="0")
    bubble = tk.Label(cell, textvariable=val_var, font=LABEL_FONT,
                      bg=IR_YELLOW, fg="#111827", padx=18, pady=6)
    bubble.pack(pady=5)

    ir_vars.append(val_var)
    ir_labels.append(bubble)

# ---------- LDR card ----------
ldr_card = tk.Frame(bottom_frame, bg=CARD_BG, bd=2, relief="ridge",
                    highlightbackground=CARD_BORDER)
ldr_card.pack(fill="both", expand=True)

ldr_inner = tk.Frame(ldr_card, bg=CARD_BG)
ldr_inner.pack(fill="both", expand=True, padx=25, pady=15)

tk.Label(ldr_inner, text="LDR SENSOR STATE",
         font=LABEL_FONT, bg=CARD_BG,
         fg=TEXT_MUTED).pack(side="left")

ldr_text_var = tk.StringVar(value="WAITING...")
LDR_Display = tk.Label(ldr_inner, textvariable=ldr_text_var,
                       font=BIG_FONT, bg=CARD_BG, fg=ACCENT_CYAN)
LDR_Display.pack(side="left", padx=40)

# ---------- Serial ----------
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.05)
except Exception:
    ser = None
    print("Could not open Serial Port!")

def update_serial():
    if ser:
        try:
            while ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue

                with open("monitoring.txt", "a") as f:
                    f.write(f"{datetime.now()} {line}\n")

                # LDR:DAY / LDR:NIGHT
                if line.startswith("LDR:"):
                    status = line.split(":")[1]
                    ldr_text_var.set(status)
                    LDR_Display.config(
                        fg="#22c55e" if status == "DAY" else "#38bdf8"
                    )

                # IR_STATE:index:0/1
                elif line.startswith("IR_STATE:"):
                    parts = line.split(":")
                    if len(parts) >= 3:
                        idx = int(parts[1])
                        state = parts[2]
                        if 0 <= idx < len(ir_vars):
                            ir_vars[idx].set(state)
                            if state == "1":
                                ir_labels[idx].config(bg=IR_GREEN, fg="white")
                            else:
                                ir_labels[idx].config(bg=IR_YELLOW, fg="#111827")

                # LED:index:ON/OFF
                elif line.startswith("LED:"):
                    parts = line.split(":")
                    if len(parts) >= 3:
                        idx = int(parts[1])
                        state = parts[2]   # "ON" / "OFF"
                        if 0 <= idx < len(light_vars):
                            if current_led_states[idx] != state:
                                current_led_states[idx] = state
                                light_vars[idx].set("ON" if state == "ON" else "OFF")
                                light_labels[idx].config(
                                    bg=LED_ON if state == "ON" else LED_OFF
                                )

        except Exception as e:
            print(f"Data Error: {e}")

    root.after(50, update_serial)

update_serial()
root.mainloop()
