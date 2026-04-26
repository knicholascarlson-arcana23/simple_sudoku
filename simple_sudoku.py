import streamlit as st

st.set_page_config(page_title="Custom Sudoku", layout="centered")
st.title("My Custom Sudoku Solver")

# 1. Initialize variables
if "initialized" not in st.session_state:
    for r in range(9):
        for c in range(9):
            st.session_state[f"cell_{r}_{c}"] = ""
    st.session_state.initialized = True
    st.session_state.locked = False
    st.session_state.confirming = False
    st.session_state.original_puzzle = {}

# --- NEW FEATURE: GENERATE 81-DIGIT STRING ---
current_puzzle_string = ""
for r in range(9):
    for c in range(9):
        val = str(st.session_state.get(f"cell_{r}_{c}", "")).strip()
        if len(val) == 1 and val.isdigit():
            current_puzzle_string += val
        else:
            current_puzzle_string += "0"

# 2. Top Controls & Save/Load Menu
col1, col2 = st.columns([1, 1])
with col1:
    error_check_on = st.toggle("Enable Error Checking", value=True)
with col2:
    if st.button("Reset Entire Board", type="primary"):
        for r in range(9):
            for c in range(9):
                st.session_state[f"cell_{r}_{c}"] = ""
        st.session_state.locked = False
        st.session_state.confirming = False
        st.session_state.original_puzzle = {}
        st.rerun()

# --- NEW FEATURE: SAVE / LOAD UI ---
with st.expander("💾 Save / Load Puzzle Options"):
    st.write("**Export Current Board:**")
    st.code(current_puzzle_string)
    
    st.download_button(
        label="Download as .txt file",
        data=current_puzzle_string,
        file_name="my_sudoku_puzzle.txt",
        mime="text/plain"
    )
    
    st.divider()
    
    st.write("**Import a Board:**")
    import_string = st.text_input("Paste an 81-digit string here:")
    if st.button("Load String"):
        clean_string = import_string.strip()
        if len(clean_string) == 81 and clean_string.isdigit():
            st.session_state.locked = False
            st.session_state.original_puzzle = {}
            idx = 0
            for r in range(9):
                for c in range(9):
                    char = clean_string[idx]
                    if char != '0':
                        st.session_state[f"cell_{r}_{c}"] = char
                    else:
                        st.session_state[f"cell_{r}_{c}"] = ""
                    idx += 1
            st.rerun()
        else:
            st.error("String must be exactly 81 numbers long!")

st.divider()

# 3. The Lock Mechanism
if not st.session_state.locked:
    if not st.session_state.confirming:
        if st.button("Lock Puzzle Numbers"):
            st.session_state.confirming = True
            st.rerun()
    else:
        st.warning("Are you sure these numbers are correct?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, Lock It In"):
                st.session_state.locked = True
                st.session_state.confirming = False
                for r in range(9):
                    for c in range(9):
                        val = str(st.session_state.get(f"cell_{r}_{c}", "")).strip()
                        if val and val.isdigit() and len(val) == 1:
                            st.session_state.original_puzzle[f"{r}_{c}"] = True
                st.rerun()
        with c2:
            if st.button("No, Let Me Edit"):
                st.session_state.confirming = False
                st.rerun()
else:
    st.success("Puzzle Locked! The original numbers are now grayed out and safe.")
    if st.button("Unlock Puzzle (Will keep your progress)"):
        st.session_state.locked = False
        st.session_state.original_puzzle = {}
        st.rerun()

st.write("**Instructions:** Type a single digit for your answer. Type multiple digits for pencil notes.")

# 4. Build the grid
column_widths = [1, 1, 1, 0.3, 1, 1, 1, 0.3, 1, 1, 1]
input_positions = [0, 1, 2, 4, 5, 6, 8, 9, 10]

for r in range(9):
    if r == 3 or r == 6:
        st.divider()
        
    cols = st.columns(column_widths)
    
    for logical_c, layout_pos in enumerate(input_positions):
        with cols[layout_pos]:
            is_disabled = False
            if st.session_state.locked and f"{r}_{logical_c}" in st.session_state.original_puzzle:
                is_disabled = True
                
            st.text_input(
                label=" ", 
                label_visibility="collapsed", 
                max_chars=9, 
                disabled=is_disabled, 
                key=f"cell_{r}_{logical_c}"   
            )

# 5. Error Checking Logic
if error_check_on:
    logical_grid = [[str(st.session_state.get(f"cell_{r}_{c}", "")) for c in range(9)] for r in range(9)]
    errors = []
    
    for row in range(9):
        for col in range(9):
            raw_val = logical_grid[row][col].strip().replace(" ", "")
            
            if not raw_val or len(raw_val) > 1: 
                continue
                
            if not raw_val.isdigit() or raw_val == '0':
                errors.append(f"Oops! '{raw_val}' in Row {row+1} is not a valid number.")
                continue
            
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
