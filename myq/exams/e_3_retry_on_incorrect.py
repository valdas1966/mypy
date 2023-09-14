from myq.subs.question.sub_1_text import QuestionText
from f_utils import u_input


q = QuestionText(text='2+2', answer='4')
prompt = f'{q.text}:'
is_correct = None
while not is_correct:
    response, dt_start, dt_finish = u_input.get(prompt, with_dt=True)
    if response == u_input.Symbols.EXIT.value:
        print('EXIT MYQ')
        break
    is_correct = q.answer == response
    print(prompt, response, dt_start, dt_finish, is_correct)
    if not is_correct:
        print(f'The correct answer is: {q.answer}')
