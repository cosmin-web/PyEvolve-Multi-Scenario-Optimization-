import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Importam modulele noastre
from algoritm import EvolutieDiferentiala
from probleme import ProblemaEnergie, ProblemaRuta, ProblemaPortofoliu


class Aplicatie(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proiect IA - Optimizare Evolutiva")
        self.geometry("950x680")

        # --- Setari (Stanga) ---
        frame_setari = ttk.LabelFrame(self, text="Parametri Algoritm")
        frame_setari.place(x=10, y=10, width=280, height=300)

        # Campuri input
        self.creaza_input(frame_setari, "Marime Populatie:", "30", "entry_pop")
        self.creaza_input(frame_setari, "Numar Generatii:", "100", "entry_gen")
        self.creaza_input(frame_setari, "Factor Mutatie (F):", "0.5", "entry_f")
        self.creaza_input(frame_setari, "Probabilitate CR:", "0.7", "entry_cr")

        # --- Selectie Problema ---
        frame_prob = ttk.LabelFrame(self, text="Selectare Tema")
        frame_prob.place(x=10, y=320, width=280, height=150)

        self.var_problema = tk.StringVar(value="energie")
        r1 = ttk.Radiobutton(frame_prob, text="1. Consum Energie", variable=self.var_problema, value="energie")
        r2 = ttk.Radiobutton(frame_prob, text="2. Ruta Optima", variable=self.var_problema, value="ruta")
        r3 = ttk.Radiobutton(frame_prob, text="3. Portofoliu Investitii", variable=self.var_problema,
                             value="portofoliu")

        r1.pack(anchor="w", padx=10, pady=8)
        r2.pack(anchor="w", padx=10, pady=8)
        r3.pack(anchor="w", padx=10, pady=8)

        # Buton Start
        btn_start = ttk.Button(self, text="START OPTIMIZARE", command=self.start_algoritm)
        btn_start.place(x=10, y=490, width=280, height=50)

        # --- Rezultate si Grafic ---
        self.text_rezultate = scrolledtext.ScrolledText(self, width=60, height=10)
        self.text_rezultate.place(x=310, y=10, width=620, height=220)

        self.frame_grafic = tk.Frame(self, bg="white")
        self.frame_grafic.place(x=310, y=240, width=620, height=420)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafic)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def creaza_input(self, parent, text, default, var_name):
        """Helper pentru creare inputuri."""
        ttk.Label(parent, text=text).pack(pady=5)
        entry = ttk.Entry(parent)
        entry.insert(0, default)
        entry.pack()
        setattr(self, var_name, entry)

    def start_algoritm(self):
        try:
            pop_size = int(self.entry_pop.get())
            max_gen = int(self.entry_gen.get())
            F = float(self.entry_f.get())
            CR = float(self.entry_cr.get())

            tip_problema = self.var_problema.get()

            # Initializare Problema
            if tip_problema == "energie":
                pb = ProblemaEnergie()
            elif tip_problema == "ruta":
                pb = ProblemaRuta()
            elif tip_problema == "portofoliu":
                pb = ProblemaPortofoliu()

            limite = pb.get_limite()
            # La energie, dimensiunea e nr de aparate, la restul e dat de 'n'
            if hasattr(pb, 'aparate'):
                dim = len(pb.aparate)
            else:
                dim = pb.n

            fitness_func = pb.fitness

            # Rulare
            self.text_rezultate.delete(1.0, tk.END)
            self.text_rezultate.insert(tk.END, f"Ruleaza optimizarea pentru: {tip_problema.upper()}...\n")
            self.update()

            algo = EvolutieDiferentiala(fitness_func, limite, dim, pop_size, F, CR, max_gen)
            best_sol, best_score, istoric = algo.optimizeaza()

            # Afisare Rezultate
            self.text_rezultate.insert(tk.END, "-" * 50 + "\n")
            self.text_rezultate.insert(tk.END, f"Fitness Final: {best_score:.4f}\n")
            self.text_rezultate.insert(tk.END, "-" * 50 + "\n")

            if tip_problema == "energie":
                self.text_rezultate.insert(tk.END, "ORAR RECOMANDAT:\n")
                factor_pompa = best_sol[-1]
                self.text_rezultate.insert(tk.END, f"> Setare Pompa Caldura: {factor_pompa:.2f} (Factor Putere)\n")

                for i in range(len(best_sol) - 1):
                    val = best_sol[i]
                    nume = pb.aparate[i][2]
                    ora = int(val)
                    minut = int((val - ora) * 60)
                    self.text_rezultate.insert(tk.END, f"> {nume}: Pornire la {ora:02d}:{minut:02d}\n")

            elif tip_problema == "ruta":
                self.text_rezultate.insert(tk.END, "TRASEU OPTIM:\n")
                ordine = np.argsort(best_sol)

                nume_locatii = []
                for i in ordine:
                    nume_locatii.append(pb.nume[i])
                nume_locatii.append(nume_locatii[0])

                traseu = " -> ".join(nume_locatii)
                self.text_rezultate.insert(tk.END, f"{traseu}\n")

            elif tip_problema == "portofoliu":
                self.text_rezultate.insert(tk.END, "PORTOFOLIU INVESTITII (Ponderi %):\n")
                suma = np.sum(best_sol)
                if suma < 1e-6:
                    ponderi = np.zeros(len(best_sol))
                else:
                    ponderi = (best_sol / suma) * 100

                for i in range(pb.n):
                    nume = pb.active[i][0]
                    proc = ponderi[i]
                    if proc > 0.0001:
                        self.text_rezultate.insert(tk.END, f"> {nume}: {proc:.4f}%\n")
                    else:
                        self.text_rezultate.insert(tk.END, f"> {nume}: 0.0000%\n")

            # Grafic
            self.ax.clear()
            self.ax.plot(istoric, color='#0055AA', linewidth=2)
            self.ax.set_title(f"Convergenta - {tip_problema.capitalize()}")
            self.ax.set_xlabel("Generatii")
            self.ax.set_ylabel("Fitness")
            self.ax.grid(True, linestyle='--')
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Eroare", "Verificati datele introduse.")


if __name__ == "__main__":
    app = Aplicatie()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.destroy()