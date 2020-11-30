import requests
import shutil
from image_utils import ImageText, Image
from PIL import ImageFilter


class ProcessImage:

    def __init__(self, image_path_array, text, attribution=""):
        self.image_path_array = image_path_array
        self.text = text
        self.attribution = attribution

    def download_images(self):
        filename_array = []
        for image_path in self.image_path_array:
            filename = image_path.split("/")[-1]
            r = requests.get(image_path, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open("pics/{}".format(filename), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                filename_array.append(filename)
        return filename_array

    def generate_images(self, image_files_array):
        text_color = 'rgb(255, 255, 255)'
        font_name_credit = 'Roboto-Italic[wdth,wght].ttf'
        font_name = 'MeriendaOne-Regular.ttf'
        initial_font_size = 30
        initial_credit_size = 15
        text = self.text
        credit = self.attribution
        text_box_size = {'xlarge': .80, 'large': .50, 'medium': .40, 'small': .30, 'xsmall': .10}
        max_box_size = text_box_size['xlarge']
        if len(self.text) > 2070:
            self.text = 'Sorry, text too large'
        if len(self.text) <= 80:
            max_box_size = text_box_size['xsmall']
        if len(self.text) <= 150:
            max_box_size = text_box_size['small']
        elif len(self.text) <= 300:
            max_box_size = text_box_size['medium']
        elif len(self.text) <= 450:
            max_box_size = text_box_size['large']
        generated_image_files = []
        for image_file in image_files_array:
            image_file = "pics/{}".format(image_file)
            image2 = Image.open(image_file)
            image = image2.filter(ImageFilter.BoxBlur(0))
            img = ImageText(image_file, background=(0, 255, 255, 200))
            img2 = ImageText(image, background=(255, 255, 255, 200))
            text_box_size = img.write_text_box((5, 0), text, box_width=image.size[0] - 10, font_filename=font_name,
                                               font_size=initial_font_size, color=text_color)
            while text_box_size[1] < max_box_size * img.size[1]:
                initial_font_size += 3
                text_box_size = img.write_text_box((5, 0), text, box_width=image.size[0] - 10, font_filename=font_name,
                                                   font_size=initial_font_size, color=text_color)
            if text_box_size[1] > max_box_size * img.size[1]:
                initial_font_size -= 3
            text_box_size = img2.write_text_box((5, 0), text, box_width=image.size[0] - 10, font_filename=font_name,
                                                font_size=initial_font_size, color=text_color, place="center")
            credit_box_size = img.write_text_box((0, text_box_size[1] + initial_font_size), credit,
                                                 box_width=image.size[0] - 10, font_filename=font_name,
                                                 font_size=initial_credit_size, color=text_color)
            while credit_box_size[1] < .9 * (
                    img.size[1] - text_box_size[1]) and initial_credit_size < initial_font_size * .75:
                initial_credit_size += 3
                credit_box_size = img.write_text_box((0, text_box_size[1] + initial_font_size), credit,
                                                     box_width=image.size[0] - 10, font_filename=font_name_credit,
                                                     font_size=initial_credit_size, color=text_color)
            if credit_box_size[1] > .9 * (
                    img.size[1] - text_box_size[1]) or initial_credit_size > initial_font_size * .75:
                initial_credit_size -= 3
            img2.write_text_box((7, text_box_size[1] + initial_font_size), credit, box_width=image.size[0] - 10,
                                font_filename=font_name_credit,
                                font_size=initial_credit_size, color=text_color, place="right")
            generated_image_file_name = image_file.split('.')[0] + '.png'
            img2.save(generated_image_file_name)
            generated_image_files.append(generated_image_file_name)
        return generated_image_files
