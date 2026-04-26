import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Custom Sudoku", layout="centered")
st.title("My Custom Sudoku Solver")

# 1. Define the 11 columns (9 real, 2 gaps)
col_names = ["c0", "c1", "c2", "gap1", "c3", "c4", "c5", "gap2", "c6", "c7", "c8"]

# 2. Build the 11x11 visual grid
if 'board' not in st.session_state:
    initial_grid = np.full((11, 11), "")
    
    # Fill the gap rows (Row 3 and Row 7) with dashes to look like borders
    for i in range(11):
        initial_grid[3, i] = "—"
        initial_grid[7, i] = "—"
        
    st.session_state.board = pd.DataFrame(initial_grid, columns=col_names)

# 3. Controls
col1, col2 = st.columns([1, 1])
with col1:
    error_check_on = st.toggle("Enable Error Checking", value=True)
with col2:
    if st.button("Reset Board", type="primary"):
        # Reset but keep the dashed borders
        reset_grid = np.full((11, 11), "")
        for i in range(11):
            reset_grid[3, i] = "—"
            reset_grid[7, i] = "—"
        st.session_state.board = pd.DataFrame(reset_grid, columns=col_names)
        st.rerun()

st.write("Enter your puzzle below:")

# 4. Configure the columns (Make gaps narrow and un-clickable)
col_config = {}
for c in col_names:
    if "gap" in c:
        # The gap columns are locked and thin
        col_config[c] = st.column_config.TextColumn(label=" ", width=15, disabled=True)
    else:
        # The playable columns are square
        col_config[c] = st.column_config.TextColumn(label=" ", width=40, max_chars=1)

# 5. Display the board
edited_df = st.data_editor(
    st.session_state.board, 
    column_config=col_config,
    use_container_width=False,
    hide_index=True
)

st.session_state.board = edited_df

# 6. Error Checking Logic
if error_check_on:
    ui_grid = edited_df.values.tolist()
    
    # --- MODEL-VIEW SEPARATION ---
    # Extract the pure 9x9 data out of the 11x11 visual board
    logical_grid = []
    for r in range(11):
        if r in [3, 7]: continue # Skip the gap rows
        
        clean_row = []
        for c in range(11):
            if c in [3, 7]: continue # Skip the gap columns
            clean_row.append(ui_grid[r][c])
            
        logical_grid.append(clean_row)
        
    # --- STANDARD 9x9 MATH ---
    # Now we run the exact same math on our clean logical_grid!
    errors = []
    for row in range(9):
        for col in range(9):
            val = str(logical_grid[row][col]).strip()
            
            if not val or val == '—': 
                continue
                
            if not val.isdigit() or val == '0':
                errors.append(f"Oops! '{val}' in Row {row+1} is not a valid number.")
                continue
            
            if logical_grid[row].count(val) > 1:
                errors.append(f"Row {row+1} has too many {val}s.")
            
            col_values = [logical_grid[r][col] for r in range(9)]
            if col_values.count(val) > 1:
                errors.append(f"Column {col+1} has too many {val}s.")
                
            box_row_start = (row // 3) * 3
            box_col_start = (col // 3) * 3
            box_values = [logical_grid[r][c] for r in range(box_row_start, box_row_start+3) for c in range(box_col_start, box_col_start+3)]
            if box_values.count(val) > 1:
                errors.append(f"The 3x3 block containing Row {row+1}, Col {col+1} has too many {val}s.")
    
    unique_errors = list(set(errors))
    for error in unique_errors:
        st.error(error)
