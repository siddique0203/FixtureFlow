import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import math


def generate_knockout_fixture():
    input_data = text_input.get("1.0", tk.END).strip()
    if not input_data:
        messagebox.showwarning("Input Error", "Please Enter Team Names!")
        return

    # Parse and validate input codes
    unique_codes = list(set(code.strip() for code in input_data.split("\n") if code.strip()))
    total_teams = len(unique_codes)

    if total_teams < 2:
        messagebox.showwarning("Input Error", "At least two unique teams are required!")
        return

    # Shuffle teams
    random.shuffle(unique_codes)

    # Calculate byes
    next_power_of_2 = 2 ** math.ceil(math.log2(total_teams))
    byes = next_power_of_2 - total_teams

    # Generate fixtures
    fixtures = []
    first_round_teams = unique_codes[:]
    bye_teams = first_round_teams[:byes]
    non_bye_teams = first_round_teams[byes:]

    round_num = 1
    match_counter = 1
    next_round = []

    # Display total teams and bye information
    fixtures.append(f"Total Teams: {total_teams}")
    fixtures.append(f"Teams with Bye: {byes}")

    # Calculate total matches and rounds
    total_matches = (total_teams - byes) // 2 + byes
    total_rounds = math.ceil(math.log2(total_teams))

    fixtures.append(f"Total Matches: {total_matches}")
    fixtures.append(f"Total Rounds: {total_rounds}")
    fixtures.append("")  # Add an empty line for separation

    # First round
    fixtures.append(f"Round {round_num} Fixtures:")
    while non_bye_teams:
        team1 = non_bye_teams.pop(0)
        if non_bye_teams:
            team2 = non_bye_teams.pop(0)
            fixtures.append(f"Match {match_counter}: {team1} vs {team2}")
            next_round.append(f"Match {match_counter} winner")
        else:
            fixtures.append(f"Match {match_counter}: {team1} (Bye)")
            next_round.append(team1)
        match_counter += 1

    for bye_team in bye_teams:
        fixtures.append(f"{bye_team} advances due to bye")
        next_round.append(bye_team)

    # Subsequent rounds
    round_num += 1
    while len(next_round) > 2:
        fixtures.append(f"\nRound {round_num} Fixtures:")
        current_round = next_round
        next_round = []

        for i in range(0, len(current_round), 2):
            team1 = current_round[i]
            team2 = current_round[i + 1]
            fixtures.append(f"Match {match_counter}: {team1} vs {team2}")
            next_round.append(f"Match {match_counter} winner")
            match_counter += 1

        round_num += 1

    # Final match
    fixtures.append(f"\nFinal:")
    fixtures.append(f"Match {match_counter}: {next_round[0]} vs {next_round[1]}")

    # Display fixtures in the output box
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "\n".join(fixtures))


def copy_to_clipboard():
    output_data = text_output.get("1.0", tk.END).strip()
    if not output_data:
        messagebox.showwarning("No Data", "No fixtures to copy!")
        return
    root.clipboard_clear()
    root.clipboard_append(output_data)
    root.update()
    messagebox.showinfo("Copied", "Fixture copied to clipboard!")


def save_to_file():
    output_data = text_output.get("1.0", tk.END).strip()
    if not output_data:
        messagebox.showwarning("No Data", "No fixtures to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_data)
        messagebox.showinfo("Saved", f"Fixture saved to {file_path}!")


def show_fixture_table():
    output_data = text_output.get("1.0", tk.END).strip()
    if not output_data:
        messagebox.showwarning("No Data", "No fixtures available to display table!")
        return

    # Split output data to get match details and rounds
    round_matches = {}
    current_round = None
    final_match = None

    for line in output_data.split("\n"):
        if line.startswith("Round"):
            current_round = line
            round_matches[current_round] = []
        elif "vs" in line and current_round:
            round_matches[current_round].append(line)
        elif line.startswith("Final:"):
            final_match = []
            current_round = None
        elif final_match is not None and "vs" in line:
            final_match.append(line)

    # Create a new window for the fixture table
    table_window = tk.Toplevel(root)
    table_window.title("Round-Wise Fixture Table")
    table_window.geometry("600x600")

    # Create a canvas for scrollable content
    canvas = tk.Canvas(table_window, bg="#f1f1f1")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Add a vertical scrollbar to the canvas
    scrollbar = ttk.Scrollbar(table_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame inside the canvas for adding content
    container = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=container, anchor="nw")

    # Add each round's fixtures inside a labeled frame
    for round_header, matches in round_matches.items():
        round_frame = ttk.LabelFrame(container, text=round_header, padding=10)
        round_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for match in matches:
            tk.Label(round_frame, text=match, font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=2)

    # Add final match in its own labeled frame
    if final_match:
        final_frame = ttk.LabelFrame(container, text="Final Round", padding=10)
        final_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for match in final_match:
            tk.Label(final_frame, text=match, font=("Helvetica", 12, "bold")).pack(anchor="w", padx=10, pady=5)

# GUI Code remains the same for buttons and main application window


# Create GUI
root = tk.Tk()
root.title("Knockout Fixture Generator")
root.geometry("800x600")
root.configure(bg="#f1f8e9")

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TLabel", font=("Helvetica", 12))

# Header
header = tk.Label(root, text="🏆 Knockout Fixture Generator 🏆", bg="#689f38", fg="white",
                  font=("Helvetica", 20, "bold"), pady=10)
header.pack(fill=tk.X)

# Input frame
input_frame = ttk.LabelFrame(root, text="Enter Team Names (One Per Line)", padding=10)
input_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=10)

text_input = tk.Text(input_frame, height=10, font=("Courier", 12), wrap=tk.WORD)
text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Action buttons
action_frame = ttk.Frame(root)
action_frame.pack(fill=tk.X, pady=10)

generate_button = tk.Button(action_frame, text="Generate Fixture", command=generate_knockout_fixture, bg="#4caf50",
                            fg="white", font=("Helvetica", 12, "bold"))
generate_button.pack(side=tk.LEFT, padx=10)

copy_button = tk.Button(action_frame, text="Copy Fixture", command=copy_to_clipboard, bg="#03a9f4", fg="white",
                        font=("Helvetica", 12, "bold"))
copy_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(action_frame, text="Save Fixture", command=save_to_file, bg="#ff5722", fg="white",
                        font=("Helvetica", 12, "bold"))
save_button.pack(side=tk.LEFT, padx=10)

table_button = tk.Button(action_frame, text="Fixture Table", command=show_fixture_table, bg="#9c27b0", fg="white",
                         font=("Helvetica", 12, "bold"))
table_button.pack(side=tk.LEFT, padx=10)

# Output frame
output_frame = ttk.LabelFrame(root, text="Generated Fixtures", padding=10)
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

text_output = tk.Text(output_frame, height=15, font=("Courier", 12), wrap=tk.WORD, bg="#ffffff")
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

# Scrollbar for output
scrollbar = ttk.Scrollbar(output_frame, command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_output.config(yscrollcommand=scrollbar.set)

# Developer Info popup
def show_developer_info():
    messagebox.showinfo("Developer Info",
                        "Name: Md Abu Bakar Siddique\n"
                        "Student ID: 22-48322-3\n"
                        "Email: siddique0203@gmail.com\n"
                        "Phone: +8801756-736045\n"
                        "Last Update: 26 July 2025"
                        )

# Footer with Label (left) and Button (right)
footer_frame = tk.Frame(root, bg="#689f38")
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

footer_label = tk.Label(footer_frame, text="⚙️ Created by [Abu Bakar Siddique]", bg="#689f38", fg="white",
                        font=("Helvetica", 19), pady=5)
footer_label.pack(side=tk.TOP, padx=10)

info_button = tk.Button(footer_frame, text="Developer Info", bg="white", fg="#689f38",
                        font=("Helvetica", 12, "bold"), command=show_developer_info)
info_button.pack(side=tk.RIGHT, padx=10, pady=5)




root.state('zoomed')           # Maximize the window (keeps minimize/close buttons)
root.resizable(False, False)   # Disable resizing

# Run the application
root.mainloop()
