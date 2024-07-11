from f_gui.pyqt.app import App
from proj.myq.gui.inner.container_qa import ContainerQA


class AppQA(App):

    def __init__(self) -> None:
        App.__init__(self, name='Myq')
        con_qa = ContainerQA(on_enter=AppQA._on_enter)
        self.add(con_qa, 10, 30, 80, 40)

    @staticmethod
    def _on_enter() -> None:
        print('ENTER')


app = AppQA()
app.run()
