from ProcessedSubmit import ProcessedSubmit
import re


def loadProcessedSubmits(filePath: str):
    '''
    load processed submits given the id of problem
    :param problem_id
    :return: list of ProcessedSubmits
    '''

    submits = []

    with open(filePath) as src:
        user_id = 0
        for line in src.readlines():
            if len(line) > 0:
                if re.match("user", line):
                    user_id = line.split(' ')[1]
                else:
                    submits.append(ProcessedSubmit.parseFromStr(line))
                    submits[-1].metadata['user_id'] = user_id

    return submits


def getUniqueSumbits(submits):
    '''
    get submits unique when canonized
    :param submits
    :return: list of ProcessedSubmits
    '''

    unique_canonized = dict()

    for submit in submits:
        key = submit.functions_to_unicode(use_canonized=True)

        if key not in unique_canonized:
            unique_canonized[key] = submit
            # apend metadata for possible later use
            submit.metadata['total_times'] = []

        unique_canonized[key].metadata['total_times'].append(submit.total_time)

    return list(unique_canonized.values())
