# Environment & Project Setup Guide

This guide outlines the exact steps required to initialize the local development environment and data pipeline architecture for the Olist Performance Analysis project.

---

## 1. System Requirements & Core Dependencies
Ensure your local machine has the following baseline technologies installed before proceeding:
* **Operating System:** Windows 11 (x86-64)
* **Python Engine:** Version 3.14.3
* **Database Engine:** PostgreSQL 17.10 (via pgAdmin 4)
* **Version Control:** Git 2.53.0

Verify your core CLI tools are active:

```bash
python --version
git --version
psql --version
```

---

## 2. Repository Initialization & Directory Scaffolding

### Step 1: Clone the Repository
Clone the repository from GitHub and navigate to the root directory:

```bash
git clone <your-repository-url>
cd olist-performance-analysis
```

### Step 2: Automated Directory Creation
Instead of creating folders manually, you could run the automation script included in `docs/setup.py`. This script uses Python's `os` module to instantly build the standardized directory tree and injects hidden `.gitkeep` files to preserve empty directory tracking within Git.

Run this command from your root:

```bash
python setup.py
```
---

## 3. Environment Dependency Configuration
To prevent library fragmentation and ensure 100% computational reproducibility, install the exact footprint recorded in `requirements.txt`.

### Step 1: Fix Local Script Path Execution (Windows Only)

If your terminal fails to recognize global pip execution commands, manually append the Python core scripts directory to your system environment variables path:

```text
C:\Users\USER\AppData\Local\Programs\Python\pythoncore-3.14-64\Scripts
```

### Step 2: Install Pinned Packages
Execute the bulk manager installation command:

```bash
pip install -r requirements.txt
```
---

## 4. Secure Data Acquisition Pipeline (Kaggle API)
To protect underlying credentials, this project explicitly rejects storing unencrypted, plain-text local `kaggle.json` files in the working directory. Instead, authentication tokens are injected directly into active terminal memory buffers.


### Step 1: Inject Credentials into Active Terminal Memory
Identify your active VS Code terminal profile and run the corresponding initialization strings:

For PowerShell:

```PowerShell
$env:KAGGLE_USERNAME="your_kaggle_username"
$env:KAGGLE_KEY="your_actual_api_key_hash"
```

For Git Bash:

```Bash
export KAGGLE_USERNAME="your_kaggle_username"
export KAGGLE_KEY="your_actual_api_key_hash"
```

### Step 2: Trigger the Dataset Pull
With credentials stored securely in your temporary terminal session memory, execute the automated extraction script to route the raw compressed zip files directly into your ignored data warehouse folder:

```Bash
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw
```

*(Note: Windows 11 natively supports tar -xf to unzip files directly from the command line without installing third-party tools).*

### Step 3: Verify Raw Data Payload
Confirm that all 9 target relational files are present inside `data/raw/`:

- `olist_orders_dataset.csv`

- `olist_order_items_dataset.csv`

- `olist_order_payments_dataset.csv`

- `olist_order_reviews_dataset.csv`

- `olist_customers_dataset.csv`

- `olist_products_dataset.csv`

- `olist_sellers_dataset.csv`

- `olist_geolocation_dataset.csv`

- `product_category_name_translation.csv`

--- 

## 5. Database Warehousing Target
Local data relational transformations are processed inside a dedicated PostgreSQL server instance.

```bash
# Create project database via CLI
psql -U postgres -c "CREATE DATABASE olist_performance;"
```

- Server: localhost

- Port: 5432

- Target Database Name: olist_performance

- Interface Tooling: pgAdmin 4 / SQLAlchemy Engine Core
---