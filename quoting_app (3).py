
import streamlit as st
import pandas as pd
import math
import os

# --- Configuration ---
MATERIALS_DIR = "materials"
LABOUR_DIR = "labour"
UNITS_PER_PALLET = 50
COST_PER_PALLET = 30

# --- Product Selection ---
st.title("🧾 Product Quoting Tool")

product_files = [f.split('_')[0] for f in os.listdir(MATERIALS_DIR) if f.endswith("_materials.xlsx")]
if not product_files:
    st.error("No product materials found. Upload files in 'materials/' directory.")
    st.stop()

product_code = st.selectbox("Select a product", sorted(product_files))

# --- Load Files ---
materials_file = os.path.join(MATERIALS_DIR, f"{product_code}_materials.xlsx")
labour_file = os.path.join(LABOUR_DIR, f"{product_code}_employees.xlsx")

try:
    materials_df = pd.read_excel(materials_file)
    employees_df = pd.read_excel(labour_file)
except FileNotFoundError:
    st.error(f"Missing file for product {product_code}.")
    st.stop()

# --- User Inputs ---
st.sidebar.header("📥 Input Settings")
quantity_ordered = st.sidebar.number_input("Quantity Ordered", min_value=1, value=100)
output_per_employee_per_day = st.sidebar.number_input("Units per Employee per Day", min_value=1, value=20)
margin_rate = st.sidebar.slider("Desired Profit Margin (%)", 0, 100, 20)

wage_on_cost_pct = st.sidebar.slider("Wage on-Cost (%)", 0, 100, 31)
factory_oh_pct = st.sidebar.slider("Factory Overhead (%)", 0, 100, 45)
corp_oh_pct = st.sidebar.slider("Corporate Overhead (%)", 0, 100, 20)

min_freight_cost = st.sidebar.number_input("Minimum Freight Cost ($)", min_value=0.0, value=100.0)

# --- Labour Cost Calculation ---
employees_df["Base Cost"] = employees_df["Hours"] * employees_df["RATE/hour"]
base_labour_total = employees_df["Base Cost"].sum()

num_employees = len(employees_df)
team_daily_output = output_per_employee_per_day * num_employees
days_required = quantity_ordered / team_daily_output
overhead_multiplier = 1 + (wage_on_cost_pct + factory_oh_pct + corp_oh_pct) / 100
total_labour_cost = base_labour_total * days_required * overhead_multiplier

# --- Material Cost Calculation ---
# Assumes materials_df has columns: 'UNIT COST' and 'QUANTITY' (total quantity for the order)
materials_df["Total"] = materials_df["UNIT COST"] * materials_df["USAGE PER UNIT"] * team_daily_output
total_material_cost = materials_df["Total"].sum()

# --- Freight Calculation ---
num_pallets = math.ceil(quantity_ordered / UNITS_PER_PALLET)
freight_cost = max(num_pallets * COST_PER_PALLET, min_freight_cost)

# --- Other Costs ---
packaging_cost = 0.75 * quantity_ordered
equipment_cost = 0.50 * quantity_ordered
consumables_cost = 0.30 * quantity_ordered
contingency_cost = 0.20 * quantity_ordered
storage_cost = 0.10 * quantity_ordered

# --- Total Calculation ---
raw_total = (
    total_labour_cost + total_material_cost + packaging_cost +
    equipment_cost + consumables_cost + contingency_cost +
    storage_cost + freight_cost
)
final_quote = raw_total * (1 + margin_rate / 100)
price_per_item = final_quote / team_daily_output                       ####33333333333

# --- Display Output ---
st.header(f"📦 Product: {product_code}")
st.subheader("🧮 Cost Breakdown")

st.markdown(f"**Total Labour Cost:** ${total_labour_cost:,.2f}")
st.markdown(f"**Total Material Cost:** ${total_material_cost:,.2f}")
st.markdown(f"**Packaging:** ${packaging_cost:,.2f}")
st.markdown(f"**Equipment Use:** ${equipment_cost:,.2f}")
st.markdown(f"**Consumables:** ${consumables_cost:,.2f}")
st.markdown(f"**Contingency:** ${contingency_cost:,.2f}")
st.markdown(f"**Storage:** ${storage_cost:,.2f}")
st.markdown(f"**Freight ({num_pallets} pallet(s)):** ${freight_cost:,.2f}")
st.markdown("---")
st.markdown(f"**Raw Total (before margin):** ${raw_total:,.2f}")
st.success(f"💰 Final Quoted Price (with {margin_rate}% margin): ${final_quote:,.2f}")
st.info(f"📦 Price per Item: ${price_per_item:,.2f}")

st.write("👷 Base daily labour cost:", base_labour_total)
st.write("👥 Team daily output:", team_daily_output)
st.write("📅 Days required:", days_required)
st.write("⚙️ Overhead multiplier:", overhead_multiplier)
st.write("💰 Total Labour Cost:", total_labour_cost)

