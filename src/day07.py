import utils

class FileSystemElement:
    def __init__(self, name:str, size:int = 0, dir_ind:bool = True):
        self.name = name
        self.size = size
        self.dir_ind = dir_ind
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def _calc_folder_size(self):
        if not self.dir_ind:
            raise Exception('not a folder')
        if self.size == 0:
            folder_size = 0
            for child in self.children:
                if child.dir_ind and child.size == 0:
                    child._calc_folder_size()
                folder_size += child.size
            self.size = folder_size
        return self.size

    def get_subfolders_size_sum(self, max_size:int = -1) -> int:
        sum = 0
        if max_size == -1 or self._calc_folder_size() <= max_size:
            sum += self.size
        for child in self.children:
            if child.dir_ind:
                sum += child.get_subfolders_size_sum(max_size)
        return sum

    def _calc_smallest_deletable_subfolder(self, min_deletion_size:int):
        smallest_deletable_folder = self
        for child in self.children:
            if child.dir_ind and child.size > min_deletion_size:
                child_smallest_deletable_folder = child._calc_smallest_deletable_subfolder(min_deletion_size)
                if child_smallest_deletable_folder.size < smallest_deletable_folder.size:
                    smallest_deletable_folder = child_smallest_deletable_folder
        return smallest_deletable_folder

    def get_smallest_deletable_subfolder(self, disk_space:int, update_space:int):
        available_space = disk_space - self._calc_folder_size()
        min_deletion_size = max(update_space - available_space, 0)
        return self._calc_smallest_deletable_subfolder(min_deletion_size)

    def get_names_of_children(self):
        for child in self.children:
            yield child.name

def build_file_system(input_path:str, part:int) -> FileSystemElement:
    top_folder = None
    curr_folder = None
    contents = None

    with open(input_path) as f:
        for line in f:
            if line.strip() == '$ cd /':
                if not top_folder:
                    top_folder = FileSystemElement(name='/')
                curr_folder = top_folder
            elif line.strip() == '$ cd ..':
                if curr_folder.name != '/':
                    curr_folder = curr_folder.parent
            elif line[:5] == '$ cd ':
                name = line[5:].strip()
                if name not in curr_folder.get_names_of_children():
                    child = FileSystemElement(name)
                    curr_folder.add_child(child)
                curr_folder = curr_folder.get_child(name)
            elif line.strip() == '$ ls':
                continue
            elif line[0] != '$':
                element, name = str.split(line.strip(), ' ')
                if element == 'dir':
                    size = 0
                    dir_ind = True
                else:
                    size = int(element)
                    dir_ind = False
                if name not in curr_folder.get_names_of_children():
                    child = FileSystemElement(name,size,dir_ind)
                    curr_folder.add_child(child)

    return top_folder

def get_answer(input_path:str, part:int) -> str:
    top_folder = build_file_system(input_path, part)
    if part == 1:
        return top_folder.get_subfolders_size_sum(max_size=100_000)
    if part == 2:
        smallest_deletable_subfolder = top_folder.get_smallest_deletable_subfolder(
            disk_space=70_000_000,
            update_space = 30_000_000
        )
        return smallest_deletable_subfolder.size

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )