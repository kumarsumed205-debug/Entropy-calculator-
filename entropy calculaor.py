import tkinter as tk
from tkinter import ttk, messagebox
import math

class EntropyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Entropy Change Calculator")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        # Apply a simple style
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

        # Constants
        self.R = 8.314  # J/(mol*K)

        # Create Tab Control
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Initialize Tabs
        self.setup_phase_tab()
        self.setup_heating_tab()
        self.setup_expansion_tab()
        self.setup_spontaneity_tab()

    def create_input_row(self, parent, label_text, row):
        """Helper to create a standard label and entry row"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, sticky='ew', padx=10, pady=5)
        return entry

    def get_float(self, entry):
        """Helper to safely get float from entry"""
        try:
            val = float(entry.get())
            return val
        except ValueError:
            return None

    def to_kelvin(self, temp, unit_var):
        """Converts T to Kelvin based on dropdown"""
        if unit_var.get() == "Celsius":
            return temp + 273.15
        return temp

    # ----------------------------------------------------------------
    # TAB 1: Phase Change
    # ----------------------------------------------------------------
    def setup_phase_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Phase Change')
        frame.columnconfigure(1, weight=1)

        # Title
        ttk.Label(frame, text="ΔS = ΔH / T", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Inputs
        self.ph_dh = self.create_input_row(frame, "Enthalpy (ΔH) [kJ/mol]:", 1)
        
        ttk.Label(frame, text="Temperature:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        temp_frame = ttk.Frame(frame)
        temp_frame.grid(row=2, column=1, sticky='ew', padx=10)
        
        self.ph_t = ttk.Entry(temp_frame, width=15)
        self.ph_t.pack(side='left', fill='x', expand=True)
        
        self.ph_unit = tk.StringVar(value="Celsius")
        ttk.OptionMenu(temp_frame, self.ph_unit, "Celsius", "Celsius", "Kelvin").pack(side='left', padx=5)

        # Button
        ttk.Button(frame, text="Calculate ΔS", command=self.calc_phase).grid(row=3, column=0, columnspan=2, pady=15, sticky='ew', padx=10)

        # Result Area
        self.ph_result = tk.StringVar()
        lbl = ttk.Label(frame, textvariable=self.ph_result, background="#f0f0f0", relief="sunken", padding=10)
        lbl.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=10, pady=5)

    def calc_phase(self):
        dh = self.get_float(self.ph_dh)
        t = self.get_float(self.ph_t)

        if dh is None or t is None:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        t_k = self.to_kelvin(t, self.ph_unit)
        if t_k <= 0:
            messagebox.showerror("Error", "Temperature must be > 0 K")
            return

        dh_joules = dh * 1000
        ds = dh_joules / t_k

        res_text = (f"Temperature: {t_k:.2f} K\n"
                    f"ΔH: {dh_joules:.2f} J/mol\n\n"
                    f"ΔS = {ds:.4f} J/(mol·K)")
        self.ph_result.set(res_text)

    # ----------------------------------------------------------------
    # TAB 2: Heating
    # ----------------------------------------------------------------
    def setup_heating_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Heating')
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="ΔS = n · C · ln(T₂/T₁)", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        self.heat_n = self.create_input_row(frame, "Moles (n):", 1)
        self.heat_c = self.create_input_row(frame, "Heat Capacity (C) [J/mol·K]:", 2)
        
        # Temp 1
        ttk.Label(frame, text="Initial Temp (T₁):").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.heat_t1 = ttk.Entry(frame)
        self.heat_t1.grid(row=3, column=1, sticky='ew', padx=10, pady=5)

        # Temp 2
        ttk.Label(frame, text="Final Temp (T₂):").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.heat_t2 = ttk.Entry(frame)
        self.heat_t2.grid(row=4, column=1, sticky='ew', padx=10, pady=5)

        # Unit Selection
        ttk.Label(frame, text="Temperature Unit:").grid(row=5, column=0, sticky='w', padx=10)
        self.heat_unit = tk.StringVar(value="Celsius")
        ttk.OptionMenu(frame, self.heat_unit, "Celsius", "Celsius", "Kelvin").grid(row=5, column=1, sticky='w', padx=10)

        ttk.Button(frame, text="Calculate ΔS", command=self.calc_heating).grid(row=6, column=0, columnspan=2, pady=15, sticky='ew', padx=10)

        self.heat_result = tk.StringVar()
        ttk.Label(frame, textvariable=self.heat_result, background="#f0f0f0", relief="sunken", padding=10).grid(row=7, column=0, columnspan=2, sticky='nsew', padx=10)

    def calc_heating(self):
        n = self.get_float(self.heat_n)
        c = self.get_float(self.heat_c)
        t1 = self.get_float(self.heat_t1)
        t2 = self.get_float(self.heat_t2)

        if None in [n, c, t1, t2]:
            messagebox.showerror("Error", "Invalid Input")
            return

        t1_k = self.to_kelvin(t1, self.heat_unit)
        t2_k = self.to_kelvin(t2, self.heat_unit)

        if t1_k <= 0 or t2_k <= 0:
            messagebox.showerror("Error", "Temps must be > 0 K")
            return

        ds = n * c * math.log(t2_k / t1_k)

        res = (f"Initial T: {t1_k:.2f} K\n"
               f"Final T: {t2_k:.2f} K\n\n"
               f"ΔS = {ds:.4f} J/K")
        self.heat_result.set(res)

    # ----------------------------------------------------------------
    # TAB 3: Expansion
    # ----------------------------------------------------------------
    def setup_expansion_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Expansion')
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="ΔS = n · R · ln(V₂/V₁)", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        self.exp_n = self.create_input_row(frame, "Moles (n):", 1)
        self.exp_v1 = self.create_input_row(frame, "Initial Volume (V₁):", 2)
        self.exp_v2 = self.create_input_row(frame, "Final Volume (V₂):", 3)

        ttk.Button(frame, text="Calculate ΔS", command=self.calc_expansion).grid(row=4, column=0, columnspan=2, pady=15, sticky='ew', padx=10)

        self.exp_result = tk.StringVar()
        ttk.Label(frame, textvariable=self.exp_result, background="#f0f0f0", relief="sunken", padding=10).grid(row=5, column=0, columnspan=2, sticky='nsew', padx=10)

    def calc_expansion(self):
        n = self.get_float(self.exp_n)
        v1 = self.get_float(self.exp_v1)
        v2 = self.get_float(self.exp_v2)

        if None in [n, v1, v2] or v1 <= 0 or v2 <= 0:
            messagebox.showerror("Error", "Inputs must be positive numbers")
            return

        ds = n * self.R * math.log(v2 / v1)

        res = (f"Volume Ratio: {v2/v1:.2f}\n"
               f"R used: {self.R} J/(mol·K)\n\n"
               f"ΔS = {ds:.4f} J/K")
        self.exp_result.set(res)

    # ----------------------------------------------------------------
    # TAB 4: Spontaneity
    # ----------------------------------------------------------------
    def setup_spontaneity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Spontaneity')
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="ΔG = ΔH - TΔS", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        self.spon_dh = self.create_input_row(frame, "ΔH (kJ):", 1)
        self.spon_ds = self.create_input_row(frame, "ΔS (J/K):", 2)
        
        ttk.Label(frame, text="Temperature:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        t_frame = ttk.Frame(frame)
        t_frame.grid(row=3, column=1, sticky='ew', padx=10)
        self.spon_t = ttk.Entry(t_frame)
        self.spon_t.pack(side='left', fill='x', expand=True)
        self.spon_unit = tk.StringVar(value="Celsius")
        ttk.OptionMenu(t_frame, self.spon_unit, "Celsius", "Celsius", "Kelvin").pack(side='left', padx=5)

        ttk.Button(frame, text="Check Spontaneity", command=self.calc_spontaneity).grid(row=4, column=0, columnspan=2, pady=15, sticky='ew', padx=10)

        self.spon_result = tk.StringVar()
        self.spon_lbl = ttk.Label(frame, textvariable=self.spon_result, background="#f0f0f0", relief="sunken", padding=10)
        self.spon_lbl.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=10)

    def calc_spontaneity(self):
        dh_kj = self.get_float(self.spon_dh)
        ds = self.get_float(self.spon_ds)
        t = self.get_float(self.spon_t)

        if None in [dh_kj, ds, t]:
            messagebox.showerror("Error", "Invalid Input")
            return

        t_k = self.to_kelvin(t, self.spon_unit)
        if t_k <= 0:
            messagebox.showerror("Error", "T must be > 0 K")
            return

        dh_j = dh_kj * 1000
        dg = dh_j - (t_k * ds)

        status = "EQUILIBRIUM"
        color = "gray"
        if dg < 0:
            status = "SPONTANEOUS"
            color = "light green"
        elif dg > 0:
            status = "NON-SPONTANEOUS"
            color = "#ffcccc" # light red

        self.spon_lbl.configure(background=color)
        res = (f"ΔH: {dh_j:.2f} J\n"
               f"T: {t_k:.2f} K\n"
               f"ΔG = {dg:.2f} J\n\n"
               f"Result: {status}")
        self.spon_result.set(res)

if __name__ == "__main__":
    root = tk.Tk()
    app = EntropyGUI(root)
    root.mainloop()
    
