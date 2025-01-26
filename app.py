import streamlit as st
import pandas as pd

st.title("Join Excel Files for Campaigns")

# File upload fields
st.subheader("Upload the Files")
non_deliverable_file = st.file_uploader("Upload the non-deliverable list (Excel file)", type=["xlsx"])
report_file = st.file_uploader("Upload the report of all contacts (Excel file)", type=["xlsx"])

# Input fields for specifying the email column in each file
if non_deliverable_file and report_file:
    st.subheader("Specify the Columns for Joining")
    non_deliverable_column = st.text_input("Column for Emails in the Non-Deliverable List")
    report_column = st.text_input("Column for Emails in the Report of All Contacts")

    if st.button("Join the Files"):
        try:
            # Load the uploaded files into pandas DataFrames
            non_deliverable_df = pd.read_excel(non_deliverable_file)
            report_df = pd.read_excel(report_file)

            # Perform the join operation
            joined_df = pd.merge(non_deliverable_df, report_df,
                                 left_on=non_deliverable_column,
                                 right_on=report_column,
                                 how='left')

            # Convert the result to Excel format for download
            st.success("Files joined successfully!")
            st.write("Preview of the joined file:")
            st.dataframe(joined_df)

            # Provide download link
            st.subheader("Download the Joined File")
            joined_file = joined_df.to_excel(index=False, engine='openpyxl')
            st.download_button(
                label="Download Joined File",
                data=joined_file,
                file_name="joined_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
