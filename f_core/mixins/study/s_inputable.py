from f_core.mixins.user_inputable import UserInputable


i = UserInputable()
i.get_input()
print(i.dt_prompt, i.input, i.dt_input)
