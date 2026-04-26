import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Custom Sudoku", layout="centered")
st.title("My Custom Sudoku Solver")

# 1. Back to the clean 9x9 board!
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

# 3. The Cell Styling Function (Forces Light Mode & Draws Borders)
def style_sudoku_cells(df):
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    for r in range(9):
        for c in range(9):
            block_r = r // 3
            block_c = c // 3
            
            # Hardcode the backgrounds to defeat Dark Mode entirely
            if (block_r + block_c) % 2 == 0:
                bg_color = '#f0f2f6' # Very light grey
            else:
                bg_color = '#ffffff' # Pure white
                
            # Base style for every cell
            cell_style = f'background-color: {bg_color}; color: #000000; font-weight: bold; '
            
            # Draw thick black borders on the edges of the 3x3 blocks
            if c in [2, 5]:
                cell_style += 'border-right: 3px solid #000000 !important; '
            if r in [2, 5]:
                cell_style += 'border-bottom: 3px solid #000000 !important; '
                
            styles.iat[r, c] = cell_style
            
    return styles

# 4. Configure columns to be square
square_config = {
    col: st.column_config.TextColumn(label=" ", width=40, max_chars=1) 
    for col in columns
}

# Apply our hardcoded styles
styled_board = st.session_state.board.style.apply(style_sudoku_cells, axis=None)

# 5. Display the board
edited_df = st.data_editor(
    styled_board, 
    column_config=square_config,
    use_container_width=False,
    hide_index=True
)

st.session_state.board = edited_df

# 6. The Clean 9x9 Error Checking Logic
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
