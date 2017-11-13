#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Make phone-level target labels for the End-to-End model (TIMIT corpus)."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from os.path import join, basename
import numpy as np
from tqdm import tqdm

from utils.labels.phone import Phone2idx
from utils.util import mkdir_join
from timit.util import map_phone2phone


def read_phone(label_paths, vocab_file_save_path, is_test=False,
               save_vocab_file=False, save_path=None):
    """Read phone transcript.
    Args:
        label_paths (list): list of paths to label files
        vocab_file_save_path (string): path to vocabulary files
        is_test (bool, optional): Set True when proccessing the test set
        save_vocab_file (bool, optional): if True, save vocabulary files
        save_path (string, optional): path to save labels.
            If None, don't save labels.
    """
    # Make the mapping file (from phone to index)
    phone2phone_map_file_path = join(
        vocab_file_save_path, '../phone2phone.txt')
    phone61_set, phone48_set, phone39_set = set([]), set([]), set([])
    with open(phone2phone_map_file_path, 'r') as f:
        for line in f:
            line = line.strip().split()
            if line[1] != 'nan':
                phone61_set.add(line[0])
                phone48_set.add(line[1])
                phone39_set.add(line[2])
            else:
                # Ignore "q" if phone39 or phone48
                phone61_set.add(line[0])

    phone61_to_idx_map_file_path = mkdir_join(
        vocab_file_save_path, 'phone61.txt')
    phone48_to_idx_map_file_path = mkdir_join(
        vocab_file_save_path, 'phone48.txt')
    phone39_to_idx_map_file_path = mkdir_join(
        vocab_file_save_path, 'phone39.txt')

    # Save mapping file
    if save_vocab_file:
        with open(phone61_to_idx_map_file_path, 'w') as f:
            for phone in sorted(list(phone61_set)):
                f.write('%s\n' % phone)
        with open(phone48_to_idx_map_file_path, 'w') as f:
            for phone in sorted(list(phone48_set)):
                f.write('%s\n' % phone)
        with open(phone39_to_idx_map_file_path, 'w') as f:
            for phone in sorted(list(phone39_set)):
                f.write('%s\n' % phone)

    if not is_test:
        phone61_to_idx = Phone2idx(
            vocab_file_path=phone61_to_idx_map_file_path)
        phone48_to_idx = Phone2idx(
            vocab_file_path=phone48_to_idx_map_file_path)
        phone39_to_idx = Phone2idx(
            vocab_file_path=phone39_to_idx_map_file_path)

    print('===> Reading & Saving target labels...')
    for label_path in tqdm(label_paths):
        speaker = label_path.split('/')[-2]
        utt_index = basename(label_path).split('.')[0]

        phone61_list = []
        with open(label_path, 'r') as f:
            for line in f:
                line = line.strip().split(' ')
                # start_frame = line[0]
                # end_frame = line[1]
                phone61_list.append(line[2])

        # Map from 61 phones to the corresponding phones
        phone48_list = map_phone2phone(phone61_list, 'phone48',
                                       phone2phone_map_file_path)
        phone39_list = map_phone2phone(phone61_list, 'phone39',
                                       phone2phone_map_file_path)

        # for debug
        # print(' '.join(phone61_list))
        # print(' '.join(phone48_list))
        # print(' '.join(phone39_list))
        # print('-----')

        if save_path is not None:
            save_file_name = speaker + '_' + utt_index + '.npy'

            if is_test:
                # Save target labels as string
                np.save(mkdir_join(save_path, 'phone61', save_file_name),
                        ' '.join(phone61_list))
                np.save(mkdir_join(save_path, 'phone48', save_file_name),
                        ' '.join(phone48_list))
                np.save(mkdir_join(save_path, 'phone39', save_file_name),
                        ' '.join(phone39_list))
            else:
                # Save target labels as index
                np.save(mkdir_join(save_path, 'phone61', save_file_name),
                        phone61_to_idx(phone61_list))
                np.save(mkdir_join(save_path, 'phone48', save_file_name),
                        phone48_to_idx(phone48_list))
                np.save(mkdir_join(save_path, 'phone39', save_file_name),
                        phone39_to_idx(phone39_list))
