"""Exercise the real Action controller; CI adds a disconnected network namespace."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def read_outputs(path):
    lines = path.read_text().splitlines(); result = {}
    while lines:
        key, delimiter = lines.pop(0).split('<<', 1); values = []
        while lines[0] != delimiter: values.append(lines.pop(0))
        lines.pop(0); result[key] = '\n'.join(values)
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--network-namespace', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp); repo = folder / 'repo'; repo.mkdir()
        def git(*values):
            return subprocess.check_output(['git', '-C', str(repo), *values], text=True, stderr=subprocess.DEVNULL).strip()
        git('init', '-q', '-b', 'main'); git('config', 'user.name', 'Offline fixture')
        git('config', 'user.email', 'fixture@example.invalid'); git('config', 'commit.gpgsign', 'false')
        file = repo / '.github/workflows/ci.yml'; file.parent.mkdir(parents=True)
        base_text = 'on: workflow_dispatch\npermissions: {}\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps: [{run: echo fixture}]\n'
        file.write_text(base_text); git('add', '.'); git('commit', '-qm', 'base'); base = git('rev-parse', 'HEAD')
        file.write_text(base_text.replace('permissions: {}', 'permissions: {id-token: write}').replace('runs-on: ubuntu-latest', 'runs-on: [self-hosted, prod]\n    environment: production'))
        git('commit', '-qam', 'head'); head = git('rev-parse', 'HEAD')
        # Proposed Python modules are data, never imports of the isolated Action.
        (repo / 'yaml.py').write_text('raise RuntimeError("PROPOSED_IMPORT_EXECUTED")')
        for mode in ('advisory', 'require-complete'):
            env = {'PATH': os.environ['PATH'], 'RUNNER_TEMP': tmp, 'PRIVILEGE_MODE': mode,
                   'PRIVILEGE_BASE': base, 'PRIVILEGE_HEAD': head, 'PRIVILEGE_DEFAULTS': '',
                   'PRIVILEGE_REPOSITORY': str(repo), 'GITHUB_OUTPUT': str(folder / (mode + '.out')),
                   'GITHUB_STEP_SUMMARY': str(folder / (mode + '.md')), 'PYTHONPATH': str(repo)}
            command = [sys.executable, '-I', '-S', str(ROOT / 'scripts/action_runner.py')]
            if args.network_namespace:
                command = ['sudo', 'unshare', '--net', '--', 'setpriv', '--reuid', str(os.getuid()),
                           '--regid', str(os.getgid()), '--clear-groups', 'env',
                           *[f'{key}={value}' for key, value in env.items()], *command]
            start = time.monotonic()
            cp = subprocess.run(command, env={**os.environ, **env}, cwd=repo, capture_output=True, text=True, timeout=30)
            if cp.returncode: raise RuntimeError('Offline Action failed: ' + cp.stdout[-1000:] + cp.stderr[-1000:])
            outputs = read_outputs(Path(env['GITHUB_OUTPUT']))
            report = json.loads(Path(outputs['report-path']).read_text())
            assert outputs['analysis-status'] == 'complete' and outputs['review-status'] == 'suggested'
            assert {f['rule'] for f in report['findings']} == {'WF001', 'WF005', 'WF007'}
            assert (outputs['base-sha'], outputs['head-sha']) == (base, head)
            assert 'not approval to merge' in Path(env['GITHUB_STEP_SUMMARY']).read_text()
            print('WPC_OFFLINE_RESULT=' + json.dumps({'mode': mode, 'analysis': 'complete', 'review': 'suggested',
                  'rules': ['WF001', 'WF005', 'WF007'], 'networkNamespace': args.network_namespace,
                  'seconds': round(time.monotonic() - start, 3)}))


if __name__ == '__main__': main()
