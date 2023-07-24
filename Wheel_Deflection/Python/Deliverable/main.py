import tkinter as tk
from tkinter import messagebox
from Calculations import *
from Graphs import *


class TireCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enter Info")
        self.energy_value = None
        self.deformation_value = None

        # Create labels and input boxes for each question
        label_weight = tk.Label(self.root, text="Rider Weight (in lbs):")
        label_aggression = tk.Label(self.root, text="Rider Aggression (1-10):")
        label_finesse_power = tk.Label(self.root, text="Rider Finesse-Power (1-10):")
        label_trail_environment = tk.Label(self.root, text="Trail Environment (1-10):")
        label_front_travel = tk.Label(self.root, text="Front Suspension Travel (in mm):")
        label_rear_travel = tk.Label(self.root, text="Rear Suspension Travel (in mm):")

        # Subtext labels for each question
        subtext_aggression = tk.Label(self.root, text="1 = Very conservative (not okay with falling ever)\n"
                                                      "5 = Interested in expanding comfort zone/abilities\n"
                                                      "10 = Very aggressive (always out of your comfort zone)", foreground="gray")
        subtext_finesse_power = tk.Label(self.root, text="1 = I feel light and precise when I ride; always looking for the smoothest line choice\n"
                                                         "5 = I can be precise when I need to be but I'm okay with smashing\n"
                                                         "10 = I'm a monster truck; always pushing the bike into the trail", foreground="gray")
        subtext_trail_environment = tk.Label(self.root, text="1 = Smooth cross-country style trail\n"
                                                             "5 = Trail with some technical features\n"
                                                             "10 = Big rocks / sharp edges / big gap jumps", foreground="gray")

        self.entry_weight = tk.Entry(self.root)
        self.entry_aggression = tk.Entry(self.root)
        self.entry_finesse_power = tk.Entry(self.root)
        self.entry_trail_environment = tk.Entry(self.root)
        self.entry_front_travel = tk.Entry(self.root)
        self.entry_rear_travel = tk.Entry(self.root)

        # Create Calculate button
        calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)

        # Create Show Graphs button
        show_graphs_button = tk.Button(self.root, text="Show Graphs", command=self.show_graphs)

        # Place labels, input boxes, subtext, and the Calculate button in the grid
        label_weight.grid(row=0, column=0, padx=5, pady=5)
        self.entry_weight.grid(row=0, column=1, padx=5, pady=5)

        label_aggression.grid(row=2, column=0, padx=5, pady=5)
        self.entry_aggression.grid(row=2, column=1, padx=5, pady=5)
        subtext_aggression.grid(row=3, column=0, columnspan=2, padx=5, pady=(0, 10), sticky='w')

        label_finesse_power.grid(row=4, column=0, padx=5, pady=5)
        self.entry_finesse_power.grid(row=4, column=1, padx=5, pady=5)
        subtext_finesse_power.grid(row=5, column=0, columnspan=2, padx=5, pady=(0, 10), sticky='w')

        label_trail_environment.grid(row=6, column=0, padx=5, pady=5)
        self.entry_trail_environment.grid(row=6, column=1, padx=5, pady=5)
        subtext_trail_environment.grid(row=7, column=0, columnspan=2, padx=5, pady=(0, 10), sticky='w')

        label_front_travel.grid(row=8, column=0, padx=5, pady=5)
        self.entry_front_travel.grid(row=8, column=1, padx=5, pady=5)

        label_rear_travel.grid(row=10, column=0, padx=5, pady=5)
        self.entry_rear_travel.grid(row=10, column=1, padx=5, pady=5)

        calculate_button.grid(row=12, column=0, columnspan=2, padx=5, pady=10)
        show_graphs_button.grid(row=13, column=0, columnspan=2, padx=5, pady=10)

    def calculate(self):
        # Get user input values
        rider_weight = float(self.entry_weight.get())
        rider_aggression = float(self.entry_aggression.get())
        rider_finesse_power = float(self.entry_finesse_power.get())
        trail_environment = float(self.entry_trail_environment.get())
        front_travel = float(self.entry_front_travel.get())
        rear_travel = float(self.entry_rear_travel.get())

        rider_weight = calculate_weight(rider_weight)
        finesse_environment = calculate_finesse_environment(rider_finesse_power, trail_environment)
        avg_travel = calculate_suspension_travel(front_travel, rear_travel)
        deformation_value = calculate_regression_deformation(rider_weight, rider_aggression, finesse_environment, avg_travel)
        energy_value = calculate_regression_energy(rider_weight, rider_aggression, finesse_environment, avg_travel)
        self.deformation_value = deformation_value
        self.energy_value = energy_value

        best_rims = plot_results(energy_value, deformation_value, False)

        result_message = (
            f"Results:\n"
            f"The best rims for you are the:\n{best_rims[0]}\n{best_rims[1]}"
            # f"Rider Weight: {rider_weight}\n"
            # f"Rider Aggression: {rider_aggression}\n"
            # f"Finesse-Environment: {finesse_environment}\n"
            # f"Average Suspension Travel: {avg_travel}\n"
            # f"Deformation Value: {deformation_value}\n"
            # f"Energy Value: {energy_value}"
        )
        messagebox.showinfo("Results", result_message)

    # Button that shows the graph of the users results with all the rims
    def show_graphs(self):
        if self.energy_value is not None and self.deformation_value is not None:
            # Call the plot_results function with the energy and deformation values
            _ = plot_results(self.energy_value, self.deformation_value, True)
        else:
            messagebox.showwarning("Error", "Please calculate the results first.")


if __name__ == "__main__":
    calculator = TireCalculator()
    calculator.root.mainloop()


