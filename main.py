import matplotlib.pyplot as plt


class Sudoku:

    def __init__(self, A):
        self.S = A
        options = {" ": 0, ".": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}
        sudoku = []
        temp = []

        if isinstance(A, str):
            for i in range(len(A)):
                temp.append(options[A[i]])
                if (i + 1) % 9 == 0:
                    sudoku.append(temp)
                    temp = []
                self.S = sudoku
        else:
            self.S = A

    def print(self):
        print(self.S)

    def draw(self, title='', show_rc_nums=False, show_valid_vals=False):

        # Draw lines
        fig, self.ax = plt.subplots(figsize=(8, 8))
        for i in range(0, 10, 3):
            self.ax.plot([i, i], [0, 9], linewidth=2, color='k')
            self.ax.plot([0, 9], [i, i], linewidth=2, color='k')
        for i in range(1, 9):
            self.ax.plot([i, i], [0, 9], linewidth=1, color='k')
            self.ax.plot([0, 9], [i, i], linewidth=1, color='k')

        # Print row and column numbers if desired
        if show_rc_nums:
            for i in range(9):
                self.ax.text((-.5), (i + .5), str(i), size=12, color='r',
                             ha="center", va="center")
                self.ax.text((i + .5), (-.5), str(i), size=12, color='r',
                             ha="center", va="center")

        # Print known values
        for i in range(9):
            for j in range(9):
                if self.S[i][j] != 0:
                    self.ax.text((j + .5), (i + .5), str(self.S[i][j]), size=18,
                                 ha="center", va="center")

        # Print valid values using small green numbers, if desired
        if show_valid_vals and hasattr(self, 'V'):
            for i in range(9):
                for j in range(9):
                    if self.S[i][j] == 0:
                        for n in self.V[(i, j)]:
                            n1 = n - 1
                            self.ax.text((j + .5 + (n1 % 3 - 1) * .25), (i + .5 + (n1 // 3 - 1) * .25), str(n), size=10,
                                         color='g', ha="center", va="center")

        self.ax.axis('off')
        self.ax.set_title(title, y=-.05, size=18)
        self.ax.set_aspect(1.0)
        self.ax.invert_yaxis()
        plt.show()

    def find_neighbors(self):
        # Fill out dictionary N such that N[(r,c)], where (r,c) are the coordinates of a cell, contains the set of cells that
        # are in the same row, column or 3-by-3 region as cell (r,c)
        self.N = {}
        test = []
        test2 = []
        test3 = []
        columnas = []
        hileras = []
        sector = []

        # To get columns and later on add them to N
        for j in range(9):
            for i in range(9):
                if self.S[i][j] != 0: test.append(self.S[i][j])
            columnas.append(test)
            test = []

        # To get rows and add it to N
        for i in range(9):
            for j in range(9):
                if self.S[i][j] != 0: test2.append(self.S[i][j])
            hileras.append(test2)
            test2 = []
        # To get the sector (3 by 3)
        for x in range(3):
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        if self.S[i + 3 * x][j + 3 * y] != 0: test3.append(self.S[i + 3 * x][j + 3 * y])
                sector.append(test3)
                test3 = []
        for i in range(9):
            for j in range(9):
                self.N[(i, j)] = set(columnas[j] + hileras[i] + sector[3 * (i // 3) + (j // 3)])

    def init_valid(self):
        # Fill out dictionary V such that V[(r,c)], where (r,c) are the coordinates of a cell, contains the set of integers that can be
        # written in cell (r,c) without breaking any of the rules
        # If a number has already been written in cell (r,c), then V[(r,c)] should contain the empty set
        self.V = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}

        # COPIED OTHER METHOD BECAUSE IT WASNT READING SELF.N IN PART 2 FOR SOME REASON
        # TODO: FIX THAT

        self.IamnAgry = {}
        test = []
        test2 = []
        test3 = []
        columnas = []
        hileras = []
        sector = []

        # To get columns and later on add them to N
        for j in range(9):
            for i in range(9):
                if self.S[i][j] != 0: test.append(self.S[i][j])
            columnas.append(test)
            test = []

        # To get rows and add it to N
        for i in range(9):
            for j in range(9):
                if self.S[i][j] != 0: test2.append(self.S[i][j])
            hileras.append(test2)
            test2 = []
        # To get the sector (3 by 3)
        for x in range(3):
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        if self.S[i + 3 * x][j + 3 * y] != 0: test3.append(self.S[i + 3 * x][j + 3 * y])
                sector.append(test3)
                test3 = []
        for i in range(9):
            for j in range(9):
                self.IamnAgry[(i, j)] = set(columnas[j] + hileras[i] + sector[3 * (i // 3) + (j // 3)])

        # Actual method

        if self.weirdCases(): print("Llamen A dios")
        for i in range(9):
            for j in range(9):
                if self.S[i][j] == 0:
                    self.V[(i, j)] = self.V[(i, j)] - self.IamnAgry[(i, j)]
                else:
                    self.V[(i, j)] = {}
        return self.V

    def weirdCases(self):
        for i in range(9):
            for j in range(9):
                if self.S[i][j] == 0 and len(self.V[(i, j)]) == 0: return True
        return False

    def isNumberCorrect(self, num, pos):
        # Check row
        for i in range(9):
            if self.S[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if self.S[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.S[i][j] == num and (i, j) != pos:
                    return False

        return True

    # def solvetest(self):

    # if self.areThereMissing():
    # print("HERE---------------------------------------------------------------------------")
    # self.solve()
    # while self.areThereStill1s():
    # for i in range(9):
    # for j in range(9):
    # if len(self.V[(i,j)]) == 1:
    # self.S[i][j] = self.V[(i,j)].pop()
    # self.V[(i,j)] = {}
    # self.init_valid()
    # if len(self.V[(i,j)]) == 0 and self.S[i][j] == 0:
    # for x in range (1,10):
    # if self.isNumberCorrect(x,(i,j)):self.S[i][j] = i
    # self.X = []
    # for i in range (9):
    # for j in range(9):
    # self.X = self.S[i][j]

    # print(self.X)

    # return -1
    def emptyPosibleSpaces(self):
        for i in range(len(self.S)):
            for j in range(len(self.S[0])):
                if self.S[i][j] == 0: return (i, j)

        return None

    def solve(self):
        self.init_valid()
        known = set()
        find = self.emptyPosibleSpaces()
        if not find:
            return 1
        else:
            row, col = find

        for i in self.V[(row, col)]:
            if self.valid(self.S, i, (row, col)):
                self.S[row][col] = i
                if self.solve() == 1: return 1
                self.S[row][col] = 0
            self.init_valid()

        return self.checkV()
        return -1

    def checkV(self):
        for i in range(9):
            for j in range(9):
                if len(self.V[(i, j)]) == 1: return 0
        return -1

    def valid(self, tablero, num, pos):
        for i in range(9):
            for j in range(9):
                if tablero[i][j] not in self.V[(i, j)]: return False
        return True

    def valid(self, tablero, num, pos):
        # Check row
        for i in range(9):
            if tablero[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if tablero[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if tablero[i][j] == num and (i, j) != pos:
                    return False

        return True

    def to_string(self):
        # Returns a string of length 81 represeting the board
        return ''.join(str(item) for innerlist in self.S for item in innerlist)

B = [[0, 2, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 6, 0, 0], [8, 0, 3, 4, 0, 0, 0, 1, 7],
    [0, 0, 7, 2, 0, 4, 0, 0, 1], [4, 3, 0, 0, 0, 0, 0, 5, 8], [6, 0, 0, 7, 0, 8, 3, 0, 0],
    [7, 4, 0, 0, 0, 6, 5, 0, 2], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 4, 0]]
S = Sudoku(B)
S.print()
S.draw()
#Example
s = '.2.....8.......6..8.34...17..72.4..143.....586..7.83..74...65.2..5.......1.....4.'
S = Sudoku(s)
S.find_neighbors()
S.init_valid()
S.draw(show_rc_nums=True, show_valid_vals=True)
print(S.V[(0,0)])
print(S.V[(0,1)])
print(S.V[(3,6)])
