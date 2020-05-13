# Please install opencv and ffmpeg first
# pip3 install opencv
# pip3 install ffmpeg


import sys
import cv2
import numpy as np
import math
import time


print("Please enter the file name: \n")
x = input()
# Set parameters
FILENAME_IN = x
#"test_left_v.avi"
FILENAME_OUT = "undistorted.avi"
CODEC = 'avi'
FC = [582.741, 580.065]  # focal lengths
CC = [635.154, 371.917]  # principle points for same
KC = [-0.228, 0.0469, 0.0003, -0.0005, 0.0000]  # distortion coeffs for same



def create_matrix_profile(fc, cc, kc):
    """Create the camera matrix and distortion profile.
    Take in the focal lengths, principle points, and distortion coefficients
    and return the camera matrix and distortion coefficients in the form
    OpenCV needs.
    Takes:
        fc - the x and y focal lengths [focallength_x, focallength_y]
        cc - the x and y principle points [point_x, point_y]
        kc - the distortion coefficients [k1, k2, p1, p2, k3]
    Gives:
        cam_matrix - the camera matrix for the video
        distortion_profile - the distortion profile for the video
    """
    fx, fy = fc
    cx, cy = cc
    cam_matrix = np.array([[fx,  0, cx],
                           [ 0, fy, cy],
                           [ 0,  0,  1]], dtype='float32')
    distortion_profile = np.array(kc, dtype='float32')
    return cam_matrix, distortion_profile

def undistort_image(img, cam_matrix, distortion_profile):
    """Apply a distortion profile to an image.
    Takes:
        img - the image to undistort
        cam_matrix - the camera matrix for the camera
        distortion_profile - the lens' distortion
    Gives:
        undis_img - the image, undistorted
    """
    return cv2.undistort(img, cam_matrix, distortion_profile)

def log_it(message):
    """Print message to sys.stdout, without new line."""
    sys.stdout.write(message + "\r")
    sys.stdout.flush()

def imshow(img):
    cv2.namedWindow('disp')
    cv2.imshow('disp', img)
    cv2.waitKey(5000)
    cv2.destroyWindow('disp')

def cut(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (_, thresh) = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    x,y,w,h = cv2.boundingRect(cnts)
    r = max(w/ 2, h/ 2)
    img_valid = img[y:y+h, x:x+w]
    return img_valid, int(r)

def get_K_and_D(checkerboard, imgsPath):

    CHECKERBOARD = checkerboard
    subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    _img_shape = None
    objpoints = []
    imgpoints = []
    images = glob.glob(imgsPath + '/*.png')
    for fname in images:
        img = cv2.imread(fname)
        if _img_shape == None:
            _img_shape = img.shape[:2]
        else:
            assert _img_shape == img.shape[:2], "All images must share the same size."

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret == True:
            objpoints.append(objp)
            cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),subpix_criteria)
            imgpoints.append(corners)
    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    rms, _, _, _, _ = cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )
    DIM = _img_shape[::-1]
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape[::-1]))
    print("K=np.array(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")
    return DIM, K, D


def fish_eye_dis(img):
    "fish eye distortion"
    width_in, height_in = img.size;
    im_out = Image.new("RGB",(width_in,height_in));
    radius = max(width_in, height_in)/2;
    #assume the fov is 180
    #R = f*theta
    lens = radius*2/math.pi;
    for i in range(width_in):
        for j in range(height_in):
            #offset to center
            x = i - width_in/2;
            y = j - height_in/2;
            r = math.sqrt(x*x + y*y);
            theta = math.atan(r/radius);
            if theta<0.00001:
                k = 1;
            else:
                k = lens*theta/r;
                
            src_x = x*k;
            src_y = y*k;
            src_x = src_x+width_in/2;
            src_y = src_y+height_in/2;
            pixel = im.getpixel((src_x,src_y));
            im_out.putpixel((i,j),pixel);

    return im_out;

def undistort(img_path,K,D,DIM,scale=0.6,imshow=False):
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if dim1[0]!=DIM[0]:
        img = cv2.resize(img,DIM,interpolation=cv2.INTER_AREA)
    Knew = K.copy()
    if scale:#change fov
        Knew[(0,1), (0,1)] = scale * Knew[(0,1), (0,1)]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), Knew, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    if imshow:
        cv2.imshow("undistorted", undistorted_img)
    return undistorted_img

def main():
    cam_matrix, profile = create_matrix_profile(FC, CC, KC)
    # Load video
    video = cv2.VideoCapture(FILENAME_IN)
    fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    writer = cv2.VideoWriter(FILENAME_OUT, fourcc, fps, size)
    while video.grab() is True:
        log_it("On frame %i of %i."%(video.get(cv2.CAP_PROP_POS_FRAMES),
                                    frame_count))
        frame =  cv2.undistort(video.retrieve()[1], cam_matrix, profile)
        writer.write(frame)
    video.release()
    writer.release()

if __name__ == '__main__':
	main()
