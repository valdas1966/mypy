from c_timer import Timer


def compare(f_1, f_2, inputs):
    outputs_1 = list()
    outputs_2 = list()
    timer = Timer()
    for input in inputs:
        outputs_1.append(f_1(input))
    elapsed_1 = timer.elapsed()
    for input in inputs:
        outputs_2.append(f_2(input))
    elapsed_2 = timer.elapsed()
    for i, out_1 in enumerate(outputs_1):
        if out_1 != outputs_2[i]:
            print(i, inputs[i], out_1, outputs_2[i])
    print(elapsed_1, elapsed_2, elapsed_1 - elapsed_2)



from f_math import u_numbers
compare(u_numbers.factors, u_numbers.factors_2, range(1, 1000000))
