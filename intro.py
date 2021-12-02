from linebot.models.actions import MessageAction
from linebot.models.template import CarouselColumn


def intro_carousel(title, description, image_url):
    CarouselColumn(
        thumbnail_image_url=image_url,
        title=title,
        text=description,
        actions=[
            MessageAction(
                label='詳細',
                text=title + ' 詳細'
            ),
            MessageAction(
                label='これにする！',
                text=title
            )
        ]
    ),