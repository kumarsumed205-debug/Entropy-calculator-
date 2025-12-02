README.md — Entropy Change Calculator (GUI Application)
<br>
 Overview

The Entropy Change Calculator is a Python-based desktop application built using Tkinter.
It provides an intuitive GUI to calculate different entropy-related thermodynamic quantities for chemistry and physics students.

This tool includes:

Phase change entropy (ΔS = ΔH / T)

Heating entropy (ΔS = n·C·ln(T₂/T₁))

Gas expansion entropy (ΔS = n·R·ln(V₂/V₁))

Spontaneity prediction using Gibbs free energy (ΔG = ΔH – TΔS)
 Features
 <br>
 1. Phase Change Entropy

Input: ΔH (kJ/mol), Temperature (°C or K)

Converts temperature to Kelvin

Calculates entropy change using:
ΔS = ΔH / T

2. Heating Entropy

Input: Number of moles, Heat capacity, Initial & final temperature

Temperature conversion included

Formula used:
ΔS = n · C · ln(T₂/T₁)

 3. Gas Expansion Entropy

Inputs: Moles, Initial & Final Volume

Formula used:
ΔS = n · R · ln(V₂/V₁)

Uses universal gas constant (R = 8.314 J/mol·K)

 4. Spontaneity Check (Gibbs Free Energy)

Inputs: ΔH (kJ), ΔS (J/K), Temperature

Determines whether reaction is:

Spontaneous (ΔG < 0)

Non-spontaneous (ΔG > 0)

At equilibrium (ΔG = 0)

Technologies Used
<br>

Python 3

Tkinter (GUI framework)

ttk Notebook (for tab-based interface)

Math module (for logarithmic calculations)

--> Project Structure
Entropy-Calculator/
│
├── entropy_gui.py     # Main GUI code
├── README.md          # Documentation
└── (optional) assets/ # Screenshots, images

-> How to Run the Application
Step 1: Install Python

Make sure Python 3.x is installed.

Step 2: Run the script

Open terminal / command prompt:

python entropy_gui.py


The graphical window will appear immediately.

->Formulas Used
Scenario	Formula
Phase Change	ΔS = ΔH / T
Heating	ΔS = n·C·ln(T₂/T₁)
Expansion	ΔS = n·R·ln(V₂/V₁)
Spontaneity	ΔG = ΔH – TΔS
-> GUI Highlights

Clean and simple interface

Tabbed layout for easy navigation

Error handling for invalid inputs

Automatic temperature conversion

Color-coded spontaneity results

-> Future Enhancements

Add graphical plots (ΔG vs T)

Add unit converters

Add support for multiple phases

Export results as PDF/CSV

Add dark mode
