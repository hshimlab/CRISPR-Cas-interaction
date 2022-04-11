'''
2022-03-03
Yunseol Park
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pri_setup import make_paths_dict, chromedriver_setup, find_name, find_RNAfilename, find_previous_docking, save_bestscore, write_score, unzip_pdb, pymol_screenshot
import glob
import shutil
from urllib.request import urlretrieve
import os
import time
import code
import json

def wait_run(write_name, email, cas_path, rna_path, wait_time):
    driver, display = chromedriver_setup('results/pydockdna')
    driver.get('https://model3dbio.csic.es/pydockdna/info/status')
    jobs = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]').text.split('\n')
    total_jobs = sum([int(i.split(': ')[1]) for i in jobs[:-1]])
    print('{} jobs are queued'.format(total_jobs))
    time_counter = 0
    print("Start waiting")
    # Keep waiting until there are 6 jobs queued to resume running
    # (waiting until all the queued jobs are gone causes timeout and having too many queued jobs slows server down)
    while total_jobs > wait_time:
        time.sleep(1800)
        time_counter += 30
        print('waiting for: {} h {} min'.format(time_counter // 60, time_counter % 60))
        driver.refresh()
        jobs = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]').text.split('\n')
        total_jobs = sum([int(i.split(': ')[1]) for i in jobs[:-1]])
        print('{} jobs are queued'.format(total_jobs))
    driver.close()
    display.stop()
    driver, display = open_chrome(write_name, email, cas_path, rna_path)
    return driver, display

def handle_exceptions(driver, display, write_name, email, cas_path, rna_path):
    try:
        submit_error = driver.find_element(By.XPATH, '//*[@id="submit__error"]')
        print(submit_error.text)
        driver.close()
        display.stop()
        driver, display = wait_run(write_name, email, cas_path, rna_path, 9)
        print('escaped waiting session')
    except:
        try:
            email_error = driver.find_element(By.XPATH, '//*[@id="email__error"]')
            print(email_error.text)
            driver.close()
            display.stop()
            driver, display = wait_run(write_name, email, cas_path, rna_path, 9)
            print('escaped waiting session')
        except:
            return driver, display
    return driver, display

def open_chrome(write_name, email, cas_path, rna_path):
    # Set up chromedriver
    driver, display = chromedriver_setup('results/pydockdna')
    driver.get('https://model3dbio.csic.es/pydockdna')
    wait = WebDriverWait(driver, 30)
    # Disable cookies banner
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/a'))).click()
    # Write details
    driver.find_element(By.NAME, 'project_name').send_keys(write_name)
    driver.find_element(By.NAME, 'email').send_keys(email)
    # Add cas file
    driver.find_element(By.NAME, 'pdb_receptor').send_keys(cas_path)
    # Add rna file
    driver.find_element(By.NAME, 'pdb_ligand').send_keys(rna_path)
    # Click agreement checkbox
    driver.find_element(By.NAME, 'agreement').click()
    # Continue button
    driver.find_element(By.NAME, 'submit').click()
    driver.implicitly_wait(180)
    return driver, display

def submit_job(write_name, email, cas_path, rna_path, url_file):
    driver, display = open_chrome(write_name, email, cas_path, rna_path)
    # If 10 jobs are in queue, wait
    driver, display = handle_exceptions(driver, display, write_name, email, cas_path, rna_path)
    wait = WebDriverWait(driver, 30)
    # Check all checkboxes
    checkbox = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='checkbox']")))
    for check in checkbox:
        check.click()
    # Choose scoring function
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[2]/div[2]/div/form/div[2]/div[1]/label[1]/input').click()
    # Continue buttons in succession
    wait.until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="restraints_form"]/input'))).click()
    # Final submit button
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/form/input'))).click()
    print(write_name + ',' + driver.current_url, file=url_file)
    driver.close()
    display.stop()

def pydockdna_web(input_folders, save_filename, rotation=False, matching=False):
    already_written = find_previous_docking(save_filename)
    paths_dict = make_paths_dict(input_folders)
    email_counter = 0
    email_list = ['pyslucy@gmail.com', 'yunseol.park@ghent.ac.kr', 'pyslucy@naver.com', 'lucypys@gmail.com']
    email = email_list[email_counter]
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
                    submit_job(write_name, email, cas_path, rna_path, url_file)
                    print(write_name + ' finished')
                    email_counter += 1
                    if email_counter == 4:
                        e_index = email_list.index(email) + 1
                        if e_index >= len(email_list):
                            e_index = 0
                        email = email_list[e_index]
                        email_counter = 0
                    url_file.close()

def download_pydockdna(url_file):
    url_list = open(url_file, 'r').readlines()
    for line in url_list:
        split_line = line.rstrip().split(',')
        url = split_line[1]
        name = split_line[0]
        if os.path.exists('results/pydockdna/' + name + '.tgz') or os.path.isdir('results/pydockdna/' + name): 
            continue
        driver, display = chromedriver_setup('results/pydockdna')
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        print(name)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/a'))).click()
        download = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/a').get_attribute('href')
        urlretrieve(download, 'results/pydockdna/' + name + '.tgz')
        driver.quit()
        display.stop()

def pydockdna_write(url_file, save_xlsx, rotation=False, index=['']):
    download_pydockdna(url_file)
    result_dir = unzip_pdb('tgz', 'results/pydockdna')
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
        print(rna_check)
        print([index[i] for i in range(0,len(best_score[rna_type][cas_name]))])
        if rna_check in [index[i] for i in range(0,len(best_score[rna_type][cas_name]))]:
            continue
        #code.interact(local = dict(globals(), **locals()))
        filename = glob.glob('results/pydockdna/' + directory + "/*.ene")[0]
        result_line = open(filename,'r').readlines()[2].split()
        score = result_line[4]
        if rna.lower() in cas:
            best_model = result_line[0]
            model_name = '_'.join(filename.split('_')[:-1]) + '_' + best_model + '.pdb'
            os.system('cp ' + model_name + ' results/pydockdna/PDB/' + directory + '.pdb')
        best_score[rna_type][cas_name].append(float(score))
        with open(save_xlsx.split('.')[0]+'.txt', 'w') as fp:
            json.dump(best_score, fp)
    write_score(save_xlsx, best_score, rotation, index)
    pymol_screenshot('results/pydockdna/PDB')
    

if __name__ == '__main__':
    #pydockdna_web([['data/random_rotation/cas'],['data/random_rotation/rna_experimental']], 'results/pydockdna/random_rotation.txt', True, True)
    pydockdna_write('results/pydockdna/random_rotation.txt', 'results/pydockdna/pydockdna_rr_results.xlsx', True, ['0','1','2'])
