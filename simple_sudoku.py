import streamlit as st
import pandas as pd
import numpy as np

st.title("My Custom Sudoku Solver")

# 1. Inject CSS to make text bold, centered, and larger
st.markdown("""
<style>
    /* Target the dataframe cells to change text formatting */
    div[data-testid="stDataFrame"] div[role="gridcell"] {
        font-weight: bold !important;
        font-size: 20px !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Create the blank 9x9 grid with hidden column names
columns = [str(i) for i in range(9)]
if 'board' not in st.session_state:
    st.session_state.board = pd.DataFrame(np.full((9, 9), ""), columns=columns)

# 3. Add the controls
col1, col2 = st.columns([1, 1])
with col1:
    error_check_on = st.toggle("Enable Error Checking", value=True)
with col2:
    if st.button("Reset Board", type="primary"):
        st.session_state.board = pd.DataFrame(np.full((9, 9), ""), columns=columns)
        st.rerun()

st.write("Enter your puzzle below:")

# 4. Configure columns to be 40 pixels wide (square) and limit input to 1 character
square_config = {
    col: st.column_config.TextColumn(label=" ", width=40, max_chars=1) 
    for col in columns
}

# 5. Display the board
edited_df = st.data_editor(
    st.session_state.board, 
    column_config=square_config,
    use_container_width=False, # We set this to False so our 40px width is respected
    hide_index=True
)

# Save the edits to memory so they don't disappear
st.session_state.board = edited_df

# 6. The Error Checking Logic
if error_check_on:
    grid = edited_df.values.tolist()
    errors = []
    
    # Scan every cell on the board
    for row in range(9):
        for col in range(9):
            val = str(grid[row][col]).strip()
            
            # Skip empty cells
            if not val: 
                continue
                
            # Make sure they only typed a number from 1-9
            if not val.isdigit() or val == '0':
                errors.append(f"Oops! '{val}' in Row {row+1} is not a valid number.")
                continue
            
            # Check for duplicates in the current ROW
            if grid[row].count(val) > 1:
                errors.append(f"Row {row+1} has too many {val}s.")
            
            # Check for duplicates in the current COLUMN
            col_values = [grid[r][col] for r in range(9)]
            if col_values.count(val) > 1:
                errors.append(f"Column {col+1} has too many {val}s.")
                
            # Check for duplicates in the local 3x3 BLOCK
            box_row_start = (row // 3) * 3
            box_col_start = (col // 3) * 3
            box_values = [grid[r][c] for r in range(box_row_start, box_row_start+3) for c in range(box_col_start, box_col_start+3)]
            if box_values.count(val) > 1:
                errors.append(f"The 3x3 block containing Row {row+1}, Col {col+1} has too many {val}s.")
    
    # Remove duplicate error messages and display them to the user
    unique_errors = list(set(errors))
    for error in unique_errors:
        st.error(error)
