import os
import pandas as pd
from collections import defaultdict
import requests


def uniprot_search(uniprot_id):
    base_url = 'https://rest.uniprot.org/uniprotkb/search?query=accession:'
    url = base_url+uniprot_id+'&format=tsv'
    print(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        r = requests.get(url, headers=headers, stream=True)
        if r.status_code == 200:
            return r.text
        else:
            print('Status code is not 200.')
            pass
    except:
        print('Id {uniprot_id} error.'.format(uniprot_id=uniprot_id))
        raise


def read_csv(root_path):
    """
    Read csv files and save the data to a dictionary.

    Parameters:
        param1 - the root path of csv files

    Return:
        A python dict containing each file content. The key refers to the file name, and the value store the content of the file.

    Raises:
        IOerror - file input error
    """

    file_list = os.listdir(root_path)
    output_dict = {}
    whole_dict = {}
    for i in file_list:
        psm_dict = defaultdict(list)
        with open(os.path.join(root_path, i), 'r', encoding='utf-8-sig') as f:
            content = f.readlines()
            for line in content:
                line = line.strip().split(',')
                family = line[1]
                psm = float(line[0])
                if psm > 0:
                    psm_dict[family].append(psm)
        whole_dict[i.split('.')[0]] = psm_dict
    # print(whole_dict)
    # convert key: value - {c1: [{protein1:[1,1,2]}], C2:[]} to {C1:{protein1:20, protein2:20}, C2:{protein1:30, protein2:20}}
    for file_name, v in whole_dict.items():
        one_sample_dict = {}
        for uniID, psm_list in v.items():
            if uniID:
                sum_v = sum(psm_list)
                one_sample_dict[uniID] = sum_v
        output_dict[file_name] = one_sample_dict

    return output_dict


def hotmap_format(output_dict, dest_path):
    df = pd.DataFrame(output_dict).fillna(value=0)
    print(df)
    df.to_csv(dest_path, sep=',', encoding='utf-8')


def main():
    root_path = r'D:\Postgraduate\wxmy\bac_peptidase'
    dest_path = r'D:\Postgraduate\wxmy\bac_peptidase_results.csv'
    output_dict = read_csv(root_path)
    hotmap_format(output_dict, dest_path)


main()
