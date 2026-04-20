#!/usr/bin/env python3
# Regression test for the shell/Python polyglot shebang on
# ``speedtest.py``. Ensures that:
#   1. The file imports cleanly as a Python module (polyglot line is a
#      no-op string literal at module scope).
#   2. /bin/sh can execute the file directly (the polyglot exec chain
#      dispatches to a python interpreter).
#   3. If no interpreter named python3/python3.X/python exists on
#      PATH, the shell chain exits non-zero with a clear error message.

import os
import subprocess
import sys
import tempfile

HERE = os.path.abspath(os.path.dirname(__file__))
SCRIPT = os.path.normpath(os.path.join(HERE, '..', '..', 'speedtest.py'))


def assert_eq(got, want, label):
    if got != want:
        raise SystemExit('%s: got %r, want %r' % (label, got, want))


def main():
    # 1. Importable as a Python module.
    proc = subprocess.run(
        [sys.executable, '-c',
         'import sys; sys.path.insert(0, %r); '
         'import speedtest; print(speedtest.__version__)'
         % os.path.dirname(SCRIPT)],
        capture_output=True, text=True,
    )
    assert_eq(proc.returncode, 0, 'import as module')
    if not proc.stdout.strip():
        raise SystemExit('import as module: empty __version__ output')

    # 2. /bin/sh can dispatch via the polyglot chain.
    proc = subprocess.run(
        ['/bin/sh', SCRIPT, '--version'],
        capture_output=True, text=True,
    )
    assert_eq(proc.returncode, 0, 'sh dispatch')
    if 'speedtest-cli' not in proc.stdout:
        raise SystemExit(
            'sh dispatch: --version output missing "speedtest-cli":\n%s'
            % proc.stdout
        )

    # 3. With no interpreter on PATH, the chain prints an error and
    #    exits 127.
    with tempfile.TemporaryDirectory() as empty_dir:
        env = {'PATH': empty_dir}
        proc = subprocess.run(
            ['/bin/sh', SCRIPT, '--version'],
            capture_output=True, text=True, env=env,
        )
    if proc.returncode != 127:
        raise SystemExit(
            'missing-interpreter: expected exit 127, got %d\nstderr: %s'
            % (proc.returncode, proc.stderr)
        )
    if 'no python3 interpreter found' not in proc.stderr:
        raise SystemExit(
            'missing-interpreter: expected diagnostic on stderr, got:\n%s'
            % proc.stderr
        )

    print('ok')


if __name__ == '__main__':
    main()
