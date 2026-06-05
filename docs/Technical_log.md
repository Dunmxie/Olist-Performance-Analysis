# Technical Log

## Environment and Repository Setup
**Date:** June 1, 2026  
**Tools Used:** Python 3.14.3, Git 2.53.0, pip 25.3, Kaggle CLI 2.2.0, PostgreSQL 17.10

### What Was Done
- Scaffolded project directory structure
- Initialized Git with production-grade `.gitignore`
- Created README, SETUP.md, TECHNICAL_LOG.md, DATA_DICTIONARY.md
- Downloaded Olist dataset via Kaggle CLI
- Configured PostgreSQL as the project SQL engine

### Decisions and Rationale

| Decision | Choice | Rationale |
|---|---|---|
| SQL engine | PostgreSQL | Preferred |
| Data download | Kaggle CLI | Reproducible. Any reviewer can re-run with one command. |
| Raw data tracking | Excluded from Git | 9 CSVs ~100MB total. Documented in SETUP.md instead. |
| Docs structure | Separate /docs/ files | README stays clean. Technical detail lives where reviewers expect it. |

---

## Data Cleaning & Validation
**Date:** June 5, 2026  
**Tool:** Python 3.14 · pandas 3.0.3 · numpy 2.4.6  
**Input:** 9 raw CSV files: Data/Raw/  
**Output:** Data/Cleaned/Olist_Master.csv · Data/Cleaned/Olist_Orders_No_Items.csv

---

### What Was Built

Engineered a validated, item-level analytical master table from 9 relational
source tables covering 100k+ Brazilian e-commerce orders across 2016–2018.
Resolved 4 structural integrity issues before export. Every decision
documented with before/after counts and stated rationale.

---

### Cleaning Decisions

| Table | Issue | Resolution | Rows Affected |
|---|---|---|---|
| Orders | 3 timestamp columns stored as object dtype | Converted to datetime64 | 99,441 *no rows dropped* |
| Orders | 160–2,965 nulls across delivery timestamps | Retained *nulls represent real operational states (unapproved, unshipped, undelivered)* | 4,908 nulls preserved |
| Reviews | 87,656 nulls in comment title · 58,247 in comment message | Filled with empty string *nulls are valid non-responses, not missing data* | 99,224 *no rows dropped* |
| Reviews | 551 duplicate review records across 547 orders | Retained most recent review per order by review_answer_timestamp | 551 rows removed |
| Products | 610 rows missing category, name length, description length, photo count simultaneously | Category filled "Unknown" *orphaned records represent real revenue and cannot be dropped without breaking join integrity* | 610 nulls resolved |
| Products | 2 rows missing physical dimensions | Imputed with column median; weight: 700g · length: 25cm · height: 13cm · width: 20cm | 2 nulls resolved |
| Products | Column names misspelled in source | Renamed: product_name_lenght → product_name_length · product_description_lenght → product_description_length | Cosmetic *no rows affected* |
| Geolocation | 981,148 duplicate rows (98.1% of table) | Deduplicated to 19,015 unique zip code prefixes · aggregated to 27 state-level coordinates for regional mapping | 981,148 duplicates removed |
| Products | Portuguese category names | Joined to translation table *32,328 of 32,951 products mapped (98.1%)* · 623 retained as "Unknown" | 623 untranslated |

---

### Join Architecture

Built the master table using **order_items as the spine**; one row per
confirmed order item. This decision was reached after an initial build
using orders as the spine generated 775 phantom rows from orders with
no item records.

Payments aggregated to order level before joining. One order can carry
multiple payment rows (e.g. voucher + credit card split). Joining
un-aggregated payments would inflate revenue totals.

| Join | Type | Cardinality | Rationale |
|---|---|---|---|
| order_items → orders | Left | Many:1 | Orders spine replaced by items spine after row count failure |
| order_items → products | Left | Many:1 | Retains items even if product metadata is incomplete |
| order_items → customers | Left via orders | Many:1 | Customer state drives regional analysis |
| order_items → payments_agg | Left | 1:1 (post-aggregation) | Payments pre-aggregated to prevent revenue inflation |
| order_items → reviews_deduped | Left | 1:1 (post-dedup) | Most recent review retained per order |
| order_items → sellers | Left | Many:1 | Seller state used for supply-side regional cut |

---

### Retained Nulls: Documented and Expected

| Column | Null Count | % | Reason |
|---|---|---|---|
| order_approved_at | 160 | 0.16% | Orders never approved *payment not confirmed* |
| order_delivered_carrier_date | 1,783 | 1.79% | Orders never dispatched to carrier |
| order_delivered_customer_date | 2,965 | 2.98% | Orders never delivered to customer |
| review_score | 942 | 0.84% | Orders with no customer rating submitted |

---

### Validation Results: Master Table

| Check | Expected | Actual | Pass |
|---|---|---|---|
| Row count | 112,650 | 112,650 | ✓ |
| Revenue — price + freight | R$ 15,843,553.24 | R$ 15,843,553.24 | ✓ |
| Unique orders | 98,666 | 98,666 | ✓ |
| Unique customers | 98,666 | 98,666 | ✓ |
| Unique sellers | 3,095 | 3,095 | ✓ |
| States covered | 27 | 27 | ✓ |
| Critical column nulls | 0 | 0 | ✓ |

---

### Preserved Separately

**Olist_Orders_No_Items.csv**: 775 orders excluded from the item-level
master table. These orders entered the system but never progressed to
item fulfilment.

| Status | Count |
|---|---|
| Unavailable | 603 |
| Cancelled | 164 |
| Created | 5 |
| Invoiced | 2 |
| Shipped | 1 |

These records feed order-status and cancellation rate analysis.
They carry no price, product, or seller data and cannot contribute
to revenue or margin calculations.

---

### Limitations

- **No cost of goods data.** The source dataset carries no supplier cost
  or COGS field. Gross margin cannot be calculated from the data directly.
  Freight value (R$ 0.00–R$ 409.68) is used as an operational cost proxy
  where margin analysis is required.

- **Category translation gap.** 623 products (1.9%) could not be mapped
  to an English category. These are retained as "Unknown" and will appear
  as a separate category segment in all category-level analysis. Their
  revenue contribution is tracked but their category attribution is absent.

- **Review coverage.** 942 orders (0.84% of item rows) carry no review score.
  Satisfaction analysis is based on 98,666 rated orders. Unrated orders
  skew slightly toward cancelled and late-delivered status, meaning average
  satisfaction scores likely overstate actual customer sentiment marginally.

- **Date range.** Order data spans September 2016 – September 2018.
  The final month (October 2018) appears in raw timestamps but contains
  only 1 order, likely a data entry artefact. Time-series analysis
  treats August 2018 as the practical end of the reliable date range.