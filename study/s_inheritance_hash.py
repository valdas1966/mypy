class A:

    def __init__(self, x):
        self.x = x

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())


class B(A):

    def __str__(self):
        return str(self.x) + str(self.x)


a = A(x=1)
b = B(x=1)
s = {a, b}
print(s)


from f_data_structure.nodes.i_2_cell import NodeCell
a = NodeCell(name='A')
b = NodeCell()
s = {a, b}
print(s)


