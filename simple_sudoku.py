import streamlit as st
import pandas as pd
import numpy as np

st.title("My Custom Sudoku Solver")

# 1. Create a blank 9x9 grid in memory if it doesn't exist yet
if 'board' not in st.session_state:
    # Using empty strings so the grid looks clean
    st.session_state.board = pd.DataFrame(np.full((9, 9), ""))

# 2. Add the toggle switch for error checking
error_check_on = st.toggle("Enable Error Checking", value=True)

# 3. Display the interactive grid
st.write("Enter your puzzle below:")
edited_df = st.data_editor(
    st.session_state.board, 
    use_container_width=True,
    hide_index=True # Hides the row numbers to make it look like Sudoku
)

# 4. Check for errors (We will put the validation math here)
if error_check_on:
    # Logic to scan rows, columns, and 3x3 blocks goes here
    pass

# 5. Add a reset button
if st.button("Reset Board"):
    st.session_state.board = pd.DataFrame(np.full((9, 9), ""))
    st.rerun()
