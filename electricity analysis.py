# Electricity Consumption Analysis and Forecasting
# Pure Python (no external libraries) - runs on Programiz
import random

random.seed(42)
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# 1. Generate 3 years of monthly household consumption (kWh)
seasonal = [1.00, 0.92, 0.95, 1.10, 1.30, 1.45, 1.40, 1.35, 1.20, 1.00, 0.90, 0.95]
data = []
for y in range(3):
    for m in range(12):
        base = 250 + 4 * (y * 12 + m)          # slow upward trend
        data.append(round(base * seasonal[m] + random.uniform(-10, 10), 1))

print("=== ELECTRICITY CONSUMPTION ANALYSIS ===")
print("Total records:", len(data))

# 2. Basic statistics
mean = sum(data) / len(data)
print("Average monthly use : %.2f kWh" % mean)
print("Highest month       : %.1f kWh (%s year %d)" % (max(data), months[data.index(max(data)) % 12], data.index(max(data)) // 12 + 1))
print("Lowest month        : %.1f kWh (%s year %d)" % (min(data), months[data.index(min(data)) % 12], data.index(min(data)) // 12 + 1))

# 3. Yearly totals
print("\n--- Yearly Totals ---")
for y in range(3):
    print("Year %d: %.1f kWh" % (y + 1, sum(data[y*12:(y+1)*12])))

# 4. Monthly averages (text bar chart)
print("\n--- Average by Month ---")
for m in range(12):
    avg = sum(data[m::12]) / 3
    print("%s | %-30s %.1f" % (months[m], "#" * int(avg / 12), avg))

# 5. Linear trend (least squares)
n = len(data)
xs = list(range(n))
xm = sum(xs) / n
slope = sum((x - xm) * (d - mean) for x, d in zip(xs, data)) / sum((x - xm) ** 2 for x in xs)
intercept = mean - slope * xm
print("\nTrend: consumption changes by %.2f kWh per month" % slope)

# 6. Seasonal index = actual / trend, averaged per month
index = []
for m in range(12):
    ratios = [data[i] / (intercept + slope * i) for i in range(m, n, 12)]
    index.append(sum(ratios) / len(ratios))

def predict(i):
    return (intercept + slope * i) * index[i % 12]

# 7. Accuracy check on fitted data
mape = sum(abs(data[i] - predict(i)) / data[i] for i in range(n)) / n * 100
print("Model error (MAPE): %.2f%%  | Accuracy: %.2f%%" % (mape, 100 - mape))

# 8. Forecast next 12 months
print("\n--- Forecast: Next 12 Months ---")
total = 0
for k in range(12):
    f = predict(n + k)
    total += f
    print("%s (Year 4): %7.1f kWh" % (months[k], f))
print("Forecast total for Year 4: %.1f kWh" % total)
print("Estimated bill @ Rs 7/unit: Rs %.0f" % (total * 7))
