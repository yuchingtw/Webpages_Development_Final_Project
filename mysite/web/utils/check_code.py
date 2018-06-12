import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 生成隨機字串
def getRandomChar():
    # 產生一串小寫字母+數字
    ran = string.ascii_lowercase+string.digits
    char = ''
    for i in range(4):
        char += random.choice(ran)
    return char

# 回傳隨機顏色
def getRandomColor():
    return (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))


def create_code():

    # 建立圖片(色彩模式，大小，背景色)
    img = Image.new('RGB', (120, 30), (255, 255, 255))
    # 建立畫布
    draw = ImageDraw.Draw(img)
    #設置字體
    font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 30)
    
    code = getRandomChar()
    # 把產生的隨機字串畫在畫布上
    for t in range(4):
        draw.text((30*t+5, 0), code[t], getRandomColor(), font)

    # 產生干擾判斷的點
    for _ in range(random.randint(0, 50)):
        # (位置,顏色)
        draw.point((random.randint(0, 120), random.randint(0, 30)),
                   fill=getRandomColor())

    # 使用模糊濾鏡讓圖片模糊
    img = img.filter(ImageFilter.BLUR)
    #測試用的save
    #img.save(''.join(code)+'.jpg','jpeg')
    return img,code

if __name__ == '__main__':
    create_code()
