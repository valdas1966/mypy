from f_gui.pyqt.app import App
from proj.myq.gui.inner.container_qa import ContainerQA


class AppQA(App):

    def __init__(self) -> None:
        App.__init__(self, name='Myq')
        self.background = 'black'
        con_qa = ContainerQA(on_enter=AppQA._on_enter)
        con_qa.position.relative = (0.1, 0.3, 0.8, 0.4)
        self.add(con_qa)

    @staticmethod
    def _on_enter() -> None:
        print('ENTER')


app = AppQA()
app.run()
