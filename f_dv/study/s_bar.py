from f_dv.bar import Bar


labels = ['A', 'B', 'C', 'D']
values = [3, 5, 8, 10]

bar = Bar(labels,
          values,
          name_labels='Words',
          name_values='Numbers',
          name="My Bar Chart")
bar.show()
