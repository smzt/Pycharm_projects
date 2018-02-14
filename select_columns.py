#!/usr/bin/python
import re
import subprocess

def check_if_sample_is_control(header):
    has_control_tissue = []
    for sample in header.split("\t"):
        if sample.startswith('TCGA'):
            sample_type = sample.split("-")[3]
            sample_type = re.sub(r'([A-Z])', '', sample_type)
            if int(sample_type) >= 10:
                has_control_tissue.append(sample.split('-')[0]+'-'+sample.split('-')[1]+'-'+sample.split('-')[2])
    return has_control_tissue

def get_column_index(has_control_tissue, header):
    controls = []
    tumors = []
    controls_names = []
    for control_tissue in has_control_tissue:
        has_normal = False
        for index,sample in enumerate(header.split("\t")):
            if sample.startswith(control_tissue):
                sample_type = sample.split("-")[3]
                sample_type = re.sub(r'([A-Z])', '', sample_type)
                if int(sample_type) >= 10:
                    controls.append("$"+str(index+1))
                    controls_names.append(control_tissue)
                elif int(sample_type) < 10:
                    tumors.append("$"+str(index+1))
                    has_normal = True
        if not has_normal:
            del controls[-1]
            del controls_names[-1]
    return controls, tumors, controls_names


input_file = "/home/sheila/Documentos/Fundacion_hospital_General/LUSC/genes"
header = open(input_file).readline().rstrip()
all_controls = check_if_sample_is_control(header)
controls_tumors = get_column_index(all_controls, header)
subprocess.call(["awk '{}' {}  > /home/sheila/Documentos/Fundacion_hospital_General/LUSC/controles.txt".format("{print $1\"\t\""+'\"\t\"'.join(controls_tumors[0])+"}", input_file)], shell=True)
subprocess.call(["awk '{}' {}  > /home/sheila/Documentos/Fundacion_hospital_General/LUSC/tumor.txt".format("{print $1\"\t\""+'\"\t\"'.join(controls_tumors[1])+"}", input_file)], shell=True)

# clinical_data = "/home/sheila/Documentos/Fundacion_hospital_General/LUSC/LUAD-TP.samplefeatures.txt"
# clinical_file_handler = open(clinical_data, 'r')
# clinical_output_handler = open("/home/sheila/Documentos/Fundacion_hospital_General/clinical_data.txt", 'w')
# clinical_header = open(clinical_data).readline().rstrip()
# clinical_output_handler.write(clinical_header+"\n")
# for line in clinical_file_handler:
#     line = line.rstrip()
#     if line.split('\t')[0] in controls_tumors[2]:
#         clinical_output_handler.write(line + "\n")
