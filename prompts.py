
# 写一本精彩的6-8页儿童绘本。每页需要有2-3句故事描述用于介绍图片的内容。描述要有韵律，串起来要是一个完整的故事。

# 整体需要围绕某个场景，每一页要适当拓展添加环境、风景和辅助参照物的图片。

# 在故事开始之前，先定义一个标题，写一个“标题：｛title｝”页面。 标题不超过七个字。

# 格式如：标题：｛title｝，第1页：｛text｝。 不要写其他内容
BOOK_DESC_PROMPT = """Write an exciting {} page children's picture book. Each page needs 2-3 sentences of descriptions to 
introduce the content of the images. The description should have rhythm and be strung together to form a complete 
story. The whole needs to revolve around the following theme, and each page should be appropriately expanded to include 
images of the environment, scenery, and auxiliary references.

Before starting the story, define a title and write a "Title: {{title}}" page. The title should not exceed seven words.

The format is as follows: title: {{title}}, page 1: {{text}}. Don't write anything else

The theme of the story is:  
"""


get_book_sentiment_atmosphere = [{
    'name': 'get_lighting_and_atmosphere',
    'description': 'Generate a highly detailed visual description of the overall atmosphere and color palette of a '
                   'book',
    'parameters': {
        'type': 'object',
        'properties': {
            'lighting': {
                'type': 'string',
                # 这本书的轻松气氛，例如愉快的气氛
                'description': 'The lighting atmosphere of the book, eg. cheerful atmosphere',
            },
            'mood': {
                'type': 'string',
                # 这本书的情调，例如活泼的情调
                'description': 'The mood of the book, eg. lively mood',
            },
            'color_palette': {
                'type': 'string',
                # 这本书的调色板，例如明亮生动的调色板
                'description': 'The color palette of the book, eg. bright and vivid color palette', 
            },
            'page_summary': {
                'type': 'string',
                'description': 'a brief summary of the current passage'
            },
        },
        'required': ['lighting', 'mood', 'color_palette', 'page_summary']
    }
}]

get_visual_description = [{
    'name': 'get_every_page',
    'description': 'Generate and describe the visuals of a passage in a book. Visuals only, no characters, plot, '
                   'or people. Highly detailed',
    'parameters': {
        'type': 'object',
        'properties': {
            'base_setting': {
                'type': 'string',
                'description': 'The base setting of the passage, e.g. ancient Rome, Switzerland, etc.',
            },
            'setting': {
                'type': 'string',
                'description': 'The detailed visual setting of the passage, e.g. a a snowy mountain village',
            },
            'time_of_day': {
                'type': 'string',
                'description': 'The detailed time of day of the passage, e.g. nighttime, daytime, dawn.',
            },
            'weather': {
                'type': 'string',
                'description': 'The detailed weather of the passage, e.g. heavy rain with dark clouds.',
            },
            'key_elements': {
                'type': 'string',
                'description': 'The detailed key visual elements of the passage, e.g. colorful houses, a church, '
                               'and a lake. ',
            },
            'specific_details': {
                'type': 'string',
                'description': 'The detailed specific visual details of the passage, Within 200 characters',
            }
        },
        'required': ['base_setting', 'setting', 'time_of_day', 'weather', 'key_elements', 'specific_details']
    }
}]