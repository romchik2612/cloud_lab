import math

from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        size = self.read_input()
        step = len(self.workers) * 2
        result = []
        for i in range(0, len(self.workers)):
            result.append(self.workers[i].process(i * 2 + 1, size, step))
        reduced = self.sum(result)
        self.write_output(reduced)

    @staticmethod
    @expose
    def process(a, b, step):
        res = 0
        for i in range(a, b, step):
            res += math.factorial(i)
        return res

    @staticmethod
    @expose
    def sum(result):
        final_sum = 0
        for x in result:
            final_sum += x.value
        return final_sum

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
