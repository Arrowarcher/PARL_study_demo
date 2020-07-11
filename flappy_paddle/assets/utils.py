import cv2
import numpy as np
import matplotlib.pyplot as  plt
from PIL import Image


def show_img(img_cv):
    plt.figure()
    plt.imshow(img_cv)
    plt.axis('off')
    plt.show()

def add_alpha(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    # alpha_channel[:,:int(b_channel.shape[0])]=0
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    cv2.imwrite('shark2.png', img_BGRA)
    return img_BGRA

def set_alpha_0(img_cv):
    img = img_cv.copy()
    pos_to_white = np.where((img != [0, 0, 0,0]).all(axis=2))
    for i, j in zip(pos_to_white[0], pos_to_white[1]):
        img[i][j] = [153, 47, 134, 255]
    cv2.imwrite('p11.png', img)
    return img

def set_alpha_0_shark(img_cv):
    """
    [255 255 255 255]
[ 64  64  64 255]
[ 16  16  16 255]
[ 32  32  32 255]
[ 96  96  96 255]
[ 80  80  80 255]
[ 48  48  48 255]
[207 207 207 255]
[175 175 175 255]
[128 128 128 255]
    :param img_cv:
    :return:
    """
    img = img_cv.copy()
    # pos_to_white = np.where((img != [0, 0, 0,0]).all(axis=2))
    pos_to_white = np.where((img == [0, 0,0, 255]).all(axis=2))
    for i, j in zip(pos_to_white[0], pos_to_white[1]):
        img[i][j] = [16, 16, 16, 255]
        # print(img[i][j])
    cv2.imwrite('shark2_a.png', img)
    return img

def img_resize(img_cv):
    pic = cv2.resize(img_cv, (336, 112))
    cv2.imwrite('base1.png', pic)

def img_resize2(path):
    img = Image.open(path)
    img = img.resize((336, 112), Image.ANTIALIAS)
    # img.save('p111.png','png',quality=100)
    return img
def img_morph_open(img):
    kernel = np.ones((10, 10), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.imwrite('p11.png', opening)

def img_fuse(img1,img2):
    res = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    cv2.imwrite('new_base.png', res)
path2 = 'base.png'
path3 = 'base1.png'
# img = add_alpha(path)
# img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
# img = set_alpha_0(img)
# img_morph_open(img)
# path = 'p11.png'
# img_resize2(path)
# print(img)

img1 = cv2.imread(path2)
img2 = cv2.imread(path3)
# img_resize(img2)
img_fuse(img1,img2)