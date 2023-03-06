class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.start_list = 0
        self.start_item = 0
        self.end = len(list_of_list)

    def __iter__(self):
        self.current_list = 0
        self.current_item = self.start_item-1
        return self

    def __next__(self):
        self.current_item += 1
        if self.current_item == len(self.list_of_list[self.current_list]):
            self.current_list += 1
            self.current_item = 0
            if self.current_list == self.end:
                raise StopIteration
        item = self.list_of_list[self.current_list][self.current_item]
        return item


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


# if __name__ == '__main__':
#     test_1()


import types


def flat_generator(list_of_lists):
    list_idx = 0
    item_idx = 0
    while list_idx < len(list_of_lists):
        yield list_of_lists[list_idx][item_idx]
        item_idx += 1
        if item_idx == len(list_of_lists[list_idx]):
            list_idx += 1
            item_idx = 0
        
    




def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
    