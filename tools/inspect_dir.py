import os

tools_dir = r"C:\GitHub\Gurukuladesam\tools"
for f in os.listdir(tools_dir):
    if f.endswith('.py'):
        print(f)
