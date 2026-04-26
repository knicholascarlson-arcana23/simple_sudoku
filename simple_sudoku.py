import streamlit as st

st.set_page_config(page_title="Custom Sudoku", layout="centered")
st.title("My Custom Sudoku Solver")

# 1. Initialize the 81 individual cells
if "initialized" not in st.session_state:
    for r in range(9):
        for c in range(9):
            st.session_state[f"cell_{r}_{c}"] = ""
    st.session_state.initialized = True

# 2. Controls
col1, col2 = st.columns([1, 1])
with col1:
    error_check_on = st.toggle("Enable Error Checking", value=True)
with col2:
    if st.button("Reset Board", type="primary"):
        for r in range(9):
            for c in range(9):
                st.session_state[f"cell_{r}_{c}"] = ""
        st.rerun()

st.write("**Instructions:** Type a single digit to place your answer. Type multiple digits (e.g. '145') to leave pencil notes.")

# 3. Build the grid
column_widths = [1, 1, 1, 0.3, 1, 1, 1, 0.3, 1, 1, 1]
input_positions = [0, 1, 2, 4, 5, 6, 8, 9, 10]

for r in range(9):
    if r == 3 or r == 6:
        st.divider()
        
    cols = st.columns(column_widths)
    
    for logical_c, layout_pos in enumerate(input_positions):
        with cols[layout_pos]:
            st.text_input(
                label=" ", 
                label_visibility="collapsed", 
                max_chars=9,  # CHANGED: Allows up to 9 digits for pencil notes
                key=f"cell_{r}_{logical_c}"   
            )

# 4. Error Checking Logic (Updated for Pencil Marks)
if error_check_on:
    logical_grid = [[st.session_state[f"cell_{r}_{c}"] for c in range(9)] for r in range(9)]
    errors = []
    
    for row in range(9):
        for col in range(9):
            # Strip out spaces so if you type "1 4" it reads as "14"
            raw_val = logical_grid[row][col].strip().replace(" ", "")
            
            # THE MAGIC TRICK: If the box is empty OR contains more than 1 character, 
            # treat it as a pencil mark and ignore it for error checking!
            if not raw_val or len(raw_val) > 1: 
                continue
                
            if not raw_val.isdigit() or raw_val == '0':
                errors.append(f"Oops! '{raw_val}' in Row {row+1} is not a valid number.")
                continue
            
            # We must clean the whole row/col/box strings to properly check against the single digit
            clean_row = [logical_grid[row][c].strip().replace(" ", "") for c in range(9)]
            if clean_row.count(raw_val) > 1:
                errors.append(f"Row {row+1} has too many {raw_val}s.")
            
            clean_col = [logical_grid[r][col].strip().replace(" ", "") for r in range(9)]
            if clean_col.count(raw_val) > 1:
                errors.append(f"Column {col+1} has too many {raw_val}s.")
                
            box_row_start = (row // 3) * 3
            box_col_start = (col // 3) * 3
            clean_box = [logical_grid[r][c].strip().replace(" ", "") for r in range(box_row_start, box_row_start+3) for c in range(box_col_start, box_col_start+3)]
            if clean_box.count(raw_val) > 1:
                errors.append(f"The 3x3 block containing Row {row+1}, Col {col+1} has too many {raw_val}s.")
    
    unique_errors = list(set(errors))
    for error in unique_errors:
        st.error(error)
