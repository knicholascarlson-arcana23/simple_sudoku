import streamlit as st

st.set_page_config(page_title="Custom Sudoku", layout="centered")
st.title("My Custom Sudoku Solver")

# 1. Initialize the 81 individual cells in Streamlit's memory
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
        # Wipe all 81 variables back to empty strings
        for r in range(9):
            for c in range(9):
                st.session_state[f"cell_{r}_{c}"] = ""
        st.rerun()

st.write("Enter your puzzle below:")

# 3. Build the grid using pure layout math
# We use 11 columns total: 9 for the input boxes, and 2 thin spacer columns to separate the 3x3 blocks
column_widths = [1, 1, 1, 0.3, 1, 1, 1, 0.3, 1, 1, 1]
# These are the column indexes where the actual input boxes go (skipping the spacers at index 3 and 7)
input_positions = [0, 1, 2, 4, 5, 6, 8, 9, 10]

for r in range(9):
    # Add a horizontal line before row 3 and row 6 to separate the 3x3 blocks vertically
    if r == 3 or r == 6:
        st.divider()
        
    cols = st.columns(column_widths)
    
    # Place an input box in the correct column
    for logical_c, layout_pos in enumerate(input_positions):
        with cols[layout_pos]:
            st.text_input(
                label=" ", 
                label_visibility="collapsed", # Hides the text label above the box
                max_chars=1, 
                key=f"cell_{r}_{logical_c}"   # Streamlit automatically binds the input to this memory variable
            )

# 4. Error Checking Logic
if error_check_on:
    # Rebuild the pure 9x9 grid in Python by reading the 81 variables
    logical_grid = [[st.session_state[f"cell_{r}_{c}"] for c in range(9)] for r in range(9)]
    errors = []
    
    for row in range(9):
        for col in range(9):
            val = logical_grid[row][col].strip()
            
            if not val: 
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
