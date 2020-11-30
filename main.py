from preprocessSearchItem import Preprocess
from getImageFromPixabay import FetchImage
from processImage import ProcessImage


def main():
    string = 'Sample text'
    main_script = Preprocess(string)
    print(len(string))
    keywords = main_script.get_key_words()
    print(keywords)
    image_path = FetchImage(keywords)
    image_path_string_array = image_path.fetch_image_path()
    print(image_path_string_array)
    image_path_string_array = ''
    process_image = ProcessImage(image_path_string_array, string, "~Sample attribution")
    downloaded_images_paths = process_image.download_images()

    generated_image_files = process_image.generate_images(downloaded_images_paths)
    print(generated_image_files)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
