#!/usr/bin/python
import re
import subprocess

def check_if_sample_is_control(header):
    has_tumor_tissue = []
    has_more_than_one_sample = []
    has_tumor_tissue_name = []
    for index, sample in enumerate(header.split("\t")):
        if sample.startswith('TCGA'):
            sample_type = sample.split("-")[3]
            sample_type = re.sub(r'([A-Z])', '', sample_type)
            if int(sample_type) <= 9:
                has_tumor_tissue.append("$"+str(index+1))
                has_tumor_tissue_name.append(sample)
                if int(sample_type) > 1:
                    has_more_than_one_sample.append(sample)
    # for duplicate_sample in has_more_than_one_sample:
    #     for index_all_samples, all_samples in enumerate (has_tumor_tissue_name):
    #         new_string = duplicate_sample.split("-")
    #         name = new_string[0]+"-"+new_string[1]+"-"+new_string[2]
    #         if name in all_samples:
    #             del has_tumor_tissue[index_all_samples]
    #             del has_tumor_tissue_name[index_all_samples]


    return has_more_than_one_sample, has_tumor_tissue
    # for sample in has_more_than_one_sample:
    #     new_string = sample.split("-")
    #     name = new_string[0]+"-"+new_string[1]+"-"+new_string[2]

input_file = "/home/sheila/Documentos/Fundacion_hospital_General/LUAD/genes"
header = open(input_file).readline().rstrip()
all_controls = check_if_sample_is_control(header)

subprocess.call(["awk '{}' {}  > /home/sheila/Documentos/Fundacion_hospital_General/LUAD/LUAD_tumores.txt".format("{print $1\"\t\""+'\"\t\"'.join(all_controls[1])+"}", input_file)], shell=True)
#subprocess.call(["awk '{}' {}  > /home/sheila/Documentos/Fundacion_hospital_General/LUSC/tumor.txt".format("{print $1\"\t\""+'\"\t\"'.join(controls_tumors[1])+"}", input_file)], shell=True)

# clinical_data = "/home/sheila/Documentos/Fundacion_hospital_General/LUSC/LUAD-TP.samplefeatures.txt"
# clinical_file_handler = open(clinical_data, 'r')
# clinical_output_handler = open("/home/sheila/Documentos/Fundacion_hospital_General/clinical_data.txt", 'w')
# clinical_header = open(clinical_data).readline().rstrip()
# clinical_output_handler.write(clinical_header+"\n")
# for line in clinical_file_handler:
#     line = line.rstrip()
#     if line.split('\t')[0] in controls_tumors[2]:
#         clinical_output_handler.write(line + "\n")
