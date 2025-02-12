import numpy as np
import math
import time
import random

# Class to manage customer-related information and interactions
class Customer:
    def __init__(self, name, customer_id, is_student=False):
        self.name = name
        self.customer_id = customer_id
        self.is_student = is_student
        self.loyalty_points = 0
        self.request_history = []  # To store requests
        
    def request_ride(self, region, ride_type, distance):
        """Request a ride and calculate the estimated price."""
        ride = Ride(self, region, ride_type, distance)
        self.request_history.append(ride)
        price = ride.calculate_price()
        print(f"{self.name} requested a {ride_type} ride to {region}. Distance: {distance} km. Price: ₹{price}")
        return ride

    def add_loyalty_points(self, points):
        """Add loyalty points for the customer."""
        self.loyalty_points += points
        print(f"{self.name} now has {self.loyalty_points} loyalty points.")

# Class for managing ride requests
class Ride:
    BASE_PRICES = {
        "auto": 30,
        "cab": 50,
        "bike": 20
    }
    PRICE_PER_KM = {
        "auto": 10,
        "cab": 15,
        "bike": 5
    }

    def __init__(self, customer, region, ride_type, distance, ride_id=None):
        self.customer = customer
        self.region = region
        self.ride_type = ride_type
        self.distance = distance
        self.ride_id = ride_id or f"R{random.randint(1000, 9999)}"
        self.status = "Pending"
        self.price = 0
        
    def calculate_price(self):
        """Calculate price for ride based on distance and type."""
        base_price = self.BASE_PRICES[self.ride_type]
        price_per_km = self.PRICE_PER_KM[self.ride_type]
        self.price = base_price + (price_per_km * self.distance)
        return self.price

    def update_status(self, status):
        """Update ride status."""
        self.status = status
        print(f"Ride {self.ride_id} status updated to: {self.status}")

# Class to manage driver allocation and arrival time optimization
class Driver:
    def __init__(self, driver_id, region):
        self.driver_id = driver_id
        self.region = region
        self.is_available = True
        
    def allocate_driver(self, customer):
        """Simulate driver allocation based on customer location and demand prediction."""
        arrival_time = random.randint(5, 15)  # Random arrival time between 5 and 15 minutes
        print(f"Driver {self.driver_id} allocated to {customer.name} in Region {self.region}. Estimated arrival: {arrival_time} minutes.")
        return arrival_time

# Support class to handle customer queries instantly
class Support:
    def __init__(self):
        self.query_log = []

    def receive_query(self, customer, query):
        """Simulate immediate response to a customer query."""
        timestamp = time.ctime()
        response = f"Query received from {customer.name}: {query}. Response: Your query is being processed. Thank you!"
        self.query_log.append((timestamp, customer.name, query, response))
        print(f"Support: {response}")
        return response

# File Handling: Saving ride history to a file for future analysis
def save_ride_history(customer):
    """Save customer ride history to a file."""
    with open("ride_history.txt", "a") as file:
        for ride in customer.request_history:
            file.write(f"Customer: {customer.name}, Ride ID: {ride.ride_id}, Region: {ride.region}, Distance: {ride.distance} km, Price: ₹{ride.price}, Status: {ride.status}\n")

# Vector Space for Regional Allocation (Simplified)
def allocate_drivers_to_regions(region_data):
    """Simulate driver allocation using vector spaces for regional distances."""
    regions = np.array(region_data)  # 2D array (latitude, longitude) of regions
    driver_positions = np.random.rand(len(regions), 2)  # Random positions of drivers in 2D space (latitude, longitude)
    distances = np.linalg.norm(regions - driver_positions, axis=1)  # Calculate distances using Euclidean distance (vector space)
    print(f"Driver distances from regions: {distances}")
    return distances

# Main code simulating the customer service improvement
if __name__ == "__main__":
    # Initialize some drivers and support team
    driver1 = Driver(driver_id="D1001", region=1)
    driver2 = Driver(driver_id="D1002", region=2)

    support_team = Support()

    customers = {}
    drivers = [driver1, driver2]

    places = {
        "1": ("Charminar", 10),
        "2": ("Golkonda Fort", 15),
        "3": ("Hitech City", 20),
        "4": ("Hussain Sagar", 8),
        "5": ("Ramoji Film City", 30),
        "6": ("Nehru Zoological Park", 12),
        "7": ("Birla Mandir", 5),
        "8": ("Salar Jung Museum", 7),
        "9": ("Shilparamam", 18),
        "10": ("Lumbini Park", 6)
    }

    print("Welcome to Rapido Service")

    while True:
        print("\nWelcome to Rapido Customer Interface")
        print("1. Request a Ride")
        print("2. Check Loyalty Points")
        print("3. Contact Support")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            customer_id = input("Enter your customer ID: ")
            if customer_id not in customers:
                customer_name = input("Enter your name: ")
                is_student = input("Are you a student? (yes/no): ").lower() == 'yes'
                customers[customer_id] = Customer(name=customer_name, customer_id=customer_id, is_student=is_student)
            customer = customers[customer_id]
            print("Choose your destination:")
            for key, value in places.items():
                print(f"{key}. {value[0]} ({value[1]} km)")
            place_choice = input("Enter your choice: ")
            if place_choice in places:
                region, distance = places[place_choice]
                print("Choose ride type: 1. Auto 2. Cab 3. Bike")
                ride_choice = input("Enter your choice: ")
                ride_type = "auto" if ride_choice == '1' else "cab" if ride_choice == '2' else "bike"
                ride = customer.request_ride(region, ride_type, distance)
                driver = next((d for d in drivers if d.region == 1 and d.is_available), None)
                if driver:
                    driver.allocate_driver(customer)
                    driver.is_available = False
                else:
                    print("No available drivers in this region.")
            else:
                print("Invalid choice. Please try again.")
        elif choice == '2':
            customer_id = input("Enter your customer ID: ")
            if customer_id in customers:
                customer = customers[customer_id]
                print(f"{customer.name} has {customer.loyalty_points} loyalty points.")
            else:
                print("Customer not found.")
        elif choice == '3':
            customer_id = input("Enter your customer ID: ")
            if customer_id in customers:
                customer = customers[customer_id]
                query = input("Enter your query: ")
                support_team.receive_query(customer, query)
            else:
                print("Customer not found.")
        elif choice == '4':
            print("Exiting the interface. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    # Save ride history to file
    for customer in customers.values():
        save_ride_history(customer)

    # Simulate region allocation using vector space for distances
    region_data = [(12.9716, 77.5946), (13.0827, 80.2707), (19.0760, 72.8777)]  # Example region coordinates
    allocate_drivers_to_regions(region_data)