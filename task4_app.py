import streamlit as st
import copy

st.set_page_config(page_title="Sudoku Game", layout="centered")

# ---------------- SOLVER ----------------
def is_valid(board, r, c, num):
    n = len(board)
    box = int(n ** 0.5)

    for i in range(n):
        if board[r][i] == num or board[i][c] == num:
            return False

    start_r, start_c = r - r % box, c - c % box
    for i in range(start_r, start_r + box):
        for j in range(start_c, start_c + box):
            if board[i][j] == num:
                return False
    return True


def solve_sudoku(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                for num in range(1, n + 1):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True


# ---------------- PUZZLES ----------------
def get_puzzle(size):
    if size == 4:
        return [
            [1, 0, 0, 4],
            [0, 0, 3, 0],
            [0, 3, 0, 0],
            [2, 0, 0, 1],
        ]
    return [
        [3,0,6,5,0,8,4,0,0],
        [5,2,0,0,0,0,0,0,0],
        [0,8,7,0,0,0,0,3,1],
        [0,0,3,0,1,0,0,8,0],
        [9,0,0,8,6,3,0,0,5],
        [0,5,0,0,9,0,6,0,0],
        [1,3,0,0,0,0,2,5,0],
        [0,0,0,0,0,0,0,7,4],
        [0,0,5,2,0,6,3,0,0],
    ]


# ---------------- GRID (SAFE HTML) ----------------
def draw_grid(board):
    n = len(board)
    box = int(n ** 0.5)

    html = "<table style='border-collapse:collapse;margin:auto;'>"

    for i in range(n):
        html += "<tr>"
        for j in range(n):
            val = board[i][j]
            display = "" if val == 0 else str(val)

            bg = ""
            if "solution" in st.session_state:
                if val != 0 and val != st.session_state.solution[i][j]:
                    bg = "background-color:#ffcccc;"

            top = "3px solid black" if i % box == 0 else "1px solid black"
            left = "3px solid black" if j % box == 0 else "1px solid black"

            html += (
                "<td style='"
                "width:40px;height:40px;"
                "text-align:center;"
                "font-size:20px;"
                f"border-top:{top};"
                f"border-left:{left};"
                "border-right:1px solid black;"
                "border-bottom:1px solid black;"
                f"{bg}"
                "'>"
                + display +
                "</td>"
            )

        html += "</tr>"

    html += "</table>"
    return html


# ---------------- SESSION ----------------
if "size" not in st.session_state:
    st.session_state.size = 9

if "board" not in st.session_state:
    st.session_state.board = get_puzzle(9)

if "original" not in st.session_state:
    st.session_state.original = copy.deepcopy(st.session_state.board)

if "show_solution" not in st.session_state:
    st.session_state.show_solution = False


# ---------------- UI ----------------
st.title("🧠 Sudoku Game")

size = st.selectbox("Select Size", [4, 9])

if size != st.session_state.size:
    st.session_state.size = size
    st.session_state.board = get_puzzle(size)
    st.session_state.original = copy.deepcopy(st.session_state.board)
    st.session_state.show_solution = False
    st.session_state.pop("solution", None)
    st.rerun()


# ---------------- GRID ----------------
st.markdown(draw_grid(st.session_state.board), unsafe_allow_html=True)


# ---------------- INPUT ----------------
st.subheader("Enter Value")

c1, c2, c3 = st.columns(3)
row = c1.number_input("Row", 1, size)
col = c2.number_input("Col", 1, size)
val = c3.number_input("Value", 1, size)


# ---------------- BUTTONS ----------------
b1, b2, b3, b4 = st.columns(4)

# Add
if b1.button("Add Value"):
    r, c = row - 1, col - 1
    if st.session_state.original[r][c] == 0:
        st.session_state.board[r][c] = val
    else:
        st.warning("Fixed cell ❌")
    st.rerun()

# Solve
if b2.button("Solve"):
    temp = copy.deepcopy(st.session_state.board)
    if solve_sudoku(temp):
        st.session_state.solution = temp
        st.session_state.show_solution = True
    else:
        st.error("No solution ❌")
    st.rerun()

# Clear (one cell only)
if b3.button("Clear"):
    r, c = row - 1, col - 1
    if st.session_state.original[r][c] == 0:
        st.session_state.board[r][c] = 0
    st.session_state.show_solution = False
    st.session_state.pop("solution", None)
    st.rerun()

# Reset (full)
if b4.button("Reset"):
    st.session_state.board = copy.deepcopy(st.session_state.original)
    st.session_state.show_solution = False
    st.session_state.pop("solution", None)
    st.rerun()


# ---------------- SHOW SOLUTION ----------------
if st.session_state.show_solution:
    st.subheader("Solution")
    st.markdown(draw_grid(st.session_state.solution), unsafe_allow_html=True)