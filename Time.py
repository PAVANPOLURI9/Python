import time

# Start the timer
start_time = time.time()

# Sample code to measure
for i in range(1000000):
    pass

# End the timer
end_time = time.time()

# Calculate the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")