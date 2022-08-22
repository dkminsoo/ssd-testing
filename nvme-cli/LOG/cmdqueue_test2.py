import os


def func_check():
    log = os.system("python3 ./loggerReader2.py")
    with open("log_dict.txt") as f:
        file_read = f.read()



cmd_format_list = ["nvme write /dev/nvme0n1 -s {input1} -c {input2} -z {input3} -d writebuf",
                   "nvme read /dev/nvme0n1 -s {input4} -c {input5} -z {input6} -d readbuf"]
count = 0




iteration = 0
input_choice = 1



for i in range(0, 1024*5, 1000):
    for j in range(0, 1024*5, 1000):
        for k in range(1000, 1024*5, 1000):
            for l in range(0, 1024*5, 1000):
                for m in range(0, 1024*5, 1000):
                    for n in range(1000, 1024 * 5, 1000):

                        input1 = i
                        input2 = j
                        input3 = k
                        input4 = l
                        input5 = m
                        input6 = n

                        cmd1 = cmd_format_list[0].format(input1=input1, input2=input2, input3=input3)
                        cmd2 = cmd_format_list[1].format(input4=input4, input5=input5, input6=input6)
                        result1 = os.system(cmd1)
                        result2 = os.system(cmd2)
                        print(result1)
                        print(result2)
                        iteration += 1
                        print("Iteration: " + str(iteration))
                        print(cmd1 + " " + cmd2)
                        log = os.system("python3 ./loggerReader2.py")


'''
loop = True
iteration = 0
new = True
input_choice = 1

for cmd_format in cmd_format_list:

    for i in range(0, 1024*5, 500):
        for j in range(0, 1024*5, 500):
            for k in range(0, 1024*5, 500):

                start_block_var = i
                block_count_var = j
                data_size_var = k

                cmd = cmd_format.format(start_block=start_block_var, block_count=block_count_var, data_size=data_size_var)
                result = os.system(cmd)
                print(result)
                iteration += 1
                print("Iteration: " + str(iteration))
                print(cmd)
                new_count = func_check()
                if new_count > count:
                    print("COUNT: " + str(new_count))
                    count = new_count
                    new = True
                # else:
                    """
                    if start_block_var < 1024 * 4 and input_choice == 1:
                        print("block 1")
                        if new:
                            start_block_var = start_block_var + 15
                        else:
                            start_block_var = start_block_var * 5
                        input_choice = 2
                    elif block_count_var < 1024 * 4 and input_choice == 2:
                        print("block 2")
                        if new:
                            block_count_var = block_count_var + 15
                        else:
                            block_count_var = block_count_var * 5
                        if data_size_var >= 1024 * 4:
                            input_choice = 1
                        else:
                            input_choice = 3
                    elif data_size_var < 1024 * 4 and input_choice == 3:
                        print("block 3")
                        if new:
                            data_size_var = data_size_var + 15
                        else:
                            data_size_var = data_size_var * 5


                    else:
                        print("block 4")
                        loop = False

                    print("start: " + str(start_block_var) + ", count: " + str(block_count_var) + ", size: " + str(data_size_var) + ", input choice: " + str(input_choice))

                    new = False
                    # ...
                    """

'''
#__________TO DO
"""
THINK OF WAY TO CHANGE 3 INPUTS BASED ON BEHAVIOR
TRY WITH FOR LOOP FOR ALL POSSIBLE WAYS
"""