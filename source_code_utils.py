from type_aliases import SourceCode, Path
from typing import List
from line_range import Range
import re


def get_source_code(filename: Path) -> SourceCode:
    ''' Read file with source code to string'''
    with open(filename, 'r') as file:
        data = file.read()
    return data


def remove_comments(string: SourceCode) -> SourceCode:
    ''' Returns source code line where comments are replaces with empty string'''
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)
    return regex.sub(_replacer, string)


def complement_range(class_source: SourceCode, line_range: Range) -> Range:
    '''
    To complemnt an input range of lines to get a new range that may
    contain additional lines with closing brackets
    '''
    open_brackets = 0
    closed_brackets = 0
    n_line = 0
    has_semicolon = False
    source_code_lines = class_source.split('\n')

    for n_line, line in enumerate(source_code_lines[line_range.start:]):
        line_without_comments = remove_comments(line)
        has_semicolon = line_without_comments.count(';') > 0
        open_brackets += line_without_comments.count('{')
        closed_brackets += line_without_comments.count('}')

        if line_range.start + n_line < line_range.end:
            if open_brackets - closed_brackets == 0:
                open_brackets = 0
                closed_brackets = 0
            continue
        if closed_brackets == 0 and open_brackets == 0 and not has_semicolon:
            continue
        if open_brackets - closed_brackets == 0:
            break

    result: Range = Range(line_range.start, line_range.start + n_line)
    return result


def complement_range_file(filename: Path, inline_start: int, inline_end: int) -> Range:
    sc = get_source_code(filename)
    return complement_range(sc, Range(inline_start, inline_end))


def extract_lines_range_from_source_code(code: SourceCode, range: Range) -> List[str]:
    ''' Line Range from a to b includes a and b and start indexing from zero'''
    return code.split('\n')[range.start: range.end + 1]


def extract_method(class_source: SourceCode, method_name: str, method_start_line: int) -> SourceCode:
    assert method_name in class_source.split('\n')[method_start_line - 1] or \
         method_name in class_source.split('\n')[method_start_line]
    if '{' in class_source.split('\n')[method_start_line - 1]:
        range = complement_range(class_source, Range(method_start_line - 1))
    else:
        range = complement_range(class_source, Range(method_start_line - 1, method_start_line + 1))
    method_lines = extract_lines_range_from_source_code(class_source, range)
    return '\n'.join(method_lines)
