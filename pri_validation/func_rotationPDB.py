'''
2022.04.07
Yunseol Park
'''

import os
from pymol import cmd
import __main__
import code
import random
import code

def random_rotation():
    __main__.pymol_argv = ['pymol', '-qei']
    data_dir = '/home/yunseol/pri/data'
    directory_list = os.listdir(data_dir)
    directory_list.remove('random_rotation')
    directory_list.remove('func_rotationPDB.py')
    angle_list = list(range(40,321))
    write_file = open('random_rotation/random_rotations.txt', 'w')
    for directory in directory_list:
        if not os.path.exists('random_rotation/' + directory):
            os.mkdir('random_rotation/' + directory)
        angles = random.sample(angle_list, 3)
        angle_list = [i for i in angle_list if i not in angles]
        write_file.write('The randomized ' + directory + ' angles are: {} degrees, {} degrees, {} degrees\n'.format(angles[0], angles[1], angles[2]))
        for filenames in os.listdir(directory):
            #code.interact(local = dict(globals(), **locals()))
            for i, a in enumerate(angles):
                cmd.load(directory + '/' + filenames)
                com = cmd.centerofmass()
                cmd.rotate(com, a)
                cmd.save('random_rotation/' + directory + '/' + filenames.split('.')[0] + '_' + 'rotation' + str(i) + '.pdb')
                cmd.delete('all')
    write_file.close()

if __name__ == '__main__':
    random_rotation()


