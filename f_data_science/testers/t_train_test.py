from f_utils import u_tester
from f_data_science import u_train_test


class Tester_Train_Test:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_split()
        u_tester.print_finish(__file__)

    def tester_split(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        y = [0, 0, 0, 0, 1, 1, 1, 1]
        x_train, x_test, y_train, y_test = u_train_test.split(x, y)
        p0 = len(x_train) == len(y_train) == len(x)*0.75
        p1 = len(x_test) == len(y_test) == len(x)*0.25
        p2 = y_train.count(1) == 3
        p3 = y_test.count(1) == 1
        u_tester.run(p0, p1, p2, p3)


if __name__ == '__main__':
    Tester_Train_Test()
    