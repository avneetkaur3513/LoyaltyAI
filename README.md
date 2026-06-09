# LoyaltyAI – Vodafone Complaint Rescue Demo

This is a simple Streamlit working demo for the Vodafone "Earn Customer Loyalty" hackathon.

## How to run

1. Install Python 3.10 or above.
2. Open terminal in this folder.
3. Run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Best sample complaint

```text
I've already called twice. Nobody explained these roaming charges. This is ridiculous. I waited on hold and got transferred again. I'm considering switching provider.
```

Click **Analyze Call**, then **Apply Resolution + Send Message**.

## What to say during demo

This is the agent dashboard. A customer complaint transcript comes in live. LoyaltyAI detects frustration, identifies the complaint, checks customer history, calculates churn risk, and generates a rescue card for the agent. The agent does not need to ask the customer to repeat everything. They immediately see what happened, what to say, what action is allowed, and what offer can save the customer.

This is a hackathon prototype. It uses simulated logic, not real Vodafone customer data. In production, it would connect to CRM, call transcript, billing, network, NPS, and churn prediction systems.
