import linecache
import pefile


def transform(str):
    sum = 0
    if ord(str[5]) >= 65:
        sum += (ord(str[5]) - 55) * 256
    else:
        sum += int(str[5]) * 256
    if ord(str[6]) >= 65:
        sum += (ord(str[6]) - 55) * 16
    else:
        sum += int(str[6]) * 16
    if ord(str[7]) >= 65:
        sum += ord(str[7]) - 55
    else:
        sum += int(str[7])
    return sum

# 删除int 3
with open('c:\\users\\narthil\\source\\test\\disasm_test.txt', 'w') as f:
    f.write(''.join([line for line in open('c:\\users\\narthil\\source\\test\\disasm.txt').readlines() if 'int' not in line]))

# 继删除int 3之后的优化，删除了不必要的空行和机器码
g = open('c:\\users\\narthil\\source\\test\\disasm_test.txt')
optimize = []
for line in g:
    # 去除空行、汇编指令前的文件说明和汇编指令后的summary
    if str(line).find('004') != -1:
        optimize.append(line[:11]+line[30:])

call = open('c:\\users\\narthil\\source\\test\\disasm_call.txt', 'w')

call.write('================')
# 按函数的起始地址分块
call.write(str(str(optimize[0]).split(':', 1)[0][2:]))
call.write('================\n')
# 获取函数个数
fun_list = []
fun_list.append(str(str(optimize[0]).split(':', 1)[0][2:]))
for i, item in enumerate(optimize):
    item = item[:16] + item[22:]
    call.write(str(item))
    # 按照ret判断下一个函数的入口
    if str(item).find('ret') != -1:
        if i + 1 < len(optimize):
            call.write('\n\n================')
            call.write(str(str(optimize[i+1]).split(':', 1)[0][2:]))
            # # 如果地址小于entrypoint,则判断其为函数的入口地址
            # if str(str(optimize[i+1]).split(':', 1)[0][2:]) < eop:
            #     fun_list.append(str(str(optimize[i+1]).split(':', 1)[0][2:]))
            call.write('================\n')

call.close()

# 从这里开始是对导入表的操作
file_path = r'c:\\users\\narthil\\source\\test\\test.exe'
call = open('c:\\users\\narthil\\source\\test\\disasm_call.txt')
test = open('test.txt', 'w')

pe = pefile.PE(file_path)
sections = pe.sections

# =====【来源于OPTIONAL_HEADER的数据】=====
OPTIONAL_HEADER = pe.OPTIONAL_HEADER
# --------------------------------------
image_base = OPTIONAL_HEADER.ImageBase
# --------------------------------------

# =====【导入函数表】=====================
imported_funcitons = {}
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for dll in pe.DIRECTORY_ENTRY_IMPORT:
        for symbol in dll.imports:
            imported_funcitons[hex(symbol.address)] = {'name': symbol.name.decode(), 'dll': dll.dll}

# entry_point
eop = '00' + str(hex(OPTIONAL_HEADER.AddressOfEntryPoint + image_base))[2:]

# =====【来源于.text节的数据】============
text = sections[0]
# -------------------------------------
text_va = text.VirtualAddress
text_vs = text.Misc_VirtualSize
text_data = text.get_data()[:text_vs]

# =====【来源于.rdata节的数据】===========
rdata = sections[2]
# -------------------------------------
rdata_va = rdata.VirtualAddress
rdata_vs = rdata.Misc_VirtualSize
rdata_data = rdata.get_data()[:rdata_vs]

rdata_data_str = str(rdata_data)
r_len = len(rdata_data_str)
rdata_data_str = rdata_data_str[2:r_len-1]


# 全局变量在此
tmp = ''

for i in range(len(rdata_data_str)):
    if rdata_data_str[i] == 'x' and rdata_data_str[i+1] == '0':
        continue
    elif rdata_data_str[i] == '0' and rdata_data_str[i-1] == 'x':
        continue
    elif rdata_data_str[i] == '0' and rdata_data_str[i-1] == '0':
        continue
    else:
        tmp += rdata_data_str[i]

tmp = tmp.split('\\')

global_val = []

for i in tmp:
    if i == '':
        continue
    else:
        global_val.append(i)

print(global_val)

api_fun = {}
for line in call:
    # print(line)
    if str(line).find('ds') != -1:
        api_adrr = str(line).split(':')[2][3:9].lower()
        name = imported_funcitons['0x' + api_adrr]['name']
        # 用获取到的外部函数名替换dword ptr
        line = str(line).replace(str(line).split('call  ')[1], name)
        test.write(line + '\n')
    else:
        test.write(line)

test.close()

fun_list = []
api_list = []
call_list = []
real_call_list = []

api_index = 0
fun_index = 0
f = open('test.txt', 'r')
for line in f:
    if str(line).find('call') != -1:
        call_ins = str(line).split('call')
        if call_ins[1].find('[') != -1:
            api_list.append(call_ins[0][2:10] + ' -> ' + call_ins[1][12:])
            call_list.append(api_list[api_index])
            api_index += 1
        else:
            fun_list.append(call_ins[0][2:10] + ' -> ' + call_ins[1][2:])
            call_list.append(fun_list[fun_index])
            fun_index += 1

# 获取所有的内部函数地址
fun_list = []
for index in call_list:
    if '400' in index.split(' -> ')[1]:
        fun_list.append(index.split(' -> ')[1][:8])

fun_list = list(set(fun_list))
fun_list.sort()
real_call_list = []

wm = open('real_call_list.txt', "w")
for x in call_list:
    if transform(x.split(' -> ')[0]) >= transform(eop.upper()):
        # 主函数内调用的内部函数用main替换
        x = x.replace(x.split(' -> ')[0], '"main"')
        real_call_list.append(x)
    else:
        temp = x.split(' -> ')[0]
        for i in range(len(fun_list) - 1):
            if transform(fun_list[i]) < transform(temp) < transform(fun_list[i+1]):
                # 函数间的调用也用函数的入口地址替换
                x = x.replace(x.split(' -> ')[0], fun_list[i])
                real_call_list.append(x)

# 去掉重复的
real_call_list = list(set(real_call_list))

for i in real_call_list:
    wm.write(i)

wm.close()

file = linecache.getlines('test.txt')
par_num = ''
par_list = []
local_num = 0
local_var = []
fun_tmp = []
for index in range(len(file)):
    if 'call' in file[index]:
        for i in fun_list:
            par_num = ''
            if file[index][18:26] == i:
                temp = file[index+1][22:]
                # print(temp)
                for j in temp:
                    if j != '\n':
                        par_num += j
                    else:
                        break
                if 'h' in par_num:
                    par_num = ord(par_num[1]) - 55
                par_list.append('function ' + i + ' has ' + str(int(int(par_num) / 4)) + ' parameters')

for index in range(len(file)):
    if file[index] == '\n':
        continue
    if 'ret' not in file[index]:
        fun_tmp.append(file[index])
    else:
        for i in fun_tmp:
            if '[ebp-' in i:
                local_var.append(i.split('[')[1].split(']')[0])
                # print(local_var)
        local_var = list(set(local_var))
        local_num = len(local_var)
        print('function ' + fun_tmp[0][16:24] + ' has ' + str(local_num) + ' local variable.')
        fun_tmp = []
        local_var = []
        local_num = 0

par_list = list(set(par_list))

print(par_list)


# 这里开始分片
jcc = ['jz', 'je', 'jnz', 'jne', 'js', 'jns', 'jp', 'jpe', 'jnp', 'jpo', 'jo', 'jno', 'jc',
       'jb', 'jnae', 'jnc', 'jnb', 'jae', 'jbe', 'jna', 'jnbe', 'ja', 'jl', 'jnge', 'jnl',
       'jge', 'jle', 'jng', 'jnle', 'jg', 'jmp']
address = []    # 存储每一片指向的地址
all = []        # 存储每一行的地址
pieces = []     # 存储每一片包括的地址
j = open('jcc.txt', 'w')
depart = open('test.txt', 'r')
flag = 0

for line in depart:
    flag = 0
    for index in jcc:
        if str(line).find(index) != -1:
            flag = 1
            break
    if flag:
        if 'dword' not in line:
            address.append(str(line)[18:26])
        else:
            jump_table = str(line)[35:43]   # 这里得到了switch-case跳转表的地址

lines = linecache.getlines('test.txt')
for index in range(len(lines)):
    flag1 = 0
    flag2 = 0
    for i in jcc:
        if lines[index].find(i) != -1:
            flag1 = 1
            break
    for i in range(len(address)):
        if lines[index][2:10] == address[i]:
            flag2 = 1
            break
    if flag1 == 1:
        j.write(lines[index])
        j.write('----------------------------------------\n')
    elif flag1 == 0 and flag2 == 1:
        j.write('----------------------------------------\n')
        j.write(lines[index])
    else:
        j.write(lines[index])

depart.close()
j.close()

j = open('jcc.txt', 'r')
p = open('pieces.txt', 'w')
lines = linecache.getlines('jcc.txt')
for index in range(len(lines)):
    if lines[index] == '----------------------------------------\n' and lines[index - 1] == '----------------------------------------\n':
        continue
    p.write(lines[index])

j.close()
p.close()

# 分片结束，这里开始画流程图
cf = open('control_flow.txt', 'w')
add_sum = []
pie_sum = []

# 判断jcc指向的地址在哪一片内
for index in address:
    add_sum.append(transform(index))

for index in pieces:
    pie_sum.append(transform(index))

p = linecache.getlines('pieces.txt')
count_case = 0
for index in range(len(p)):
    if '===========' in p[index]:
        temp = p[index].split('================')[1]
        # temp = str(temp)
        if temp == '0040048B':
            for j in range(len(p)-index):
                if 'add   byte ptr' in p[index + j]:
                    count_case += 1
            break

# 处理机器码
mc = open('all.txt')
all_add = []
for line in mc:
    if line[2:7] != '00400':
        continue
    else:
        all_add.append(line)

switch_case = []
count_add = 0
machine_code = []
scadd = []
for i in range(len(all_add)):
    if all_add[i][2:10] > '0040048C':
        machine_code.append(all_add[i - 1][12:59])
        begin = ord(jump_table[7]) - 55

count_2 = 0
for i in range(len(machine_code)):
    machine_code[i] = machine_code[i].split(' ')
    if i == 0:
        switch_case.append(machine_code[i][begin:])
    else:
        for count_2 in range(0, 16, 4):
            switch_case.append(machine_code[i][count_2:count_2+4])
            if len(switch_case) == count_case:
                break

for i in range(count_case):
    temp = ''
    for j in range(len(switch_case[i])):
        temp += switch_case[i][len(switch_case[i]) - 1 - j]
    scadd.append(temp)          # 这里的scadd就是最终每一个case跳转到的地址

cf = open('control_flow.txt', 'w')

pie = linecache.getlines('pieces.txt')
entry = []      # 每一片的入口
exits = []       # 每一片的出口
jmp = []
entry.append('  004002f0')

for index in range(len(pie)):
    if '---------' in pie[index]:
        exits.append(pie[index - 1])
        entry.append(pie[index + 1])

exits.append(pie[len(pie)-1])

li = []

for index in range(len(entry)):
    temp1 = entry[index][2:10]  # 入口
    temp2 = exits[index]        # 包含出口的那一行
    flag = 0
    for k in scadd:
        if temp1 == k:
            flag = 1
            break
    if index < len(entry) - 1 and flag == 0:
        li.append('"' + temp1 + '"' + ' -> ' + '"' + entry[index+1][2:10] + '"' + '\n')
    for item in jcc:
        if item in temp2:
            if 'jmp   dword ptr' not in temp2:
                temp = temp2[18:26]
                li.append('"' + temp1 + '"' + ' -> ' + '"' + temp + '"' + '\n')

li = list(set(li))

for index in li:
    cf.write(index)
cf.close()