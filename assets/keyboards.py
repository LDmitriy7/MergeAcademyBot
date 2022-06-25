from core.objects import Keyboard


class Main(Keyboard):
    master_class = '💬 Майстер-клас'
    course = '🧑‍💻 Курс Webflow.Basic'
    website = '🌐 Відвідати веб-сайт'

    def make(self):
        self.add_rows(
            self.master_class,
            self.course,
            self.website,
        )
