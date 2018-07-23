"""
*** File Name           : History.py
*** Designer            : 稲垣 大輔
*** Date                : 2018.07.入力
*** Function            : 画像の編集履歴を管理する。
"""

"""
*** Class Name          : History
*** Designer            : 稲垣 大輔
*** Date                : 2018.07.入力
*** Function            : 入力
"""


class History:

    def __init__(self, array):
        self.filter_list = [[]]
        self.image_list = [None]
        self.image_count = 0
        self.count = 0
        self.redo_max = 0
        self.current = [0]
        self.image_list[0] = array.copy()

    """
    *** Function Name       : add_filter()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタ履歴にフィルタを追加する
    *** Return              : なし
    """

    def add_filter(self, filter_):
        self.next_filter()
        if len(self.filter_list[self.count]) == 0:
            filter_.before_image_id = self.image_count
        else:
            filter_.before_image_id = self.filter_list[self.count][-1].after_image_id
        self.next_image()
        filter_.after_image_id = self.image_count
        self.filter_list[self.count].append(filter_)

    """
    *** Function Name       : remove_filter()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタ履歴から選択されたフィルタを削除する
    *** Return              : 更新後のフィルタリスト
    """

    def remove_filter(self, f):
        rm_index = None
        for i in range(len(self.filter_list[self.count])):
            if self.filter_list[self.count][i].id == f.id:
                rm_index = i
                break
        if rm_index is None:
            return self.filter_list[self.count]
        self.next_filter()
        del self.filter_list[self.count][rm_index]
        for i in range(rm_index, len(self.filter_list[self.count])):
            if i == 0:
                self.filter_list[self.count][i].before_image_id = 0
            else:
                self.filter_list[self.count][i].before_image_id = self.filter_list[self.count][i - 1].after_image_id
            self.next_image()
            self.filter_list[self.count][i].after_image_id = self.image_count
        return self.filter_list[self.count]

    """
    *** Function Name       : swap()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタの移動を処理する。
    *** Return              : 更新後のフィルタリスト
    """

    def swap(self, filters):
        print('swap')
        try:
            ud_index = None
            for i in range(len(self.filter_list[self.count])):
                if self.filter_list[self.count][i].id != filters[i].id:
                    ud_index = i
                    break
            if ud_index is None:
                return self.filter_list[self.count]
            self.next_filter()
            self.filter_list[self.count]=filters
            for i in range(ud_index, len(self.filter_list[self.count])):
                if i == 0:
                    self.filter_list[self.count][i].before_image_id = 0
                else:
                    self.filter_list[self.count][i].before_image_id = self.filter_list[self.count][i - 1].after_image_id
                self.next_image()
                self.filter_list[self.count][i].after_image_id = self.image_count
            return self.filter_list[self.count]
        except:
            import traceback
            traceback.print_exc()

    """
    *** Function Name       : update_filter()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタのパラメータ更新を記録する。
    *** Return              : 更新後のフィルタリスト
    """

    def update_filter(self, f):
        self.next_filter()
        ud_index = -1
        for i, fil in enumerate(self.filter_list[self.count]):
            if fil.id == f.id:
                ud_index = i
                break
        self.filter_list[self.count][ud_index] = f
        for i in range(ud_index, len(self.filter_list[self.count])):
            if i == 0:
                self.filter_list[self.count][i].before_image_id = 0
            else:
                self.filter_list[self.count][i].before_image_id = self.filter_list[self.count][i - 1].after_image_id
            self.next_image()
            self.filter_list[self.count][i].after_image_id = self.image_count
        return self.filter_list[self.count]

    """
    *** Function Name       : undo()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタリストの状態を一つ戻す。
    *** Return              : 更新後画像, 更新後フィルタリスト, undo可否
    """

    def undo(self):
        if (self.count != 0):
            self.count -= 1
            self.redo_max += 1
        return (self.image_list[self.current[self.count]], self.filter_list[self.count], self.count != 0)

    """
    *** Function Name       : redo()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタリストの状態を一つ進める。
    *** Return              : 更新後画像, 更新後フィルタリスト, redo可否
    """

    def redo(self):
        if self.redo_max > 0:
            self.count += 1
            self.redo_max -= 1
        return (self.image_list[self.current[self.count]], self.filter_list[self.count], self.redo_max > 0)

    """
    *** Function Name       : next_filter()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタリストを履歴に格納する。
    *** Return              : なし
    """

    def next_filter(self):
        import copy
        self.count += 1
        self.filter_list.append([])
        self.filter_list[self.count].clear()
        try:
            # self.filter_list[self.count] = copy.copy(self.filter_list[self.count - 1])
            for i in range(len(self.filter_list[self.count - 1])):
                n_filter = copy.copy(self.filter_list[self.count - 1][i])
                self.filter_list[self.count].append(n_filter)
        except:
            import traceback
            traceback.print_exc()
        self.current.append(self.current[self.count - 1])
        self.redo_max = 0

    """
    *** Function Name       : next_image()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : 画像を履歴に格納する。
    *** Return              : なし
    """

    def next_image(self):
        self.image_count += 1
        self.image_list.append(None)

    """
    *** Function Name       : apply()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.07.入力
    *** Function            : フィルタリストのフィルタを適用する
    *** Return              : 更新後画像, 更新後フィルタリスト
    """

    def apply(self):
        self.next_filter()
        f = None
        for i, f in enumerate(self.filter_list[self.count]):
            if self.image_list[f.after_image_id] is not None:
                continue
            self.image_list[f.after_image_id] = f.apply(self.image_list[f.before_image_id].copy())
            print('apply', f.get_name())
        else:
            if f is not None:
                self.current[self.count] = f.after_image_id
            else:
                self.current[self.count] = 0

        return (self.image_list[self.current[self.count]], self.filter_list[self.count])
