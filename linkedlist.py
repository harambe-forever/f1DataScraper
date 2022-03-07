

class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None


class SLinkedList:
    def __init__(self):
        self.headval = None

    def listprint(self):
        printval = self.headval
        while printval is not None:
            print(printval.dataval)
            printval = printval.nextval

    def AtBeginning(self, newdata):
        NewNode = Node(newdata)
        NewNode.nextval = self.headval
        self.headval = NewNode

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        last = self.headval
        while last.nextval:
            last = last.nextval
        last.nextval = NewNode

    def InBetween(self, middle_node, newdata):
        if middle_node is None:
            print("The mentioned node is absent")
            return
        NewNode = Node(newdata)
        NewNode.nextval = middle_node.nextval
        middle_node.nextval = NewNode

    def RemoveNode(self, RemoveKey):
        head = self.headval
        if head is not None:
            if (head.dataval == RemoveKey):
                self.head = head.nextval
                head = None
                return
        while (head is not None):
            if head.dataval == RemoveKey:
                break
            prev = head
            head = head.nextval
        if head == None:
            return
        prev.nextval = head.nextval
        head = None


"""list1 = SLinkedList()
list1.headval = Node("mon")
e2 = Node("tue")
e3 = Node("wed")
list1.headval.nextval = e2
e2.nextval = e3

list1.AtBeginning("sun")
list1.AtEnd("tue")
list1.InBetween(list1.headval.nextval, "monday afternoon")
list1.RemoveNode("monday afternoon")

list1.listprint()"""
