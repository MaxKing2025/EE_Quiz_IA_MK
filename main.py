import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Load the CSV file and categorize questions
file_path = 'test.csv'
quiz_data = pd.read_csv(file_path)

def categorize_questions(quiz_data):
    sections = {
        "Section 1": [],
        "Section 2": [],
        "Section 3": [],
        "Section 4": [],
        "Section 5": []
    }

    # Divide data into five sections with 7 questions each
    questions_per_section = 7
    for section_number in range(5):
        start_index = section_number * questions_per_section
        end_index = start_index + questions_per_section
        section_questions = quiz_data.iloc[start_index:end_index]

        section_name = f"Section {section_number + 1}"
        for _, row in section_questions.iterrows():
            question_dict = {
                "question": row['Question'],
                "options": [
                    row['Correct Answer'],
                    row['Wrong answer'],
                    row['Wrong answer.1'],
                    row['Wrong answer.2']
                ],
                "correct": row['Correct Answer']
            }
            sections[section_name].append(question_dict)

    return sections

# Organize the quiz data into sections
quiz_sections = categorize_questions(quiz_data)

# Leaderboard list to store player names and scores
leaderboard = []

# Global mastery percentage and increment value
mastery_percentage = 0.0
increment_per_correct = 2.9411764705882  # Given increment per correct answer

# Track correct answers for each question
mastery_tracker = {q: 0 for section in quiz_sections.values() for q in range(len(section))}
max_mastery_per_question = 5

# Create the main window
root = tk.Tk()
root.title("Quiz with Leaderboard")
root.geometry("400x300")

def open_quiz_popup(section):
    popup = tk.Toplevel(root)
    popup.title(f"{section} Quiz")
    popup.geometry("600x400")
    popup.transient(root)
    popup.grab_set()

    score = [0]
    current_question_index = 0
    selected_answer = tk.StringVar()

    # Timer for the entire section: 2.5 minutes (150 seconds)
    section_time_limit = 80
    time_left = tk.IntVar(value=section_time_limit)
    timer_id = None  # ID to manage the section-wide timer

    def update_section_timer():
        """Update section timer each second, and end quiz if time expires."""
        current_time = time_left.get()
        if current_time > 0:
            time_left.set(current_time - 1)
            popup.after(1000, update_section_timer)
        else:
            messagebox.showwarning("Time's up!", "The section time has expired.")
            end_quiz(score[0])  # End the quiz if section time runs out

    # Start section timer
    update_section_timer()

    # Define the load_question function before it is called
    def load_question(index):
        global next_frame
        next_frame = False
        question_data = quiz_sections[section][index]

        # Clear previous widgets
        for widget in popup.winfo_children():
            widget.destroy()

        # Display question and options
        label_question = tk.Label(popup, text=f"Question {index + 1}: {question_data['question']}",
                                  font=("Helvetica", 14), wraplength=350)
        label_question.pack(pady=10)

        # Timer label for section timer
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

        # Label to display mastery percentage, updated for every question popup
        mastery_label = tk.Label(popup, text=f"Mastery: {mastery_percentage:.1f}%", font=("Helvetica", 10), fg="blue", anchor="w")
        mastery_label.pack(side="left", padx=5, pady=5)

        # Function to update mastery label based on total correct answers
        def update_mastery_label():
            if mastery_label.winfo_exists():  # Ensure label exists before updating
                mastery_label.config(text=f"Mastery: {mastery_percentage:.1f}%")

        # Update mastery percentage label initially for each new question
        update_mastery_label()

    # Function to submit the answer
    def submit_answer(index, timeout=False):
        global next_frame, mastery_percentage
        correct_answer = quiz_sections[section][index]["correct"]

        if timeout:
            messagebox.showinfo("Time's up!", f"The correct answer is {correct_answer}.")
        else:
            selected = selected_answer.get()
            if selected == correct_answer:
                score[0] += 1
                messagebox.showinfo("Result", "Correct!")

                # Update mastery tracker and mastery percentage for a correct answer
                if mastery_tracker[index] < max_mastery_per_question:
                    mastery_tracker[index] += 1
                    mastery_percentage += increment_per_correct  # Increment by 2.9411764705882%

            else:
                messagebox.showerror("Result", f"Incorrect! The correct answer is {correct_answer}.")

        # Move to the next question or end the quiz if it's the last question
        if index < len(quiz_sections[section]) - 1:
            load_question(index + 1)
            next_frame = False
        else:
            end_quiz(score[0])

    # Function to end the quiz
    def end_quiz(final_score):
        for widget in popup.winfo_children():
            widget.destroy()

        label_score = tk.Label(popup, text=f"Quiz Finished! Your score: {final_score}/{len(quiz_sections[section])}",
                               font=("Helvetica", 14))
        label_score.pack(pady=10)

        # Input field for player name
        label_name = tk.Label(popup, text="Enter your name:")
        label_name.pack(pady=5)
        player_name_entry = tk.Entry(popup)
        player_name_entry.pack(pady=5)

        def submit_name():
            player_name = player_name_entry.get()
            if player_name:
                leaderboard.append((player_name, final_score, section))
                show_leaderboard()
            popup.destroy()

        submit_button = tk.Button(popup, text="Submit Name", command=submit_name)
        submit_button.pack(pady=10)

    # Load the first question after defining load_question
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

def open_section_3():
    open_quiz_popup("Section 3")

def open_section_4():
    open_quiz_popup("Section 4")

def open_section_5():
    open_quiz_popup("Section 5")

# Function to open the main menu
def open_main_menu():
    main_menu_popup = tk.Toplevel(root)
    main_menu_popup.title("TOC")
    main_menu_popup.geometry("350x300")

    label_title = tk.Label(main_menu_popup, text="EE Research Review", font=("Helvetica", 16))
    label_title.pack(pady=10)

    # Buttons for navigating to different sections
    section1_button = tk.Button(main_menu_popup, text="Section 1 Quiz", command=open_section_1)
    section1_button.pack(fill="x", padx=10, pady=5)

    section2_button = tk.Button(main_menu_popup, text="Section 2 Quiz", command=open_section_2)
    section2_button.pack(fill="x", padx=10, pady=5)

    section3_button = tk.Button(main_menu_popup, text="Section 3 Quiz", command=open_section_3)
    section3_button.pack(fill="x", padx=10, pady=5)

    section4_button = tk.Button(main_menu_popup, text="Section 4 Quiz", command=open_section_4)
    section4_button.pack(fill="x", padx=10, pady=5)

    section5_button = tk.Button(main_menu_popup, text="Section 5 Quiz", command=open_section_5)
    section5_button.pack(fill="x", padx=10, pady=5)

    leaderboard_button = tk.Button(main_menu_popup, text="View Leaderboard", command=show_leaderboard)
    leaderboard_button.pack(fill="x", padx=10, pady=5)

# Create a button on the main window to open the main menu
menu_button = tk.Button(root, text="EE Research Review", command=open_main_menu)
menu_button.pack(pady=50)

# Start the main GUI event loop
root.mainloop()

