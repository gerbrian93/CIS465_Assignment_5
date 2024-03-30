import cv2
import numpy as np


def makebatches(lst, sizes):
    for i in range(0, len(lst), sizes):
        yield lst[i:i + sizes]

    return lst


def findDiff(img1, img2):
    num = 0
    for i in range(len(img1)):
        for j in range(len(img1[i])):
            num += abs(img1[i][j] - img2[i][j])
    return num


video1 = cv2.VideoCapture('html\Videos\Basketball_1.avi')

print('Please enter the batch size')
batchSize = int(input())
frames = 0
l = []

success, frame = video1.read()

while success:
    frames += 1
    aframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    l.append(aframe)
    success, frame = video1.read()

video1.release()

z = int(frames/batchSize)
batches = list(makebatches(l, z))

localDiff = []
localAvg = []
count = 0

for i in range(0, len(batches)):
    num = 0
    for j in range(1, len(batches[i])-1):
        frame1 = batches[i][j]
        frame2 = batches[i][j+1]
        frame1 = frame1.astype(np.int32)
        frame2 = frame2.astype(np.int32)
        value = findDiff(frame2, frame1)
        localDiff.append(value)
        num += value
    localAvg.append(round(num/len(batches[i])-1))

globalAvg = int(sum(localAvg)/(len(batches)-1))

stddev = np.std(localAvg)
beta = 0.5
keyframes = []
s = 0
count = 0

for m in range(len(batches)):
    avg = localAvg[m]
    for n in range(1, len(batches[m])-1):
        threshold = avg + (beta*stddev)
        frm1 = batches[m][n]
        frm2 = batches[m][n+1]
        frm1 = frm1.astype(np.uint8)
        frm2 = frm2.astype(np.uint8)
        avalue = localDiff[s]
        s += 1

        if avalue > threshold:
            keyframes.append(count)
            count += 1
        else:
            count += 1

filename = r"C:\Users\gerha\OneDrive\Desktop\Vidfolder\Basketball_2_745.avi"
framerate = 30
video2 = cv2.VideoWriter(filename, 0x7634706d, framerate, (576, 432))
vid = cv2.VideoCapture('html\Videos\Basketball_1.avi')
true, image = vid.read()
count2 = 0
while true:
    if count2 in keyframes:
        video2.write(image)
        count2 += 1
    else:
        count2 += 1
    true, image = vid.read()

video2.release()
cv2.destroyAllWindows()
