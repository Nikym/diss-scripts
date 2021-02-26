import cv2

ROOT_PATH = '/media/external/diss/fat_dataset/fat'

def crop_image(img):
  cropped = img[30:30+480, 160:160+640]

  return cropped

if __name__ == '__main__':
  f = ROOT_PATH + '/kitchen_0/000000.right.jpg'
  img = cv2.imread(f)

  cropped = crop_image(img)
  
  cv2.imwrite('test.jpg', cropped)