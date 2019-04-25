def derive_family_from_name(name=" "):
    name_split = name.split("_")
    new_family = ""
    if name_split[-1] == "GSM":
        if len(str(name_split[-2])) == 2:
            new_family = name[0:-7]
        else:
            new_family = name
    elif len(str(name_split[-1])) == 2:
        if name_split[-1].isnumeric():
            new_family = name[0:-3]
        elif str(name_split[-1])[-2] == "-":
            new_family = name[0:-3]
    elif len(str(name_split[-1])) == 3:
        if str(name_split[-1])[-1] == "T":
            new_family = name[0:-4]
        elif str(name_split[-1])[-3] == "-":
            new_family = name[0:-4]
        else:
            new_family = name
    else:
        new_family = name
    return new_family

# "CELLMAX-O-CPUSE_1800_DP_00"
# "CELLMAX-O-CPUSE_1800_DP_-03"
# "CELLMAX-O-CPUSE_1800_DP_00_GSM"
# "CELLMAX-O-CPUSE_1800_DP_00T"
# "CELLMAX-O-CPUSE_1800_DP_-1"
# "2600_80010248"
# 2600_80010465_GSM

Family  = derive_family_from_name("U900_80010249_900")
print(Family)