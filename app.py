import os
import cv2
import random
from pascalvoc_generator import pascalvoc_gen
from utils import (set_overlay, prepare_overlay)


HEIGHT = 768 # generic image height
WIDTH = 1024 # generic image width
ANNOTATIONS_DIR = 'annotations'
VIDEO_SOURCE = './video_sources/2.mp4'
OVERLAY_SOURCE = './overlays/25.png'
CLASS_NAME = 'speedlimit25'


cam = cv2.VideoCapture(VIDEO_SOURCE) 

cur_frame = 0
i = 0

while(True): 

    ret,frame = cam.read() 

    if ret: 
        if i == 50:
            frame = cv2.resize(frame,(WIDTH,HEIGHT))
            img = ['horizontal_img', 
                   'vertical_img', 
                   'both_img', 
                   'invert_hor_img', 
                   'invert_vert_img', 
                   'invert_both_img', 
                   'invert_orig_img', 
                   'orig']

            for c,f in enumerate(img):
                overlay = cv2.imread(OVERLAY_SOURCE, cv2.IMREAD_UNCHANGED)
                source_h, source_w, _ = overlay.shape
                res_overlay = prepare_overlay(overlay)

                if f == 'orig':
                    background = frame
                if f == 'horizontal_img':
                    background = cv2.flip( frame, 0 )
                elif f == 'vertical_img':
                    background = cv2.flip( frame, 1 )
                elif f == 'both_img':
                    background = cv2.flip( frame, -1 )  
                elif f == 'invert_hor_img':
                    background = ~cv2.flip( frame, 0 )
                elif f == 'invert_vert_img':
                    background = ~cv2.flip( frame, 1 )
                elif f == 'invert_both_img':
                    background = ~cv2.flip( frame, -1 )
                elif f == 'invert_orig_img':
                    background = ~frame

                h,w,_ = res_overlay.shape
                x = random.randint(0, HEIGHT - h)
                y = random.randint(0, WIDTH - w)
                result_img = set_overlay(background, res_overlay, (y,x))

                folder = 'images'
                image_name = CLASS_NAME + '_' + str(cur_frame) + '_' + str(c) + '.jpg'
                image_w = str(WIDTH)
                image_h = str(HEIGHT)
                name = CLASS_NAME
                bndbox = [(str(y), str(x)), (str(w + y), str(h + x))]
                xml = pascalvoc_gen(folder, image_name, image_w, image_h, name, bndbox)

                with open(ANNOTATIONS_DIR + '/' + CLASS_NAME + '_' + str(cur_frame) + '_' + str(c) + '.xml', "wb") as fh:
                    fh.write(xml)

                cv2.imwrite('./images/' + image_name, result_img) 

                #Display the results for debug. Uncomment if you need.
                result1 = cv2.rectangle(result_img, (y, x), (w + y, h + x), (255,0,0), 2)
                print(xml) 
                cv2.imshow("Result" ,result_img)
                cv2.waitKey()
                cv2.destroyAllWindows()

            i = 0 
                
        cur_frame += 1
        i += 1
    else: 
        break
