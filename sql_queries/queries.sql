-- QUERY 1: Total Revenue and Key Metrics
SELECT
    COUNT(DISTINCT Order_ID) as Total_Orders,
    COUNT(DISTINCT Customer_ID) as Unique_Customers,
    SUM(Final_Price) as Total_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value,
    ROUND(MAX(Final_Price), 2) as Max_Order_Value,
    ROUND(MIN(Final_Price), 2) as Min_Order_Value
FROM sales_data;

-- QUERY 2: Revenue by Product Category
SELECT
    Product_Category,
    COUNT(*) as Order_Count,
    SUM(Quantity) as Total_Quantity_Sold,
    ROUND(SUM(Final_Price), 2) as Total_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value,
    ROUND(100.0 * SUM(Final_Price) / (SELECT SUM(Final_Price) FROM sales_data), 2) as Revenue_Percentage
FROM sales_data
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;

-- QUERY 3: Top 10 Products by Revenue
SELECT
    Product_Name,
    Product_Category,
    COUNT(*) as Times_Sold,
    SUM(Quantity) as Total_Quantity,
    ROUND(SUM(Final_Price), 2) as Total_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value
FROM sales_data
WHERE Product_Name != 'Unknown'
GROUP BY Product_Name, Product_Category
ORDER BY Total_Revenue DESC
LIMIT 10;

-- QUERY 4: Monthly Revenue Trend
SELECT
    strftime('%Y-%m', Date) as Month,
    COUNT(*) as Order_Count,
    SUM(Quantity) as Total_Quantity,
    ROUND(SUM(Final_Price), 2) as Monthly_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value
FROM sales_data
GROUP BY strftime('%Y-%m', Date)
ORDER BY Month;

-- QUERY 5: Payment Method Analysis
SELECT
    Payment_Method,
    COUNT(*) as Transaction_Count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales_data), 2) as Percentage_of_Total,
    ROUND(SUM(Final_Price), 2) as Total_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Transaction_Value
FROM sales_data
GROUP BY Payment_Method
ORDER BY Transaction_Count DESC;

-- QUERY 6: Discount Analysis
SELECT
    CASE
        WHEN Discount_Percent = 0 THEN 'No Discount'
        WHEN Discount_Percent <= 10 THEN 'Low (1-10%)'
        WHEN Discount_Percent <= 20 THEN 'Medium (11-20%)'
        ELSE 'High (>20%)'
    END as Discount_Category,
    COUNT(*) as Order_Count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales_data), 2) as Percentage_of_Orders,
    ROUND(SUM(Final_Price), 2) as Total_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value
FROM sales_data
GROUP BY Discount_Category
ORDER BY Order_Count DESC;

-- QUERY 7: Customer Satisfaction by Category
SELECT
    Product_Category,
    Customer_Satisfaction as Rating,
    COUNT(*) as Order_Count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales_data), 2) as Percentage
FROM sales_data
GROUP BY Product_Category, Customer_Satisfaction
ORDER BY Product_Category, Customer_Satisfaction DESC;

-- QUERY 8: Shipping Performance
SELECT
    ROUND(AVG(Shipping_Days), 2) as Avg_Shipping_Days,
    MIN(Shipping_Days) as Fastest_Delivery,
    MAX(Shipping_Days) as Slowest_Delivery,
    SUM(CASE WHEN Shipping_Days <= 5 THEN 1 ELSE 0 END) as Fast_Deliveries,
    ROUND(100.0 * SUM(CASE WHEN Shipping_Days <= 5 THEN 1 ELSE 0 END) / COUNT(*), 2) as Fast_Delivery_Percentage
FROM sales_data;

-- QUERY 9: Top 10 Customers by Spending
SELECT
    Customer_ID,
    COUNT(*) as Purchase_Count,
    ROUND(SUM(Final_Price), 2) as Total_Spent,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value
FROM sales_data
GROUP BY Customer_ID
ORDER BY Total_Spent DESC
LIMIT 10;

-- QUERY 10: Products with Highest Satisfaction
SELECT
    Product_Name,
    Product_Category,
    COUNT(*) as Times_Ordered,
    ROUND(AVG(Customer_Satisfaction), 2) as Avg_Satisfaction,
    ROUND(SUM(Final_Price), 2) as Total_Revenue
FROM sales_data
WHERE Product_Name != 'Unknown'
GROUP BY Product_Name, Product_Category
HAVING COUNT(*) >= 10
ORDER BY Avg_Satisfaction DESC
LIMIT 15;

-- QUERY 11: Revenue Per Order by Category
SELECT
    Product_Category,
    COUNT(*) as Total_Orders,
    COUNT(DISTINCT Customer_ID) as Unique_Customers,
    ROUND(AVG(Quantity), 2) as Avg_Items_Per_Order,
    ROUND(SUM(Final_Price), 2) as Total_Revenue,
    ROUND(AVG(Final_Price), 2) as Avg_Order_Value,
    ROUND(AVG(Customer_Satisfaction), 2) as Avg_Satisfaction
FROM sales_data
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;

-- QUERY 12: Discount Impact on Satisfaction
SELECT
    CASE
        WHEN Discount_Percent = 0 THEN 'No Discount'
        WHEN Discount_Percent <= 10 THEN 'Low (1-10%)'
        WHEN Discount_Percent <= 20 THEN 'Medium (11-20%)'
        ELSE 'High (>20%)'
    END as Discount_Level,
    ROUND(AVG(Customer_Satisfaction), 2) as Avg_Satisfaction,
    COUNT(*) as Order_Count,
    ROUND(AVG(Final_Price), 2) as Avg_Price
FROM sales_data
GROUP BY Discount_Level
ORDER BY Avg_Satisfaction DESC;