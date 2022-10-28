import sys
import os
import webbrowser


DEFAULT_WIDTH = 240
DEFAULT_HEIGHT = 135
PAGE_NAME = 'template.html'


def parse_args() -> tuple:
    """ Получить аргументы с командной строки """
    args = sys.argv[1:]
    url, width, height = None, DEFAULT_WIDTH, DEFAULT_HEIGHT
    try:
        url = args[0]
        width = args[1]
        height = args[2]
    except IndexError:
        pass

    return url, width, height


def get_template_page_path() -> str:
    """ Получить путь то файла шаблона """
    return os.path.join(os.getcwd(), 'page', PAGE_NAME)


def get_rendered_page_path() -> str:
    """ Получить путь до файла отрендеренного шаблона """
    return os.path.join(os.getcwd(), 'page', 'rendered_template.html')


def get_page_url(path_to_page: str) -> str:
    """ Получить путь до файла с шаблоном страницы """
    template_page_abs_path = prepare_url(path_to_page)
    return f"file://{template_page_abs_path}"


def prepare_url(url: str) -> str:
    """ Подготовить ссылку к открытию в браузере. Заменяет некоторые символы их кодом """
    return url.replace(' ', '%20')


def render_page(template_page_path: str, params: dict) -> str:
    """ Создает html страницу на основе шаблона станицы `template_page_path`,
     в которой шаблоны заменены значениями из `params`. Возвращает путь до созданного файла"""
    with open(template_page_path, mode='r', encoding='utf-8') as template:
        page = template.read()

    for key, value in params.items():
        page = page.replace('{{%s}}' % key, str(value))

    rendered_page_path = get_rendered_page_path()
    with open(rendered_page_path, mode='w', encoding='utf-8') as rendered_page:
        rendered_page.write(page)

    return rendered_page_path


def main() -> None:
    youtube_video_url, width, height = parse_args()
    rendered_page = render_page(
        get_template_page_path(),
        {
            'url': youtube_video_url,
            'width': width,
            'height': height,
        }
    )
    webbrowser.open(get_page_url(rendered_page))
    os.remove(rendered_page)


if __name__ == '__main__':
    main()
