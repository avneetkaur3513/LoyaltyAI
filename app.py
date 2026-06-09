import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="LoyaltyAI – Vodafone Complaint Rescue Demo",
    page_icon="📞",
    layout="wide",
)

NEGATIVE_WORDS = [
    "angry", "ridiculous", "frustrated", "annoyed", "terrible", "bad", "awful",
    "leaving", "switching", "cancel", "complaint", "twice", "again", "charged",
    "overcharged", "confusing", "ignored", "unresolved", "waited", "transfer"
]

ISSUE_KEYWORDS = {
    "Unexpected bill charge": ["bill", "charge", "charged", "overcharged", "fees", "fee", "roaming", "invoice"],
    "Network issue": ["network", "signal", "coverage", "internet", "data", "slow", "disconnect"],
    "Repeated complaint": ["again", "twice", "third", "repeat", "unresolved", "ignored", "complaint"],
    "Cancellation risk": ["leaving", "switching", "cancel", "competitor", "comparison"]
}

def detect_issue(text):
    t = text.lower()
    scores = {issue: sum(1 for w in words if w in t) for issue, words in ISSUE_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General complaint"

def sentiment_score(text):
    t = text.lower()
    hits = sum(1 for w in NEGATIVE_WORDS if w in t)
    exclamations = text.count("!")
    return min(100, 35 + hits * 10 + exclamations * 3)

def churn_risk(text, previous_contacts, tenure_years, nps):
    s = sentiment_score(text)
    risk = s + previous_contacts * 10
    lowered = text.lower()
    if "switch" in lowered or "leaving" in lowered or "cancel" in lowered:
        risk += 20
    if nps <= 6:
        risk += 12
    if tenure_years >= 3:
        risk += 5
    risk = max(0, min(99, risk))
    if risk >= 75:
        return "HIGH 🔴", risk
    if risk >= 50:
        return "MEDIUM 🟠", risk
    return "LOW 🟢", risk

def emotion_label(score):
    if score >= 80:
        return "Frustrated → Angry (escalating)"
    if score >= 60:
        return "Frustrated and disappointed"
    if score >= 45:
        return "Concerned / dissatisfied"
    return "Neutral"

def make_recommendation(issue, risk_num, arpu, tenure):
    if "bill" in issue.lower() or "charge" in issue.lower():
        resolution = "Waive the disputed £22 charge after eligibility check"
        offer = "20GB free data for 3 months"
    elif "network" in issue.lower():
        resolution = "Run network diagnostic and apply service credit if fault is confirmed"
        offer = "Free unlimited data weekend pass"
    elif "cancellation" in issue.lower():
        resolution = "Escalate to retention specialist and review plan fit"
        offer = "Personalised loyalty plan review + retention benefit"
    else:
        resolution = "Resolve issue in-call and send written confirmation"
        offer = "Goodwill loyalty add-on based on eligibility"

    if risk_num >= 85 or arpu >= 45 or tenure >= 5:
        escalation = "Escalate if customer rejects first resolution or mentions switching again"
    else:
        escalation = "Agent can resolve within standard goodwill authority"
    return resolution, offer, escalation

def follow_up_message(name, resolution, offer):
    first = name.split()[0]
    return (
        f"Hi {first}, we're really sorry about the experience today. "
        f"We've reviewed your issue and actioned this now: {resolution}. "
        f"As a thank you for staying with Vodafone, we're also adding: {offer}. "
        f"You matter to us. — Vodafone"
    )

st.markdown("""
<style>
    .block-container {padding-top: 1.2rem;}
    .hero {
        background: linear-gradient(90deg, #e60000 0%, #b00000 100%);
        padding: 26px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
    }
    .hero h1 {margin-bottom: 0px; font-size: 42px;}
    .hero p {font-size: 18px; margin-top: 8px;}
    .metric-card {
        border: 1px solid #eeeeee;
        border-radius: 16px;
        padding: 18px;
        background: #fafafa;
        box-shadow: 0px 1px 6px rgba(0,0,0,0.05);
    }
    .rescue-card {
        border: 2px solid #e60000;
        border-radius: 18px;
        padding: 20px;
        background: #fff8f8;
    }
    .small-label {
        color: #555;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
    }
    .big-red {
        color: #e60000;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📞 LoyaltyAI</h1>
    <p>Real-time AI complaint rescue demo for Vodafone — turn a painful customer moment into a loyalty moment.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Hackathon prototype: simulated AI logic for demo purposes. No customer data is stored.")

st.sidebar.header("Customer Profile")
customer_name = st.sidebar.text_input("Customer name", "Sarah M.")
tenure_years = st.sidebar.slider("Customer tenure (years)", 0, 10, 6)
arpu = st.sidebar.slider("Monthly ARPU (£)", 10, 100, 48)
previous_contacts = st.sidebar.slider("Previous contacts for same issue", 0, 5, 2)
nps = st.sidebar.slider("Last NPS score", 0, 10, 7)

st.sidebar.header("Demo Controls")
demo_case = st.sidebar.selectbox(
    "Load sample scenario",
    ["Roaming charge complaint", "Network issue", "Cancellation risk", "Blank / custom"]
)

samples = {
    "Roaming charge complaint": "I've already called twice. Nobody explained these roaming charges. This is ridiculous. I waited on hold and got transferred again. I'm considering switching provider.",
    "Network issue": "My internet has been dropping for days and I keep getting told to restart my phone. I rely on this for work and I am really frustrated.",
    "Cancellation risk": "I want to cancel. I have been a customer for years but nobody seems to care. I can get a better deal elsewhere.",
    "Blank / custom": ""
}

left, right = st.columns([1.05, 1])

with left:
    st.subheader("1) Live complaint input")
    complaint = st.text_area(
        "Paste or type the customer complaint / live transcript",
        value=samples[demo_case],
        height=180
    )
    analyze = st.button("🔍 Analyze Call", type="primary", use_container_width=True)

    st.markdown("#### Example customer journey")
    st.markdown(
        f"""
        - **Customer:** {customer_name}
        - **Tenure:** {tenure_years} years
        - **Monthly value:** £{arpu}
        - **Previous contacts:** {previous_contacts}
        - **Last NPS:** {nps}/10
        """
    )

if analyze or complaint.strip():
    issue = detect_issue(complaint)
    sent = sentiment_score(complaint)
    risk_label, risk_num = churn_risk(complaint, previous_contacts, tenure_years, nps)
    emotion = emotion_label(sent)
    resolution, offer, escalation = make_recommendation(issue, risk_num, arpu, tenure_years)
    msg = follow_up_message(customer_name, resolution, offer)

    with right:
        st.subheader("2) Loyalty Rescue Card")
        st.markdown(f"""
        <div class="rescue-card">
            <div class="small-label">Active Call</div>
            <h3>{customer_name} | Churn Risk: <span class="big-red">{risk_label}</span></h3>
            <p><b>Complaint detected:</b> {issue}</p>
            <p><b>Sentiment:</b> {emotion}</p>
            <p><b>Risk score:</b> {risk_num}/100</p>
            <p><b>Customer profile:</b> {tenure_years} years with Vodafone | ARPU £{arpu}/month | NPS {nps}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### AI Suggested Action")
        st.success(resolution)
        st.info(f"Retention offer: {offer}")
        st.warning(f"Escalation rule: {escalation}")

        st.markdown("### Suggested Agent Opening")
        st.write(
            f"“I can see you've contacted us {previous_contacts} time(s) about this already. "
            f"I'm sorry this has taken too long. I have the full context now, and I'm going to help resolve it on this call.”"
        )

        if st.button("✅ Apply Resolution + Send Message", use_container_width=True):
            st.balloons()
            st.markdown("### Customer Message Sent")
            st.markdown(f"""
            <div class="metric-card">
                📱 <b>Vodafone Message — {datetime.now().strftime('%H:%M')}</b><br><br>
                {msg}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("### Outcome")
            st.success("Customer retained. Churn risk moved from HIGH to LOW. Follow-up pulse scheduled in 7 days.")
else:
    with right:
        st.subheader("2) Loyalty Rescue Card")
        st.info("Enter a complaint and click **Analyze Call** to generate the rescue card.")

st.divider()

st.subheader("3) How the prototype maps to the real solution")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown("### 01 Detect")
    st.write("Sentiment AI flags frustration in real time.")
with c2:
    st.markdown("### 02 Understand")
    st.write("NLP identifies complaint category, history, and churn risk.")
with c3:
    st.markdown("### 03 Generate")
    st.write("LLM drafts empathetic opening, fix, and offer.")
with c4:
    st.markdown("### 04 Act")
    st.write("Agent applies resolution with one click.")
with c5:
    st.markdown("### 05 Retain")
    st.write("Customer receives a personalised follow-up.")

st.caption("Demo built for Vodafone Earn Customer Loyalty hackathon.")
