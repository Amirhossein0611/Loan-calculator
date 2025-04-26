
import streamlit as st
import numpy as np

st.set_page_config(page_title="محاسبه‌گر وام با هزینه اشتراک", layout="centered")

st.title("محاسبه‌گر وام با لحاظ هزینه اشتراک")

# ورودی‌ها
loan_amount = st.number_input("مبلغ اسمی وام (تومان)", min_value=1_000_000, step=1_000_000, value=20_000_000)
months = st.number_input("مدت بازپرداخت (ماه)", min_value=1, step=1, value=6)
interest_rate = st.slider("نرخ سود سالانه بانک (%)", min_value=10.0, max_value=40.0, value=23.0)
subscription_fee = st.number_input("مبلغ هزینه اشتراک (تومان)", min_value=0, step=100_000, value=1_200_000)

# محاسبه اقساط طبق نرخ سود بانکی
monthly_rate = interest_rate / 12 / 100
monthly_payment = np.pmt(monthly_rate, months, -loan_amount)
total_payment = monthly_payment * months
total_interest = total_payment - loan_amount

# مبلغ واقعی دریافتی پس از کسر هزینه اشتراک
real_received = loan_amount - subscription_fee

# محاسبه نرخ مؤثر واقعی (بر مبنای مبلغ واقعی دریافتی)
cash_flows = [real_received] + [-monthly_payment] * months
try:
    irr_monthly = np.irr(cash_flows)
    irr_annual = irr_monthly * 12 * 100
except:
    irr_annual = "محاسبه‌پذیر نیست"

# خروجی‌ها
st.markdown("### 🔍 نتایج:")
st.write(f"💸 مبلغ قسط ماهانه: {monthly_payment:,.0f} تومان")
st.write(f"📈 مجموع سود طی دوره: {total_interest:,.0f} تومان")
st.write(f"💳 کل مبلغ پرداختی طی دوره: {total_payment:,.0f} تومان")
st.write(f"📥 مبلغ واقعی دریافتی (بعد از کسر هزینه اشتراک): {real_received:,.0f} تومان")
st.write(f"📊 نرخ مؤثر واقعی سالانه (با لحاظ هزینه اشتراک): {irr_annual if isinstance(irr_annual,str) else round(irr_annual, 2)}٪")
