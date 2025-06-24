
import streamlit as st
import pandas as pd

# --- Load Data ---
materials_df = pd.read_excel("Materials.xlsx")
employees_df = pd.read_excel("Employees.xlsx")

# --- Labour Cost Calculations ---
employees_df["Base Cost"] = employees_df["Hours"] * employees_df["RATE/hour"]
total_base_cost = employees_df["Base Cost"].sum()
total_overhead = total_base_cost * (0.31 + 0.45 + 0.20)
total_labour_cost = total_base_cost + total_overhead

# --- Material Cost Calculations ---
materials_df["Quantity"] = materials_df["MATERIALS"].apply(lambda x: st.number_input(f"{x} quantity:", min_value=0, value=1))
materials_df["Total"] = materials_df["Quantity"] * materials_df["UNIT COST"]
total_material_cost = materials_df["Total"].sum()

# --- Streamlit UI ---
st.title("🧾 Body Bag Quoting Tool")

# --- Material Section ---
st.header("📦 Materials")
st.dataframe(materials_df[["MATERIALS", "UNIT COST", "Quantity", "Total"]])
st.subheader(f"🧮 Total Material Cost: ${total_material_cost:,.2f}")

# --- Labour Section ---
st.header("👷 Labour")
st.dataframe(employees_df[["Employee", "Hours", "RATE/hour", "Base Cost"]])
st.text(f"🧾 Total Base Cost: ${total_base_cost:,.2f}")
st.text(f"➕ Overheads (96%): ${total_overhead:,.2f}")
st.subheader(f"✅ Final Total Labour Cost: ${total_labour_cost:,.2f}")

# --- Final Quote ---
total_quote = total_material_cost + total_labour_cost
st.header("💰 Final Quotation")
st.success(f"Estimated Total Cost: ${total_quote:,.2f}")
