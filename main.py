import streamlit as st
import pandas as pd
import mysql.connector
from PIL import Image

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vflute123!",
    database="fashion_db"
)

def authenticate(username, password):
    return username == "user123" and password == "p123"
# Function to upload designs
def upload_designs(designer_id, design_name, design_description, design_image):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Penguin_123",
        database="fashion_db"
    )

    # Check if the designer ID exists
    query_check_designer = f"SELECT * FROM Designer WHERE dsgnr_id = '{designer_id}';"
    designer_exists = execute_query(query_check_designer)

    if not designer_exists:
        st.error("Designer ID does not exist.")
        return

    # Upload the design information
    query_upload_design = f"INSERT INTO Design (d_name, des_desc, dsgnr_id) VALUES ('{design_name}', '{design_description}', '{designer_id}');"
    execute_query(query_upload_design)

    # Fetch the design ID of the uploaded design
    query_get_design_id = f"SELECT des_id FROM Design WHERE d_name = '{design_name}' AND dsgnr_id = '{designer_id}';"
    design_id = execute_query(query_get_design_id)[0]['des_id']

    # Upload the design image path to the DesignImage table
    image_path = f"designs/{design_name}_{design_id}.png"  # Adjust the path as needed
    query_upload_image = f"INSERT INTO DesignImage (des_id, image_path) VALUES ('{design_id}', '{image_path}');"
    execute_query(query_upload_image)

    # Save the uploaded image to the specified path
    design_image.save(image_path)

    # Display success message
    st.success(f"Design '{design_name}' uploaded successfully with Design ID: {design_id}")

def generate_supply_kit(designer_id, quantity):
    try:
        cursor = conn.cursor()
        cursor.callproc('GenerateSupplyKit', [designer_id, quantity])
        conn.commit()
        st.success(f"Supply Kit generated successfully for {quantity} units of designs from {designer_id}.")
    except Exception as e:
        conn.rollback()
        st.error(f"Error generating supply kit: {str(e)}")
    finally:
        cursor.close()
# Your existing code for other pages...
def manufacturer_page():
    st.header("Manufacturer Page")

    # Buttons for Manufacturer Page
    action_options = ["View Designs", "View Materials", "View Bulk Orders"]
    selected_action = st.sidebar.selectbox("Select Action", action_options)

    if selected_action == "View Designs":
        st.subheader("View Designs")
        query_designs = "SELECT * FROM ManufacturerDesignView;"
        data_designs = execute_query(query_designs)
        st.dataframe(pd.DataFrame(data_designs))

    elif selected_action == "View Materials":
        st.subheader("View Materials")
        query_materials = "SELECT * FROM SupplierMaterialView;"
        data_materials = execute_query(query_materials)
        st.dataframe(pd.DataFrame(data_materials))

    elif selected_action == "View Bulk Orders":
        st.subheader("View Bulk Orders")
        query_bulk_orders = "SELECT des_id, bulk_order_number FROM Design WHERE bulk_order_number IS NOT NULL;"
        data_bulk_orders = execute_query(query_bulk_orders)
        st.dataframe(pd.DataFrame(data_bulk_orders))


# Designer Page
def designer_page():
    st.header("Designer Page")

    # Buttons for Designer Page
    # Include buttons for different actions related to Designer

    # Upload Designs Section
    st.subheader("Upload Designs")
    designer_id_upload = st.text_input("Designer ID for Upload")
    design_name = st.text_input("Design Name")
    design_description = st.text_input("Design Description")
    design_image = st.file_uploader("Upload Design Image", type=["jpg", "jpeg", "png"])

    if st.button("Upload Design"):
        if designer_id_upload and design_name and design_image:
            upload_designs(designer_id_upload, design_name, design_description, design_image)
        else:
            st.warning("Please fill in all required fields.")


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

# Designer Page
def designer_page():
    st.header("Designer Page")

    # Buttons for Designer Page
    # Include buttons for different actions related to Designer

# ... (previous code)

# Function to add a new material using the stored procedure
def add_material(material, material_type, supplier_id, material_price):
    query = f"CALL AddMaterial('{material}', '{material_type}', '{supplier_id}', {material_price});"
    execute_query(query)

# Function to update material price using the stored procedure
def update_material(material_id, new_price):
    query = f"CALL UpdateMaterial('{material_id}', {new_price});"
    execute_query(query)

# Function to delete material using the stored procedure
def delete_material(material_id):
    query = f"CALL DeleteMaterial('{material_id}');"
    execute_query(query)

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
            add_material(material_name, material_type, supplier_id, material_price)
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
            delete_material(material_id_to_delete)
            st.success(f"Material with ID {material_id_to_delete} deleted successfully!")

            # Invalidate the cache to trigger re-execution of the "View Material" section
            st.cache(hash_funcs={pd.DataFrame: lambda _: None}).clear()

    # Add more buttons for other actions (Update Material, Bulk Order, etc.)

# ... (remaining code)

# Function to set bulk order number for a design
def set_bulk_order_number(design_id, bulk_order_number):
    query = f"CALL SetBulkOrderNumber('{design_id}', {bulk_order_number});"
    execute_query(query)

# Designer Page
def designer_page():
    st.header("Designer Page")

    # Buttons for Designer Page
    action_options = ["Upload Designs", "Generate Supply Kits", "Bulk Order", "Set Bulk Order Number"]
    selected_action = st.sidebar.selectbox("Select Action", action_options)

    if selected_action == "Set Bulk Order Number":
        st.subheader("Set Bulk Order Number")
        design_id_bulk = st.text_input("Design ID")
        bulk_order_number = st.number_input("Bulk Order Number")

        if st.button("Set Bulk Order Number"):
            set_bulk_order_number(design_id_bulk, bulk_order_number)
            st.success(f"Bulk Order Number set for Design ID {design_id_bulk}")

    if selected_action == "Upload Designs":
        st.subheader("Upload Designs")
        designer_id_upload = st.text_input("Designer ID")  # Assuming you have a way to obtain the designer ID
        design_name = st.text_input("Design Name")
        design_description = st.text_area("Design Description")
        design_image = st.file_uploader("Upload Design Image", type=["jpg", "jpeg", "png"])

        if st.button("Upload Design"):
            if design_image is not None:
                upload_designs(designer_id_upload, design_name, design_description, design_image)
            else:
                st.warning("Please upload a valid design image.")
        elif selected_action == "Generate Supply Kits":
            st.subheader("Generate Supply Kit")
            designer_id = st.text_input("Designer ID")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            if st.button("Generate Supply Kit"):
                generate_supply_kit(designer_id, quantity)


    # Add more buttons for other actions (Upload Designs, Generate Supply Kits, Bulk Order, etc.)

# ... (remaining code)

# Function to check if the user is logged in
def is_user_authenticated():
    return st.session_state.get('logged_in', False)
# Streamlit app
def main():
    # Check if the user is logged in
    if not is_user_authenticated():
        # Display login page
        st.title("FashionEase - Fashion Supply and Resource Management")
        login()
    else:
        # If logged in, proceed to the main app
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

# Function to display login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            # Set session variable to indicate that the user is logged in
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()