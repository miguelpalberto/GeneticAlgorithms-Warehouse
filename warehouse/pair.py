class Pair:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2
        self.value = 0

    def hash(self):
        return str(self.cell1.line) + "_" + str(self.cell1.column) + "_" + str(
            self.cell2.line) + "_" + str(self.cell2.column)
    ###added:
    def __hash__(self):
        return hash(str(self.cell1.line) + "_" + str(self.cell1.column) + "_" + str(
            self.cell2.line) + "_" + str(self.cell2.column))

    def __str__(self):
        return str(self.cell1.line) + "-" + str(self.cell1.column) + " / " + str(self.cell2.line) + "-" + str(
            self.cell2.column) + ": " + str(self.value)
    ###added:
    def __eq__(self, other):
        return (self.cell1 == other.cell1 and self.cell2 == other.cell2) # or (self.cell2 == other.cell1 and self.cell1 == other.cell2)
