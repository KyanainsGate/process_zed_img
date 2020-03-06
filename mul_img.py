import matplotlib.pyplot as plt
import glob
from PIL import Image, ImageDraw
import cv2
import argparse
import os
from multiprocessing import Pool
import multiprocessing as multi
import numpy as np

DEPTH_BOOL = True
RIGHT_BOOL = False
DAY = 20190404
TIME = 150302
START_ID = 2
END_ID = 2000


def _mul_2_img(png_name, save_dir='./', out_info='', show_img=False):
    """
    Specify the area of image to trim, and reduct the size of it.

    :param png_name: filename(e.g. left00***.png)
    :param save_dir: str type, output dir name
    :param out_info: str, you can rename prosecced png file
    :param show_img:
    :return:
    """
    left_00n = png_name.split('.')[-2]
    name_without_path = left_00n.split('/')[-1]
    name_len = len(name_without_path)
    path = left_00n[:-name_len]
    img_not_type_part = None
    type_flag = 'left'
    if 'left' in name_without_path:
        img_not_type_part = name_without_path[4:]
    elif 'right' in name_without_path:
        img_not_type_part = name_without_path[5:]
        type_flag = 'right'
    depth_00n = 'depth' + img_not_type_part
    depth_png_name = '.' + path + depth_00n + '.png'
    generate_img_name = save_dir + type_flag + depth_00n + '.png'
    # print(depth_png_name)
    # print(generate_img_name)

    img = cv2.imread(png_name, cv2.IMREAD_COLOR)
    img_d = cv2.imread(depth_png_name, cv2.IMREAD_GRAYSCALE) / 255.0
    img_d_for_mul = np.array([img_d, img_d, img_d, ]).transpose(1, 2, 0)
    inner = img * img_d_for_mul
    dst = inner.astype(np.uint8)
    t = cv2.imwrite(generate_img_name, dst)

    if show_img:
        cv2.imshow('image', dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def export_mulimg(import_dirname, export_dirname, start_id, end_id, mul_type='left'):
    if not os.path.exists(export_dirname):
        os.mkdir(export_dirname)
    left_img_list = _find_png(mul_type, import_dirname, start_id, end_id)
    # depth_img_list = _find_png('depth', import_dirname, start_id, end_id)
    # print(left_img_list)
    # _mul_with_depth_(left_img_list[0])
    p = Pool(7)
    p.map(_mul_with_depth_, left_img_list)
    p.close()
    pass


def _mul_with_depth_(png_filename):
    """
    Get filename(e.g. ~~.png) and export processed images;
    >> Name will change to '~~cut.png'
    >> Output dir is 'img-cut'

    :param png_filename:
    :return:
    """
    export_dir = png_filename.split('img')[0]  # Get export dirname process
    export_dir = export_dir + 'img-mul/'
    # print(export_dir)
    _mul_2_img(png_filename, save_dir=export_dir, out_info='mul')


def _find_png(png_type, dir_name, start_id, end_id):
    """
    Get the png file names, and id to process.
    The process will be done based on id
    e.g.) start_id = 3, end_id = 10, image I[n] will be processed from I[3] to I[10], 8 images.

    :param png_type: left or right or depth
    :param dir_name: directory name which contains left***.png
    :param start_id:
    :param end_id:
    :return:
    """
    png_list = glob.glob(dir_name + png_type + "*.png")
    png_list.sort()
    return png_list[start_id - 1:end_id]


if __name__ == '__main__':
    print('Start process')
    # import_dir = './' + DAY + '/' + TIME + '/' + 'img/'
    import_dir = './' + str(DAY) + '/' + str(TIME) + '/' + 'img' + '-cut/'
    export_dir = './' + str(DAY) + '/' + str(TIME) + '/' + 'img' + '-mul/'
    export_mulimg(import_dir, export_dir, START_ID, END_ID, mul_type='right')
    print('END')
