from type_aliases import SourceCode, Path
from line_range import Range

def get_source_code(filename: Path) -> SourceCode:
    ''' Read file with source code to string'''
    pass


def complement_range(class_source: SourceCode, line_range: Range) -> Range:
    '''
    To complemnt an input range of lines to get a new range that may 
    contain additional lines with closing brackets 
    '''
    pass