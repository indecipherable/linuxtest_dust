import subprocess

cmd = 'python3 rand.py'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate()
result = out
print(result)
