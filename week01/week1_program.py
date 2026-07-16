import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input_file',nargs = '+')
parser.add_argument('-o','--output',default = 'result.txt')
args = parser.parse_args()
input_paths= args.input_file
output_path = args.output

line_count = 0
word_count = 0
ans = 0
word_num = {}#存单词与对应数量的字典

#统计行数和单词数 
for input_path in input_paths:
    with open(input_path,'r',encoding ='utf-8' ) as file:
        for line in file:
            line_count += 1
            word = line.split()
            for i in word:
                word_count += 1  

    with open(input_path,'r',encoding ='utf-8') as file:
        for line in file:
            words = line.split()
            for word in words:
                word = word.lower()#改大写为小写
                word = word.strip(",.!?")#删符号
                if word in word_num:
                    word_num[word] += 1
                else:
                    word_num[word] = 1
print(line_count,word_count) 

word_sorted = sorted(word_num,key = word_num.get,reverse = True)#排序并存入
n = 0
print('出现次数最多的前 10 个单词为：')
for word in word_sorted[0:10]:#取前十个
    n+=1
    print('%d.'%n,word,word_num[word],'次')
        
#询问单词出现次数
Qword = input('请输入要查询数量的单词')
Qword = Qword.lower()
try:#用一下异常处理
    ans = word_num[Qword]
    print('%s出现了%d次'%(Qword,ans))
except KeyError:
    print("该单词不存在")

with open(output_path,'w',encoding='utf-8') as file:
    file.write(f'有{line_count}行   有{word_count}个单词 \n')
    file.write('出现次数最多的前10个单词和次数为：\n')
    n = 0
    for word in word_sorted[0:10]:
        n+=1
        file.write(f'{n}.{word}{word_num[word]}次\n')
    file.write(f"您查询的单词{Qword}出现了{ans}次\n")

