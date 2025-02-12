import math
import time
import random

# Class to handle customer details and ride requests
class Customer:
    def __init__(self, name, customer_id, region, is_student=False):
        self.name = name
        self.customer_id = customer_id
        self.region = region
        self.is_student = is_student
        self.ride_history = []

    def request_ride(self):
        ride = Ride(self)
        self.ride_history.append(ride)
        return ride

# Class to handle ride details and pricing
class Ride:
    def __init__(self, customer):
        self.customer = customer
        self.status = "Pending"
        self.price = 0
        self.allocate_driver()

    def calculate_price(self):
        self.price = 15  # Fixed price for simplicity
        if self.customer.is_student:
            self.price -= 5  # Discount for students
        return self.price

    def allocate_driver(self):
        driver = Driver(self.customer.region)
        distance = driver.calculate_distance(self.customer.region)
        self.driver = driver
        self.driver.assign_ride(self)

# Class to handle driver details and allocation
class Driver:
    def __init__(self, region):
        self.region = region
        self.is_available = True

    def calculate_distance(self, customer_region):
        driver_coords = (random.randint(1, 10), random.randint(1, 10))  # Random coordinates for drivers
        customer_coords = (customer_region[0], customer_region[1])
        distance = math.dist(driver_coords, customer_coords)  # Euclidean distance between driver and customer
        return distance

    def assign_ride(self, ride):
        self.status = "Assigned"
        ride.status = "Driver Assigned"
        print(f"Driver assigned to {ride.customer.name}. Ride status: {ride.status}")

# Class to handle customer queries and support
class Support:
    def __init__(self):
        self.query_log = []

    def receive_query(self, customer, query):
        timestamp = time.ctime()
        response = f"Query received from {customer.name}: {query}. Response: Your query is being processed."
        self.query_log.append((timestamp, customer.name, query, response))
        return response

# Simulate a simple customer interaction
def main():
    # Take customer input
    customer_name = input("Enter your name: ")
    customer_id = input("Enter your customer ID: ")
    region = tuple(map(int, input("Enter your region (as x, y coordinates): ").split(',')))
    is_student = input("Are you a student? (yes/no): ").strip().lower() == 'yes'

    customer = Customer(customer_name, customer_id, region, is_student)
    
    # Request a ride
    ride = customer.request_ride()
    print(f"Ride requested by {customer.name}. The calculated price: ${ride.calculate_price()}")

    # Assign driver and calculate distance
    print(f"Assigning driver to customer {customer.name}...")
    ride.allocate_driver()

    # Handle customer query for support
    support = Support()
    query = input("Enter your support query: ")
    print(support.receive_query(customer, query))

    # In-memory logs (instead of file handling)
    ride_history_log = f"{time.ctime()} - Ride Requested by {customer.name} (ID: {customer_id}) from {region}, Price: ${ride.price}\n"
    support_log = f"{time.ctime()} - Query from {customer.name}: {query}\n"
    
    # Print logs (for simulation, instead of writing to files)
    print("\n---- Ride History Log ----")
    print(ride_history_log)
    print("\n---- Support Log ----")
    print(support_log)

if __name__ == "__main__":
    main()
