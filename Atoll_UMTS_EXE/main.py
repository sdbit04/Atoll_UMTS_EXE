
from Atoll_UMTS_EXE.antennas_xml_update import *
import os

origReplacement = {"CUSTOM_NEMS_ANTENNA_NAME": "FAMILY", "z:row":"z_row","rs:data" :"rs_data","rs:insert" : "rs_insert","rs:nullable":"rs_nullable", "rs:fixedlength":"rs_fixedlength", "s:extends":"s_extends", "s:Schema":"s_Schema", "s:ElementType":"s_ElementType","s:AttributeType":"s_AttributeType","s:datatype":"s_datatype", "rs:updatable":"rs_updatable","dt:type":"dt_type","rs:number":"rs_number","rs:write":"rs_write","dt:maxLength":"dt_maxLength", "rs:precision":"rs_precision","rs:maybenull":"rs_maybenull", "rs:long":"rs_long", "xmlns:s":"xmlns_s", "xmlns:dt":"xmlns_dt","xmlns:rs":"xmlns_rs", "xmlns:z":"xmlns_z"}
replacementOrig = {"z_row":"z:row","rs_data":"rs:data","rs_insert" : "rs:insert","rs_nullable":"rs:nullable", "rs_fixedlength":"rs:fixedlength", "s_extends":"s:extends", "s_Schema":"s:Schema", "s_ElementType":"s:ElementType","s_AttributeType":"s:AttributeType","s_datatype":"s:datatype", "rs_updatable":"rs:updatable","dt_type":"dt:type","rs_number":"rs:number","rs_write":"rs:write","dt_maxLength":"dt:maxLength", "rs_precision":"rs:precision","rs_maybenull":"rs:maybenull", "rs_long":"rs:long", "xmlns_s":"xmlns:s", "xmlns_dt":"xmlns:dt","xmlns_rs":"xmlns:rs" ,"xmlns_z":"xmlns:z"}

if __name__ == "__main__":
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
        print("Please provide a valid input directory which stores antennas.xml and utransmitter.xml")
    if not os.path.isdir(xml_dir_out):
        print("Please provide an existing output directory")

    if not os.path.isdir(xml_dir_in):
        print("Please provide valid input directory")
        exit()
    if not os.path.isdir(xml_dir_out):
        print("Please provide valid output directory")
        exit()

    antenna_n_family = beautify_family_attr(origReplacement,replacementOrig,xml_dir_in, xml_dir_out)
    create_profile_translator(xml_dir_in, xml_dir_out, antenna_n_family)

