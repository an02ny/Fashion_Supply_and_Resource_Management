import mysql.connector
import streamlit as st

#establish connection to mysql server

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Penguin_123",
    database="fashion_supply_resource_management"


)

#cursor object

mycursor=mydb.cursor()
print("Connection Established")

#create streamlit webapp

def main():
    st.title("CRUD Operations with MySQL")

    #options for CRUD Operations

    option=st.sidebar.selectbox("Select which CRUD Operation",("Create","Update","Read","Delete"))

    #template for selected CRUD Operations
    if option=="Create":
        st.subheader("Create Record")

        name=st.text_input("Enter Name: ")
        design_id=st.text_input("Enter Design_id: ")
        contact_info=st.text_input("Enter contact_info: ")
        designer_id=st.text_input("Enter Designer_id: ")
        
        if st.button("Create"):
            sql="insert into designers(design_id,designer_id,contact_info,name) values(%s,%s,%s,%s)"
            val=(design_id,designer_id,contact_info,name)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Created Successfully")

    elif option=="Update":
        st.subheader("Update Record")
    
    elif option=="Read":
        st.subheader("Read Record")
    
    elif option=="Delete":
        st.subheader("Delete Record")





if __name__=="__main__":
    main()
