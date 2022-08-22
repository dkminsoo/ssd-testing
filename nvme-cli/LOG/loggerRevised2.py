import os


def func_check():
    log = os.system("python3 ./loggerReader2.py")



cmd_format1 = "nvme write /dev/nvme0n1 -s {input1} -c {input2} -z {input3} -d readbuf"
cmd_format2 = "nvme read /dev/nvme0n1 -s {input4} -c {input5} -z {input6} -d readbuf"

iteration = 0



for i in range(0, 1024 * 1, 500):
    for j in range(0, 1024 * 1, 500):
        for k in range(0, 1024 * 1, 500):
            for l in range(0, 1024 * 1, 500):
                for m in range(0, 1024 * 1, 500):
                    for n in range(0, 1024 * 1, 500):
                        input1 = i
                        input2 = j
                        input3 = k
                        input4 = l
                        input5 = m
                        input6 = n

                        cmd1 = cmd_format1.format(input1=input1, input2=input2, input3=input3)
                        result1 = os.system(cmd1)
                        cmd2 = cmd_format2.format(input4=input4, input5=input5, input6=input6)
                        result2 = os.system(cmd2)
                        print(result1)
                        print(result2)
                        iteration += 1
                        print("Iteration: " + str(iteration))
                        print(cmd1)
                        print(cmd2)

new_count = func_check()
