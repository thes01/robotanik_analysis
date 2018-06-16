import Problem
import json


def createRobotanikGraphViewer(problem: Problem, data, title, filename_suffix=""):
    puzzles_data_json = json.dumps([{
        'title': problem.title,
        'about': problem.about,
        'robotCol': problem.robotCol,
        'robotRow': problem.robotRow,
        'robotDir': problem.robotDir,
        'subs': json.loads(problem.subs),
        'allowedCommands': problem.allowedCommands,
        'board': problem.board_str
    }])

    with open('generated_html/{}{}.html'.format(problem.getFirstId(), filename_suffix), 'w') as output:
        with open('createRobotanikGraphViewer_template.html') as template:
            replaced = template.read()
            replaced = replaced.replace('__TEMPLATE_TITLE', title)
            replaced = replaced.replace('__TEMPLATE_PUZZLES', puzzles_data_json)
            replaced = replaced.replace('__TEMPLATE_DATA', json.dumps(data))
            replaced = replaced.replace('./', '../html_src/')
            output.write(replaced)