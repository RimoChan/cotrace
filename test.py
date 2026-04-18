import cotrace


class AA:
    def __init__(self):
        ...

    def q(self):
        ...

class A(AA):
    def __init__(self):
        super().__init__()
        for _ in range(3):
            b()

def b():
    for _ in range(3):
        c()

def c():
    0


if __name__ == '__main__':
    print(cotrace.__file__)
    cotrace.auto_call_trace([__file__])
    A().q()
    assert not cotrace.trace_exception
