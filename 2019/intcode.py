def execute_intcode(p, ip, relative_base, input, output):
    while ip >= 0:
        instr = p[ip]

        def read(i):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                return p[p[ip+i]]
            elif mode == 1:
                return p[ip+i]
            else:
                return p[p[ip+i] + relative_base]

        def write(i, v):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                p[p[ip+i]] = v
            else:
                assert mode == 2
                p[p[ip+i] + relative_base] = v

        if instr % 100 == 1:
            write(3, read(1) + read(2))
            ip += 4
        elif instr % 100 == 2:
            write(3, read(1) * read(2))
            ip += 4
        elif instr % 100 == 3:
            if not input:
                break
            write(1, input.pop(0))
            ip += 2
        elif instr % 100 == 4:
            output.append(read(1))
            ip += 2
        elif instr % 100 == 5:
            if read(1) != 0:
                ip = read(2)
            else:
                ip += 3
        elif instr % 100 == 6:
            if read(1) == 0:
                ip = read(2)
            else:
                ip += 3
        elif instr % 100 == 7:
            if read(1) < read(2):
                write(3, 1)
            else:
                write(3, 0)
            ip += 4
        elif instr % 100 == 8:
            if read(1) == read(2):
                write(3, 1)
            else:
                write(3, 0)
            ip += 4
        elif instr % 100 == 9:
            relative_base += read(1)
            ip += 2
        elif instr % 100 == 99:
            ip = -1

    return ip, relative_base


class IntCode:
    def __init__(self, program, input = None, output = None):
        self.program = program.copy()
        self.ip = 0
        self.relative_base = 0
        self.input = input or []
        self.output = output or []

    @property
    def done(self):
        return self.ip == -1

    def execute(self):
        self.ip, self.relative_base = execute_intcode(
            self.program, self.ip, self.relative_base, self.input, self.output
        )

    def run(self, input):
        self.input = input
        self.output = []
        self.execute()
        return self.output
