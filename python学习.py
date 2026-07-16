print(123)
#注释
'''
zhushi
'''
print("黄家诚","你好",sep='！')
print("hello",end=",")

num1_ = 1
num2 = "欢迎"
print(num1_,num2)

print(type(num1_))

num3 = 1.3 #double
num4 = True #True == 1 False == 0
num5 = 1 + 2j #complex
string1 = "数据类型" #str
string2 = """
1
2
3
"""
print(type(num5))
print(type(num3))
print(type(num4))
print(type(num4+1))
print(type(string1))
print(string2)

name = "黄家诚"
age = 19
weight = 70.0
print("我的名字叫%s ，我%d岁"%(name,age))
print("%04d"%age)
print("%.3f"%weight)
print(f"我的名字叫{name} ，我{age}岁")#格式化输出

print(1/1) #浮点数
print(1//2) #取整除
print(1%2) #取余数
print(2**2) #幂

"""name1= input("请输入你的名字：")
#print(name1)"""

#\t 制表符 四个空字符
#\n 换行符
#\r 回车 当前回到本行开头
#\\ 反斜杠 可输出\t等原本字符 或print(r"six\tadad")表示中间无转译

#input(age) #input是字符串输入 
if age == '18':
    print("No")
elif age >18 and age<20:
    print("Yes")
elif age =='20':
    print(age)

while age == '18':
    print("No")
    age = 0

string2 = "abcdefg"
for i in string2:
    print(i)
for i in range(1,5,1):
    print(i)

print("2"*5)

if 'a' in string2:
    print("有a")

print(string2[0])#从左往右 
print(string2[-1])#从右往左

print(string2.find("bc",0,5))#find(子字符串，起始，终止) 返回位置 没找到返回-1

print(string2.index("bc",0,5))#index(子字符串，起始，终止) 返回位置 没找到报错

name = "aaaaaannnnnnnbbbbbb"
print (name.count('an',0,20))

#startswith(子字符串，开始，结束) 是否已某个字符串开头
#endswith
#isupper 是否都是大写

#修改元素
name = "黄,家诚"
print(name.replace("家诚",'加成'))

#split指定分隔符切分字符串、
print(name.split(','))

#capitalize()第一个字符大写
#lower()大写转换为小写 upper()小写转换为大写

#列表
li = ['one','two','three','four']
li.append('five')#直接添加
li.extend('six')#分散添加 把s i x 分别往后加入
li.insert(0,'zero')#在0处添加zero进去
if 'one' in li:
    print("No")

#index find count 都可以用在列表

del li[2]#删除第几个
print(li)
li.pop()#默认删除最后一个
print(li)
li.remove('one')#直接删除最开始指定元素

num = [1,5,6,32,78,1,2]
num.sort()
print(num)
num.reverse()
print(num)

[num.append(i) for i in range(1,11) if i%2==1]#格式[表达式 for i in 列表 if 条件]
print(num)

li = [0,1,2,[1,2]]
print(li[3][1])

#元组 只支持查询操作 不支持增删改 可以用count index len
tua = (1,)#只有一个的时候记得加逗号
info = (name,age)
print("%s的年龄是%d"%info)#后面的%(name,age)本身就是个元组

#字典 字典名 = {键1：值1，键2:值2...}保存一个物体的所有信息
dic = {'name':'jay','age':18}
print(dic['name'],dic['age'])
print(dic.get('name'))#查找
dic['age'] = 20#修改
dic['tele'] = 1887256#没有键名就是新增
del dic#删除字典
dic = {'name':'jay','age':18}
del dic['age']#删除相关键值对与值
dic.pop('name')#删除相关键值对与值
dic.clear()#清空字典所有东西但保留字典

print(len(dic))#len()返回有几个键值对
print(dic.keys())#keys()返回所有键名
print(dic.values())#values()返回所有值
print(dic.items())#items()以元组形式返回键值对

#集合 集合名 = {元素1，元素2，元素3} 集合具有无序性 唯一性 不能查询 只能添加和删除
s1 = set()#空集合
s1 = {'a','b','c','d'}

s1.add(1)#一次只能添加一个元素
s1.update('efg')#拆开分别添加 放可迭代对象
s1.update([1,2,3])
s1.remove(1)#没有会报错
s1.discard(1)#没有不会改变

#交集并集
s2 = {'a','m'}
print(s1&s2)#交集 没有返回空集合set()
print(s1|s2)#并集 

li = [1,2,3,4]
li2 = li #li改变li2也会改变
li.append(5)
import copy
from re import A, L
li = [1,2,3,4]
li2 = copy.copy(li)#浅拷贝 外层地址不同 嵌套地址共享
li3 = copy.deepcopy(li2)#深拷贝 都拷贝了一遍 地址不共享 

#函数
def greeting():
    print('hi')
    return'hello'
greeting()
print(greeting())

def add1(a,b,c=8):#必备参数 默认参数要在位置参数后面 可变参数*d
    return a+b
print(add1(1,2,3)) 
def func(*d):#*d以  元组  形式接受可以是多个或不传
    print(d)
func(1,2,3)

def fund(**kwargs):#以  字典  形式接收
    print(kwargs)
fund(name = 'huang')

def funa():
    global a#声明全局变量
    a = 100

add = lambda a,b:a+b#匿名函数 形参：返回值
print(add(1,2))

#拆包
tua = (1,2,3,4)
a,b,c,d = tua
print(a,b,c,d)
a,*b = tua#其他的全放到b中

#读取文件
#with open("文件名","读取模式",)
with open('C:/Users/26648/Desktop/study plan/outputs/summer-training-materials/week01_text.txt') as file:
    content = file.read()
    #for line in file:
        #print(line.strip())
    #content = file.readlines()
    print(len(content))#长度
    line_num = 0
    words_num = 0
with open('C:/Users/26648/Desktop/study plan/outputs/summer-training-materials/week01_text.txt') as file:
    for line in file:
        line_num += 1
        words = line.split()
        words_num += len(words)
    print(line_num,words_num)
with open('C:/Users/26648/Desktop/study plan/outputs/summer-training-materials/week01_text.txt') as file:
    words_num1 = 0
    content = file.read()
    words = content.split()
    words_num1 += len(words)
    print(words_num1)

#with open('C:/Users/26648/Desktop/study plan/outputs/summer-training-materials/week01_text.txt','w')as file:
 #   file.write()
 
#异常处理
try:
    print(9/0)
except ZeroDivisionError:
    print('Error')

with open('C:/Users/26648/Desktop/result_1.txt','w') as file:
    file.write('行数%d,单词数%d'%(line_num,words_num))











