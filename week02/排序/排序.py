#归并排序 用了递归 是稳定排序 时间复杂度O(nlogn)
def merge(left,right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])#当一个已经塞完时把另外一边的全部塞进去
    result.extend(right[j:])
    return result
def merge_sort(numbers):
    if len(numbers) <= 1:#终止条件
        return numbers.copy()
    mid = len(numbers)//2#两个杠是整除
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])
    return merge(left, right)


#插入排序是稳定排序 若>改为>=则不稳定 时间复杂度O(n方)
def insertion_sort(numbers):
    result = numbers.copy()
    n =len(result)
    for i in range(1,n):
        current = result[i]
        j = i - 1
        while j >= 0 and result[j]>current:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result



#选择排序是不稳定排序 时间复杂度O(n方)
def selection_sort(numbers):
    result = numbers.copy()
    n =len(result)
    for i in range(n-1):
       min1 = i
       for j in range(i+1,n):
            if result[j] < result[min1]:
                min1 = j
       switch = result[min1]
       result[min1] = result[i]
       result[i] = switch
    return result



#冒泡排序是稳定排序 两层循环 时间复杂度为O(n方)
def bubble_sort(numbers):
    result = numbers.copy()#不用copy只会改名 
    n =len(result)
    for i in range(0,n-1):
        for j in range(0,n-i-1):
            if result[j]>result[j+1]:
                switch = result[j]
                result[j] = result[j+1]
                result[j+1] = switch
    return result



# numbers = []
# n = int(input('请输入个数'))
# for i in range(n):
#     number = int(input())
#     numbers.append(number)
# print(bubble_sort(numbers))


#算法测试
import time
# start = time.perf_counter()
# end = time.perf_counter()
# used_time = end - start
# print(used_time)

import random
numbers = []
for i in range(2000):
    number = random.randint(1,10000)
    numbers.append(number)

start = time.perf_counter()
bubble_result = bubble_sort(numbers)
end = time.perf_counter()
bubble_time = end - start


start = time.perf_counter()
selection_result = selection_sort(numbers)
end = time.perf_counter()
selection_time = end - start


start = time.perf_counter()
insertion_result = insertion_sort(numbers)
end = time.perf_counter()
insertion_time = end - start


start = time.perf_counter()
merge_result = merge_sort(numbers)
end = time.perf_counter()
merge_time = end - start

print("冒泡排序用时：", bubble_time, "秒")
print("选择排序用时：", selection_time, "秒")
print("插入排序用时：", insertion_time, "秒")
print("归并排序用时：", merge_time, "秒")


