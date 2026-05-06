import pandas as pd
import numpy as np
import os
from datetime import datetime

FILE_NAME = "students.txt"

if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()


def load_data():
    try:
        df = pd.read_csv(FILE_NAME,
                         names=["ID", "Name", "Age", "Marks", "Course", "Grade", "Date"])
        return df
    except:
        return pd.DataFrame(columns=["ID", "Name", "Age", "Marks", "Course", "Grade", "Date"])


def save_data(df):
    df.to_csv(FILE_NAME, index=False, header=False)


def calculate_grade(marks):
    if marks >= 85:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


# MAIN FUNCTIONS

def add_student():
    df = load_data()

    try:
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        marks = int(input("Enter marks: "))
        course = input("Enter course: ")
    except:
        print(" Invalid input\n")
        return

    new_id = 1 if df.empty else df["ID"].astype(int).max() + 1
    grade = calculate_grade(marks)
    date = datetime.now().strftime("%Y-%m-%d")

    new_data = pd.DataFrame([[new_id, name, age, marks, course, grade, date]],
                            columns=df.columns)

    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)

    print(f" Student added on {date}!\n")


def view_students():
    df = load_data()

    if df.empty:
        print("No records found\n")
    else:
        print("\n--- Student Records ---")
        print(df.to_string(index=False))
    print()


def search_student():
    df = load_data()
    name = input("Enter name to search: ")

    result = df[df["Name"].str.contains(name, case=False)]

    if result.empty:
        print(" No record found\n")
    else:
        print(result.to_string(index=False))
    print()


def update_student():
    df = load_data()

    try:
        sid = int(input("Enter ID to update: "))
    except:
        print(" Invalid ID\n")
        return

    if sid not in df["ID"].astype(int).values:
        print(" Student not found\n")
        return

    # Show current record
    print("\nCurrent Record:")
    print(df[df["ID"].astype(int) == sid].to_string(index=False))

    print("\nEnter new details (press Enter to keep old value)")

    current = df[df["ID"].astype(int) == sid].iloc[0]

    name = input(f"Name ({current['Name']}): ") or current['Name']
    age_input = input(f"Age ({current['Age']}): ")
    marks_input = input(f"Marks ({current['Marks']}): ")
    course = input(f"Course ({current['Course']}): ") or current['Course']

    age = int(age_input) if age_input else int(current['Age'])
    marks = int(marks_input) if marks_input else int(current['Marks'])

    grade = calculate_grade(marks)
    date = datetime.now().strftime("%Y-%m-%d")

    df.loc[df["ID"].astype(int) == sid] = [sid, name, age, marks, course, grade, date]
    save_data(df)

    print("Record updated successfully!\n")


def delete_student():
    df = load_data()

    try:
        sid = int(input("Enter ID to delete: "))
    except:
        print(" Invalid ID\n")
        return

    if sid not in df["ID"].astype(int).values:
        print("Student not found\n")
        return

    # Delete
    df = df[df["ID"].astype(int) != sid]

    # Reset IDs
    df = df.reset_index(drop=True)
    df["ID"] = df.index + 1

    save_data(df)

    print("Record deleted and IDs updated!\n")


#  ANALAYSIS FUNCTION

def analyze_data():
    df = load_data()

    if df.empty:
        print("No data\n")
        return

    marks = df["Marks"].astype(int).to_numpy()

    print("\n--- Analysis ---")
    print("Average:", np.mean(marks))
    print("Max:", np.max(marks))
    print("Min:", np.min(marks))

    print("\nTopper:")
    print(df.loc[df["Marks"].astype(int).idxmax()])
    print()


# MAIN MENU

def main():
    while True:
        print("====== Student System (TXT File) ======")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Analyze Data")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            analyze_data()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print(" Invalid choice\n")


main()
