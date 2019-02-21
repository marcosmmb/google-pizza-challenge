import math

class Slice:
    def __init__(self, first_cell, last_cell):
        self.first_cell = first_cell
        self.last_cell = last_cell

    def update(self, x1, y1, x2, y2):
        self.first_cell = (x1, y1)
        self.last_cell = (x2, y2)

    @property
    def size(self):
        x = self.last_cell[0] - self.first_cell[0] + 1
        y = self.last_cell[1] - self.first_cell[1] + 1
        return x, y

    def __repr__(self):
        return "<Slice (x={}, y={}) -> (x={}, y={})>".format(self.first_cell[0], self.first_cell[1], self.last_cell[0], self.last_cell[1])

class Groupmap:
    def __init__(self, R, C):
        self.slices = dict()
        self.matrix = [[0 for x in range(C)] for y in range(R)]

    def delete_slice(self, value):
        # resets given slice
        if value in self.slices.keys():
            old_slice = self.slices[value]
            for x in range(old_slice.first_cell[0], old_slice.last_cell[0]+1):
                for y in range(old_slice.first_cell[1], old_slice.last_cell[1]+1):
                    try:
                        self.matrix[x][y] = 0
                    except:
                        pass
    
    def update(self, x1, y1, x2, y2, value):
        # update groupmap cells with a given slice value

        self.delete_slice(value)

        new_slice = Slice((x1, y1), (x2, y2))
        self.slices[value] = new_slice
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                try:
                    self.matrix[x][y] = value
                except:
                    pass

    def __repr__(self):
        string = str()
        for l in self.matrix:
            aux = [str(i) for i in l]
            string += " ".join(aux) + "\n"
        return string

class Pizza:
    def __init__(self, file_name = "b_small.in"):

        self.current_slice_value = 1
        self.major_slice_value=1

        self.old_row = 0
        self.old_col = 0

        self.current_row = 0
        self.current_col = 0

        file_input = Pizza.read_input(file_name)
        self.input = Pizza.process_input(file_input)

        self.pizza = self.input["matrix"]
        self.tomato_amount, self.mushroom_amount = self.ingredient_amounts
        self.tomato_proportion, self.mushroom_proportion, self.global_proportion = self.ingredient_proportion

        self.groupmap = Groupmap(self.input["R"], self.input["C"])
        self.update_groupmap()

    @staticmethod
    def read_input(file_name):
        # lê arquivo de entrada e retorna ele em forma de lista de strings
        full_matrix = list()

        with open(file_name, 'r') as input_file:
            for l in input_file:
                full_matrix.append(l.split())

        return full_matrix

    @staticmethod
    def process_input(full_matrix):
        # transforma entrada lida em um dicionário com as informações relevantes e a matriz/pizza como lista de strings
        data = dict()
        data["R"] = int(full_matrix[0][0])
        data["C"] = int(full_matrix[0][1])
        data["L"] = int(full_matrix[0][2])
        data["H"] = int(full_matrix[0][3])
        data["matrix"] = [s[0] for s in full_matrix[1:]]

        return data

    @property
    def ingredient_amounts(self):
        # returns the amount number of each ingredient
        pizza_matrix = self.input["matrix"]

        tomato_amount = 0
        mushroom_amount = 0

        for row in pizza_matrix:
            for cell in row:
                if cell == "T":
                    tomato_amount += 1
                elif cell == "M":
                    mushroom_amount += 1
        
        return tomato_amount, mushroom_amount

    @property
    def ingredient_proportion(self):
        # returns the proportion of both ingredients on pizza and proportion by eachother
        tm, mm  = self.ingredient_amounts
        cell_amount = tm + mm

        tomato_proportion = tm/cell_amount
        mushroom_proportion = mm/cell_amount

        return tomato_proportion, mushroom_proportion, round(tm/mm, 1)

    @property
    def max_slice_amount(self):
        # return the maximum slice amount of a pizza matrix
        tomato_amount, mushroom_amount = self.ingredient_amounts
        minor = min(tomato_amount, mushroom_amount)
        L = self.input["L"]

        return int(minor/L)

    @property
    def min_slice_amount(self):
        # return the minimum slice amount of a pizza matrix
        R = self.input["R"]
        C = self.input["C"]
        H = self.input["H"]

        return int( math.ceil( (R*C)/H ) )

    def set_cell(self, r, c):

        self.clear_steps()

        self.current_slice_value = self.groupmap.matrix[r][c]

        assert r < self.input["R"]
        assert c < self.input["C"]

        self.old_row = self.current_row
        self.old_col = self.current_col

        self.current_row = r
        self.current_col = c
        self.update_groupmap()

        return self.current_cell

    @property
    def current_cell(self):
        data = dict()
        data["row"] = self.current_row
        data["col"] = self.current_col
        data["type"] = self.cell_type(self.current_row, self.current_col)
        return data

    @property
    def current_slice_size(self):
        return self.groupmap.slices[self.current_slice_value].size

    @property
    def current_slice_area(self):
        size = self.current_slice_size
        return size[0] * size[1]

    def cell_type(self, r, c):
        return self.pizza[r][c]

    def update_groupmap(self):
        self.groupmap.update(self.old_row, self.old_col, self.current_row, self.current_col, self.current_slice_value)

    def go_right(self, steps=1):
        try:
            assert self.current_col < self.input["C"]-1
        except:
            return self.current_cell

        self.current_col += steps
        self.update_groupmap()

        try:
            assert self.current_slice_area <= self.input["H"]
        except:
            self.current_col -= steps
            self.update_groupmap()

        return self.current_cell

    def go_down(self, steps=1):
        try:
            assert self.current_row < self.input["R"]-1
        except:
            return self.current_cell

        self.current_row += steps
        self.update_groupmap()

        try:
            assert self.current_slice_area <= self.input["H"]
        except:
            self.current_row -= steps
            self.update_groupmap()
    
        return self.current_cell

    def go_diagonal(self, steps=1):
        try:
            assert self.current_col < self.input["C"]-1
            assert self.current_row < self.input["R"]-1
        except:
            return self.current_cell

        self.current_row += steps
        self.current_col += steps
        self.update_groupmap()

        try:
            assert self.current_slice_area <= self.input["H"]
        except:
            self.current_row -= steps
            self.current_col -= steps
            self.update_groupmap()

        return self.current_cell

    def commit_steps(self):

        self.update_groupmap()

        self.old_col = self.current_col
        self.old_row = self.current_row

        self.current_slice_value += 1
        self.major_slice_value += 1

    def clear_steps(self):
        self.current_col = self.old_col
        self.current_row = self.old_row

        self.groupmap.delete_slice(self.current_slice_value)
        self.update_groupmap()

        self.current_slice_value = self.major_slice_value

    def __repr__(self):
        string = str()
        for l in self.pizza:
            aux = [str(i) for i in l]
            string += " ".join(aux) + "\n"
        return string


pizza = Pizza()
print(pizza.groupmap)
pizza.clear_steps()
print(pizza.set_cell(3,3))
print(pizza.groupmap)
print(pizza.go_down())
print(pizza.groupmap)
print(pizza.go_down())
print(pizza.groupmap)
