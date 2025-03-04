import matplotlib.pyplot as plt
import pandas as pd

# Load data
data = pd.read_csv("cookie_performance_5.csv")      #insert the name of the file
x = data["Time Between Buys"].tolist()
y = data["Cookies Per Second"].tolist()

# Create and style the graph
plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label="Cookies per second")

# Labels and title
plt.xlabel("Time Between Buys (seconds)")
plt.ylabel("Cookies per Second")
plt.title("Cookie Clicker Performance Over Time")
plt.legend()
plt.grid(True)
plt.show()