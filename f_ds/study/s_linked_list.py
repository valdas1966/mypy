from f_ds.linked_list import LinkedList, NodePrevNext as Node


a = Node(uid='A')
b = Node(uid='B')
c = Node(uid='C')
a.next = b
linked = LinkedList()
linked.append(node=a)
print(linked)
#linked.append(node=b)
#print(linked)
linked.append(node=c)
print(linked)




