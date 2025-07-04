import streamlit as st
import tempfile
import os
from insurance_pipeline.main import run_pipeline
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Insurance Template Filler", layout="centered")

st.title("Insurance GLR Template Filler")
st.markdown("Upload a `.docx` insurance template and photo report `.pdf` files. The output will be a filled PDF report.")

# Upload .docx Template
template_file = st.file_uploader("Upload Insurance Template (.docx)", type=["docx"])

# Upload multiple .pdf Reports
report_files = st.file_uploader("Upload Photo Reports (.pdf)", type=["pdf"], accept_multiple_files=True)

def embed_pdf(pdf_path):
    pdf_viewer(pdf_path)

if st.button("Generate Filled PDF"):
    if template_file and report_files:
        with st.spinner("Processing..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save template
                template_path = os.path.join(temp_dir, "template.docx")
                with open(template_path, "wb") as f:
                    f.write(template_file.read())

                # Save reports
                reports_dir = os.path.join(temp_dir, "reports")
                os.makedirs(reports_dir, exist_ok=True)
                for i, file in enumerate(report_files):
                    file_path = os.path.join(reports_dir, f"report_{i+1}.pdf")
                    with open(file_path, "wb") as f:
                        f.write(file.read())

                # Generate filled PDF
                pdf_path = run_pipeline(folder_path=reports_dir, template_path=template_path, output_path=os.path.join(temp_dir, "filled_output.docx"))

                if pdf_path and os.path.exists(pdf_path):
                    st.success("PDF successfully generated!")

                    # Download Button
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download Filled PDF",
                            data=f,
                            file_name="filled_report.pdf",
                            mime="application/pdf"
                        )

                    st.markdown("### Preview of Filled PDF")
                    embed_pdf(pdf_path)
                else:
                    st.error("Failed to generate PDF.")
    else:
        st.warning("Please upload a template and at least one report PDF.")
