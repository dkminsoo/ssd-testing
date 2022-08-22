import os


def func_check():
    log = os.system("python3 ./loggerReader2.py")
    counter = 0
    with open("log_dict.txt") as f:
        file_read = f.read()
        for i in range(0, len(file_read) - 1):
            if file_read[i] == ":":
                counter += 1
        return counter


cmd_format_list = ["nvme read /dev/nvme0n1 -s {start_block} -c {block_count} -z {data_size} -d readbuf"]
count = 0

start_block_var = 1
block_count_var = 1
data_size_var = 1

loop = True
iteration = 0
new = True
input_choice = 1

for cmd_format in cmd_format_list:

    while start_block_var < 1024 * 5:
        while block_count_var < 1024 * 5:
            while data_size_var < 1024 * 5:

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
                else:
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


#__________TO DO
"""
THINK OF WAY TO CHANGE 3 INPUTS BASED ON BEHAVIOR
TRY WITH FOR LOOP FOR ALL POSSIBLE WAYS
"""