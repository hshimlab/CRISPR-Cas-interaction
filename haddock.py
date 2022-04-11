from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pri_setup import make_paths_dict, chromedriver_setup, find_name, find_RNAfilename, find_previous_docking, save_bestscore, write_score, unzip_pdb, pymol_screenshot
import os
import time
import glob
import shutil
import code
import json


def submit_job(write_name, cas_path, rna_path, url_file):
    # Set up chromedriver
    driver, display = chromedriver_setup('results/haddock')
    driver.get('https://wenmr.science.uu.nl/haddock2.4/submit/1')
    wait = WebDriverWait(driver, 30)
    # Disable cookies banner
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/a'))).click()
    # Login
    driver.find_element(By.ID, 'email').send_keys('pyslucy@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('haddockpw01')
    driver.find_element(By.ID, 'remember_me').click()
    driver.find_element(By.ID, 'login').click()
    # Write details
    driver.find_element(By.NAME, 'runname').send_keys(write_name)
    # Add cas file
    driver.find_element(By.NAME, 'p1_pdb_file').send_keys(cas_path)
    # Add rna file
    moltype_selector = Select(driver.find_element(By.XPATH, '//*[@id="p2_moleculetype"]'))
    moltype_selector.select_by_visible_text('Nucleic acid (DNA and/or RNA)')
    driver.find_element(By.NAME, 'p2_pdb_file').send_keys(rna_path)
    # Continue button
    driver.find_element(By.XPATH, '//*[@id="submit"]').click()
    driver.implicitly_wait(180)
    #code.interact(local = dict(globals(), **locals()))
    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'submit'))).click()
        #code.interact(local = dict(globals(), **locals()))
        # Choose parameters
        ranair = driver.find_element_by_id("ranair")
        driver.execute_script("arguments[0].click();", ranair)
        driver.find_element(By.XPATH, '//*[@id="submitHaddock"]/div[11]/div[1]/h4/a').click()
        driver.find_element(By.XPATH, '//*[@id="epsilon_0"]').clear()
        driver.find_element(By.XPATH, '//*[@id="epsilon_0"]').send_keys('78.0')
        driver.find_element(By.XPATH, '//*[@id="epsilon_1"]').clear()
        driver.find_element(By.XPATH, '//*[@id="epsilon_1"]').send_keys('78.0')
        # Final submit button
        driver.find_element(By.ID, 'submit').click()
        # Covid popup
        wait.until(EC.element_to_be_clickable((By.ID, 'covidConfirmNo'))).click()
        print(write_name + ',' + driver.current_url, file=url_file)
        print(driver.current_url)
        driver.close()
        display.stop()
    except:
        print('enterting error')
        #code.interact(local = dict(globals(), **locals()))
        error = driver.find_element(By.XPATH, '//*[@class="alert alert-danger"]')
        print('Error:' + error.text)
        print(write_name + ',' + ' '.join(error.text.split('\n')), file=url_file)
        driver.close()
        display.stop()

def haddock_web(input_folders, save_filename, rotation=False, matching=False):
    already_written = find_previous_docking(save_filename)
    paths_dict = make_paths_dict(input_folders)
    url_file = open(save_filename, 'a')
    for cas_value in paths_dict['cas'].values():
        for cas_path in cas_value:
            cas_filename = cas_path.split("/")[-1]
            cas_name = find_name(cas_filename, rotation)
            for rna_key, rna_value in paths_dict['rna'].items():
                for rna_path in rna_value:
                    rna_filename = find_RNAfilename(cas_filename, rna_path, rotation, matching)
                    if matching and rna_filename not in rna_path:
                        continue
                    rna_name = find_name(rna_filename, rotation)
                    write_name = cas_name + 'vs' + rna_name + '_' + rna_key.split('_')[-1]
                    if write_name in already_written:
                        continue
                    url_file = open(save_filename, 'a')
                    print('start ' + write_name)
                    submit_job(write_name, cas_path, rna_path, url_file)
                    print(write_name + ' finished')
                    url_file.close()

def download_haddock(url_file):
    for line in open(url_file, 'r').readlines():
        line = line.rstrip()
        name, url = line.split(',')
        if 'Error' in url:
            print(name, ' error, submit again')
            continue
        if os.path.exists('results/haddock/' + name + '.tgz') or os.path.isdir('results/haddock/' + name):
            continue
        driver, display = chromedriver_setup('results/haddock')
        driver.get(url)
        print(name)
        # Disable cookies banner
        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/a'))).click()
        download_run = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/p[2]/a[1]').get_attribute('href')
        urlretrieve(download_run, 'results/haddock/' + name + '.tgz')
        '''# Plots
        if rna.lower() in cas.lower():
            download_plots = driver.find_element(By.XPATH, '//*[@id="graphics"]/a').get_attribute('href')
            urlretrieve(download_plots, 'results/haddock/' + line + '_plots.tgz')'''
        driver.quit()
        display.stop()

def haddock_write(url_file,save_xlsx, rotation=False, index=['']):
    download_haddock(url_file)    
    result_dir = unzip_pdb('tgz', 'results/haddock')
    best_score = save_bestscore(save_xlsx)
    for directory in result_dir:
        name, rna_type = directory.split('_')
        cas, rna = name.split('vs')
        cas = cas.split('_')[0]
        rna = rna.split('_')[0]
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
        if rna_check in [index[i] for i in range(0,len(best_score[rna_type][cas_name]))]:
            continue
        inner_directory = glob.glob('results/haddock/' + directory + '/*-' + directory)[0]
        filename = inner_directory + "/clusters_haddock-sorted.stat_best4"
        s = open(filename,'r').readlines()[1].split()
        if rna.lower() in cas:
            pdb_name = inner_directory + '/cluster' + s[0].split('clust')[1] + '_1.pdb'
            print(pdb_name)
            os.system('cp ' + pdb_name + ' results/haddock/PDB/' + directory + '.pdb')
        h_score = s[1]
        best_score[rna_type][cas_name].append(float(h_score))
        with open(save_xlsx.split('.')[0]+'.txt', 'w') as fp:
            json.dump(best_score, fp)
    write_score(save_xlsx, best_score, rotation, index)
    pymol_screenshot('results/haddock/PDB')

if __name__ == '__main__':
    #6e9f0
    #haddock_web([['data/random_rotation/cas'],['data/random_rotation/rna_experimental']], 'results/haddock/random_rotation.txt', True, True)
    haddock_write('results/haddock/random_rotation.txt', 'results/haddock/haddock_rr_results.xlsx', True, ['0','1','2'])