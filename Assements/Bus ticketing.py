import datetime  # For date and time handling

# Seasonal Discounts
SEASONAL_DISCOUNTS = {
    "Winter": 0.10,  # 10% discount
    "Summer": 0.15,  # 15% discount
    "Monsoon": 0.05  # 5% discount
}

# Offers
WEEKEND_DISCOUNT = 0.10  # 10% off on weekends
STUDENT_DISCOUNT = 0.20  # 20% discount for students


# Function to calculate seasonal discount
def get_seasonal_discount():
    current_month = datetime.datetime.now().month
    if current_month in [12, 1, 2]:
        return SEASONAL_DISCOUNTS["Winter"]
    elif current_month in [6, 7, 8]:
        return SEASONAL_DISCOUNTS["Summer"]
    elif current_month in [9, 10, 11]:
        return SEASONAL_DISCOUNTS["Monsoon"]
    else:
        return 0  # No discount for other months


# Function to check if it's a weekend
def is_weekend():
    current_day = datetime.datetime.now().weekday()  # Monday = 0, Sunday = 6
    return current_day in [5, 6]  # Saturday or Sunday


# Main Ticket Booking System
def book_ticket():
    base_ticket_price = 500  # Base price for one ticket
    print("Welcome to the Bus Ticket Booking System!")

    # User inputs
    name = input("Enter your name: ")
    is_student = input("Are you a student? (yes/no): ").strip().lower() == "yes"
    num_tickets = int(input("How many tickets would you like to book? "))

    # Calculate seasonal discount
    seasonal_discount = get_seasonal_discount()

    # Weekend discount
    weekend_discount = WEEKEND_DISCOUNT if is_weekend() else 0

    # Total discount
    total_discount = seasonal_discount + (STUDENT_DISCOUNT if is_student else 0) + weekend_discount
    total_discount = min(total_discount, 0.30)  # Cap total discount to 30%

    # Calculate total price
    total_price = base_ticket_price * num_tickets
    discounted_price = total_price * (1 - total_discount)

    # Summary
    print("\nBooking Summary:")
    print(f"Name: {name}")
    print(f"Number of Tickets: {num_tickets}")
    print(f"Base Ticket Price: ₹{base_ticket_price}")
    print(f"Total Base Price: ₹{total_price}")
    print(f"Seasonal Discount: {seasonal_discount * 100}%")
    print(f"Weekend Discount: {weekend_discount * 100}%")
    if is_student:
        print(f"Student Discount: {STUDENT_DISCOUNT * 100}%")
    print(f"Total Discount Applied: {total_discount * 100}%")
    print(f"Final Price to Pay: ₹{discounted_price:.2f}")

    print("\nThank you for booking with us! Have a safe journey!")


# Booking Loop
while True:
    book_ticket()
    another_booking = input("\nDo you want to book another ticket? (yes/no): ").strip().lower()
    if another_booking != "yes":
        print("Goodbye!")
        break
