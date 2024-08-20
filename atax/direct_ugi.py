import os

# Constants
FILE_PATH = "state/user_selections.txt"
MAX_NUMBERS = 4

def print_instructions():
    print("""
Welcome to the Number Input System!
Instructions:
1. Type a number (0-16) to add it to the sequence.
2. Type 's' to submit the sequence and save it to a file.
3. Type 'r' to reset the current sequence.
4. Type 'exit' to exit the program.

Important:
- You can enter up to 4 numbers in a sequence.
- If the file 'user_selections.txt' already exists, you must remove it or wait until it burns before submitting a new sequence.
""")

def main():
    print_instructions()

    user_sequence = []

    while True:
        user_input = input("Enter a command: ").strip().lower()

        if user_input == "exit":
            print("Exiting the program.")
            break
        elif user_input.isdigit():
            number = int(user_input)
            if 0 <= number <= 16:
                if len(user_sequence) >= MAX_NUMBERS:
                    print(f"Error: You can't enter more than {MAX_NUMBERS} numbers; if you want other numbers, you can reset the sequence by typing 'r', or submit by typing 's'.")
                else:
                    user_sequence.append(user_input)
                    print(f"Added {user_input} to the sequence. Current sequence: {', '.join(user_sequence)}")
            else:
                print("Invalid number. Please enter a number between 0 and 16.")
        elif user_input == "s":
            if not user_sequence:
                print("Error: You must enter at least one number before submitting.")
            elif os.path.exists(FILE_PATH):
                print("File already exists. You need to remove the file or wait until its images get burned, before continuing.")
            else:
                with open(FILE_PATH, "w") as file:
                    file.write("\n".join(user_sequence))
                print(f"Sequence saved to {FILE_PATH}.")
                user_sequence.clear()  # Reset the sequence after saving
        elif user_input == "r":
            user_sequence.clear()
            print("Sequence reset. You can start entering numbers again.")
        else:
            print("Invalid command. Please enter a number between 0 and 16, 's' to submit, 'r' to reset, or 'exit' to quit.")

if __name__ == "__main__":
    main()