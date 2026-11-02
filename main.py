import os

COURSE_FEES = {
    "BCA": 45000,
    "BTech": 60000,
    "MBA": 80000
}

FILE_NAME = "fees.txt"
students = []


def calculate_fee(student):
    total_fee = COURSE_FEES[student["course"]]
    paid = student["paid"]
    due = total_fee - paid

    if paid == 0:
        status = "Unpaid"
    elif due == 0:
        status = "Paid"
    else:
        status = "Partial"

    return total_fee, due, status


def save_records():
    with open(FILE_NAME, "w") as file:
        for student in students:
            file.write(
                f'{student["roll"]},'
                f'{student["name"]},'
                f'{student["course"]},'
                f'{student["paid"]}\n'
            )


def load_records():
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r") as file:
        for line in file:
            try:
                roll, name, course, paid = line.strip().split(",")

                if course not in COURSE_FEES:
                    continue

                student = {
                    "roll": int(roll),
                    "name": name,
                    "course": course,
                    "paid": int(paid)
                }

                if not find_student(student["roll"]):
                    students.append(student)

            except (ValueError, TypeError):
                continue


def find_student(roll):
    for student in students:
        if student["roll"] == roll:
            return student
    return None


def add_student():
    try:
        roll = int(input("Enter Roll Number: "))

        if roll <= 0:
            print("Invalid roll number.")
            return

        if find_student(roll):
            print("Student already exists.")
            return

        name = input("Enter Student Name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        if "," in name:
            print("Name cannot contain a comma (breaks file storage).")
            return

        print("Available Courses: BCA, BTech, MBA")
        course_input = input("Enter Course: ").strip().lower()

        course_map = {
            "bca": "BCA",
            "btech": "BTech",
            "mba": "MBA"
        }

        course = course_map.get(course_input)

        if course is None:
            print("Invalid course.")
            return

        student = {
            "roll": roll,
            "name": name,
            "course": course,
            "paid": 0
        }

        students.append(student)
        save_records()

        total_fee, due, status = calculate_fee(student)

        print(
            f"Student added: {roll} | {name} | {course} | "
            f"Total Fee: {total_fee} | Paid: 0 | "
            f"Due: {due} | Status: {status}"
        )

    except ValueError:
        print("Please enter a valid roll number.")


def pay_fee():
    try:
        roll = int(input("Enter Roll Number: "))
        student = find_student(roll)

        if student is None:
            print("Student not found.")
            return

        total_fee, due, status = calculate_fee(student)

        amount = int(input("Enter Payment Amount: "))

        if amount <= 0:
            print("Invalid payment amount. Payment rejected.")
            return

        if amount > due:
            print(f"Amount exceeds due ({due}). Payment rejected.")
            return

        student["paid"] += amount
        save_records()

        total_fee, due, status = calculate_fee(student)

        print(
            f"Payment received. Paid: {student['paid']} | "
            f"Due: {due} | Status: {status}"
        )

    except ValueError:
        print("Please enter valid numeric values.")


def search_student():
    try:
        roll = int(input("Enter Roll Number to Search: "))
        student = find_student(roll)

        if student is None:
            print("Student not found.")
            return

        total_fee, due, status = calculate_fee(student)

        print(f"Roll: {student['roll']}")
        print(f"Name: {student['name']}")
        print(f"Course: {student['course']}")
        print(f"Total Fee: {total_fee}")
        print(f"Paid: {student['paid']}")
        print(f"Due: {due}")
        print(f"Status: {status}")

    except ValueError:
        print("Please enter a valid roll number.")


def pending_dues():
    print("Students with Pending Dues:")
    found = False

    for student in students:
        total_fee, due, status = calculate_fee(student)

        if due > 0:
            print(
                f"{student['roll']} | {student['name']} | "
                f"Due: {due}"
            )
            found = True

    if not found:
        print("No pending dues!")


def main():
    load_records()

    while True:
        print("\n===== STUDENT FEE MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Pay Fee")
        print("3. Search Student")
        print("4. Pending Dues")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            pay_fee()
        elif choice == "3":
            search_student()
        elif choice == "4":
            pending_dues()
        elif choice == "5":
            save_records()
            print("Records saved. Thank you!")
            break
        else:
            print("Invalid choice. Select 1 to 5.")


if __name__ == "__main__":
    main()
