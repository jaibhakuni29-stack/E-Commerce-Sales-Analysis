import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("E-COMMERCE SALES ANALYTICS - PROJECT 1")
print("="*80)

# Load data
print("\n[STEP 1] Loading data...")
df = pd.read_csv('data/raw_sales_data.csv')
print(f"✓ Loaded {len(df)} records")

# Show first few rows
print("\n[STEP 2] First few records:")
print(df.head())

# Basic statistics
print("\n[STEP 3] Data Statistics:")
print(df[['Quantity', 'Unit_Price', 'Final_Price']].describe())

# Key metrics
print("\n[STEP 4] Key Metrics:")
print(f"Total Revenue: ₹{df['Final_Price'].sum():,.2f}")
print(f"Average Order Value: ₹{df['Final_Price'].mean():,.2f}")
print(f"Total Orders: {len(df)}")
print(f"Unique Customers: {df['Customer_ID'].nunique()}")

# Revenue by category
print("\n[STEP 5] Revenue by Category:")
revenue_by_cat = df.groupby('Product_Category')['Final_Price'].sum().sort_values(ascending=False)
print(revenue_by_cat)

# Create visualizations
print("\n[STEP 6] Creating visualizations...")

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Visualization 1: Revenue Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(df['Final_Price'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0].set_title('Distribution of Order Values', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Final Price (₹)')
axes[0].set_ylabel('Frequency')
axes[1].boxplot(df['Final_Price'], vert=True)
axes[1].set_title('Order Value Range (Box Plot)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Final Price (₹)')
plt.tight_layout()
plt.savefig('visualizations/01_revenue_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_revenue_distribution.png")
plt.close()

# Visualization 2: Revenue by Category
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
category_revenue = df.groupby('Product_Category')['Final_Price'].sum().sort_values(ascending=False)
axes[0].bar(category_revenue.index, category_revenue.values, color='skyblue', edgecolor='black')
axes[0].set_title('Total Revenue by Category', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Revenue (₹)')
axes[0].tick_params(axis='x', rotation=45)
colors = plt.cm.Set3(range(len(category_revenue)))
axes[1].pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%', colors=colors, startangle=90)
axes[1].set_title('Revenue Distribution by Category', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/02_revenue_by_category.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_revenue_by_category.png")
plt.close()

# Visualization 3: Top 10 Products
top_10_products = df.groupby('Product_Name')['Final_Price'].sum().sort_values(ascending=True).tail(10)
plt.figure(figsize=(12, 6))
plt.barh(top_10_products.index, top_10_products.values, color='coral', edgecolor='black')
plt.title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Revenue (₹)')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('visualizations/03_top_10_products.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_top_10_products.png")
plt.close()

# Visualization 4: Discount Impact
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(df['Discount_Percent'], df['Final_Price'], alpha=0.5, color='purple')
axes[0].set_title('Impact of Discount on Order Value', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Discount Percent (%)')
axes[0].set_ylabel('Final Price (₹)')
axes[0].grid(True, alpha=0.3)
axes[1].bar(['No Discount', 'Low (1-10%)', 'Medium (11-20%)', 'High (>20%)'], 
            [df[df['Discount_Percent']==0]['Final_Price'].mean(),
             df[(df['Discount_Percent']>0) & (df['Discount_Percent']<=10)]['Final_Price'].mean(),
             df[(df['Discount_Percent']>10) & (df['Discount_Percent']<=20)]['Final_Price'].mean(),
             df[df['Discount_Percent']>20]['Final_Price'].mean()],
            color='lightgreen', edgecolor='black')
axes[1].set_title('Average Order Value by Discount Level', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Average Price (₹)')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('visualizations/04_discount_impact.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 04_discount_impact.png")
plt.close()

# Visualization 5: Customer Satisfaction
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
satisfaction_counts = df['Customer_Satisfaction'].value_counts().sort_index()
axes[0].bar(satisfaction_counts.index, satisfaction_counts.values, color='gold', edgecolor='black')
axes[0].set_title('Distribution of Customer Satisfaction Ratings', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Rating (1-5)')
axes[0].set_ylabel('Number of Orders')
axes[0].grid(True, alpha=0.3, axis='y')
satisfaction_by_category = df.groupby('Product_Category')['Customer_Satisfaction'].mean()
axes[1].barh(satisfaction_by_category.index, satisfaction_by_category.values, color='lightcoral', edgecolor='black')
axes[1].set_title('Average Customer Satisfaction by Category', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Average Rating')
axes[1].grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('visualizations/05_customer_satisfaction.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 05_customer_satisfaction.png")
plt.close()

# Visualization 6: Correlation Heatmap
corr_cols = ['Quantity', 'Unit_Price', 'Discount_Percent', 'Final_Price', 'Shipping_Days', 'Customer_Satisfaction']
correlation_matrix = df[corr_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True, linewidths=1)
plt.title('Correlation Heatmap - Numerical Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/06_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 06_correlation_heatmap.png")
plt.close()

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)
print("\nAll visualizations saved in the visualizations folder!")
