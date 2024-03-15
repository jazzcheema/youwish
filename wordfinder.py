from random import choice


class WordFinder:
    """Word Finder: finds random words from a dictionary."""

    def __init__(self, path):
        """Initializes attribute words to be an empty list,
        creates attribute path which saves the input path,
        and calls read_file which populates words attribute with lines
        from the file found at path"""

        self.path = path
        self.words = []
        self.__read_file__(path)

        print(f"Accessing the lamp to read {len(self.words)} words")

    def __repr__(self):
        """Returns representation of instance of WordFinder class"""

        return f"WordFinder created from {self.path}"

    def __append_line__(self, line):
        """Strips trailing whitespace off of line and
        appends it to words attribute"""

        self.words.append(line.strip())

    def __read_file__(self, path):
        """Takes in file path and calls append_line on each line in that file
        If file does not exist then it prints 'File does not exist' and
        returns an empty list"""

        try:
            file = open(path)
            for line in file:
                self.__append_line__(line)
            file.close()

        except FileNotFoundError:
            print('File does not exist')

    def random(self):
        """Returns a random word from self.words"""
        return choice(self.words)


class RandomWordFinder(WordFinder):
    """Sub-class of WordFinder. Removes lines that start with '#' and empty
    lines."""

    def __append_line__(self, line):
        """Checks if line is valid, if it is, strips trailing whitespace
        from line and appends it to words attribute"""

        if line[0] not in ['#', '\n']:
            self.words.append(line.strip())
