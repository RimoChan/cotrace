import sys
import time
import types
import atexit
import shutil
import logging
import threading
import functools

from pathlib import Path
from typing import Optional, Iterable, List

stack: List[Optional[types.FrameType]] = [None]

trace_exception = None


class P:
    def __init__(self, file):
        self.pre = None
        self.start_time = time.time()
        self.file = file
        self.输出缓冲 = []
        self.输出缓冲长度限制 = 256
        self.锁 = threading.Lock()
        threading.Thread(target=self.自动刷新, daemon=True).start()
        atexit.register(self.刷新)

    def 自动刷新(self):
        while True:
            self.刷新()
            time.sleep(0.5)

    def 刷新(self):
        with self.锁:
            a = []
            for i, 时间 in self.输出缓冲:
                if not a or a[-1][0] != i:
                    a.append([i, 时间, 1])
                else:
                    a[-1][2] += 1
            self.输出缓冲 = []
            for i, 时间, 次数 in a:
                print(' | '.join([
                    i,
                    f' *{次数} ' if (次数 > 1) else '    ',
                    f'{时间:.3f}'
                ]), file=self.file)
            self.file.flush()

    def 写(self, x: str):
        self.输出缓冲.append((x, time.time()-self.start_time))
        if len(self.输出缓冲) >= self.输出缓冲长度限制:
            self.刷新()

    def __del__(self):
        self.刷新()


@functools.lru_cache(maxsize=None)
def 计算所有祖先(filename):
    try:
        pt = Path(filename).resolve()
    except OSError:
        return set()
    return set([*pt.parents, pt])


def frame转class(frame):
    try:
        if 'self' not in frame.f_locals:
            return None
        for cls in frame.f_locals['self'].__class__.__mro__:
            func = cls.__dict__.get(frame.f_code.co_name, None)
            if getattr(func, '__code__', None) is frame.f_code:
                return cls
    except Exception:
        return None


def auto_call_trace(paths: Iterable[str], *, width: Optional[int] = None, indent: int = 2, file=None):
    if width is None:
        width = shutil.get_terminal_size((80, 20)).columns - 20
    if not file:
        file = sys.stdout
    pj = P(file=file)
    paths = set([Path(x).resolve() for x in paths])
    print(f'函数名{" "*(width-12)}位置 | 次数 | 时间', file=file)
    print('='*(width+12), file=file)
    def f(frame: types.FrameType, event, arg):
        global trace_exception
        if sys is None or sys.is_finalizing():
            return
        try:
            if not 计算所有祖先(frame.f_code.co_filename) & paths:
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
                if sys.version_info.minor >= 11:
                    名字 = c.co_qualname
                else:
                    名字 = c.co_name
                    cls = frame转class(x)
                    if cls:
                        名字 = f'{cls.__name__}.{名字}'
                前 = 缩进 + 名字
                后 = f'[L{c.co_firstlineno}, {c.co_filename}]'
                l = len(前+后)
                l += len([i for i in 前+后 if ord(i) > 127])
                pj.写(f'{前}{max(1, width-2-l)*" "}{后}')
        except Exception as e:
            logging.exception(e)
            trace_exception = e
    sys.settrace(f)
