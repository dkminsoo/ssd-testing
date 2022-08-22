with open("log_dict.txt") as r:
    with open("logSorted.txt") as w:
        while True:
            line = r.readline()
            if line.indexOf("-s") > 0:
