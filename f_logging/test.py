from dec import log_info_without_self, log_all_methods


@log_all_methods(decorator=log_info_without_self)
class X:

    print('start class')

    def __init__(self):
        print('init')


x = X()