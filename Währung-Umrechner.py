import tkinter as tk
from tkinter import messagebox
import re

root = tk.Tk()
root.title("Währung Rechner")
root.geometry("500x560")
root.configure(bg="#b6c8d1")




tk.Label(root, text="Währung Umrechner", bg="#b6c8d1", font=("Arial", 18)).pack(padx=10, pady=10)
tk.Label(root, text="Bitte Ihre Währung eingeben (z.B. 34₱+45$)", bg="#b6c8d1", font=("Arial", 14)).pack(padx=10, pady=10)

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 18), justify="right")
entry.pack(padx=10, fill="x", ipady=8)


target_var = tk.StringVar(value="Fr")
target_frame = tk.Frame(root, bg="#b6c8d1")
target_frame.pack(fill="x", padx=10, pady=5)

tk.Label(target_frame, text="Ausgabe in:", bg="#b6c8d1", font=("Arial", 12)).pack(side="left")
for sym in ["Fr", "$", "₱"]:
    tk.Radiobutton(target_frame, text=sym, value=sym, variable=target_var, bg="#b6c8d1").pack(side="left", padx=6)

result_label = tk.Label(root, text="Resultat", bg="#b6c8d1", font=("Arial", 16))
result_label.pack(padx=10, pady=10)


to_chf = {
    "Fr": 1.0,
    "$": 0.90,     
    "₱": 0.016     
}


allowed_chars = set("0123456789.+-*/() x:,Fr$₱ ")

def normalize_ops(expr: str) -> str:
    return expr.replace("x", "*").replace(":", "/")

def convert_currencies_to_chf(expr: str) -> str:
    """
    Wandelt z.B. '34₱ + 45$' -> '(34*0.016) + (45*0.90)' um
    Unterstützt auch '34 Fr' oder '34Fr'.
    """

    expr = expr.replace(",", ".")

 
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*Fr\b', r'(\1*%s)' % to_chf["Fr"], expr)


    expr = re.sub(r'(\d+(?:\.\d+)?)\s*\$', r'(\1*%s)' % to_chf["$"], expr)
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*₱', r'(\1*%s)' % to_chf["₱"], expr)

    return expr

def calculate():
    expr = entry_var.get().strip()

 
    if any(ch not in allowed_chars for ch in expr):
        messagebox.showerror("Fehler", "Ungültige Zeichen im Ausdruck!")
        return

    try:
        expr = normalize_ops(expr)
        expr_chf = convert_currencies_to_chf(expr)


        result_chf = eval(expr_chf, {"__builtins__": {}}, {})

        target = target_var.get()
    
        result_target = result_chf / to_chf[target]

        result_label.config(text=f"= {result_target:.2f} {target}   (Basis: {result_chf:.2f} Fr)")
    except Exception:
        messagebox.showerror("Fehler", "Ungültige Rechnung!")

def add_number(t):
    entry_var.set(entry_var.get() + str(t))

def delete_last():
    s = entry_var.get()
    if s:
        entry_var.set(s[:-1])

def clear_all():
    entry_var.set("")
    result_label.config(text="Resultat")

buttonframe = tk.Frame(root)
buttonframe.pack(fill="x", padx=10)

for i in range(3):
    buttonframe.columnconfigure(i, weight=1)

buttons = [
    ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
    ("Fr", 4, 0), ("$", 4, 1), ("₱", 4, 2),
    ("+", 3, 0), ("-", 3, 1), (":", 3, 2),
    ("x", 5, 0), ("0", 5, 1), ("=", 5, 2),
    ("C", 6, 0), ("Del", 6, 2),
]

for text, row, col in buttons:
    if text == "Del":
        cmd = delete_last
    elif text == "C":
        cmd = clear_all
    elif text == "=":
        cmd = calculate
    else:
        cmd = lambda t=text: add_number(t)

    tk.Button(
        buttonframe, text=text, font=("Arial", 18),
        command=cmd, bg="#879196", fg="white",
        activebackground="#879196", relief="flat", bd=0
    ).grid(row=row, column=col, sticky="we", padx=2, pady=2)

root.bind("<Return>", lambda _e: calculate())
root.bind("<Escape>", lambda _e: clear_all())

root.mainloop()
