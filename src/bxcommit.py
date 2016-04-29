from os import path
import re

def bx_commit_check(ui, repo, node, **kwargs):
    """

    # changelog, contains a list of hashesh of revisions
    # print repo.changelog

    # hash of revision about to create
    # repo[node]

    # get type of a variable
    # type(variable)

    # a description of the commit
    # print repo[node].description()

    # to view all methods and fields of a class (class instance)
    # print dir(repo[node])
    # inspect.getmembers(repo[node], predicate=inspect.ismethod)

    # to get options from .hgrc
    # abort_on_error = ui.configbool('codesniffer', 'abort_on_error', True)

    """

    i =         0
    failed =    False
    errors =    {}
    result =    'Yes'

    forbidden_substrings = ui.config('bxcommit', 'forbidden', '').split(':')

    if(len(forbidden_substrings) == 0):
        return 1

    for diff in repo[node].diff():
        i += 1
        if not(i % 2):
            diff = diff.split('\n')

            #from_file =           diff[0]
            to_file =              parse_diff_file_name(diff[1].rstrip('\n'))
            line_numbers =         int(parse_diff_start_line(diff[2].rstrip('\n')))

            line_offset = line_numbers

            diff = diff[3:]

            for line in diff:
                if not check_line(line, forbidden_substrings):

                    if not (to_file in errors):
                        errors[to_file] = []

                    errors[to_file].append({'line': line, 'num': line_offset})
                    failed = True

                line_offset += 1

    if failed:
        ui.warn('Forbidden strings found inside diffs:\n\n')

        for file_name in errors:
            for line in xrange(0, len(errors[file_name])):
                print 'File: '+file_name+':'+str(errors[file_name][line]['num'])
                print errors[file_name][line]['line']

        result = ui.prompt('\nPlease, re-check. Type "Yes" if you think those diffs are correct, Ctrl+C otherwise...\n', default="No")

    return 0 if result == 'Yes' else 1

def parse_diff_file_name(file_string):
    return re.search('\+\+\+ b/(.+)\t', file_string).group(1)

def parse_diff_start_line(line_string):
    return re.search('@@ -\d+,\d+ \+(\d+),', line_string).group(1)

def check_line(line, forbidden):

    result = True

    if (len(line) > 0) and (line[0] == "+"):
        for bad_string in forbidden:
            if line.find(bad_string) >= 0:
                result = False

    return result
