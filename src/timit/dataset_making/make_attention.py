#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Make dataset for Attention model (TIMIT corpus)."""

import os
import sys
import shutil
import glob
from tqdm import tqdm

sys.path.append('../')
sys.path.append('../../../')
from prepare_path import Prepare
from inputs.input_data_global_norm import read_htk
from labels.attention.character import read_text
from labels.attention.phone import read_phone
from utils.util import mkdir


def main(label_type):

    print('===== ' + label_type + ' =====')
    prep = Prepare()
    save_path = mkdir(os.path.join(prep.data_root_path, 'dataset'))
    save_path = mkdir(os.path.join(save_path, 'attention'))
    save_path = mkdir(os.path.join(save_path, label_type))

    # reset directory
    if not os.path.isfile(os.path.join(save_path, 'check.txt')):
        print('=> Deleting old dataset...')
        for c in tqdm(os.listdir(save_path)):
            shutil.rmtree(os.path.join(save_path, c))
    else:
        print('Already exists.')
        return 0

    train_save_path = mkdir(os.path.join(save_path, 'train'))
    dev_save_path = mkdir(os.path.join(save_path, 'dev'))
    test_save_path = mkdir(os.path.join(save_path, 'test'))

    input_train_save_path = mkdir(os.path.join(train_save_path, 'input'))
    label_train_save_path = mkdir(os.path.join(train_save_path, 'label'))
    input_dev_save_path = mkdir(os.path.join(dev_save_path, 'input'))
    label_dev_save_path = mkdir(os.path.join(dev_save_path, 'label'))
    input_test_save_path = mkdir(os.path.join(test_save_path, 'input'))
    label_test_save_path = mkdir(os.path.join(test_save_path, 'label'))

    ####################
    # train
    ####################
    print('---------- train ----------')
    # read htk files, save input data as npy files, save frame num dict as a pickle file
    print('=> Processing input data...')
    htk_train_paths = [os.path.join(prep.data_root_path, htk_dir)
                       for htk_dir in sorted(glob.glob(os.path.join(prep.data_root_path, 'fbank/train/*.htk')))]
    train_mean, train_std = read_htk(htk_paths=htk_train_paths,
                                     save_path=input_train_save_path,
                                     normalize=True,
                                     is_training=True)

    # read labels, save labels as npy files
    print('=> Processing ground truth labels...')
    if label_type == 'character':
        label_train_paths = prep.text(data_type='train')
        read_text(label_paths=label_train_paths,
                  save_path=label_train_save_path)
    else:
        label_train_paths = prep.phone(data_type='train')
        read_phone(label_paths=label_train_paths,
                   save_path=label_train_save_path,
                   label_type=label_type)

    ####################
    # dev
    ####################
    print('---------- dev ----------')
    # read htk files, save input data as npy files, save frame num dict as a pickle file
    print('=> Processing input data...')
    htk_dev_paths = [os.path.join(prep.data_root_path, htk_dir)
                     for htk_dir in sorted(glob.glob(os.path.join(prep.data_root_path, 'fbank/dev/*.htk')))]
    read_htk(htk_paths=htk_dev_paths,
             save_path=input_dev_save_path,
             normalize=True,
             is_training=False,
             train_mean=train_mean,
             train_std=train_std)

    # read labels, save labels as npy files
    print('=> Processing ground truth labels...')
    if label_type == 'character':
        label_dev_paths = prep.text(data_type='dev')
        read_text(label_paths=label_dev_paths,
                  save_path=label_dev_save_path)
    else:
        label_dev_paths = prep.phone(data_type='dev')
        read_phone(label_paths=label_dev_paths,
                   save_path=label_dev_save_path,
                   label_type=label_type)

    ####################
    # test
    ####################
    print('---------- test ----------')
    # read htk files, save input data as npy files, save frame num dict as a pickle file
    print('=> Processing input data...')
    htk_test_paths = [os.path.join(prep.data_root_path, htk_dir)
                      for htk_dir in sorted(glob.glob(os.path.join(prep.data_root_path, 'fbank/test/*.htk')))]
    read_htk(htk_paths=htk_test_paths,
             save_path=input_test_save_path,
             normalize=True,
             is_training=False,
             train_mean=train_mean,
             train_std=train_std)

    # read labels, save labels as npy files
    print('=> Processing ground truth labels...')
    if label_type == 'character':
        label_test_paths = prep.text(data_type='test')
        read_text(label_paths=label_test_paths,
                  save_path=label_test_save_path)
    else:
        label_test_paths = prep.phone(data_type='test')
        read_phone(label_paths=label_test_paths,
                   save_path=label_test_save_path,
                   label_type=label_type)

    # make a confirmation file to prove that dataset was saved correctly
    with open(os.path.join(save_path, 'check.txt'), 'w') as f:
        f.write('')
    print('Successfully completed!')


if __name__ == '__main__':

    print('=======================================')
    print('=          TIMIT (Attention)          =')
    print('=======================================')

    label_types = ['character', 'phone61', 'phone48', 'phone39']
    for label_type in label_types:
        main(label_type)
