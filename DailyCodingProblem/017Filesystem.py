# This problem was asked by Google.

# Suppose we represent our file system by a string in the following manner:
# The string "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext" represents:
# dir
#     subdir1
#     subdir2
#         file.ext

# The directory dir contains an empty sub-directory subdir1 and a
# sub-directory subdir2 containing a file file.ext.

# The string:

# "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"

# represents:
# dir
#     subdir1
#         file1.ext
#         subsubdir1
#     subdir2
#         subsubdir2
#             file2.ext

# The directory dir contains two sub-directories subdir1 and subdir2.
# subdir1 contains a file file1.ext and an empty second-level sub-directory
# subsubdir1. subdir2 contains a second-level sub-directory subsubdir2
# containing a file file2.ext.

# We are interested in finding the longest (number of characters) absolute
# path to a file within our file system.
# For example, in the second example above, the longest absolute path is:
#
# "dir/subdir2/subsubdir2/file2.ext"
#
# and its length is 32 (not including the double quotes).

# Given a string representing the file system in the above format,
# return the length of the longest absolute path to a file in the abstracted
# file system. If there is no file in the system, return 0.

# Note:
# The name of a file contains at least a period and an extension.
# The name of a directory or sub-directory will not contain a period.


fs1 = "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext"
fs2 = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
fs3 = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext\ndir2\n\tsubdir2\n\t\t\tfile3.ext"


def find_longest_path(fs):
    fs_elements = fs.split('\n')

    if len(fs_elements) == 0:
        return 0

    longest_path = recurse_fs(fs_elements, [], [], 0)

    return '/'.join(longest_path)


def recurse_fs(fs_elements, current_path, longest_path, level):

    # e.g.
    #  'dir1',                  dir1
    #  '\tsubdir1'              dir1/subdir1
    #  '\t\tfile1.ext'          dir1/subdir1/file1.ext
    #  '\t\tsubsubdir1'         dir1/subdir1/subsubdir1
    #  '\tsubdir2'              dir1/subdir2
    #  '\t\tsubsubdir2'         dir1/subdir2/subsubdir2
    #  '\t\t\tfile2.ext'        dir1/subdir2/subsubdir2/file2.ext
    #  'dir2'                   dir2

    if len(fs_elements) == 0:
        return longest_path

    for element in fs_elements:
        num_tabs, elem = strip_tabs(element)

        while num_tabs < level:
            current_path.pop()
            level -= 1

        current_path.append(elem)

        if num_tabs == level:
            # It's a subdir or file

            if is_file(elem):
                if path_len(current_path) > path_len(longest_path):
                    longest_path = current_path.copy()

            return recurse_fs(fs_elements[1:],
                              current_path,
                              longest_path,
                              level+1)

        current_path.pop()

    return longest_path


def strip_tabs(element):
    count = 0
    for i in element:
        if i == '\t':
            count += 1
        else:
            break

    return count, element[count:]


def is_file(element):
    return len(element.split('.')) == 2


def path_len(path):
    return sum([len(e) for e in path])


if __name__ == "__main__":

    for filesystem in [fs1, fs2, fs3]:
        longest_path = find_longest_path(filesystem)
        print("Longest path in\n{}\nis:\n{} (len {})\n"
              .format(filesystem, longest_path, len(longest_path)))
