from f_core.mixins.generators.g_comparable import GenComparable, Item


items = GenComparable.gen_list(length=2)  # [Item(1), Item(2)]
print([item.val for item in items])

print(items[0].key_comparison())
print(Item(val=0).key_comparison())