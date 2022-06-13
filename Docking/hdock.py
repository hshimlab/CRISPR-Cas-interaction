'''
2022-04-04
Yunseol Park
'''

from selenium.webdriver.common.by import By
from pri_setup import make_paths_dict, chromedriver_setup, find_name, find_RNAfilename, find_previous_docking, save_bestscore, write_score, pymol_screenshot, unzip_pdb
from PIL import Image
import pandas as pd
import time
import json
from statistics import mean
from urllib.request import urlretrieve
import os

def submit_job(write_name, cas_path, rna_path, url_file, template_free):
    '''
    This function uses chromedriver to submit jobs.

    Args:
        write_name (str): the name of the protein-rna complex to run docking
        cas_path (str): the path name of the cas protein
        rna_path (str): the path name of the crispr rna
        url_file (file): the file to save the resulting url of docking session
    Returns:
        None
    '''
    # Set up chromedriver
    driver, display = chromedriver_setup('results/hdock')
    driver.get('http://hdock.phys.hust.edu.cn/')
    # Add files
    driver.find_element(By.NAME, 'pdbfile1').send_keys(cas_path)
    driver.find_element(By.NAME, 'pdbfile2').send_keys(rna_path)
    # Write details
    if template_free:
        driver.find_element(By.XPATH, '//*[@id="form1"]/table/tbody/tr[6]/td/ul/li[1]/input').click()
    driver.find_element(By.NAME, 'jobname').send_keys(write_name)
    # Continue button
    driver.find_element(By.NAME, 'upload').click()
    driver.implicitly_wait(180)
    print(write_name + ',' + driver.current_url, file=url_file)
    driver.close()
    display.stop()

def hdock_web(input_folders, save_filename, matching=False, template_free=True, rotation=False):
    '''
    This function uses chromedriver to submit jobs.

    Args:
        input_folders (list): a list of lists with the first list containing cas and the second containing the rna file paths
        save_filename (str): the name of the file to save the docking results url to
        rotation (boolean): whether the inputs are randomly rotated into different orientations
        matching (boolean): whether only the matching pdb files will be used for docking
    Returns:
        None
    '''
    already_written = find_previous_docking(save_filename)
    paths_dict = make_paths_dict(input_folders)
    for cas_value in paths_dict['cas'].values():
        for cas_path in cas_value:
            cas_filename = cas_path.split("/")[-1]
            cas_name = find_name(cas_filename, rotation)
            for rna_key, rna_value in paths_dict['rna'].items():
                for rna_path in rna_value:
                    if rotation:
                        rna_filename = find_RNAfilename(cas_filename, rna_path, rotation, matching)
                    else:
                        rna_filename = rna_path.split('/')[-1]
                    if rotation and matching and rna_filename not in rna_path:
                        continue
                    elif not rotation and matching and rna_filename.split('.')[0].split('_')[0].lower() not in cas_filename.split('.')[0].lower():
                        continue
                    rna_name = find_name(rna_filename, rotation)
                    write_name = cas_name + 'vs' + rna_name + '_' + rna_key.split('_')[-1]
                    if write_name in already_written:
                        continue
                    url_file = open(save_filename, 'a')
                    print('start ' + write_name)
                    submit_job(write_name, cas_path, rna_path, url_file, template_free)
                    print(write_name + ' finished')
                    url_file.close()

def hdock_write_validation(url_file, save_xlsx, rotation=False, index=['']):
    best_score = save_bestscore(save_xlsx)
    print(best_score)
    for line in open(url_file, 'r').readlines():
        line = line.rstrip()
        split_line = line.rstrip().split(',')
        url = split_line[1]
        name = split_line[0]
        cas, rna = name.split('_')[0].split('vs')
        if rotation:
            cas_name = cas[:-1]
            rna_check = rna[-1]
        else:
            cas_name = cas
            rna_check = rna
        rna_type = name.split('_')[1]
        if rna_type not in best_score:
            best_score[rna_type] = {}
        if cas_name not in best_score[rna_type]:
            best_score[rna_type][cas_name] = []
        if rna_check in [index[i] for i in range(0,len(best_score[rna_type][cas_name]))]:
            continue
        print(name)
        driver, display = chromedriver_setup('results/hdock')
        driver.get(url)
        score = driver.find_element(By.XPATH, '/html/body/center/table[4]/tbody/tr[2]/td[1]').text
        best_score[rna_type][cas_name].append(score)
        with open(save_xlsx.split('.')[0]+'.txt', 'w') as fp:
            json.dump(best_score, fp)
        best_pdb = driver.find_element(By.XPATH, '/html/body/center/table[1]/tbody/tr/td/div/a[3]').get_attribute('href')
        urlretrieve(best_pdb, 'results/hdock/PDB/' + name + '.pdb')
        driver.close()
        display.stop()
    write_score(save_xlsx, best_score, rotation, index)
    pymol_screenshot('results/hdock/PDB')

def hdock_write_TOP10(url_file, save_xlsx, matching=False, rotation=False, index=None):
    best_score = save_bestscore(save_xlsx)
    print(best_score)
    previous_rna = ''
    download_list = []
    first_level_dir = url_file.split('.')[0]
    if not os.path.exists(first_level_dir):
        os.mkdir(first_level_dir)
    for line in open(url_file, 'r').readlines():
        line = line.rstrip()
        write_name, rna_type = name.split('__')
        cas, rna = write_name.split('vs')
        if rotation:
            cas_name = cas[:-1]
            rna_check = rna[-1]
        else:
            cas_name = cas
            rna_check = rna
        if rna_type not in best_score:
            best_score[rna_type] = {}
        if cas_name not in best_score[rna_type]:
            best_score[rna_type][cas_name] = []
        if not matching and not index:
            index = []
        elif not matching and previous_rna != rna_type:
            index = []
            previous_rna = rna_type
        elif not matching and rna not in index and previous_rna == rna_type:
            index.append(rna)
        elif matching and index == None:
            index = ['']
        if first_level_dir != 'results/hdock/' + rna_type:
            download_dir = first_level_dir + '/' + rna_type
        else:
            download_dir = 'results/hdock/' + rna_type
        if download_dir not in download_list:
            download_list.append(download_dir)
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        print(name)
        driver, display = chromedriver_setup(download_dir)
        driver.get(url)
        if (not matching and len(best_score[rna_type][write_name]) == 0)\
        or (matching and len(best_score[rna_type][write_name]) != 1):
            top10_score = [driver.find_element(By.XPATH, '/html/body/center/table[4]/tbody/tr[2]/td['+str(i)+']').text for i in range(1,11)]
            for score in top10_score:
                best_score[rna_type][write_name].append(score)
            with open(save_xlsx.split('.')[0]+'.txt', 'w') as fp:
                json.dump(best_score, fp)
        if not (os.path.exists(download_dir + '/PDB/' + write_name + '.tar.gz') or\
            os.path.exists(download_dir + '/PDB/' + write_name)):
            best_pdb = driver.find_element(By.XPATH, '/html/body/center/table[1]/tbody/tr/td/div/a[23]').get_attribute('href')
            if not os.path.exists(download_dir + '/PDB'):
                os.mkdir(download_dir + '/PDB')
            urlretrieve(best_pdb, download_dir + '/PDB/' + write_name + '.tar.gz')
        driver.quit()
        display.stop()
        print(best_score)
    for download_dir in download_list:
        unzip_pdb('tar.gz', download_dir + '/PDB', True)
        all_dir = os.listdir(download_dir + '/PDB')
        for name in all_dir:
            inner_directory = glob.glob(download_dir + '/PDB/' + name + '/*')[0]
            for model in os.listdir(inner_directory):
                no = model.split('_')[1]
                os.rename(inner_directory + '/' + model, download_dir + '/PDB/' + name + '_' + no)
    write_score(save_xlsx, best_score, rotation, index)


if __name__ == '__main__':
    #6iv80
    #hdock_web([['data/random_rotation/cas'],['data/random_rotation/rna_experimental']], 'results/hdock/random_rotation.txt', True, True)
    hdock_write_validation('results/hdock/random_rotation.txt', 'results/hdock/hdock_rr_results.xlsx', True, ['0','1','2'])
