# Data Dictionary & Dataset Notes

This document provides a comprehensive overview of the raw Olist Brazilian E-Commerce dataset schema, relational keys, volume tracking, and baseline data quality issues identified prior to ingestion.

---

## 1. Dataset Metadata
* **Data Source:** Olist Brazilian E-Commerce Public Dataset
* **Access URL:** [Dataset Link](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
* **Licensing:** CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike)
* **Dataset Volume:** 9 distinct relational tables (CSV format)

---

## 2. Core Relational Schema Map

| Filename | Approx. Rows | Primary / Foreign Key Fields |
| :--- | :--- | :--- |
| `olist_orders_dataset.csv` | 99,441 | `order_id`, `customer_id` |
| `olist_order_items_dataset.csv` | 112,650 | `order_id`, `product_id`, `seller_id` |
| `olist_order_payments_dataset.csv` | 103,886 | `order_id` |
| `olist_order_reviews_dataset.csv` | 99,224 | `order_id` |
| `olist_customers_dataset.csv` | 99,441 | `customer_id` |
| `olist_products_dataset.csv` | 32,951 | `product_id` |
| `olist_sellers_dataset.csv` | 3,095 | `seller_id` |
| `olist_geolocation_dataset.csv` | 1,000,163 | `geolocation_zip_code_prefix` |
| `product_category_name_translation.csv` | 71 | `product_category_name` |

---

## 3. Cleaned Tables

### Olist_Master.csv
**Location:** Data/Cleaned/Olist_Master.csv  
**Rows:** 112,650 · **Columns:** 31 · **Size:** 47.4 MB  
**Grain:** One row per confirmed order item  
**Source tables joined:** order_items · orders · products · customers · payments · reviews · sellers

| Column | Type | Source Table | Description |
|---|---|---|---|
| order_id | string | orders / order_items | Unique order identifier |
| order_item_id | int | order_items | Item sequence within an order |
| customer_id | string | orders | Links to customer record |
| customer_unique_id | string | customers | Deduplicated customer identifier across multiple orders |
| order_status | string | orders | Final order state: delivered · shipped · cancelled · unavailable · others |
| order_purchase_timestamp | datetime | orders | Timestamp customer placed the order |
| order_approved_at | datetime | orders | Timestamp payment was confirmed; 160 nulls (unapproved orders) |
| order_delivered_carrier_date | datetime | orders | Timestamp handed to carrier; 1,783 nulls |
| order_delivered_customer_date | datetime | orders | Timestamp delivered to customer; 2,965 nulls |
| order_estimated_delivery_date | datetime | orders | Estimated delivery date at time of purchase |
| product_id | string | order_items | Links to product record |
| seller_id | string | order_items | Links to seller record |
| shipping_limit_date | datetime | order_items | Deadline for seller to dispatch item |
| price | float | order_items | Item sale price in BRL |
| freight_value | float | order_items | Freight cost allocated to item in BRL |
| product_category_name | string | products | Original Portuguese category name |
| category_english | string | products + translation | English category name; 623 products retained as "Unknown" |
| product_weight_g | float | products | Product weight in grams; 2 values imputed with median (700g) |
| product_length_cm | float | products | Product length in cm; 2 values imputed with median (25cm) |
| product_height_cm | float | products | Product height in cm; 2 values imputed with median (13cm) |
| product_width_cm | float | products | Product width in cm; 2 values imputed with median (20cm) |
| city | string | customers | Customer city |
| state | string | customers | Customer state (2-letter BR code) |
| customer_zip_code_prefix | string | customers | Customer zip code prefix |
| total_payment_value | float | payments (aggregated) | Total payment per order; sum across all payment methods |
| payment_installments | int | payments (aggregated) | Maximum instalment count selected for the order |
| payment_type | string | payments (aggregated) | Primary payment method |
| review_score | float | reviews (deduplicated) | Customer rating 1–5; 942 nulls (unrated orders) |
| review_comment_message | string | reviews (deduplicated) | Customer written review; empty string where no comment submitted |
| seller_state | string | sellers | Seller's registered state |
| seller_city | string | sellers | Seller's registered city |

---

### Olist_Orders_No_Items.csv
**Location:** Data/Cleaned/Olist_Orders_No_Items.csv  
**Rows:** 775 · **Columns:** 8 · **Size:** 0.1 MB  
**Grain:** One row per order with no confirmed item record  
**Purpose:** Cancellation rate and order-status analysis only

| Column | Type | Description |
|---|---|---|
| order_id | string | Unique order identifier |
| customer_id | string | Links to customer record |
| order_status | string | unavailable (603) · cancelled (164) · created (5) · invoiced (2) · shipped (1) |
| order_purchase_timestamp | datetime | Timestamp order was placed |
| order_approved_at | datetime | Null for most; approval never reached |
| order_delivered_carrier_date | datetime | Null for all; no dispatch occurred |
| order_delivered_customer_date | datetime | Null for all; no delivery occurred |
| order_estimated_delivery_date | datetime | Estimated delivery date at time of order creation |

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| No COGS data | Gross margin cannot be calculated | Freight value used as operational cost proxy |
| 623 uncategorised products | 1.9% of product base has no category attribution | Retained as "Unknown" revenue tracked, category excluded from segment analysis |
| 942 unrated orders | Satisfaction scores based on 98.8% of item rows | Noted in all satisfaction analysis unrated orders skew toward cancelled/late status |
| Date range ends Sept 2018 | Oct 2018 contains 1 order likely artefact | Time-series analysis treats Aug 2018 as practical end of reliable data |
| No supplier cost fields | Supply-side margin analysis not possible | Out of scope flagged in final memo limitations section |