import re
with open(r'C:\Users\沈家\.config\clash\config.yaml', 'r', encoding='utf-8') as f:
    a = f.read()
aa = re.findall(r'external-controller: (.*?)\n', str(a), re.DOTALL)[0]
print(aa)
