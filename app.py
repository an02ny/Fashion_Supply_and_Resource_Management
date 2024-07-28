import streamlit as st
import pandas as pd
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vflute123!", #WRITE YOUR DB CONFIG PASSWORD HERE
    database="fashion_db"
)

# Function to execute SQL queries and fetch data
def execute_query(query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Supplier Page
# Supplier Page
def supplier_page():
    st.header("Supplier Page")

    # Buttons for Supplier Page
    action_options = ["View Material", "Add Material", "Update Material", "Delete Material"]
    selected_action = st.sidebar.selectbox("Select Action", action_options)

    if selected_action == "View Material":
        st.subheader("View Material")
        query = "SELECT * FROM SupplierMaterialView;"
        data = execute_query(query)
        st.dataframe(pd.DataFrame(data))

    elif selected_action == "Add Material":
        st.subheader("Add Material")
        material_name = st.text_input("Material Name")
        material_type = st.text_input("Material Type")
        material_price = st.number_input("Material Price")
        supplier_id = st.text_input("Supplier ID")

        if st.button("Add Material"):
            query = f"INSERT INTO Material (material, type, s_id, mat_price) VALUES ('{material_name}', '{material_type}', '{supplier_id}', {material_price});"
            execute_query(query)
            st.success("Material added successfully!")

            # Fetch and display updated material data
            query_view = "SELECT * FROM SupplierMaterialView;"
            updated_data = execute_query(query_view)
            st.subheader("Updated Material Data")
            st.dataframe(pd.DataFrame(updated_data))
    elif selected_action == "Delete Material":
        st.subheader("Delete Material")
        material_id_to_delete = st.text_input("Material ID to Delete")

        if st.button("Delete Material"):
            query_delete = f"DELETE FROM Material WHERE mat_id = {material_id_to_delete};"
            execute_query(query_delete)
            st.success(f"Material with ID {material_id_to_delete} deleted successfully!")

            # Invalidate the cache to trigger re-execution of the "View Material" section
            st.cache(hash_funcs={pd.DataFrame: lambda _: None}).clear()

    # Add more buttons for other actions (Update Material, Delete Material, etc.)

    # Add more buttons for other actions (Update Material, Delete Material, etc.)

# Manufacturer Page
def manufacturer_page():
    st.header("Manufacturer Page")

    # Buttons for Manufacturer Page
    # Include buttons for different actions related to Manufacturer

# Designer Page
def designer_page():
    st.header("Designer Page")

    # Buttons for Designer Page
    # Include buttons for different actions related to Designer

# Streamlit app
def main():
    st.title("FashionEase - Fashion Supply and Resource Management")

    # Sidebar navigation
    page_options = ["Supplier", "Manufacturer", "Designer"]
    selected_page = st.sidebar.radio("Select Page", page_options)

    if selected_page == "Supplier":
        supplier_page()
    elif selected_page == "Manufacturer":
        manufacturer_page()
    elif selected_page == "Designer":
        designer_page()

if __name__ == "__main__":
    main()
