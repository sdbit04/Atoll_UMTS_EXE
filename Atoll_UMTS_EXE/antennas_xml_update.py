import os
import xml.etree.ElementTree as et

def replace_field_name(OrigNew_dict, xml_path_in, xml_path_out):
    with open(xml_path_in, "r") as file:
        serial = file.read()
        for key in OrigNew_dict.keys():
            serial = serial.replace(key, OrigNew_dict.get(key)) # This return a string that need to be stored
    with open(xml_path_out, "w") as file_out:
        file_out.write(serial)


def revert_field_name(NewOrig_dict, xml_path_in, xml_path_out):
    with open(xml_path_in, "r") as file:
        serial = file.read()
        for key in NewOrig_dict.keys():
            serial = serial.replace(key, NewOrig_dict.get(key)) # This return a string that need to be stored
    with open(xml_path_out, "w") as file_out:
        file_out.write(serial)


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


def beautify_family_attr(origReplacement, replacementOrig, xml_dir_in, xml_dir_out):
    _xml_dir_in = xml_dir_in
    _xml_dir_out = xml_dir_out
    _xml_path_in = os.path.realpath(os.path.join(_xml_dir_in, "antennas.xml"))
    _xml_path_out = os.path.realpath(os.path.join(_xml_dir_out, "antennas.xml"))
    _xml_path_out_tmp = os.path.realpath(os.path.join(_xml_dir_out, "antennas_tmp.xml"))

    replace_field_name(origReplacement, _xml_path_in, _xml_path_out_tmp)
    xml_tree_object = et.parse(_xml_path_out_tmp)
    data = xml_tree_object.find("rs_data/rs_insert")    # Find immediate parent node
    rows = data.findall('z_row')    # File all child rows under the data node
    antenna_n_family = {}

    for row in rows:
        family_old = str(row.get("NAME"))
        family_new = derive_family_from_name(family_old)
        row.set("FAMILY", family_new)
        antenna_n_family[row.get("NAME")] = row.get("FAMILY") # Adding KV pair into directory
    xml_tree_object.write(_xml_path_out_tmp)  # TODO: Changed path to the temp output antennas.xml
    revert_field_name(replacementOrig, _xml_path_out_tmp, _xml_path_out) # TODO: at this step we create exact output we need
    return antenna_n_family


def create_profile_translator(xml_dir_in, xml_dir_out, antenna_n_family_dir):
    _xml_dir_in = xml_dir_in
    _xml_dir_out = xml_dir_out
    profiletranslator_path_out = os.path.realpath(os.path.join(_xml_dir_out, "PROFILESTRANSLATOR03.txt"))
    antenna_n_family = antenna_n_family_dir
    antenna_k = antenna_n_family.keys()
    utransmitter_file = os.path.realpath(os.path.join(_xml_dir_in, "utransmitters.xml"))
    utransmitter_file_out = os.path.realpath(os.path.join(_xml_dir_out, "utransmitters_tmp.xml"))
    with open(profiletranslator_path_out, 'w') as profiletranslator:
        print("Name\tMatch", file=profiletranslator)
    utransmitter_fields = {"rs:data": "rsdata", "z:row": "zrow"}
    replace_field_name(utransmitter_fields, utransmitter_file, utransmitter_file_out)
    utransmitter_tree = et.parse(utransmitter_file_out)
    rows = utransmitter_tree.findall("rsdata/zrow")
    uniq_antennas = set()
    for row in rows:
        uniq_antennas.add(row.get("ANTENNA_NAME"))

    with open(profiletranslator_path_out, 'a') as profiletranslator:
        for antenna in uniq_antennas:
            if antenna in antenna_k:
                print("{}\t{}/{}".format(antenna, antenna_n_family[antenna], antenna), file=profiletranslator)


if __name__ == "__main__":
    origReplacement = {"CUSTOM_NEMS_ANTENNA_NAME": "FAMILY", "z:row": "z_row", "rs:data": "rs_data",
                       "rs:insert": "rs_insert", "rs:nullable": "rs_nullable", "rs:fixedlength": "rs_fixedlength",
                       "s:extends": "s_extends", "s:Schema": "s_Schema", "s:ElementType": "s_ElementType",
                       "s:AttributeType": "s_AttributeType", "s:datatype": "s_datatype", "rs:updatable": "rs_updatable",
                       "dt:type": "dt_type", "rs:number": "rs_number", "rs:write": "rs_write",
                       "dt:maxLength": "dt_maxLength", "rs:precision": "rs_precision", "rs:maybenull": "rs_maybenull",
                       "rs:long": "rs_long", "xmlns:s": "xmlns_s", "xmlns:dt": "xmlns_dt", "xmlns:rs": "xmlns_rs",
                       "xmlns:z": "xmlns_z"}
    replacementOrig = {"z_row": "z:row", "rs_data": "rs:data", "rs_insert": "rs:insert", "rs_nullable": "rs:nullable",
                       "rs_fixedlength": "rs:fixedlength", "s_extends": "s:extends", "s_Schema": "s:Schema",
                       "s_ElementType": "s:ElementType", "s_AttributeType": "s:AttributeType",
                       "s_datatype": "s:datatype", "rs_updatable": "rs:updatable", "dt_type": "dt:type",
                       "rs_number": "rs:number", "rs_write": "rs:write", "dt_maxLength": "dt:maxLength",
                       "rs_precision": "rs:precision", "rs_maybenull": "rs:maybenull", "rs_long": "rs:long",
                       "xmlns_s": "xmlns:s", "xmlns_dt": "xmlns:dt", "xmlns_rs": "xmlns:rs", "xmlns_z": "xmlns:z"}
    xml_dir_in = ""
    xml_dir_out = ""
    with open("antennas_xml_update.properties", "r") as properties:
        for line in properties.readlines():
            if str(line)[0:10] == "xml_dir_in":
                xml_dir_in = str(line).split(sep="=")[1].rstrip("\n")

            if str(line)[0:11] == "xml_dir_out":
                xml_dir_out = str(line).split(sep="=")[1].rstrip("\n")

    print("input dir=" + xml_dir_in)
    print("output dir=" + xml_dir_out)

    if not os.path.isdir(xml_dir_in):
        print("Please provide valid input directory")
        exit()
    if not os.path.isdir(xml_dir_out):
        print("Please provide valid output directory")
        exit()

    antenna_n_family = beautify_family_attr(origReplacement,replacementOrig,xml_dir_in, xml_dir_out)
    create_profile_translator(xml_dir_in, xml_dir_out, antenna_n_family)
