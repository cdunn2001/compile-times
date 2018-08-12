# http://pastie.org/pastes/10943133/text
# Copyright (c) 2016 1wd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import timeit
import subprocess

def do(args):
    print("do {}".format(args))
    start = timeit.default_timer()
    subprocess.call(args)
    end = timeit.default_timer()
    return end - start

langs = [
    #("VC++", "cpp", ["cl.exe", "/nologo", "/Od"], False),
    ("Nim", "nim", ["nim", "c", "--opt:none", "--checks:off"], False),
    ("Clang++", "cpp", ["clang++", "-O0"], False),
    ("Clang", "c", ["clang", "-O0"], False),
    ("D", "d", ["dmd"], False),
    ("Go", "go", ["go", "build", "-gcflags", '-N -l'], False),
    #("Pascal", "pas", ["fpc.exe", "-v0", "-O-"], False),
    #("Rust", "rs", ["rustc", "-C", "opt-level=0"], False),

    ##("VC++ (opt)", "cpp", ["cl.exe", "/nologo", "/O2"], True),
    ("Nim (opt)", "nim", ["nim", "c", "-d:release"], False),
    ("Clang++ (opt)", "cpp", ["clang++", "-O2"], True),
    ("Clang (opt)", "c", ["clang", "-O2"], True),
    ("D (opt)", "d", ["dmd", "-O"], True),
    ("Go (opt)", "go", ["go", "build"], True),
    ##("Pascal (opt)", "pas", ["fpc.exe", "-v0", "-O2"], True),
    #("Rust (opt)", "rs", ["rustc", "-C", "opt-level=2"], True),
]

num_seeds = 1
n0 = 0
n = 1
n_step = 10000

opt_levels = [
    False,
    True,
]

results = []

print "n={}, n_step={}".format(n, n_step)
for i in range(n0, n):
    num_funcs = n_step * (i+1)
    print "Generate code: i={}, num_funcs={}...".format(i, num_funcs)
    for seed in range(num_seeds):
        do(["python2.7", "./cogen.py",
            str(seed), str(num_funcs)])

    row = [num_funcs]
    for lang, ext, args, opt in langs:
        if opt not in opt_levels: continue
        print "%s..." % lang
        t = 0
        for seed in range(num_seeds):
            filename = 'test_%s_s%s_n%s.%s' % (ext, seed, num_funcs, ext)
            t += do(args + [filename])
        row.append(t / num_seeds)
    results.append(row)

print "Create CSV..."
with open("results.csv", "w") as f:
    f.write(','.join(["n"] + [lang[0] for lang in langs]))
    f.write('\n')
    for row in results:
        f.write(','.join(str(x) for x in row))
        f.write('\n')
