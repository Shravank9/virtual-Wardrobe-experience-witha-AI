import subprocess
import sys

# Install required packages
subprocess.check_call([
    sys.executable,
    "-m",
    "pip",
    "install",
    "opencv-python-headless",
    "pillow",
    "numpy"
])

import cv2
import os
from PIL import Image
import numpy as np
import glob
import warnings
import argparse



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--background',
        type=bool,
        default=True,
        help='Define removing background or not'
    )

    opt = parser.parse_args()

    # =====================================
    # READ INPUT IMAGE
    # =====================================

    img = cv2.imread("./static/origin_web.jpg")

    if img is None:

        print("Input image not found")

        exit()

    ori_img = cv2.resize(
        img,
        (768, 1024)
    )

    cv2.imwrite(
        "./origin.jpg",
        ori_img
    )

    # =====================================
    # RESIZE INPUT IMAGE
    # =====================================

    img = cv2.imread('origin.jpg')

    img = cv2.resize(
        img,
        (384, 512)
    )

    cv2.imwrite(
        'resized_img.jpg',
        img
    )

    # =====================================
    # GET CLOTH MASK
    # =====================================

    print("Get mask of cloth")

    os.system(
        "python get_cloth_mask.py"
    )

    # =====================================
    # GET POSENET
    # =====================================

    print("Get openpose coordinate using posenet")

    os.system(
        "python posenet.py"
    )

    # =====================================
    # GRAPHONOMY SEGMENTATION
    # =====================================

    print("Generate semantic segmentation")

    os.chdir("./Graphonomy-master")

    os.system(
        "python exp/inference/inference.py "
        "--loadmodel ./inference.pth "
        "--img_path ../resized_img.jpg "
        "--output_path ../ "
        "--output_name /resized_segmentation_img"
    )

    os.chdir("../")

    # =====================================
    # LOAD SEGMENTATION MASK
    # =====================================

    mask_img = cv2.imread(
        './resized_segmentation_img.png',
        cv2.IMREAD_GRAYSCALE
    )

    if mask_img is None:

        print("Segmentation image not generated")

        exit()

    mask_img = cv2.resize(
        mask_img,
        (768, 1024)
    )

    k = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    mask_img = cv2.erode(
        mask_img,
        k
    )

    img_seg = cv2.bitwise_and(
        ori_img,
        ori_img,
        mask=mask_img
    )

    back_ground = ori_img - img_seg

    img_seg = np.where(
        img_seg == 0,
        215,
        img_seg
    )

    cv2.imwrite(
        "./seg_img.png",
        img_seg
    )

    img = cv2.resize(
        img_seg,
        (768, 1024)
    )

    cv2.imwrite(
        './HR-VITON-main/test/test/image/00001_00.jpg',
        img
    )

    # =====================================
    # GENERATE GRAYSCALE SEGMENTATION
    # =====================================

    os.system(
        "python get_seg_grayscale.py"
    )

    # =====================================
    # DENSEPOSE
    # =====================================

    print("Generate Densepose image")

    os.system(
        "python detectron2/projects/DensePose/apply_net.py "
        "dump "
        "detectron2/projects/DensePose/configs/densepose_rcnn_R_50_FPN_s1x.yaml "
        "https://dl.fbaipublicfiles.com/densepose/densepose_rcnn_R_50_FPN_s1x/165712039/model_final_162be9.pkl "
        "origin.jpg "
        "--output output.pkl -v"
    )

    os.system(
        "python get_densepose.py"
    )

    # =====================================
    # RUN HR-VITON
    # =====================================

    print("Run HR-VITON")

    os.chdir("./HR-VITON-main")

    os.system(
        "python test_generator.py "
        "--cuda False "
        "--test_name test1 "
        "--tocg_checkpoint mtviton.pth "
        "--gpu_ids -1 "
        "--gen_checkpoint gen.pth "
        "--datasetting unpaired "
        "--data_list t2.txt "
        "--dataroot ./test"
    )

    # =====================================
    # OUTPUT IMAGES
    # =====================================

    l = glob.glob("./Output/*.png")

    if len(l) == 0:

        print("No output images generated")

        exit()

    # ADD BACKGROUND
    if opt.background:

        for i in l:

            img = cv2.imread(i)

            img = cv2.bitwise_and(
                img,
                img,
                mask=mask_img
            )

            img = img + back_ground

            cv2.imwrite(
                i,
                img
            )

    else:

        for i in l:

            img = cv2.imread(i)

            cv2.imwrite(
                i,
                img
            )

    os.chdir("../")

    cv2.imwrite(
        "./static/finalimg.png",
        img
    )

    print("Final image generated successfully")
