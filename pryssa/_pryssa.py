import pickle
import inspect, tempfile
import os, sys, linecache
import sys, re, hashlib


class PryssaTracer:
    def __init__(self, key):
        self.filename = inspect.stack()[2][1]
        self.end_line = None
        self.key = key
        self.pryssa_file = os.path.join(tempfile.gettempdir(), 'pryssa_{}.pickle'.format(hashlib.md5(repr((key, self.filename)).encode()).hexdigest()))
    
    def _trace(self, frame, event, arg):
        if self.end_line is None:
            self.end_line = self.find_end(frame)
            self.vars = re.match('.*?PRYSSA (.*)', linecache.getline(self.filename, self.end_line)).groups()[0].split()
            self.func_name = frame.f_code.co_name
            self.hit_end = False
            try:
                print('pryssa: trying to load from {}'.format(self.pryssa_file))
                with open(self.pryssa_file, 'rb') as f:
                    res = pickle.load(f)
                    for k, v in res.items():
                        frame.f_locals[k] = v
                    self.hit_end = True
                    self.jump_to_end(frame)
            except (OSError, EOFError):
                print('pryssa: failed')
        if frame.f_code.co_filename == self.filename and frame.f_code.co_name == self.func_name and not self.hit_end and frame.f_lineno >= self.end_line:
            self.hit_end = True
            d = {}
            for v in self.vars:
                d[v] = frame.f_locals[v]
            print('pryssa: saving')
            with open(self.pryssa_file, 'wb') as f:
                pickle.dump(d, f)
    
    def jump_to_end(self, frame):
        frame.f_lineno = self.end_line
        
    def find_end(self, frame):
        line = frame.f_lineno
        while 'PRYSSA' not in linecache.getline(self.filename, line):
            line += 1
        return line

        
def pryssa(*args):
    tr = PryssaTracer(args)
    sys.settrace(tr._trace)
    frame = sys._getframe().f_back
    while frame:
        frame.f_trace = tr._trace
        frame = frame.f_back 
    