import os


def func_check():
    log = os.system("python3 ./loggerReader2.py")



cmd_format_list = ["nvme resv-acquire /dev/nvme0n1 -n {input6} -c {input1} -p {input2} -i {input3} -a {input4} -t {input5}"]

iteration = 0

for cmd_format in cmd_format_list:
    for n in range(0, 1024 * 1, 500):
        for i in range(0, 1024 * 1, 500):
            for j in range(0, 1024 * 1, 500):
                for k in range(0, 1024 * 1, 500):
                    for l in range(0, 1024 * 1, 500):
                        for m in range(0, 1024 * 1, 500):
                            input1 = i
                            input2 = j
                            input3 = k
                            input4 = l
                            input5 = m
                            input6 = n

                            cmd = cmd_format.format(input6=input6, input1=input1, input2=input2, input3=input3, input4=input4, input5=input5)
                            result = os.system(cmd)
                            print(result)
                            iteration += 1
                            print("Iteration: " + str(iteration))
                            print(cmd)

new_count = func_check()
