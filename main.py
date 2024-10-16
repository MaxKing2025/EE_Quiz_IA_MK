import tkinter as tk
from tkinter import messagebox

# Sample quiz data organized by sections
quiz_data = {
    "Section 1": [
        {"question": "What is the word limit for the Extended Essay?", "options": ["2000 words", "1000 words", "4000 words", "500 words"], "correct": "4000 words"},
        {"question": "What is the largest planet?", "options": ["Earth", "Jupiter", "Saturn", "Mars"], "correct": "Jupiter"}
    ],
    "Section 2": [
        {"question": "Which element has the chemical symbol 'O'?", "options": ["Oxygen", "Gold", "Silver", "Helium"], "correct": "Oxygen"},
        {"question": "What is the fastest land animal?", "options": ["Cheetah", "Lion", "Horse", "Elephant"], "correct": "Cheetah"}
    ]
}

# Leaderboard list to store player names and scores
leaderboard = []

# Create the main window
root = tk.Tk()
root.title("Quiz with Leaderboard")
root.geometry("400x300")

# Function to open a quiz for a specific section
leaderboard = []


def open_quiz_popup(section):
    popup = tk.Toplevel(root)
    popup.title(f"{section} Quiz")
    popup.geometry("400x350")
    popup.transient(root)
    popup.grab_set()

    # Track the score and current question
    score = [0]
    current_question_index = 0
    selected_answer = tk.StringVar()

    # Function to load the current question with a timer
    def load_question(index):
        question_data = quiz_data[section][index]

        # Clear previous widgets
        for widget in popup.winfo_children():
            widget.destroy()

        # Timer countdown in seconds
        countdown_time = 30  # 30 seconds for each question
        time_left = tk.IntVar(value=countdown_time)

        # Function to update the timer
        def update_timer():
            current_time = time_left.get()
            if current_time > 0:
                time_left.set(current_time - 1)
                popup.after(1000, update_timer)  # Update every second
            else:
                # Time is up, move to the next question
                messagebox.showwarning("Time's up!", "Moving to the next question.")
                submit_answer(index, timeout=True)

        # Display the question
        label_question = tk.Label(popup, text=f"Question {index + 1}: {question_data['question']}",
                                  font=("Helvetica", 14), wraplength=350)
        label_question.pack(pady=10)

        # Timer label
        timer_label = tk.Label(popup, textvariable=time_left, font=("Helvetica", 12), fg="red")
        timer_label.pack(pady=5)

        # Reset selected answer
        selected_answer.set("")

        # Create radio buttons for each answer option
        for option in question_data["options"]:
            radio_button = tk.Radiobutton(popup, text=option, variable=selected_answer, value=option)
            radio_button.pack(anchor="w", padx=20)

        # Submit button to check the answer
        submit_button = tk.Button(popup, text="Submit", command=lambda: submit_answer(index))
        submit_button.pack(pady=10)

        # Start the timer
        update_timer()

    # Function to submit the answer
    def submit_answer(index, timeout=False):
        correct_answer = quiz_data[section][index]["correct"]

        if timeout:
            messagebox.showinfo("Time's up!", f"The correct answer is {correct_answer}.")
        else:
            selected = selected_answer.get()
            if selected == correct_answer:
                score[0] += 1
                messagebox.showinfo("Result", "Correct!")
            else:
                messagebox.showerror("Result", f"Incorrect! The correct answer is {correct_answer}.")

        # Move to the next question or end the quiz
        if index < len(quiz_data[section]) - 1:
            load_question(index + 1)
        else:
            end_quiz(score[0])

    # Function to end the quiz
    def end_quiz(final_score):
        for widget in popup.winfo_children():
            widget.destroy()

        label_score = tk.Label(popup, text=f"Quiz Finished! Your score: {final_score}/{len(quiz_data[section])}",
                               font=("Helvetica", 14))
        label_score.pack(pady=10)

        # Input field for player name
        label_name = tk.Label(popup, text="Enter your name:")
        label_name.pack(pady=5)
        player_name_entry = tk.Entry(popup)
        player_name_entry.pack(pady=5)

        # Submit button to save score and show leaderboard
        def submit_name():
            player_name = player_name_entry.get()
            if player_name:
                # Append player name, score, and section to leaderboard
                leaderboard.append((player_name, final_score, section))
                show_leaderboard()
            popup.destroy()

        submit_button = tk.Button(popup, text="Submit Name", command=submit_name)
        submit_button.pack(pady=10)

    # Load the first question
    load_question(current_question_index)


# Function to display the leaderboard
def show_leaderboard():
    leaderboard_popup = tk.Toplevel(root)
    leaderboard_popup.title("Leaderboard")
    leaderboard_popup.geometry("300x300")

    # Sort the leaderboard by score in descending order
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)

    # Display the leaderboard
    label_title = tk.Label(leaderboard_popup, text="Leaderboard", font=("Helvetica", 16))
    label_title.pack(pady=10)

    for idx, entry in enumerate(sorted_leaderboard):
        name, score, section = entry
        label_entry = tk.Label(leaderboard_popup, text=f"{idx + 1}. {name}: {score} points (Section: {section})",
                               font=("Helvetica", 12))
        label_entry.pack(pady=5)

# Main menu functions for each section
def open_section_1():
    open_quiz_popup("Section 1")

def open_section_2():
    open_quiz_popup("Section 2")

# Function to open the main menu
def open_main_menu():
    main_menu_popup = tk.Toplevel(root)
    main_menu_popup.title("TOC")
    main_menu_popup.geometry("300x200")

    label_title = tk.Label(main_menu_popup, text="EE Research Review", font=("Helvetica", 16))
    label_title.pack(pady=10)

    # Buttons for navigating to different sections
    section1_button = tk.Button(main_menu_popup, text="Section 1 Quiz", command=open_section_1)
    section1_button.pack(fill="x", padx=10, pady=5)

    section2_button = tk.Button(main_menu_popup, text="Section 2 Quiz", command=open_section_2)
    section2_button.pack(fill="x", padx=10, pady=5)

    leaderboard_button = tk.Button(main_menu_popup, text="View Leaderboard", command=show_leaderboard)
    leaderboard_button.pack(fill="x", padx=10, pady=5)

# Create a button on the main window to open the main menu
menu_button = tk.Button(root, text="EE Research Review", command=open_main_menu)
menu_button.pack(pady=50)

# Start the main GUI event loop
root.mainloop()

