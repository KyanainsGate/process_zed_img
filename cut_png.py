"""
 Trimming and down-sizing the image data
 which are filmed by ZED(or ZED-mini) camera.
 Only left images are processed by python-opencv module.

"""
import matplotlib.pyplot as plt
import glob
from PIL import Image, ImageDraw
import cv2
import argparse
import os
from multiprocessing import Pool
import multiprocessing as multi

CUT_TYPES = ['Square', 'Original', ]

parser = argparse.ArgumentParser(description='Training method')
parser.add_argument('date')
parser.add_argument('time')
parser.add_argument('usable_cpu', type=int)
parser.add_argument('start_id', type=int)
parser.add_argument('end_id', type=int)
parser.add_argument('--depth', action='store_true')
parser.add_argument('--right', action='store_true')

args = parser.parse_args()

DAY = args.date
TIME = args.time
USABLE_CPU = args.usable_cpu
START_ID = args.start_id
END_ID = args.end_id
DEPTH_BOOL = args.depth
RIGHT_BOOL = args.right
H_RANGE = [0, 376]  # cvae_2019ver ... original size
W_RANGE = [148, 524]  # cvae_2019ver ... squared size
# W_RANGE = [0, 672]  # cvae_2019ver ... original size
COMPRESS = 8  # cvae_2019ver
SQUARED_IMG_SIZE = 64


# im_size = 64 # ito deformable
# H_RANGE = [0, 720] # ito deformable
# W_RANGE = [210, 930] # ito deformable


def _cut_forcuspoint_range(png_name, h_range=H_RANGE, w_range=W_RANGE, im_size=SQUARED_IMG_SIZE,
                           compress_ratio=COMPRESS, save_dir='./', out_info='',
                           show_img=False):
    """
    Specify the area of image to trim, and reduct the size of it.

    :param png_name: filename(e.g. left00***.png)
    :param h_range: list type, [top_lim, bottom_lim]
    :param w_range: list type, [left_lim, right_lim]
    :param im_size: int type, the processed image size (square image will be produced)
    :param save_dir: str type, output dir name
    :param out_info: str, you can rename prosecced png file
    :param show_img:
    :return:
    """
    h_min, h_max = h_range
    w_min, w_max = w_range
    w, h = (w_max - w_min), (h_max - h_min)
    img = cv2.imread(png_name, cv2.IMREAD_COLOR)
    img_RGB = img[:, :, [0, 1, 2]]
    dst = img_RGB[h_min:h_max, w_min:w_max, :]
    if w == h:
        # Square images will be generated
        dst = cv2.resize(dst, (im_size, im_size))
    else:
        # NOT squared images will be generated
        im_w = int(w / compress_ratio)
        im_h = int(h / compress_ratio)
        dst = cv2.resize(dst, (im_w, im_h))

    left_00n = png_name.split('.')[-2]
    left_00n = left_00n.split('/')[-1]
    out_name = save_dir + left_00n + out_info + '.png'
    t = cv2.imwrite(out_name, dst)

    if show_img:
        cv2.imshow('image', dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def _compress_(png_name, ):
    return 0


def _cut_multi_(png_filename):
    """
    Get filename(e.g. ~~.png) and export processed images;
    >> Name will change to '~~cut.png'
    >> Output dir is 'img-cut'

    :param png_filename:
    :return:
    """
    export_dir = png_filename.split('img')[0]  # Get export dirname process
    export_dir = export_dir + 'img-cut/'
    _cut_forcuspoint_range(png_filename, save_dir=export_dir, out_info='cut')


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


def export_cutimg(import_dirname, start_id, end_id):
    export_dirname = import_dir[:-1] + '-cut'  # Get export dirname process
    if not os.path.exists(export_dirname):
        os.mkdir(export_dirname)
    left_img_list = _find_png('left', import_dirname, start_id, end_id)
    if DEPTH_BOOL:
        depth_img_list = _find_png('depth', import_dirname, start_id, end_id)
        left_img_list.extend(depth_img_list)
    if RIGHT_BOOL:
        right_img_list = _find_png('right', import_dirname, start_id, end_id)
        left_img_list.extend(right_img_list)
    p = Pool(USABLE_CPU)
    p.map(_cut_multi_, left_img_list)
    p.close()
    pass


if __name__ == '__main__':
    print('Start process')
    import_dir = './' + DAY + '/' + TIME + '/' + 'img/'
    export_cutimg(import_dir, START_ID, END_ID)
    print('END')
