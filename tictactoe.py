import tkinter as tk
from tkinter import messagebox
from queue import Queue
from PIL import Image, ImageTk
import pygame
import sys
import os

# Fungsi untuk mendapatkan path resource saat dibundel PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Inisialisasi pygame untuk sound
pygame.mixer.init()

root = tk.Tk()
root.title("Tic Tac Toe by Tulip 🌷")
root.geometry("450x700")
root.configure(bg="#1b103e")  # Background gelap
root.resizable(False, False)

player_queue = Queue()
player_queue.put("O")
player_queue.put("X")

buttons = []
scores = {"X": 0, "O": 0}
winner_combo = []

# =========================================================================
# FUNGSI UNTUK MENGAMBIL GAMBAR
# =========================================================================

# PENTING: Untuk mengatasi HTTP Error 404, SANGAT DISARANKAN
# UNTUK MENGUNDUH SEMUA GAMBAR INI SECARA LOKAL
# (simpan di folder yang sama dengan tictactoe.py)
# DAN GUNAKAN resource_path() untuk memuatnya!
# Contoh:
# default_icon_img = Image.open(resource_path("default_icon.png")).resize(size)
# return ImageTk.PhotoImage(default_icon_img)



# Inisialisasi ikon dengan prioritas ke URL, tapi dengan fallback ke gambar transparan
# SOLUSI PALING BAIK: GANTI INI DENGAN GAMBAR LOKAL ANDA SENDIRI!
# Misal:
# icon1 = ImageTk.PhotoImage(Image.open(resource_path("player_o_icon.png")).resize((40,40)))
# icon2 = ImageTk.PhotoImage(Image.open(resource_path("player_x_icon.png")).resize((40,40)))
# fire_icon1 = ImageTk.PhotoImage(Image.open(resource_path("fire_icon.png")).resize((30,30)))

# Coba URL yang ada, jika error akan transparan
icon1 = ImageTk.PhotoImage(Image.open(resource_path("player_o_icon.png")).resize((40,40)))
icon2 = ImageTk.PhotoImage(Image.open(resource_path("player_x_icon.png")).resize((40,40)))
fire_icon1 = ImageTk.PhotoImage(Image.open(resource_path("fire_icon.png")).resize((30,30)))
fire_icon2 = fire_icon1 # Jika fire_icon2 sama dengan fire_icon1

# PASTIKAN resource_path() DIGUNAKAN UNTUK SEMUA FILE SUARA INI!
click_sound = pygame.mixer.Sound(resource_path("click_sound.wav"))
win_sound = pygame.mixer.Sound(resource_path("win_sound.wav"))
draw_sound = pygame.mixer.Sound(resource_path("draw_sound.wav"))

# === FRAME MENU UTAMA ===
main_menu_frame = tk.Frame(root, bg="#1b103e")
main_menu_frame.pack(fill="both", expand=True)

title = tk.Label(main_menu_frame, text="TIC TAC TOE", font=("DRAGON HUNTER", 36), fg="#ff5f5f", bg="#1b103e")
title.pack(pady=(80, 10))

subtitle = tk.Label(main_menu_frame, text="by Tulip 🌷", font=("Gabriola", 18), fg="#ff5f5f", bg="#1b103e")
subtitle.pack(pady=(0, 50))

# Fungsi tombol animasi
def on_enter(e): e.widget.config(bg="#ff4d4d")
def on_leave(e): e.widget.config(bg="#ff5f5f")

def create_menu_button(text, command=None):
    btn = tk.Button(main_menu_frame, text=text, font=("Helvetica", 16), fg="white", bg="#ff5f5f",
                    activebackground="#ff4d4d", bd=0, relief="flat", command=command)
    btn.pack(pady=10, ipadx=50, ipady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.config(cursor="hand2")
    return btn

# Tombol Menu
def start_game():
    main_menu_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

create_menu_button("Play", start_game)
create_menu_button("Settings")  # nanti diubah di bawah
create_menu_button("Quit", root.quit)

# Ikon Sosial Media
social_frame = tk.Frame(main_menu_frame, bg="#1b103e")
social_frame.pack(pady=40)

social_icon_twitter = ImageTk.PhotoImage(Image.open(resource_path("twitter_icon.png")).resize((24,24)))
social_icon_instagram = ImageTk.PhotoImage(Image.open(resource_path("instagram_icon.png")).resize((24,24)))
social_icon_discord = ImageTk.PhotoImage(Image.open(resource_path("discord_icon.png")).resize((24,24)))

# Kemudian gunakan variabel PhotoImage yang sudah dibuat
label_twitter = tk.Label(social_frame, image=social_icon_twitter, bg="#1b103e")
label_twitter.image = social_icon_twitter # Penting: simpan referensi untuk mencegah garbage collection
label_twitter.pack(side="left", padx=10)

label_instagram = tk.Label(social_frame, image=social_icon_instagram, bg="#1b103e")
label_instagram.image = social_icon_instagram
label_instagram.pack(side="left", padx=10)

label_discord = tk.Label(social_frame, image=social_icon_discord, bg="#1b103e")
label_discord.image = social_icon_discord
label_discord.pack(side="left", padx=10)

# Versi aplikasi
version_label = tk.Label(main_menu_frame, text="v.0101", fg="white", bg="#ff5f5f", font=("Arial", 10))
version_label.place(relx=0.98, rely=0.98, anchor="se")

# === FRAME SETTINGS ===
settings_frame = tk.Frame(root, bg="#1b103e")

def change_game_bg_color(color):
    game_frame.configure(bg=color)
    frame_top.configure(bg=color)
    # Update semua elemen di game_frame yang latar belakangnya putih agar seragam
    for widget in frame_top.winfo_children():
        widget.configure(bg=color)
        for child in widget.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=color)
    turn_label.configure(bg=color)

def show_settings():
    main_menu_frame.pack_forget()
    settings_frame.pack(fill="both", expand=True)

def back_to_menu():
    settings_frame.pack_forget()
    main_menu_frame.pack(fill="both", expand=True)

# Judul Settings
tk.Label(settings_frame, text="Settings", font=("Helvetica", 24, "bold"), fg="#ff5f5f", bg="#1b103e").pack(pady=30)

# Pilihan warna background game
colors = {
    "Putih": "white",
    "Abu-Abu": "#d3d3d3",
    "Biru Muda": "#add8e6",
    "Hitam": "#1b103e",
    "Krem": "#f5f5dc"
}

color_buttons_frame = tk.Frame(settings_frame, bg="#1b103e")
color_buttons_frame.pack(pady=20)

for name, hex_color in colors.items():
    btn = tk.Button(color_buttons_frame, text=name, bg=hex_color, fg="black", width=10,
                    command=lambda c=hex_color: change_game_bg_color(c))
    btn.pack(side="left", padx=10)

# Tombol kembali
btn_back = tk.Button(settings_frame, text="Back", font=("Helvetica", 14), fg="white", bg="#ff5f5f", bd=0,
                     relief="flat", command=back_to_menu)
btn_back.pack(pady=30)
btn_back.bind("<Enter>", on_enter)
btn_back.bind("<Leave>", on_leave)
btn_back.config(cursor="hand2")

# Ubah tombol Settings di menu utama untuk memanggil show_settings
for widget in main_menu_frame.winfo_children():
    if isinstance(widget, tk.Button) and widget["text"] == "Settings":
        widget.config(command=show_settings)
        break

# === FRAME GAME ===
game_frame = tk.Frame(root, bg="#f5f5dc")

frame_top = tk.Frame(game_frame, bg="#f5f5dc")
frame_top.grid(row=0, column=0, columnspan=3, pady=10)

# Tombol Back ke Menu di pojok kiri atas game
back_to_menu_btn = tk.Button(game_frame, text="← Menu", font=("Arial", 10), fg="#f5f5dc", bg="#ff5f5f",
                             bd=0, relief="flat", cursor="hand2",
                             command=lambda: (game_frame.pack_forget(), main_menu_frame.pack(fill="both", expand=True)))
back_to_menu_btn.place(x=10, y=10)

# Animasi hover tombol Back to Menu
def back_btn_enter(e): e.widget.config(bg="#ff4d4d")
def back_btn_leave(e): e.widget.config(bg="#ff5f5f")


back_to_menu_btn.bind("<Enter>", back_btn_enter)
back_to_menu_btn.bind("<Leave>", back_btn_leave)


# Player 1
player1_frame = tk.Frame(frame_top, bg="#f5f5dc")
player1_frame.pack(side="left", padx=40)
tk.Label(player1_frame, image=icon1, bg="#f5f5dc").pack()
tk.Label(player1_frame, text="Player 1", bg="#f5f5dc", font=("Arial", 10)).pack()
tk.Label(player1_frame, text="⭕", bg="#f5f5dc", fg="red", font=("Arial", 12)).pack()
score_o_label = tk.Label(player1_frame, text="0", bg="#f5f5dc", font=("Arial", 12))
score_o_label.pack()
fire_o_label = tk.Label(player1_frame, image="", bg="#f5f5dc")
fire_o_label.pack()

# Player 2
player2_frame = tk.Frame(frame_top, bg="#f5f5dc")
player2_frame.pack(side="right", padx=40)
tk.Label(player2_frame, image=icon2, bg="#f5f5dc").pack()
tk.Label(player2_frame, text="Player 2", bg="#f5f5dc", font=("Arial", 10)).pack()
tk.Label(player2_frame, text="❌", bg="#f5f5dc", fg="blue", font=("Arial", 12)).pack()
score_x_label = tk.Label(player2_frame, text="0", bg="#f5f5dc", font=("Arial", 12))
score_x_label.pack()
fire_x_label = tk.Label(player2_frame, image="", bg="#f5f5dc")
fire_x_label.pack()

turn_label = tk.Label(game_frame, text=f"Giliran: {player_queue.queue[0]}", font=("Arial", 14), bg="#f5f5dc")
turn_label.grid(row=1, column=0, columnspan=3, pady=10)

def update_score():
    score_o_label.config(text=str(scores["O"]))
    score_x_label.config(text=str(scores["X"]))
    if scores["O"] > scores["X"]:
        fire_o_label.config(image=fire_icon1)
        fire_x_label.config(image="")
    elif scores["X"] > scores["O"]:
        fire_x_label.config(image=fire_icon2)
        fire_o_label.config(image="")
    else:
        fire_o_label.config(image="")
        fire_x_label.config(image="")

def check_winner():
    global winner_combo
    combos = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in combos:
        if buttons[a]["text"] == buttons[b]["text"] == buttons[c]["text"] != "":
            winner_combo = [a, b, c]
            highlight_winner()
            scores[buttons[a]["text"]] += 1
            update_score()
            win_sound.play()
            messagebox.showinfo("Game Over", f"Pemain {buttons[a]['text']} menang!")
            reset_board()
            return
    if all(btn["text"] != "" for btn in buttons):
        draw_sound.play()
        messagebox.showinfo("Game Over", "Seri!")
        reset_board()

def highlight_winner():
    for i in winner_combo:
        buttons[i].config(bg="lightgreen")

def on_click(i):
    if buttons[i]["text"] == "":
        current = player_queue.get()
        buttons[i]["text"] = current
        buttons[i].config(fg="red" if current == "O" else "blue")
        click_sound.play()
        check_winner()
        player_queue.put(current)
        turn_label.config(text=f"Giliran: {player_queue.queue[0]}")

def reset_board():
    global winner_combo
    for btn in buttons:
        btn.config(text="", bg="SystemButtonFace")
    winner_combo = []
    turn_label.config(text=f"Giliran: {player_queue.queue[0]}")

def reset_all():
    global scores
    scores = {"X": 0, "O": 0}
    update_score()
    reset_board()

# Buat papan permainan
for i in range(9):
    btn = tk.Button(game_frame, text="", font=("Arial", 32), width=5, height=2, command=lambda i=i: on_click(i))
    btn.grid(row=(i//3)+2, column=i%3, padx=5, pady=5)
    buttons.append(btn)

reset_button = tk.Button(game_frame, text="Reset Game", command=reset_board, bg="orange", font=("Arial", 12))
reset_button.grid(row=5, column=0, pady=10)

reset_all_button = tk.Button(game_frame, text="Reset Skor", command=reset_all, bg="red", fg="white", font=("Arial", 12))
reset_all_button.grid(row=5, column=2, pady=10)

# Jalankan aplikasi
root.mainloop()