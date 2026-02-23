Markdown
# KRED | Smart Financial CRM

**KRED** is a high-performance, minimalist CRM designed for rapid data sanitization, revenue recovery, and global itinerary management. Built for speed and precision, it transforms messy spreadsheets into actionable financial insights.



## 🚀 Core Features

* **Alpine UI:** A high-contrast, professional interface designed for 2026 standards.
* **Global Timezone Intelligence:** Automatically detects client local time via phone numbers to optimize outreach timing.
* **Revenue Recovery Engine:** Intelligent sorting that highlights high-value outstanding debts (🔴 HIGH Priority).
* **Live Data Editor:** Sync changes directly within the browser with a sleek, minimalist ledger.
* **One-Click Outreach:** Automated professional email templates for seamless debt collection.

## 🛠 Installation & Setup

To run **KRED** locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/KRED.git](https://github.com/YOUR_USERNAME/KRED.git)
   cd KRED
Install dependencies:

Bash
pip install -r requirements.txt
Launch the Command Center:

Bash
streamlit run kred_app.py
📊 Data Structure
KRED works best with files containing the following headers:

NAME: Client or Guest name.

AMOUNT: Total contract value.

PAID: Amount already collected.

PHONE: International format (e.g., +44, +1) for time zone detection.

🔒 Security & Performance
Zero Persistence: KRED processes data in-session for maximum privacy.

Lightweight: Optimized for Streamlit Cloud deployment.

Developed by Bruno | Powered by the KRED Engine 1.0