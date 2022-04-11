'''
2022-04-04
Yunseol Park
'''

from selenium import webdriver
import os
from pyvirtualdisplay import Display
import json
import glob
from urllib.request import urlretrieve
import pandas as pd
from statistics import mean
import shutil
from pymol import cmd
import __main__
import code

def find_previous_docking(save_filename):
    already_written = []
    if os.path.exists(save_filename):
        savedfile = open(save_filename, 'r').readlines()
        already_written = [i.split(',')[0] for i in savedfile]
    return already_written

def make_paths_dict(input_folders):
    '''
    This function makes a dictionary of paths of all the input pdb files.
    Args:
        input_folders (list): a list of lists with the first list containing cas and the second containing the rna file paths
    Return:
        paths_dict (dict): a dictionary of dictionaries containing the file paths of every pdb file in 'input_folders'
    '''
    paths_dict = {'cas':{}, 'rna':{}}
    for folder in input_folders:
        for cas_rna in folder:
            foldername = cas_rna.split('/')[-1]
            # Find whether sequence is cas or rna
            first_key = foldername.split('_')[0]
            paths_dict[first_key][foldername] = []
            for filename in sorted(os.listdir(cas_rna)):
                path = os.path.join(cas_rna, filename)
                paths_dict[first_key][foldername].append(os.path.abspath(path))
    print(paths_dict)
    return paths_dict

def chromedriver_setup(download_dir):
    '''
    This function opens chromedriver.
    Args:
        download_dir (str): the directory name to download results to
    Return:
        driver (chromedriver): opened chromedriver
        display (): opened virtual display
    '''
    # Set options
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}    # Download directory
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    # Open display
    display = Display(visible=0, size=(1920,1080))
    display.start()
    # Open chromedriver
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
    driver.set_page_load_timeout(1000000)
    driver.maximize_window()
    return driver, display

def find_name(filename, rotation):
    '''
    This function takes the name of the pdb file and returns the session name.
    Args:
        filename (str): the name of pdb file (eg. 5w1h_cas.pdb)
        rotation (boolean): whether the inputs are randomly rotated into different orientations
    Return:
        name (str): the name of the session (eg. 5w1h)
    '''
    if rotation:        # Add rotation number
        postfix = filename.split('.')[0].split('_')[-1][-1]
    else:
        postfix = ''
    if '_' in filename:
        name = filename.split('_')[0]
    else:
        name = filename.split('.')[0]
    name += postfix
    return name 

def find_RNAfilename(cas_filename, rna_path, rotation, matching):
    '''
    This function finds the corresponding name of the rna pdb file using the cas pdb file name.
    Args:
        cas_filename (str): the name of pdb file (eg. 5w1h_cas_rotation0.pdb)
        rna_path (str): the path of the corresponding rna file
        rotation (boolean): whether the inputs are randomly rotated into different orientations
        matching (boolean): whether only the matching pdb files will be used for docking
    Return:
        rna_filename (str): the name of the session (eg. 5w1h)
    '''
    if matching:
        rna_prefix = cas_filename.split('_')
        if rotation:
            rna_filename = rna_prefix[0] + '_rna_' + rna_prefix[2]
        else:
            rna_filename = rna_prefix[0] + '_rna.pdb'
    else:
        rna_filename = rna_path.split("/")[-1]
    return rna_filename

def save_bestscore(save_xlsx):
    if os.path.exists(save_xlsx.split('.')[0]+'.txt'):
        with open(save_xlsx.split('.')[0] + '.txt', 'r') as fp:
            best_score = json.load(fp)
    else:
        best_score = {}
    return best_score

def write_score(save_xlsx, best_score, rotation, index):
    writer = pd.ExcelWriter(save_xlsx, engine='xlsxwriter')
    for key, value in best_score.items():
        print(key, index)
        df = pd.DataFrame(value, index=index)
        df = df.transpose()
        df.to_excel(writer, sheet_name=key)
        if rotation:
            avg_dict = {df_key:mean([float(s) for s in df_value]) for df_key, df_value in value.items()}
            avg_df = pd.DataFrame(avg_dict, index=['avg_' + key])
            avg_df = avg_df.transpose()
            avg_df.to_excel(writer, sheet_name='avg_'+key)
    writer.save()
    writer.close()

def pymol_screenshot(pdb_files):
    __main__.pymol_argv = ['pymol', '-qei']    
    write_dir = '/'.join(pdb_files.split('/')[:-1]) + '/' + 'images'
    '''if not os.path.isdir(write_dir):
        os.makedirs(write_dir)'''
    for pdb in os.listdir(pdb_files):
        name = pdb.split('.')[0]
        '''if name not in ['5w1iABvs5W1I_shortRNAa','5w1iABvs5W1I_shortRNAb','5w1iCDvs5W1I_shortRNAa','5w1iCDvs5W1I_shortRNAb','7os0AFvs7OS0_shortRNAa','7os0AFvs7OS0_shortRNAb','7os0CDvs7OS0_shortRNAa','7os0CDvs7OS0_shortRNAb']:
            continue'''
        #code.interact(local = dict(globals(), **locals()))
        if pdb.split('.')[1] != 'pdb':
            continue
        cmd.load(pdb_files + '/' + pdb)
        cmd.zoom('vis')
        cmd.png(write_dir + '/' + name)
        cmd.delete('all')
    cmd.quit()

def unzip_pdb(tar_type, save_dir):
    print('download complete')
    current_path = os.getcwd()
    os.chdir(save_dir)
    if len(glob.glob('/*.tgz')) == 0:
        os.system('for a in `ls -l *.' + tar_type + '`; do tar -zxvf $a --one-top-level; done')
        os.system('rm *.tgz')
    result_dir = sorted(list(filter(os.path.isdir, os.listdir())))
    #code.interact(local = dict(globals(), **locals()))
    os.chdir(current_path)
    if 'PDB' in result_dir:
        result_dir.remove('PDB')
    else:
        os.makedirs(save_dir + '/PDB')
    if 'images' in result_dir:
        result_dir.remove('images')
    else:
         os.makedirs(save_dir + '/images')
    return result_dir
