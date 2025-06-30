import customtkinter as ctk
from tkinter import messagebox
from threading import Thread

def run_in_thread(target_function):
    thread = Thread(target=target_function)
    thread.start()

def create_entry_with_label(master, label_text):
    ctk.CTkLabel(master, text=label_text).pack()
    entry = ctk.CTkEntry(master)
    entry.pack()
    return entry
