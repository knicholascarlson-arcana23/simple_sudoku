import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Custom Sudoku", layout="centered")
st.title("My Custom Sudoku Solver")

# 1. Initialize the blank 9x9 board in memory
columns = [str(i) for i in range(9)]
if 'board' not in st.session_state:
    st.session_state.board = pd.DataFrame(np.full((9, 9), ""), columns=columns)

# 2. Controls
col1, col2 = st.columns([1, 1])
with col1:
    error_check_on = st.toggle("Enable Error Checking", value=True)
with col2:
    if st.button("Reset Board", type="primary"):
        st.session_state.board = pd.DataFrame(np.full((9, 9), ""), columns=columns)
        st.rerun()

st.write("Enter your puzzle below:")

# 3. The Styling Function for the 3x3 Checkerboard Pattern
def style_sudoku_grid(df):
    # Create an empty dataframe to hold our CSS styles
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    for r in range(9):
        for c in range(9):
            # Calculate which 3x3 block we are currently in
            block_r = r // 3
            block_c = c // 3
            
            # Checkerboard logic: alternate background colors based on the block
            if (block_r + block_c) % 2 == 0:
                bg = 'background-color: #e0e4e8;' # Light grey-blue shade
            else:
                bg = 'background-color: #ffffff;' # Pure white
            
            # Apply the background and force the text to be bold and black
            styles.iat[r, c] = f'{bg} color: #000000; font-weight: bold;'
    return styles

# 4. Configure the columns to be square
square_config = {
    col: st.column_config.TextColumn(label=" ", width=40, max_chars=1) 
    for col in columns
}

# Apply the styling function to our current board state
styled_board = st.session_state.board.style.apply(style_sudoku_grid, axis=None)

# 5. Display the board (passing in the styled board)
edited_df = st.data_editor(
    styled_board, 
    column_config=square_config,
    use_container_width=False,
    hide_index=True
)

# Save edits back to memory
st.session_state.board = edited_df

# 6. Error Checking Logic
if error_check_on:
    grid = edited_df.values.tolist()
    errors = []
    
    for row in range(9):
        for col in range(9):
            val = str(grid[row][col]).strip()
            
            if not val: 
                continue
                
            if not val.isdigit() or val == '0':
                errors.append(f"Oops! '{val}' in Row {row+1} is not a valid number.")
                continue
            
            if grid[row].count(val) > 1:
                errors.append(f"Row {row+1} has too many {val}s.")
            
            col_values = [grid[r][col] for r in range(9)]
            if col_values.count(val) > 1:
                errors.append(f"Column {col+1} has too many {val}s.")
                
            box_row_start = (row // 3) * 3
            box_col_start = (col // 3) * 3
            box_values = [grid[r][c] for r in range(box_row_start, box_row_start+3) for c in range(box_col_start, box_col_start+3)]
            if box_values.count(val) > 1:
                errors.append(f"The 3x3 block containing Row {row+1}, Col {col+1} has too many {val}s.")
    
    unique_errors = list(set(errors))
    for error in unique_errors:
        st.error(error)
