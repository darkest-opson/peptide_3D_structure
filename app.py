import streamlit as st
import pandas as pd
import requests
import py3Dmol
import io


import streamlit as st
import py3Dmol

def show_pdb(pdb_string):
    view = py3Dmol.view(width=600, height=400)
    view.addModel(pdb_string, 'pdb')
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.setBackgroundColor('white')
    view.zoomTo()
    st.components.v1.html(view._make_html(), height=400)


st.set_page_config(page_title="Peptide Tools", layout="wide")
st.title("🧬 3D structure prediction and visualisation")

st.markdown("Use the tools below to analyze peptide sequences for predicted 3D structure.")

st.header("🧫 3D Visualisation")
try:
        # Example usage with a PDB file
    uploaded_file = st.file_uploader("Upload a PDB file", type=['pdb'])

    if uploaded_file:
        pdb_data = uploaded_file.read().decode("utf-8")
        show_pdb(pdb_data)
except Exception as e:
    st.error(f"Error in fetching or rendering structure: {e}")


# Tool 3: 3D Protein Structure Visualization
st.header("🧫 3D Protein Structure Prediction")
structure_input = st.text_input("Enter peptide sequence for 3D structure:", key="structure_input")

if structure_input:
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            'https://api.esmatlas.com/foldSequence/v1/pdb/', 
            headers=headers, 
            data=structure_input,
            verify=False  # Disable SSL for demo/testing purposes
        )
        pdb_string = response.content.decode('utf-8')
         # Create downloadable StringIO file for the PDB
        pdb_file = io.BytesIO(pdb_string.encode("UTF-8"))
        st.download_button(
            label="📥 Download PDB File",
            data=pdb_file,
            file_name="predicted_structure.pdb",
            mime="chemical/x-pdb"
        )
        view = py3Dmol.view(width=700, height=400)
        view.addModel(pdb_string, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.setBackgroundColor('black')
        view.zoomTo()
        st.components.v1.html(view._make_html(), height=400)
       
    except Exception as e:
        st.error(f"Error in fetching or rendering structure: {e}")


