from pixabay import Image
import random


class FetchImage:

    def __init__(self, search_term):
        self.search_terms = search_term
        self.image_url = ""
        self.api_key = ''

    def fetch_image_path(self):
        image = Image(self.api_key)
        image_path_array = []
        selected_search_terms = []
        if self.search_terms.__len__() <= 3:
            selected_search_terms = self.search_terms
        else:
            while selected_search_terms.__len__() < 3:
                selected_search_terms.append(self.search_terms[random.randint(0, self.search_terms.__len__() - 1)])
        for term in selected_search_terms:
            try:
                ims = image.search(q=term, image_type='photo', orientation='vertical')
                number_of_hits = ims['hits'].__len__()
                selected_index_array = []
                if 2 >= number_of_hits > 0:
                    while selected_index_array.__len__() <= number_of_hits:
                        selected_index = random.randint(0, number_of_hits - 1)
                        selected_index_array.append(selected_index)
                else:
                    while selected_index_array.__len__() < 2:
                        selected_index = random.randint(0, number_of_hits - 1)
                        selected_index_array.append(selected_index)
                for selected_index in selected_index_array:
                    image_path = ims['hits'][selected_index]['largeImageURL']
                    image_path_array.append(image_path)
            except IndexError:
                continue
            except ValueError:
                continue
        if len(image_path_array) == 0:
            term = 'sorry'
            try:
                ims = image.search(q=term, image_type='photo', orientation='vertical')
                image_path_array = {'apology_image': ims['hits'][0]['largeImageURL']}
            except IndexError:
                print("Index Error")
            except ValueError:
                print("Value Error")
        return image_path_array
