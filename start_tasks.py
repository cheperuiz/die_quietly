import argparse
import subprocess
def monitor_forever(ps):
    while True:
        for p in ps:
            if p.poll() is not None:
                print('Process {} is dead, killing main process'.format(p.pid))
                for p in ps:
                    p.terminate()
                return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start tasks')
    parser.add_argument('--n', type=int, default=10, help='Number of tasks to start  (default: 10)')
    args = parser.parse_args()
    ps = []
    for i in range(args.n):
        p =subprocess.Popen(['python', 'task.py'])
        ps.append(p)
    api = subprocess.Popen(['uvicorn', 'main:app','--host', '0.0.0.0'])
    ps.append(api)
    monitor_forever(ps)

