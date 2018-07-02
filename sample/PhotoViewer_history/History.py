class History:
    filter_list = [[]]
    image_list = [None]
    image_count = 0
    count = 0
    redo_max = 0
    current = [0]

    def __init__(self, array):
        self.image_list[0] = array.copy()

    def add_filter(self, filter):
        self.next_filter()
        print('add ', filter.get_name(), self.image_count)
        filter.image_id = self.image_count
        self.filter_list[self.count].append(filter)
        self.next_image()

    def remove_filter(self, f):
        self.next_filter()
        for fil in self.filter_list[self.count][self.filter_list[self.count].index(f):]:
            fil.isApplied = False
        self.current[self.count] = min(self.current[self.count], f.image_id)
        self.filter_list[self.count].remove(f)

    def undo(self):
        if (self.count != 0):
            self.count -= 1
            self.redo_max += 1
        print(self.count)
        return (self.image_list[self.current[self.count]], self.filter_list[self.count])

    def redo(self):
        print(self.redo_max)
        if not (self.count > self.redo_max):
            self.count += 1
        return self.image_list[self.current[self.count]]

    def get_filter_list(self):
        return self.filter_list[self.count].copy()

    def next_filter(self):
        self.count += 1
        self.filter_list.append([])
        self.filter_list[self.count] = self.filter_list[self.count - 1].copy()
        self.current.append(self.current[self.count - 1])
        self.redo_max = 0

    def next_image(self):
        self.image_count += 1
        self.image_list.append(None)

    def swap(self, n1, n2):
        self.current = min(self.filter_list[self.count][n1][1], self.filter_list[self.count][n2][1])
        self.filter_list[self.count][n1], self.filter_list[self.count][n2] = self.filter_list[self.count][n2], \
                                                                             self.filter_list[self.count][n1]

    def apply(self):
        try:
            self.next_filter()
            array = self.image_list[self.current[self.count]].copy()
            for f in self.filter_list[self.count]:
                if f.isApplied and f.image_id < self.current[self.count]:
                    print('con')
                    continue
                if f.isUpdate:
                    self.next_image()
                    f.isUpdate = False
                array = f.apply(array)
                f.isApplied = True
                print('run')
                self.current[self.count] += 1
                self.image_list[self.current[self.count]] = array.copy()
        except:
            import traceback
            traceback.print_exc()
        print(self.current)
        return self.image_list[self.current[self.count]]


'''
全フィルタを保存する
時系列の履歴
undoはcountを一つ戻すだけ
redoはmaxまではcountを増やす

'''
