import cv2
import numpy as np


def cameraCapture():

    # take photo
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)


    ###############################################################
    #
    # You have only 5 sec to put sudoku card in front of camera
    #
    ###############################################################

    i = 0
    if camera.isOpened():   
        print("Camera opened")
        print("You have only 5 sec to put sudoku card in front of camera")
        while i < 25:
            cv2.waitKey(5)
            _, image = camera.read()
            cv2.imwrite("../resources/srcImage.jpg", image)
            i += 1
        print("Camera release") 
        camera.release()    
        del(camera)


def segmentation():

    # black & white
    img = cv2.imread('../resources/srcImage.jpg')
    img = cv2.GaussianBlur(img,(5,5),0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    mask = np.zeros((gray.shape),np.uint8)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

    # !! disable WARN 
    np.seterr(divide='ignore', invalid='ignore')

    close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
    div = np.float32(gray)/(close)
    res = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
    res2 = cv2.cvtColor(res,cv2.COLOR_GRAY2BGR)
    cv2.imwrite("../resources/opencv-1.png", res2)


    # cutting the sudoku square
    thresh = cv2.adaptiveThreshold(res,255,0,1,19,2)
    contour,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    best_cnt = None
    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = cnt

    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)
    res = cv2.bitwise_and(res,mask)
    cv2.imwrite("../resources/opencv-2.png", res)

    # vertical lines
    kernelx = cv2.getStructuringElement(cv2.MORPH_RECT,(2,10))

    dx = cv2.Sobel(res,cv2.CV_16S,1,0)
    dx = cv2.convertScaleAbs(dx)
    cv2.normalize(dx,dx,0,255,cv2.NORM_MINMAX)
    ret,close = cv2.threshold(dx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernelx,iterations = 1)

    contour, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h = cv2.boundingRect(cnt)
        if h/w > 5:
            cv2.drawContours(close,[cnt],0,255,-1)
        else:
            cv2.drawContours(close,[cnt],0,0,-1)
    close = cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations = 2)
    closex = close.copy()
    cv2.imwrite("../resources/opencv-3.png", closex)

    # horizontal lines
    kernely = cv2.getStructuringElement(cv2.MORPH_RECT,(10,2))
    dy = cv2.Sobel(res,cv2.CV_16S,0,2)
    dy = cv2.convertScaleAbs(dy)
    cv2.normalize(dy,dy,0,255,cv2.NORM_MINMAX)
    ret,close = cv2.threshold(dy,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernely)

    contour, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h = cv2.boundingRect(cnt)
        if w/h > 5:
            cv2.drawContours(close,[cnt],0,255,-1)
        else:
            cv2.drawContours(close,[cnt],0,0,-1)

    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,None,iterations = 2)
    closey = close.copy()
    cv2.imwrite("../resources/opencv-4.png", closey)

    # finding grid points
    res = cv2.bitwise_and(closex,closey)
    cv2.imwrite("../resources/opencv-5.png", res)

    # finding centroids
    contour, hier = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    centroids = []
    for cnt in contour:
        mom = cv2.moments(cnt)
        try:
            if mom['m00'] < 0.001:
                continue;

            (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
            cv2.circle(img,(x,y),4,(0,255,0),-1)
            centroids.append((x,y))
        except:
            print("Division by zero")


    # sorting them

    if len(centroids) != 100:
      print("You've got an ugly picture! Try again")

    centroids = np.array(centroids,dtype = np.float32)
    c = centroids.reshape((len(centroids),2))
    c2 = c[np.argsort(c[:,1])]
    b = np.vstack(
        [c2[i*10:(i+1)*10][np.argsort(c2[i*10:(i+1)*10,0])] for i in xrange(10)]
    )
    bm = b.reshape((10,10,2))

    # creating better image 
    output = np.zeros((450,450,3),np.uint8)
    for i,j in enumerate(b):
        ri = i/10
        ci = i%10
        if ci != 9 and ri!=9:
            src = bm[ri:ri+2, ci:ci+2 , :].reshape((4,2))
            dst = np.array( [ [ci*50,ri*50],[(ci+1)*50-1,ri*50],[ci*50,(ri+1)*50-1],[(ci+1)*50-1,(ri+1)*50-1] ], np.float32)
            retval = cv2.getPerspectiveTransform(src,dst)
            warp = cv2.warpPerspective(res2,retval,(450,450))
            output[ri*50:(ri+1)*50-1 , ci*50:(ci+1)*50-1] = warp[ri*50:(ri+1)*50-1 , ci*50:(ci+1)*50-1].copy()

    cv2.imwrite("../resources/opencv-7.png", output) 
    

def trainingDigits():

    im = cv2.imread('../resources/opencv-7.png') 
    im3 = im.copy()

    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    thresh = cv2.adaptiveThreshold(blur,255, cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY,11,2)
    # thresh = cv2.adaptiveThreshold(blur,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY_INV,11,2)

    # Now finding Contours

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    samples =  np.empty((0,100))
    responses = []
    keys = [i for i in range(48,58)]

    for cnt in contours:
        if cv2.contourArea(cnt)>50:
            [x,y,w,h] = cv2.boundingRect(cnt)

            if  h>28:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                cv2.imshow('norm',im)
                key = cv2.waitKey(0)

                ################################################
                #
                # Uncomment if your keyboard is strange and have different values under the digits 
                # (this values should be between 48 - 58) :)
                #
                #################################################33
                # key = key - (1114032 - 48)
             
                print key
                if key in keys:
                    print int(chr(key))
                    responses.append(int(chr(key)))
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)
             

    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    print "training complete"

    np.savetxt('../trainingDigits/generalsamples.data',samples)
    np.savetxt('../trainingDigits/generalresponses.data',responses)


def testingDigits():
    #######   training part    ############### 
    samples = np.loadtxt('../trainingDigits/generalsamples.data',np.float32)
    responses = np.loadtxt('../trainingDigits/generalresponses.data',np.float32)
    responses = responses.reshape((responses.size,1))

    model = cv2.KNearest()
    model.train(samples,responses)

    ############################# testing part  #########################

    im = cv2.imread('../resources/opencv-7.png')
    out = np.zeros(im.shape,np.uint8)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY,11,2)
    # thresh = cv2.adaptiveThreshold(blur,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY_INV,11,2
    # thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt)>50:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  h>28:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
                string = str(int((results[0][0])))
                cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

    # cv2.imshow('im',im)
    # cv2.imshow('out',out)
    cv2.imwrite("../resources/opencv-8.png", out) 
    cv2.waitKey(0)


if __name__ == '__main__':
    cameraCapture() 
    segmentation()

    # trainingDigits()
    testingDigits()