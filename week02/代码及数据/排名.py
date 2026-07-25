import pandas as pd
import time
import random
input_path = 'week02_students.csv'
df = pd.read_csv(input_path,encoding = 'utf-8')

print('字段类型：')
print(df.dtypes)
print('缺失值：')
print(df.isnull().sum())
print('重复值：')
print(df.duplicated().sum())


ids = set()
keep = []#保留的行数
for index,row in df.iterrows():#iterrows会提供索引和数据 用index和row去接住
    student_id = row['student_id']
    if student_id not in ids:
        ids.add(student_id)
        keep.append(index)
df = df.loc[keep].copy()
df = df.reset_index(drop = True)
print('去重后：')
print(df)


#统计每班人数
class_num = {}
for classN in df['class']:
    if classN in class_num:
        class_num[classN] += 1
    else:
        class_num[classN] = 1
print('每班人数：')
print(class_num)


#每班学号
class_students = {}
for index,row in df.iterrows():
    classN = row['class']
    student_id = row['student_id']
    if classN not in class_students:
        class_students[classN] = []
    class_students[classN].append(student_id)
print('按班级分类：')
print(class_students)


#处理异常值
score_columns = ['math','english','programming']
for column in score_columns:
    abn_condition = (df[column] < 0) | (df[column] > 100)
    df.loc[abn_condition,column] = pd.NA

#处理缺失值
for column in score_columns:
    meanScore = df[column].mean()
    df[column] = df[column].fillna(meanScore)
print(df)


#计算平均分
df['average'] = df[score_columns].mean(axis = 1)


#筛选85分以上的
Hcondition = df['average'] > 85
Hstudents = df[Hcondition]
print('平均分85以上的：')
print(Hstudents)


#按班分组
grouped = df.groupby('class')
summary_columns = ['math','english','programming','average']
class_average = grouped[summary_columns].mean()
print('每个班的平均成绩')
print(class_average)


#排序
start = time.perf_counter()
usort = df.sort_values(by = 'average',ascending = True)#升序
end = time.perf_counter()
sortTime = end - start
print('使用pandas升序排序后：')
print(usort)
dsort = df.sort_values(by = 'average',ascending = False)
print('使用pandas降序排序后：')
print(dsort)


#逐行查找
def line_search(dataframe,targetId):
    for index,row in dataframe.iterrows():
        if row['student_id'] == targetId:
            return row.to_dict()


#字典查找
student_index = {}
for index,row in df.iterrows():
    student_id = row['student_id']
    student_index[student_id] = row.to_dict()
def dic_search(targetId):
    return student_index.get(targetId)


#比较查找速度
targetId = 'S020'
start = time.perf_counter()
for i in range(1000):
    lineR = line_search(df,targetId)
end = time.perf_counter()
lineTime = end - start
print('分别查找1000次后\n逐行查找:',lineTime,'秒')

start = time.perf_counter()
for i in range(1000):
    DicR = dic_search(targetId)
end = time.perf_counter()
DicTime = end - start
print('字典查找:',DicTime,'秒')


#4个排序
#归并排序
def merge(left,right,a = True):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if a:
            if left[i]['average'] <= right[j]['average']:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if left[i]['average'] >= right[j]['average']:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
    result.extend(left[i:])#当一个已经塞完时把另外一边的全部塞进去
    result.extend(right[j:])
    return result
def merge_sort(numbers,a = True):
    if len(numbers) <= 1:#终止条件
        return numbers.copy()
    mid = len(numbers)//2#两个杠是整除
    left = merge_sort(numbers[:mid],a)
    right = merge_sort(numbers[mid:],a)
    return merge(left, right,a)


#插入排序
def insertion_sort(numbers,a = True):
    result = numbers.copy()
    n =len(result)
    for i in range(1,n):
        current = result[i]
        j = i - 1
        if a:
            while j >= 0 and result[j]['average'] > current['average']:
                result[j + 1] = result[j]
                j -= 1
        else:
            while j >= 0 and result[j]['average'] < current['average']:
                result[j + 1] = result[j]
                j -= 1
        result[j + 1] = current
    return result



#选择排序
def selection_sort(numbers,a = True):
    result = numbers.copy()
    n =len(result)
    for i in range(n-1):
       min1 = i
       for j in range(i+1,n):
            if a:
                if result[j]['average'] < result[min1]['average']:
                    min1 = j
            else:
                if result[j]['average'] > result[min1]['average']:
                    min1 = j
       switch = result[min1]
       result[min1] = result[i]
       result[i] = switch
    return result



#冒泡排序
def bubble_sort(numbers,a = True):
    result = numbers.copy()#不用copy只会改名 
    n =len(result)
    for i in range(0,n-1):
        for j in range(0,n-i-1):
            if a:
                if result[j]['average']>result[j+1]['average']:
                    switch = result[j]
                    result[j] = result[j+1]
                    result[j+1] = switch
            else:
                if result[j]['average']<result[j+1]['average']:
                    switch = result[j]
                    result[j] = result[j+1]
                    result[j+1] = switch
    return result


#转化为字典
student_records = []
for index,row in df.iterrows():
    student_records.append(row.to_dict())


bubble_up = bubble_sort(student_records, True)
selection_up = selection_sort(student_records, True)
insertion_up = insertion_sort(student_records, True)
merge_up = merge_sort(student_records, True)

bubble_down = bubble_sort(student_records, False)
selection_down = selection_sort(student_records, False)
insertion_down = insertion_sort(student_records, False)
merge_down = merge_sort(student_records, False)

print('归并排序升序结果：')
for student in merge_up:
    print(student["student_id"],student["average"])
print('\n归并排序降序结果：')
for student in merge_down:
    print(student["student_id"],student["average"])


#调用计时
test_numbers = [
    {"student_id": "T001", "average": 80},
    {"student_id": "T002", "average": 90},
    {"student_id": "T003", "average": 80},
    {"student_id": "T004", "average": 70}
]
test_bubble = bubble_sort(test_numbers, True)
test_selection = selection_sort(test_numbers, True)
test_insertion = insertion_sort(test_numbers, True)
test_merge = merge_sort(test_numbers, True)
print("\n重复分数升序正确性测试：")


#用列表在字典中提取average
def G_averages(records):#
    averages = []
    for student in records:
        averages.append(student["average"])
    return averages
expected_up = [70, 80, 80, 90]
print("冒泡：",G_averages(test_bubble) == expected_up)
print("选择：",G_averages(test_selection) == expected_up)
print("插入：",G_averages(test_insertion) == expected_up)
print("归并：",G_averages(test_merge) == expected_up)

#制造随机数据
def create_test_data(size):
    data = []
    for i in range(size):
        student = {
            'student_id':'R'+str(i),
            'average':random.randint(0,100)
            }
        data.append(student)
    return data


size_values = []
bubble_times = []
selection_times = []
insertion_times = []
merge_times = []
sorted_times = []

#提取字典中的average
def get_average(student):
    return student['average']

sizes = [100,500,1000]
for size in sizes:
    print("\n数据数量：",size)
    test_data = create_test_data(size)

    start = time.perf_counter()
    bubble_sort(test_data, True)
    end = time.perf_counter()
    bubble_time = end - start
    print("冒泡排序：",bubble_time ,"秒")

    start = time.perf_counter()
    selection_sort(test_data, True)
    end = time.perf_counter()
    selection_time = end - start
    print("选择排序：",selection_time,"秒")

    start = time.perf_counter()
    insertion_sort(test_data, True)
    end = time.perf_counter()
    insertion_time = end - start
    print("插入排序:",insertion_time,"秒")

    start = time.perf_counter()
    merge_sort(test_data, True)
    end = time.perf_counter()
    merge_time = end - start
    print("归并排序：",merge_time,"秒")

    start = time.perf_counter()
    sorted(test_data, key=get_average)
    end = time.perf_counter()
    sorted_time = end - start
    print("内置sorted：",sorted_time,"秒")

    size_values.append(size)
    bubble_times.append(bubble_time)
    selection_times.append(selection_time)
    insertion_times.append(insertion_time)
    merge_times.append(merge_time)
    sorted_times.append(sorted_time)




#绘图
import matplotlib.pyplot as plt
#各班平均分柱状图
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.figure(figsize = (8,5))
bars = plt.bar(class_average.index,class_average['average'],color = ['skyblue'])
plt.title('各班平均分')
plt.xlabel('班级')
plt.ylabel('平均分')
plt.bar_label(bars,fmt = '%.2f')
plt.tight_layout()
plt.savefig('class_average.png',dpi = 300)
#plt.show()
plt.close()

#学生分布直方图
plt.figure(figsize=(8, 5))
plt.hist(df["average"],bins=8,color="skyblue",edgecolor="black")
plt.title("学生平均分分布")
plt.xlabel("平均分")
plt.ylabel("学生人数")
plt.tight_layout()
plt.savefig("average_distribution.png",dpi=300)
#plt.show()
plt.close()


#运行时间折线图
plt.figure(figsize=(9, 6))
plt.plot(
    size_values,
    bubble_times,
    marker="o",
    label="冒泡排序"
)
plt.plot(
    size_values,
    selection_times,
    marker="o",
    label="选择排序"
)
plt.plot(
    size_values,
    insertion_times,
    marker="o",
    label="插入排序"
)
plt.plot(
    size_values,
    merge_times,
    marker="o",
    label="归并排序"
)
plt.plot(
    size_values,
    sorted_times,
    marker="o",
    label="内置sorted"
)
plt.title("不同数据规模的排序时间")
plt.xlabel("数据数量")
plt.ylabel("运行时间（秒）")
plt.grid(
    linestyle="--",
    alpha=0.5
)
plt.legend()
plt.tight_layout()
plt.savefig(
    "sorting_time.png",
    dpi=300
)
plt.close()



#保存清洗数据
output_df = df.copy()
output_df['average'] = output_df['average'].round(2)

output_df.to_csv(
    'clean_students.csv',
    index = False,
    encoding = 'utf-8-sig'
    )

#保存升序结果
merge_up_df = pd.DataFrame(merge_up)
merge_up_df['average'] = merge_up_df['average'].round(2)
merge_up_df.to_csv(
    'students_up.csv',
    index = False,
    encoding = 'utf-8-sig'
    )


#保存降序结果
merge_down_df = pd.DataFrame(merge_down)
merge_down_df['average'] = merge_down_df['average'].round(2)
merge_down_df.to_csv(
    'students_down.csv',
    index = False,
    encoding = 'utf-8-sig'
    )

#保存班级汇总
class_average_df = class_average.reset_index()
class_average_df = class_average_df.round(2)
class_average_df.to_csv(
    "class_summary.csv",
    index=False,
    encoding="utf-8-sig"
)
