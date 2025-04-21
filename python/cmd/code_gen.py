ori = """BonusChestEnabled              bool           `nbt:"bonusChestEnabled"`
	BonusChestSpawned              bool           `nbt:"bonusChestSpawned"`"""

vaild = """    bonus_chest_enabled: bool = False
    bonus_chest_spawned: bool = False"""

oriP = []
for i in ori.split("\n"):
    oriP.append(i.split())

vaildP = []
for i in vaild.split("\n"):
    vaildP.append(i.split(":")[0].replace(" ", "", -1))

for i in range(len(oriP)):
    gg = oriP[i][-1].split('`nbt:"')
    if len(gg) == 1:
        match oriP[i][1]:
            case "bool":
                print('"' + oriP[i][0] + '": nbtlib.tag.Byte(self.' + vaildP[i] + "),")
            case "int32":
                print('"' + oriP[i][0] + '": nbtlib.tag.Int(self.' + vaildP[i] + "),")
            case "int64":
                print('"' + oriP[i][0] + '": nbtlib.tag.Long(self.' + vaildP[i] + "),")
            case "float32":
                print('"' + oriP[i][0] + '": nbtlib.tag.Float(self.' + vaildP[i] + "),")
            case "string":
                print(
                    '"' + oriP[i][0] + '": nbtlib.tag.String(self.' + vaildP[i] + "),"
                )
            case _:
                print(oriP[i][1])
    else:
        match oriP[i][1]:
            case "bool":
                print('"' + gg[1][:-2] + '": nbtlib.tag.Byte(self.' + vaildP[i] + "),")
            case "int32":
                print('"' + gg[1][:-2] + '": nbtlib.tag.Int(self.' + vaildP[i] + "),")
            case "int64":
                print('"' + gg[1][:-2] + '": nbtlib.tag.Long(self.' + vaildP[i] + "),")
            case "float32":
                print('"' + gg[1][:-2] + '": nbtlib.tag.Float(self.' + vaildP[i] + "),")
            case "string":
                print(
                    '"' + gg[1][:-2] + '": nbtlib.tag.String(self.' + vaildP[i] + "),"
                )
            case _:
                print(oriP[i][1])

print("######")

for i in range(len(oriP)):
    gg = oriP[i][-1].split('`nbt:"')
    if len(gg) == 1:
        match oriP[i][1]:
            case "bool":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = bool(compound["'
                    + oriP[i][0]
                    + '"]) # type: ignore'
                )
            case "int32" | "int64":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = int(compound["'
                    + oriP[i][0]
                    + '"]) # type: ignore'
                )
            case "float32":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = float(compound["'
                    + oriP[i][0]
                    + '"]) # type: ignore'
                )
            case "string":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = str(compound["'
                    + oriP[i][0]
                    + '"]) # type: ignore'
                )
            case _:
                print(oriP[i][1])
    else:
        match oriP[i][1]:
            case "bool":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = bool(compound["'
                    + gg[1][:-2]
                    + '"]) # type: ignore'
                )
            case "int32" | "int64":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = int(compound["'
                    + gg[1][:-2]
                    + '"]) # type: ignore'
                )
            case "float32":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = float(compound["'
                    + gg[1][:-2]
                    + '"]) # type: ignore'
                )
            case "string":
                print(
                    "        "
                    + "self."
                    + vaildP[i]
                    + ' = str(compound["'
                    + gg[1][:-2]
                    + '"]) # type: ignore'
                )
            case _:
                print(oriP[i][1])
