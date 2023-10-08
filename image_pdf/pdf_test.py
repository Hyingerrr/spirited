import unittest

from image_pdf.pdf_client import generate_page_title, pdf_generator


class TestGenPdf(unittest.TestCase):

    def test_build_title_page(self) :
        img_path = "../images/1.png"
        text = "a cute girl"
        output_filename = "./title.pdf"
        image_size = (1360, 1174)

        try:
            generate_page_title(img_path, text, output_filename, image_size)
        except:
            print("occur an error")


    def test_pdf_generate(self):
        result_name = '../images/test1.pdf'
        pages_images_mapping = [('../images/1.png', 'Build a book'),
            ('../images/2.png', 'a magical forest, a sunlit glade, morning, clear skies, tall trees, colorful flowers, a sparkling stream, sunlight filtering through the trees, warm and vibrant colors ,sunlight filtering through the trees, joyful and adventurous, warm and vibrant, On a sunny morning, little kitty Milk Tea wakes up and decides to go on an adventure in the forest. She meets a friendly squirrel and together they explore the forest, play, and find a hidden treasure. They form a strong friendship and return home with hearts full of joy and magical memories., in the style of 印象派'),
                                ('../images/3.png', "a lush forest, a serene woodland with towering trees, a sunny morning, a gentle breeze, sunlight filtering through ttrees, Milk Tea's paws pattered on the forest floor as she ventured deeper into the woods. The tall trees whispered secrets, and sunlight danced through the leaves above. She breathed in the fresh scent of pine and felt the cool breeze brush against her whiskers. The forest was alive with excitement. ,sunlight filtering through the trees, joyful and adventurous, warm and vibrant, On a sunny morning, little kitty Milk Tea wakes up and decides to go on an adventure in the forest. She meets a friendly squirrel and together they explore the forest, play, and find a hidden treasure. They form a strong friendship and return home with hearts full of joy and magical memories., in the style of 印象派")]
        try:
            res = pdf_generator(pages_images_mapping, result_name)
        except Exception as e:
            print(e)
        else:
            print(res)