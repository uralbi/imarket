from PIL import Image


def image_process(image_path):
    raw_image = Image.open(image_path)
    rgb_image = raw_image.convert('RGB')
    width, height = rgb_image.size
    img_ratio = round(width/height,2)

    if img_ratio < 0.8:
        cr_size = (height - width) / 2.2
        cr_image = rgb_image.crop((0, cr_size, width , height- cr_size))
        cr_image.save(image_path)
    elif img_ratio > 1.6:
        cr_size = (width - height) / 2.7
        cr_image = rgb_image.crop((0 + cr_size, 0, width - cr_size, height))
        cr_image.save(image_path)

    rgb_image = Image.open(image_path)
    width, height = rgb_image.size
    img_ratio = round(width/height,2)

    max_size = 900
    new_width = width
    new_height = height

    if img_ratio >= 1 and width > max_size:
        new_ratio = round(max_size/width,3)
        new_width=round(new_ratio*width,0)
        new_height=round(new_ratio*height,0)
    elif img_ratio <= 1 and height > max_size:
        new_ratio = round(max_size/height,3)
        new_width=round(new_ratio*width,0)
        new_height=round(new_ratio*height,0)

    new_size=(int(new_width), int(new_height))
    rsz = rgb_image.resize(new_size)
    rsz.save(image_path)

