# Quick Suite Topics Configuration Guide

This guide provides the recommended topic structure for the Retail Intelligence Quick Suite setup.

---

## Topic 1: Sales & Revenue Analytics

| Field | Value |
|-------|-------|
| **Name** | Sales & Revenue Analytics |
| **Description** | Product sales performance, revenue trends, profit margins, and order analysis across all retail locations and time periods. |
| **Custom Description** | Use this topic to analyze sales data including revenue, profit, quantity sold, and product performance. Ask questions like "What are the top 5 products by revenue?", "Show monthly sales trends", "Which categories have the highest profit margins?", or "Compare sales across locations." |

**Datasets to include:**
- `product_sales_data`
- `segment_category_performance`
- `segment_channel_performance`

---

## Topic 2: Inventory & Supply Chain

| Field | Value |
|-------|-------|
| **Name** | Inventory & Supply Chain |
| **Description** | Inventory levels, stock management, supplier information, and product catalog across all warehouse locations. |
| **Custom Description** | Use this topic for inventory and supply chain questions. Ask about stock levels, reorder points, supplier details, and product information. Example questions: "Which products are below reorder point?", "Show inventory levels at LOC001", "Who supplies product P000001?", "List products with low stock." |

**Datasets to include:**
- `inventory_master`
- `product_master`
- `supplier_master`
- `site_master`

---

## Topic 3: Marketing Performance

| Field | Value |
|-------|-------|
| **Name** | Marketing Performance |
| **Description** | Marketing campaign effectiveness, ad spend analysis, ROI metrics, and channel performance across all marketing initiatives. |
| **Custom Description** | Use this topic to analyze marketing campaigns and advertising effectiveness. Ask questions like "What's the ROI of our email campaigns?", "Compare ad spend vs revenue by channel", "Which campaigns had the best conversion rate?", or "Show monthly marketing performance trends." |

**Datasets to include:**
- `marketing_performance`
- `campaign_performance`
- `campaign_summary`

---

## Topic 4: Demand Forecasting

| Field | Value |
|-------|-------|
| **Name** | Demand Forecasting |
| **Description** | Demand predictions, forecast accuracy metrics, and planning data for inventory optimization and supply chain planning. |
| **Custom Description** | Use this topic for demand planning and forecast analysis. Ask about predicted demand, forecast accuracy, and planning metrics. Example questions: "What's the forecasted demand for next month?", "Show forecast accuracy by category", "Which products have the highest forecast error?", "Compare actual vs predicted sales." |

**Datasets to include:**
- `demand_forecast`
- `forecast_accuracy_comparison`
- `category_forecast_accuracy`
- `monthly_forecast_accuracy`

---

## Topic 5: Customer Insights

| Field | Value |
|-------|-------|
| **Name** | Customer Insights |
| **Description** | Customer demographics, purchase behavior, feedback sentiment, and customer segmentation analysis. |
| **Custom Description** | Use this topic to understand customers and their feedback. Ask about customer segments, satisfaction scores, and purchase patterns. Example questions: "What's the average customer satisfaction score?", "Show feedback by product category", "Which customer segments buy the most?", "List recent customer complaints." |

**Datasets to include:**
- `customer_master_data`
- `customer_feedback`
- `customer_orders`

---

## Setup Instructions

1. Go to **QuickSight Console** → **Topics**
2. Click **New topic**
3. Enter the **Name** and **Description** from above
4. Add the listed datasets for each topic
5. In **Topic settings**, paste the **Custom Description**
6. Configure field synonyms as needed
7. Save and publish the topic
8. Repeat for all 5 topics
9. In **Quick Suite** → **Knowledge**, add all topics to your chat agent

---

## CSV to Dataset Mapping

| CSV File | QuickSight Dataset Name |
|----------|------------------------|
| `product_sales_data.csv` | sample_product_sales |
| `segment_category_performance.csv` | sample_segment_category_performance |
| `segment_channel_performance.csv` | sample_segment_channel_performance |
| `inventory_master.csv` | (needs to be created) |
| `product_master.csv` | (needs to be created) |
| `supplier_master.csv` | (needs to be created) |
| `site_master.csv` | (needs to be created) |
| `marketing_performance.csv` | sample_marketing_performance |
| `campaign_performance.csv` | (needs to be created) |
| `campaign_summary.csv` | (needs to be created) |
| `demand_forecast.csv` | sample_demand_forecast |
| `customer_master_data.csv` | (needs to be created) |
| `customer_feedback.csv` | (needs to be created) |
| `customer_orders.csv` | (needs to be created) |

Note: Datasets marked "(needs to be created)" are not in the current CloudFormation template and would need to be manually added to QuickSight.
