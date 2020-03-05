import picamera, json, requests, os, random
from time import sleep
from PIL import Image, ImageDraw

#capture an image
camera = picamera.PiCamera()
camera.capture('image1.jpg')
print('caputred image')

#make a prediction on the image
url ='https://app.nanonets.com/api/v2/ObjectDetection/Model/150def91-2905-4c01-ad4a-e8eed48eb133/LabelUrls/'
data = {'file': open('image1.jpg', 'rb'), \
    'modelId': ('', '150def91-2905-4c01-ad4a-e8eed48eb133')}
response = requests.post(url, auth=requests.auth.HTTPBasicAuth('maqrHoFs5ozl-_Qb6rK-M-KuasJxqiiu', ''), files=data)
print(response.text)

#draw boxes on the image
response = json.loads(response.text)
im = Image.open("image1.jpg")
draw = ImageDraw.Draw(im, mode="RGBA")
prediction = response["result"][0]["prediction"]
for i in prediction:
    draw.rectangle((i["xmin"],i["ymin"], i["xmax"],i["ymax"]), fill=(random.randint(1, 255),random.randint(1, 255),random.randint(1, 255),127))
im.save("image2.jpg")
os.system("xdg-open image2.jpg")