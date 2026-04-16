import cotrace


class A:
    def a():
        for _ in range(3):
            b()

def b():
    for _ in range(3):
        c()

def c():
    0


if __name__ == '__main__':
    cotrace.auto_call_trace([__file__])
    A.a()
    assert not cotrace.trace_exception
