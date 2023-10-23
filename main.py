import tkinter as tk
from tkinter import ttk
import json
import time
import threading
import asyncio

auto_calc_thread = None
ayarlar_dosyasi = "ayarlar.json"
def ayarlari_oku():
    try:
        with open(ayarlar_dosyasi, "r") as dosya:
            ayarlar = json.load(dosya)
            kargo_entry.insert(0, ayarlar.get("kargo", ""))
            komisyon_entry.insert(0, ayarlar.get("komisyon", ""))
    except FileNotFoundError:
        pass

def ayarlari_kaydet():
    kargo_deger = kargo_entry.get()
    komisyon_deger = komisyon_entry.get()

    ayarlar = {
        "kargo": kargo_deger,
        "komisyon": komisyon_deger
    }

    with open(ayarlar_dosyasi, "w") as dosya:
        json.dump(ayarlar, dosya)

def hesapla():
    try:
        satis_fiyati = float(satis_entry.get())
        alim_fiyati = float(alim_entry.get())
        kargo_fiyati = float(kargo_entry.get())
        komisyon = satis_fiyati * float(komisyon_entry.get()) / 100

        komisyon_sonuc_label.config(text=f"Komisyon: {komisyon:.2f} TL")
        sonuc = satis_fiyati - alim_fiyati - kargo_fiyati - komisyon
        bold_red_label.config(text=f"Kâr Sonuç: {sonuc:.2f} TL")
    except ValueError:
        komisyon_sonuc_label.config(text="Geçersiz Giriş")


def on_exit():
    ayarlari_kaydet()
    window.destroy()

def start_auto_calc_thread():
    global auto_calc_thread
    if not auto_calc_thread:
        auto_calc_thread = threading.Thread(target=hesapla)
        auto_calc_thread.daemon = True
        auto_calc_thread.start()

window = tk.Tk()
window.title("Hesaplayıcı")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = 200
window_height = 260

x_position = screen_width - window_width - 20
y_position = screen_height - window_height - 100

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

style = ttk.Style()
style.configure("BoldRed.TLabel", foreground="red", font=("Arial", 12, "bold"))

bold_red_label = ttk.Label(window, text="", style="BoldRed.TLabel")
bold_red_label.pack()

satis_label = tk.Label(window, text="Satış Fiyatı (TL):")
satis_label.pack()
satis_entry = tk.Entry(window)
satis_entry.pack()

alim_label = tk.Label(window, text="Alış Fiyatı (TL):")
alim_label.pack()
alim_entry = tk.Entry(window)
alim_entry.pack()

kargo_label = tk.Label(window, text="Kargo Fiyatı (TL):")
kargo_label.pack()
kargo_entry = tk.Entry(window)
kargo_entry.pack()

komisyon_label = tk.Label(window, text="Komisyon oranı: %")
komisyon_label.pack()
komisyon_entry = tk.Entry(window)
komisyon_entry.pack()

hesapla_dugme = tk.Button(window, text="Hesapla", command=hesapla)
hesapla_dugme.pack()

bold_red_label = ttk.Label(window, text="Kâr sonuç:", style="BoldRed.TLabel")
bold_red_label.pack()

komisyon_sonuc_label = tk.Label(window, text="")
komisyon_sonuc_label.pack()

ayarlari_oku()

window.protocol("WM_DELETE_WINDOW", on_exit)
window.mainloop()
