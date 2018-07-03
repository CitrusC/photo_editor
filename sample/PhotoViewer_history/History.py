class History:

    def __init__(self, array):
        self.filter_list = [[]]
        self.image_list = [None]
        self.image_count = 0
        self.count = 0
        self.redo_max = 0
        self.current = [0]
        self.image_list[0] = array.copy()

    def add_filter(self, filter_):
        self.next_filter()
        print('add ', filter_.get_name(), self.image_count)
        if len(self.filter_list[self.count]) == 0:
            filter_.before_image_id = self.image_count
        else:
            filter_.before_image_id = self.filter_list[self.count][-1].after_image_id
        self.next_image()
        filter_.after_image_id = self.image_count
        self.filter_list[self.count].append(filter_)

    def remove_filter(self, f):
        try:
            self.next_filter()
            rm_index = self.filter_list[self.count].index(f)
            self.filter_list[self.count].remove(f)
            print(len(self.filter_list[self.count]))
            for i in range(rm_index, len(self.filter_list[self.count])):
                self.filter_list[self.count][i].before_image_id = self.filter_list[self.count][i - 1].after_image_id
                self.next_image()
                self.filter_list[self.count][i].after_image_id = self.image_count
        except:
            import traceback
            traceback.print_exc()
        return self.filter_list[self.count]

    def swap(self, filters):
        self.next_filter()
        for i in range(len(self.filter_list[self.count])):
            if self.filter_list[self.count][i] is filters[i]:
                ud_index = i
                continue
            else:
                ud_index += 1
                break
        self.filter_list[self.count] = filters.copy()
        for i in range(ud_index, len(self.filter_list[self.count])):
            self.filter_list[self.count][i].before_image_id = self.filter_list[self.count][i - 1].after_image_id
            self.next_image()
            self.filter_list[self.count][i].after_image_id = self.image_count
        return self.filter_list[self.count]

    def update_filter(self, f):
        try:
            self.next_filter()
            ud_index = self.filter_list[self.count].index(f)
            for i in range(ud_index, len(self.filter_list[self.count])):
                self.filter_list[self.count][i].before_image_id = self.filter_list[self.count][i - 1].after_image_id
                self.next_image()
                self.filter_list[self.count][i].after_image_id = self.image_count
        except:
            import traceback
            traceback.print_exc()
        return self.filter_list[self.count]

    def undo(self):
        if (self.count != 0):
            self.count -= 1
            self.redo_max += 1
        print(self.count)
        return (self.image_list[self.current[self.count]], self.filter_list[self.count], self.count != 0)

    def redo(self):
        print(self.count)
        if self.redo_max > 0:
            self.count += 1
            self.redo_max -= 1
        return (self.image_list[self.current[self.count]], self.filter_list[self.count], self.redo_max > 0)

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

    def apply(self):
        self.next_filter()
        for i, f in enumerate(self.filter_list[self.count]):
            if self.image_list[f.after_image_id] is not None:
                print('skip')
                continue
            print('apply {}: {} -> {}'.format(f.get_name(), f.before_image_id, f.after_image_id))
            self.image_list[f.after_image_id] = f.apply(self.image_list[f.before_image_id].copy())
        else:
            self.current[self.count] = f.after_image_id
        return (self.image_list[self.current[self.count]], self.filter_list[self.count])
