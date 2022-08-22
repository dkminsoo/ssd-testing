import json

log_dict = {}
key2b = []
param = ""
keyList = []

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
                if key not in log_dict:
                    log_dict[key] = set()
                log_dict[key].add(param)
            key = ""
            keyList = []
            param = data["param"]
        else:
            keyList.append(data["id"])
            param = param + "\n" + data["msg"]
    if param != "":
        keyList.sort()
        key = ""
        for i in keyList:
            key += "_" + str(i)
        if key not in log_dict:
            log_dict[key] = set()

        log_dict[key].add(param)

# print(log_dict)
print("Number of keys: " + str(len(log_dict.keys())))

# Add to file log_dict.txt
with open("log_dict.txt", "w") as f:
    f.write(str(log_dict))
