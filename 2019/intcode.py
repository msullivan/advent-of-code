import array

def execute_intcode(p, ip, relative_base, input, output, max):
    cnt = 0
    while ip >= 0:
        if max and cnt > max:
            break
        cnt += 1

        instr = p[ip]

        def read(i):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                addr = p[ip+i]
            elif mode == 1:
                addr = ip+i
            else:
                addr = p[ip+i] + relative_base
            if addr >= len(p):
                p.extend([0]*addr)
            return p[addr]

        def write(i, v):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                addr = p[ip+i]
            else:
                assert mode == 2
                addr = p[ip+i] + relative_base
            if addr >= len(p):
                p.extend([0]*addr)
            p[addr] = v

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

    return ip, relative_base, cnt


try:
    from _intcode import execute_intcode
except ImportError as e:
    pass


class IntCode:
    def __init__(self, program, input = None, output = None):
        self.program = array.array('q', program)

        self.ip = 0
        self.relative_base = 0
        self.input = input or []
        self.output = output or []
        self.spew = False

    @property
    def done(self):
        return self.ip == -1

    def execute(self, max=None):
        max = 0 if max is None else max
        self.ip, self.relative_base, cnt = execute_intcode(
            self.program, self.ip, self.relative_base, self.input, self.output, max
        )
        if max and cnt >= max:
            raise ValueError('ran too long', cnt)

    def run(self, input, max=None):
        self.input = input
        self.output = []
        self.execute(max)
        return self.output
