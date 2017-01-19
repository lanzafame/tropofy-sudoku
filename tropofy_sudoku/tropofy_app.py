import os
import StringIO
from pulp import *

from sqlalchemy.types import Integer
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship, backref

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.widgets import ExecuteFunction, SimpleGrid
from tropofy.database.tropofy_orm import DataSetMixin


class SudokuRow(DataSetMixin):
    col1 = Column(Integer, nullable=True)
    col2 = Column(Integer, nullable=True)
    col3 = Column(Integer, nullable=True)
    col4 = Column(Integer, nullable=True)
    col5 = Column(Integer, nullable=True)
    col6 = Column(Integer, nullable=True)
    col7 = Column(Integer, nullable=True)
    col8 = Column(Integer, nullable=True)
    col9 = Column(Integer, nullable=True)

    def __init__(self, col1, col2, col3, col4, col5, col6, col7, col8, col9):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.col4 = col4
        self.col5 = col5
        self.col6 = col6
        self.col7 = col7
        self.col8 = col8
        self.col9 = col9


class SudokuAnswerRow(DataSetMixin):
    col1 = Column(Integer, nullable=True)
    col2 = Column(Integer, nullable=True)
    col3 = Column(Integer, nullable=True)
    col4 = Column(Integer, nullable=True)
    col5 = Column(Integer, nullable=True)
    col6 = Column(Integer, nullable=True)
    col7 = Column(Integer, nullable=True)
    col8 = Column(Integer, nullable=True)
    col9 = Column(Integer, nullable=True)

    def __init__(self, col1, col2, col3, col4, col5, col6, col7, col8, col9):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.col4 = col4
        self.col5 = col5
        self.col6 = col6
        self.col7 = col7
        self.col8 = col8
        self.col9 = col9


class ExecuteSolver(ExecuteFunction):

    def get_button_text(self, app_session):
        return "Solve Sudoku Puzzle"

    def execute_function(self, app_session):
        solve_sudoku_puzzle_using_pulp(app_session)


class SudokuApp(AppWithDataSets):

    def get_name(self):
        return 'Sudoku Solver'

    def get_examples(self):
        return {"Demo data set from Gurobi": load_example_data}

    def get_gui(self):
        step_group1 = StepGroup(name='Enter your sudoku puzzle')
        step_group1.add_step(Step(name='Enter your sudoku puzzle', widgets=[SimpleGrid(SudokuRow)]))

        step_group2 = StepGroup(name='Solve')
        step_group2.add_step(Step(name='Solve your sudoku puzzle', widgets=[ExecuteSolver()]))

        step_group3 = StepGroup(name='View the solution')
        step_group3.add_step(Step(name='View the solution', widgets=[SimpleGrid(SudokuAnswerRow)]))

        return [step_group1, step_group2, step_group3]

    def get_icon_url(self):
        return 'https://s3-ap-southeast-2.amazonaws.com/tropofy.com/static/css/img/tropofy_example_app_icons/sudoku.png'

    def get_home_page_content(self):
        return {
            'content_app_name_header': '''
            <div>
            <span style="vertical-align: middle;">Sudoku Solver</span>
            <img src="https://s3-ap-southeast-2.amazonaws.com/tropofy.com/static/css/img/tropofy_example_app_icons/sudoku.png" alt="main logo" style="width:15%">
            </div>''',

            'content_single_column_app_description': '''
            <p>No problem solving related toolkit is complete without a sudoku solver worked example!</p>''',

            'content_row_4_col_1_content': '''
            This app was created using the <a href="http://www.tropofy.com" target="_blank">Tropofy platform</a>.
            '''
        }


def load_example_data(app_session):
    app_session.data_set.add(SudokuRow(None, 2, 8, 4, 7, 6, 3, None, None))
    app_session.data_set.add(SudokuRow(None, None, None, 8, 3, 9, None, 2, None))
    app_session.data_set.add(SudokuRow(7, None, None, 5, 1, 2, None, 8, None))
    app_session.data_set.add(SudokuRow(None, None, 1, 7, 9, None, None, 4, None))
    app_session.data_set.add(SudokuRow(3, None, None, None, None, None, None, None, None))
    app_session.data_set.add(SudokuRow(None, None, 9, None, None, None, 1, None, None))
    app_session.data_set.add(SudokuRow(None, 5, None, None, 8, None, None, None, None))
    app_session.data_set.add(SudokuRow(None, None, 6, 9, 2, None, None, None, 5))
    app_session.data_set.add(SudokuRow(None, None, 2, 6, 4, 5, None, None, 8))


def solve_sudoku_puzzle_using_pulp(app_session):
    """
    The Sudoku Problem Formulation for the PuLP Modeller
    Authors: Antony Phillips, Dr Stuart Mitcehll, PuLP
    See http://pythonhosted.org/PuLP/CaseStudies/a_sudoku_problem.html
    Used with permission
    """
    data_set = app_session.data_set

    # A list of strings from "1" to "9" is created
    Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # The Vals, Rows and Cols sequences all follow this form
    Vals = Sequence
    Rows = Sequence
    Cols = Sequence

    # The boxes list is created, with the row and column index of each square in each box
    Boxes = []
    for i in range(3):
        for j in range(3):
            Boxes += [[(Rows[3 * i + k], Cols[3 * j + l]) for k in range(3) for l in range(3)]]

    # The prob variable is created to contain the problem data
    prob = LpProblem("Sudoku Problem", LpMinimize)

    # The problem variables are created
    choices = LpVariable.dicts("Choice", (Vals, Rows, Cols), 0, 1, LpInteger)

    # The arbitrary objective function is added
    prob += 0, "Arbitrary Objective Function"

    # A constraint ensuring that only one value can be in each square is created
    for r in Rows:
        for c in Cols:
            prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

    # The row, column and box constraints are added for each value
    for v in Vals:
        for r in Rows:
            prob += lpSum([choices[v][r][c] for c in Cols]) == 1, ""
        for c in Cols:
            prob += lpSum([choices[v][r][c] for r in Rows]) == 1, ""
        for b in Boxes:
            prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1, ""

    # The starting numbers are entered as constraints
    starting_grid = []
    for r in data_set.query(SudokuRow).all():
        starting_grid.append([r.col1, r.col2, r.col3, r.col4, r.col5, r.col6, r.col7, r.col8, r.col9])

    for i in range(9):
        for j in range(9):
            if starting_grid[i][j]:
                prob += choices[str(starting_grid[i][j])][str(i + 1)][str(j + 1)] == 1, ""

    prob.solve()

    # The status of the solution is printed to the screen
    app_session.task_manager.send_progress_message("Status: %s" % LpStatus[prob.status])

    # The solution is written to a string
    sudokuout = StringIO.StringIO()
    for r in Rows:
        if r == "1" or r == "4" or r == "7":
            sudokuout.write("+-------+-------+-------+<br>")
        row_sol = []
        for c in Cols:
            for v in Vals:
                if value(choices[v][r][c]) == 1:
                    if c == "1" or c == "4" or c == "7":
                        sudokuout.write("| ")
                    sudokuout.write(v + " ")
                    row_sol.append(v)
                    if c == "9":
                        sudokuout.write("|<br>")
        data_set.add(SudokuAnswerRow(row_sol[0], row_sol[1], row_sol[2], row_sol[3], row_sol[4], row_sol[5], row_sol[6], row_sol[7], row_sol[8]))
    sudokuout.write("+-------+-------+-------+")

    app_session.task_manager.send_progress_message(sudokuout.getvalue())