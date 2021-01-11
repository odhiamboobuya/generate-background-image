from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from preprocessSearchItem import Preprocess
from getImageFromPixabay import FetchImage
from processImage import ProcessImage
import api_keys_config as cfg


def start(bot, update):
    update.message.reply_text(
        'Hello, send us your glorious text and we\'ll put a background on it! You can find a sample without '
        'attribution at https://t.me/book_excerpts/268')
    update.message.reply_text(
        'If the text is from a book or you wish to add an attribution, you can find a sample with attribution at '
        'https://t.me/book_excerpts/271')
    #update.message.reply_text(
     #   'You can also upload your preferred background image, and we\'ll work with it instead of one of ours ')


def start2(bot, update):
    update.message.reply_text('Please wait as we generate your image. Could take a literal minute :-(')
    chat_id = update.message.chat_id
    string = update.message.text
    string_without_credit = string
    if string.split('$$').__len__() == 3:
        credit = string.split('$$')[1]
        string_without_credit = string.replace('$$' + credit + '$$', '').strip()
    if string.split('##').__len__() == 3:
        custom_keywords = string.split('##')[1]
        string = string.replace('##' + custom_keywords + '##', '').strip()
        keywords = custom_keywords.split(' ')
    else:      
        main_script = Preprocess(string_without_credit)
        keywords = main_script.get_key_words()
    print(keywords)
    image_path = FetchImage(keywords)
    image_path_string_array = image_path.fetch_image_path()
    if type(image_path_string_array) is dict:
        string = 'Sorry, image not found'
        image_path_string_array = [image_path_string_array['apology_image']]
    print(image_path_string_array)
    if string.split('$$').__len__() == 3:
        credit = string.split('$$')[1]
        string = string.replace('$$' + credit + '$$', '').strip()
        process_image = ProcessImage(image_path_string_array, string, "~" + credit)
    else:
        process_image = ProcessImage(image_path_string_array, string)
    downloaded_images_paths = process_image.download_images()
    for path in downloaded_images_paths:
        try:
            generated_image_file = process_image.generate_images([path])
            print(generated_image_file)
            update.message.reply_text(
                "Image {} of {}".format(downloaded_images_paths.index(path) + 1, len(downloaded_images_paths)))
            bot.send_photo(chat_id=chat_id, photo=open(generated_image_file[0], 'rb'))
        except Exception as e:
            print("encountered error: {}".format(e))
    update.message.reply_text('Done. please paste the message again to repeat the search')


def stop(bot, update):
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END


def main():
    updater = Updater(cfg.api_keys['telegram'])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start2))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
