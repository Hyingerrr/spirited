import time
from concurrent.futures import ThreadPoolExecutor

import save_deeplake
from book_maker import BookMaker
from dotenv import load_dotenv
from image_pdf import pdf_client

load_dotenv('conf.env')


def test_app_generate():
    inputs = 'a cute girl is running near the river and singing and jumping'
    model_name = 'gpt-3.5-turbo-0613'
    style = 'Monet, impressionist art style, loose brushstrokes, vibrant colors, painted, painted light'
    app = BookMaker(inputs, model_name, style)

    story_pages = ["Title: Lily's Joyful Adventure\n\n",
                   "\nLily skips along the river's bend,\nHer laughter echoing with every bend.\nShe twirls and sings "
                   "a merry tune,\nUnder the golden sun and a sky so blue.\n\n",
                   "\nThe river sparkles with a magical glow,\nAs Lily's feet dance to and fro.\nShe jumps over "
                   "pebbles, oh so small,\nAnd splashes in the water, having a ball.\n\nAmidst the green trees and "
                   "flowers so bright,\nLily's joy shines with all her might.\nShe sings with the birds, "
                   "their melodies entwined,\nAs she explores the wonders she's destined to find.\n\n",
                   "\nThe wind whispers secrets through the trees,\nAs Lily's laughter floats on the breeze.\nShe "
                   "leaps over rocks, as graceful as a fawn,\nAnd makes friends with creatures, big and small.\n\nA "
                   "bunny hops by, its fluffy tail so spry,\nWhile a squirrel chatters, scampering up high.\nLily "
                   "giggles and joins in their playful game,\nAs they all frolic together, without any shame.\n\nWith "
                   "each bound and skip, she fills the air,\nWith joy and happiness, beyond compare.\nLily's "
                   "adventure, so full of glee,\nIs a reminder for all to be wild and free.\n\nEnd of story."
                   ]
    # app.make_pages_prompt(story_pages)
    app.runner()
    # self.assertEqual(result, expected_value)


def save_to_deeplake():
    sd_prompts = [
        "a countryside, along a picturesque river, daytime, clear skies, sparkling river, green trees, "
        "colorful flowers, golden sunlight, vibrant colors ,golden sunlight, joyful and playful, bright and vivid, "
        "Lily skips along the river's bend, her laughter echoing with every bend. She twirls and sings a merry tune, "
        "under the golden sun and a sky so blue. The river sparkles with a magical glow, as Lily's feet dance to and "
        "fro. She jumps over pebbles, oh so small, and splashes in the water, having a ball. Amidst the green trees "
        "and flowers so bright, Lily's joy shines with all her might. She sings with the birds, their melodies "
        "entwined, as she explores the wonders she's destined to find. The wind whispers secrets through the trees, "
        "as Lily's laughter floats on the breeze. She leaps over rocks, as graceful as a fawn, and makes friends with "
        "creatures, big and small. A bunny hops by, its fluffy tail so spry, while a squirrel chatters, scampering up "
        "high. Lily giggles and joins in their playful game, as they all frolic together, without any shame. With "
        "each bound and skip, she fills the air, with joy and happiness, beyond compare. Lily's adventure, "
        "so full of glee, is a reminder for all to be wild and free., in the style of Monet, impressionist art style, "
        "loose brushstrokes, vibrant colors, painted, painted light",
        "a picturesque countryside, a serene riverbank, midday, sunny, sparkling river, green trees, "
        "colorful flowers, Lily jumping over pebbles, splashing in the water ,golden sunlight, joyful and playful, "
        "bright and vivid, Lily skips along the river's bend, her laughter echoing with every bend. She twirls and "
        "sings a merry tune, under the golden sun and a sky so blue. The river sparkles with a magical glow, "
        "as Lily's feet dance to and fro. She jumps over pebbles, oh so small, and splashes in the water, "
        "having a ball. Amidst the green trees and flowers so bright, Lily's joy shines with all her might. She sings "
        "with the birds, their melodies entwined, as she explores the wonders she's destined to find. The wind "
        "whispers secrets through the trees, as Lily's laughter floats on the breeze. She leaps over rocks, "
        "as graceful as a fawn, and makes friends with creatures, big and small. A bunny hops by, its fluffy tail so "
        "spry, while a squirrel chatters, scampering up high. Lily giggles and joins in their playful game, "
        "as they all frolic together, without any shame. With each bound and skip, she fills the air, with joy and "
        "happiness, beyond compare. Lily's adventure, so full of glee, is a reminder for all to be wild and free., "
        "in the style of Monet, impressionist art style, loose brushstrokes, vibrant colors, painted, painted light",
        "enchanted forest, a lush green meadow, afternoon, sunny, trees, river, rocks, whispering wind, playful animals ,golden sunlight, joyful and playful, bright and vivid, Lily skips along the river's bend, her laughter echoing with every bend. She twirls and sings a merry tune, under the golden sun and a sky so blue. The river sparkles with a magical glow, as Lily's feet dance to and fro. She jumps over pebbles, oh so small, and splashes in the water, having a ball. Amidst the green trees and flowers so bright, Lily's joy shines with all her might. She sings with the birds, their melodies entwined, as she explores the wonders she's destined to find. The wind whispers secrets through the trees, as Lily's laughter floats on the breeze. She leaps over rocks, as graceful as a fawn, and makes friends with creatures, big and small. A bunny hops by, its fluffy tail so spry, while a squirrel chatters, scampering up high. Lily giggles and joins in their playful game, as they all frolic together, without any shame. With each bound and skip, she fills the air, with joy and happiness, beyond compare. Lily's adventure, so full of glee, is a reminder for all to be wild and free., in the style of Monet, impressionist art style, loose brushstrokes, vibrant colors, painted, painted light"
    ]
    images = ['./images/1.png', './images/2.png', './images/3.png']
    ds = save_deeplake.DeeplakeClient()
    ds.save_executor(sd_prompts, images)


def thread_some():
    sd_pages_prompts = [1, 2, 3, 4, 5]

    def generate_image(no):
        print(f"当前是{no}")

    with ThreadPoolExecutor(max_workers=3) as executor:
        image_urls = list(executor.map(generate_image, sd_pages_prompts))


def book_generate():
    inputs = 'a cute girl is running near the river and singing and jumping'
    model_name = 'gpt-3.5-turbo-0613'
    style = 'Monet, impressionist art style, loose brushstrokes, vibrant colors, painted, painted light'
    app = BookMaker(inputs, model_name, style)
    sd_pages_prompts = app.runner()

    pdf_name = app.story_title.replace(" ", "_") + ".pdf".strip('"')
    print("PDF文件名：" + pdf_name)
    pdf_client.pdf_generator(sd_pages_prompts, pdf_name)


if __name__ == '__main__':
    # test_app_generate()
    # save_to_deeplake()

    book_generate()

    for _ in range(10):
        thread_some()
        print("&&&&&&&&&&&&&&&&&")
