import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# Path to the "Report of All Contacts" file
REPORT_FILE_PATH = "C:\\Users\\noga\\PycharmProjects\\pythonProject\\Join non-delivered with CS owner App\\All contacts and accounts-2025-01-30-20-13-40.xlsx"


# Function to load the background image
def set_background(image_file):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{image_file}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        h1, h2, h3, label {{
            color: white !important;
        }}
        .uploadedFile {{
            color: white !important;
            font-size: 14px;
            text-align: left;
        }}
        .stFileUploader div {{
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Function to load and encode the background image
def load_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded


# Load and set the background image
bg_image = load_background("background.png")
set_background(bg_image)

# App Title
st.title("Join Non-Deliverable List with Contact Details")

# File upload field
st.subheader("Upload the Non-Deliverable List (Excel file)")
non_deliverable_file = st.file_uploader("Upload the non-deliverable list", type=["xlsx"], key="file1")
if non_deliverable_file:
    st.markdown(f"<div class='uploadedFile'>{non_deliverable_file.name}</div>", unsafe_allow_html=True)

# Processing the uploaded file
if non_deliverable_file:
    try:
        # Load the files into pandas DataFrames
        non_deliverable_df = pd.read_excel(non_deliverable_file)
        report_df = pd.read_excel(REPORT_FILE_PATH)

        # Perform the join operation
        joined_df = pd.merge(non_deliverable_df, report_df,
                             left_on="Recipient", right_on="Email",
                             how='left')

        # Drop the "Email" column since we already have "Recipient"
        joined_df.drop(columns=['Email'], inplace=True, errors='ignore')

        # Show success message and preview
        st.success("Files joined successfully!")
        st.write("Preview of the joined file:")
        st.dataframe(joined_df)

        # Save the result to an Excel file in memory
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            joined_df.to_excel(writer, index=False)
        buffer.seek(0)

        # Provide download link
        st.subheader("Download the Joined File")
        st.download_button(
            label="Download Joined File",
            data=buffer,
            file_name="joined_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
