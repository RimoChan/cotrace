import sys
import time
import logging
import functools
from pathlib import Path


stack = [None]


class P():
    def __init__(self, need_time):
        self.pre = None
        self.n = 0
        self.first = True
        self.need_time = need_time
        self.start_time = time.time()

    def _g(self):
        if self.n > 1:
            sys.stdout.write('\r')
            if self.need_time:
                sys.stdout.write('%.3f' % (time.time()-self.start_time))
            sys.stdout.write(f'{self.pre} * {self.n}')
        if self.n == 1:
            if not self.first:
                sys.stdout.write('\n')
            if self.need_time:
                sys.stdout.write('%.3f' % (time.time()-self.start_time))
            sys.stdout.write(self.pre)
            self.first = False

    def count_print(self, x):
        x = str(x)
        if x != self.pre:
            self.pre = x
            self.n = 0
        self.n += 1
        self._g()


@functools.lru_cache(maxsize=None)
def pa(filename):
    try:
        pt = Path(filename).resolve()
    except OSError:
        return set()
    return set([*pt.parents, pt])


def auto_call_trace(paths, *, width=60, indent=2):
    pj = P(need_time=True)
    paths = set([Path(x).resolve() for x in paths])
    print(f'时间 | 函数名{" "*(width-14)}位置 | 次数')
    print('='*(width+10))
    def f(frame, event, arg):
        try:
            if not pa(frame.f_code.co_filename) & paths:
                return
            rs = [frame]
            p = frame
            while p:
                p = p.f_back
                if p in stack:
                    while stack[-1] != p:
                        stack.pop()
                    break
                rs.append(p)
            s = rs[::-1]
            stack.extend(s)
            for i, x in enumerate(s):
                缩进 = ' '*indent*(len(stack)-len(s)+i-1)
                c = x.f_code
                前 = 缩进+c.co_name
                后 = f'[L{c.co_firstlineno}, {c.co_filename}]'
                l = len(前+后)
                l += len([i for i in 前+后 if ord(i) > 127])
                pj.count_print(f'|{前}{max(1, width-2-l)*" "}{后}|')
        except Exception as e:
            logging.exception(e)
    sys.settrace(f)
