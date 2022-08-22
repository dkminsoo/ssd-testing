import json

log_dict = {}
key2b = []
param = ""
keyList = []
success = False

with open("logger.txt") as f:
    while True:
        line = f.readline()
        if not line: 
            break
        data = json.loads(line)
        if data["type"] == "start_signal":
            if param != "":
                keyList.sort()
                key = ""
                for i in keyList:
                    key += "_" + str(i)
                if success:
                    key += "_SUCCESS"
                if key not in log_dict:
                    log_dict[key] = []
                log_dict[key].append(param)
            key = ""
            keyList = []
            success = False
            param = data["param"]
        else:
            keyList.append(data["id"])
            if "msg" in data:
                param = param + "\n" + data["msg"]
            if "result" in data:
                success = True
    if param != "":
        keyList.sort()
        key = ""
        for i in keyList:
            key += "_" + str(i)
        if success:
            key += "_SUCCESS"
        if key not in log_dict:
            log_dict[key] = []
        success = False
        log_dict[key].append(param)

# print(log_dict)
print("Number of keys: " + str(len(log_dict.keys())))

# Add to file log_dict.txt
with open("log_dict.txt", "w") as f:
    # for letter in str(log_dict):
    #     f.write(letter)
    #     if letter == "," or letter == ':':
    #         f.write('\n')
    for k,v in log_dict.items():
        f.write("----PATTERN----" + k + "\n")
        for strings in v:
            f.write(strings + '\n')
