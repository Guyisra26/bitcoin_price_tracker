# Bitcoin Price Tracker

---

## Requirements

- Python 3.11+
- Coinbase API: [https://api.coinbase.com/v2/prices/BTC-USD/spot](https://api.coinbase.com/v2/prices/BTC-USD/spot)

Install required dependencies:

```bash
pip install -r requirements.txt
```

Dependencies used:

- `pydantic[email]` – For schema validation and config parsing
- `uplink` – For API client abstraction
- `matplotlib` – For graph generation
- `requests` – For HTTP requests (if needed directly)
- Python standard libraries: `json`, `logging`, `datetime`, `time`, `smtplib`, `email`, etc.

---

## Configuration

All settings are defined in `config.json`:

```json
{
  "core_config": {
    "base_url": "https://api.coinbase.com/v2/",
    "base": "BTC",
    "currency": "USD",
    "run_minutes": 60,
    "interval_seconds": 60
  },
  "email_config": {
    "sender_email": "youremail@gmail.com",
    "app_password": "your_app_password",
    "recipient_email": "recipient@example.com",
    "subject": "Bitcoin Price Report",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 465
  }
}
```

Notes:
- Use a Gmail **App Password**, not your normal email password
- You can adjust duration and interval for testing purposes

---

## Outputs

- `btc_usd.json` — Stores all collected prices with timestamps
- `btc_usd_graph.png` — Graph of BTC price vs time
- Email — Sent to the configured address, with:
  - The highest BTC-USD value
  - The attached graph image

---

## Running the Script

Before running the script, make sure to install the required packages:

```bash
pip install -r requirements.txt
```

Then, run the script:

```bash
python main.py
```

Make sure to fill in your email credentials in `config.json` beforehand.

---