import ast

def get_student_data():
    # Ask the user to enter a list of students with their names and grades
    student_input = input("Enter the student data (e.g., [{'name': 'Alice', 'grade': 85}, {'name': 'Bob', 'grade': 92}]): ")

    try:
        # Safely evaluate the input string into a Python data structure
        student_data = ast.literal_eval(student_input)

        # Check if the input is a list of dictionaries
        if isinstance(student_data, list) and all(isinstance(i, dict) and 'name' in i and 'grade' in i for i in student_data):
            # Validate that all grades are numbers between 0 and 100
            for student in student_data:
                if not (0 <= student['grade'] <= 100):
                    print(f"Invalid grade {student['grade']} for student {student['name']}. Grade must be between 0 and 100.")
                    return None
            print("\nStudent data successfully loaded!")
            return student_data
        else:
            print("Invalid input format! Please make sure it's a list of dictionaries with 'name' and 'grade'.")
            return None
    except (ValueError, SyntaxError):
        print("Error: Invalid data entered. Please ensure the input format is correct.")
        return None

def calculate_average_grade(students):
    if not students:
        return None
    
    total_grade = sum(student['grade'] for student in students)
    average_grade = total_grade / len(students)
    return average_grade

def students_above_grade(students, threshold):
    if not students:
        return None
    
    above_threshold = [student['name'] for student in students if student['grade'] > threshold]
    return above_threshold

def main():
    # Get student data from the user
    students = get_student_data()

    if students:
        # Calculate and display average grade
        average_grade = calculate_average_grade(students)
        if average_grade is not None:
            print(f"\nThe average grade of the students is: {average_grade:.2f}")
        
        # Find students with grades above a certain threshold (e.g., 90)
        threshold = 90
        above_90 = students_above_grade(students, threshold)
        if above_90 is not None:
            print(f"\nStudents with grades above {threshold}: {', '.join(above_90)}")

if __name__ == "__main__":
    main()
