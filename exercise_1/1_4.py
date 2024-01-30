import os

def portfolio_cost(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")
    
    with open(file_path, "r") as file:
        data = file.readlines()
        total_cost = 0
        for line in data:
            current_line = line.split()
            try:
                current_unit_price = float(current_line[-1])
                number_shares = int(current_line[1])
                current_cost = current_unit_price * number_shares
            except ValueError as e:
                print("Couldn't parse:", repr(line))
                print("Reason:", e)
                # raise ValueError("Invalid value found in line: ",repr(line))
            
            total_cost += current_cost
        return total_cost
    
    

# print("Total cost: ", portfolio_cost("../Data/portfolio.dat"))