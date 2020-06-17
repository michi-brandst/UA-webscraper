from web import get_pdf, upload_file


class Article:
    def __init__(self, article_html):
        self.name = article_html.div.div.div.h4.a.text
        self.__original_name = self.name
        self.__name_wo_index = self.name
        self.__format_name()

        self.link = article_html.div.div.p.a['href']
        self.__index = 0

        self.__pdf = None

    def __str__(self):
        return f'Article {self.__original_name}'

    def set_index(self, index):
        self.__index = index
        self.name = f'{self.__index}_{self.name}'

    def __format_name(self):
        chars = ['Unearthed Arcana: ', ':', ',', '!']

        for c in chars:
            self.name = self.name.replace(c, '')

        self.name = self.name.replace(' ', '_')
        self.name = self.name.lower()
        self.__name_wo_index = self.name

    def get_original_name(self):
        return self.__original_name

    def get_name_without_index(self):
        return self.__name_wo_index

    def get_index(self):
        return self.__index

    def load_pdf(self, dir):

        self.__pdf = get_pdf(self)

        if not self.__pdf:
            return

        with open(f'{dir}/{self.name}.pdf', 'wb') as f:
            f.write(self.__pdf)

        print(f'{self.__original_name} written in cache directory.')

        upload_file(self, dir)

        # clear from memory
        self.__pdf = None
