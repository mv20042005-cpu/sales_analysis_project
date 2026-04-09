import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# STEP 1: Create output folder
# -----------------------------
os.makedirs("output", exist_ok=True)

# -----------------------------
# STEP 2: Load dataset
# -----------------------------
try:
    df = pd.read_csv("data/sales_data.csv")
    print("Dataset loaded successfully.\n")
except FileNotFoundError:
    print("Error: sales_data.csv file not found in the data folder.")
    exit()

# -----------------------------
# STEP 3: Basic inspection
# -----------------------------
print("First 5 rows:")
print(df.head(), "\n")

print("Dataset info:")
print(df.info(), "\n")

print("Missing values:")
print(df.isnull().sum(), "\n")

# -----------------------------
# STEP 4: Data preprocessing
# -----------------------------
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Remove duplicate rows if any
df = df.drop_duplicates()

# Handle missing dates
df = df.dropna(subset=["Order_Date"])

# Create Sales column
df["Sales"] = df["Quantity"] * df["Unit_Price"]

# Create Month column
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# -----------------------------
# STEP 5: Overall summary
# -----------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
average_sales = df["Sales"].mean()

print("----- SALES SUMMARY -----")
print(f"Total Sales: ₹{total_sales:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Average Sales per Order: ₹{average_sales:,.2f}\n")

# Save summary to text file
with open("output/sales_summary.txt", "w", encoding="utf-8") as f:
    f.write("SALES ANALYSIS SUMMARY\n")
    f.write("======================\n")
    f.write(f"Total Sales: ₹{total_sales:,.2f}\n")
    f.write(f"Total Profit: ₹{total_profit:,.2f}\n")
    f.write(f"Total Orders: {total_orders}\n")
    f.write(f"Average Sales per Order: ₹{average_sales:,.2f}\n")

# -----------------------------
# STEP 6: Monthly sales analysis
# -----------------------------
monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()
print("Monthly Sales:")
print(monthly_sales, "\n")

plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/monthly_sales.png")
plt.close()
plt.show(block=False)
plt.pause(3)
plt.close()

# -----------------------------
# STEP 7: Category-wise sales
# -----------------------------
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
print("Category-wise Sales:")
print(category_sales, "\n")

plt.figure(figsize=(8, 5))
sns.barplot(x=category_sales.index, y=category_sales.values)
plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("output/category_sales.png")
plt.close()
plt.show(block=False)
plt.pause(3)
plt.close()

# -----------------------------
# STEP 8: Top 5 products by sales
# -----------------------------
top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)
print("Top 5 Products by Sales:")
print(top_products, "\n")

plt.figure(figsize=(10, 5))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Top 5 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("output/top_products.png")
plt.close()
plt.show(block=False)
plt.pause(3)
plt.close()

# -----------------------------
# STEP 9: Region-wise sales
# -----------------------------
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
print("Region-wise Sales:")
print(region_sales, "\n")

# -----------------------------
# STEP 10: Best category and best month
# -----------------------------
best_category = category_sales.idxmax()
best_month = monthly_sales.idxmax()

print(f"Best Performing Category: {best_category}")
print(f"Best Performing Month: {best_month}")

with open("output/sales_summary.txt", "a", encoding="utf-8") as f:
    f.write(f"Best Performing Category: {best_category}\n")
    f.write(f"Best Performing Month: {best_month}\n")

print("\nProject completed successfully!")
print("Charts saved in the output folder.")