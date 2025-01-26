import streamlit as st
import pandas as pd

# Function to set the background image
# Function to set the background image
# Function to set the background image
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
        h1, h2, h3 {{
            color: white !important;
        }}
        label {{
            color: white !important;
        }}
        .stTextInput > label {{
            color: white !important;
        }}
        .stMarkdown > div {{
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
    import base64
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        print(f"Loading background image from: {image_path}")

    return encoded

# Set the background using the full path
bg_image = load_background("C:/Users/noga/PycharmProjects/pythonProject/Join non-delivered with CS owner App/background.png")
set_background(bg_image)

# App Title
st.title("Join Excel Files for Campaigns")

# File upload fields
st.subheader("Upload the Files")
non_deliverable_file = st.file_uploader("Upload the non-deliverable list (Excel file)", type=["xlsx"], key="file1")
if non_deliverable_file:
    st.markdown(f"<div class='uploadedFile'>{non_deliverable_file.name}</div>", unsafe_allow_html=True)

report_file = st.file_uploader("Upload the report of all contacts (Excel file)", type=["xlsx"], key="file2")
if report_file:
    st.markdown(f"<div class='uploadedFile'>{report_file.name}</div>", unsafe_allow_html=True)

# Input fields for specifying the email column in each file
if non_deliverable_file and report_file:
    st.subheader("Specify the Columns for Joining")
    non_deliverable_column = st.text_input("Column for Emails in the Non-Deliverable List (copy the column header text)")
    report_column = st.text_input("Column for Emails in the Report of All Contacts (copy the column header text)")

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

            # Use BytesIO to save the Excel file to memory
            from io import BytesIO
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

# Footer Section
st.markdown(
    """
    <style>
    .footer {{
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        text-align: left;
        padding: 10px 20px;
        font-size: 14px;
    }}
    a {{
        color: #f1c40f;
        text-decoration: none;
    }}
    </style>
    <div class="footer">
        <p>If you have any questions or need help, contact me at: <a href="mailto:Noga@dotcompliance.com">Noga@dotcompliance.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
