
total_cost = 0

file_path = "../Data/portfolio.dat"

# Open the .dat file
with open(file_path, "r") as file:
    data = file.readlines()  # Use readlines() to read each line as a list item
    
    for line in data:
        current_line = line.split() 
        total_cost += float(current_line[-1])  # Uncomment this line to calculate the total cost
        
print("Total cost: ", total_cost)

