# n!階乘
def factorial(num):
    tmp=num
    for i in range(num-1,0,-1):
        tmp*=i
    return tmp

#計算組合數 C n取m
def combination(n,m):
    nn = factorial(n)
    mm = factorial(m)
    m_d_n = factorial(n-m)
    result = nn/(mm*m_d_n)
    return result

if __name__ == '__main__':
    input_num = [int(i) for i in input('請輸入兩個以","隔開的數字，計算 n取m :').split(',')]
    result = int(combination(input_num[0],input_num[1]))
    print(result)