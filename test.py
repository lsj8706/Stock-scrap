import re
p = re.compile('[a-z]+')
str1 = "12645pthnon"
if p.search(str1):
    m = p.findall(str1)
    print(m)
else:
    print("no match")
