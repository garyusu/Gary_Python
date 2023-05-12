import re

r_str = '香蕉 banana 蘋果 Apple'
r1 = re.sub(r'\s+', '', r_str) # 去除包含換行的所有空白
pattern = re.compile(r'[^A-z]+',re.I)
r = pattern.search(r1)


print("是否全英文：" + r_str)
if r == None:
    print("符合")
else:
    print("不符")
print(r)


r_str1 = '\/:*?<>|\/:*?<>|'
r2 = re.sub(r'\\\/\:\*\?\<\>\|', '', r_str1) #消除特殊字元，建檔名用

# print(r2)

#取代特殊字元，建檔名用
r3 = r_str1.replace('\\','＼').replace('/','／').replace(':','：')
r3 = r3.replace('*','＊').replace('?','？').replace('<','＜')
r3 = r3.replace('>','＞').replace('|','｜')

# print(r3)

r_str2 = '<Face yuu_004.jpg>'

pattern2 = re.compile(r'(\S+?\.jpg)',re.I)
r4 = pattern2.findall(r_str2)
print(r4)

pattern3 = re.compile(r'\S+?\.jpg',re.I)
r5 = pattern3.search(r_str2)
print("+" + r5.group() + "+")