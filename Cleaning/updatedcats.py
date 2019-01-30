# Categories
error_map = {
    'Cognition': {'associated decision making', 'assumptions decision making', 'decision making component',
                  'decision making constellation', 'decision making practices', 'decision making',
                  'emphasize prudent choices', 'emphasize prudent'},
    'Performance': {'executing work activities', 'executing work', 'making practices emphasize',
                    'work activities'},
    "Team": {'coordinate work activities', 'coordinate work', 'peer checking', 'effectively communicate expectations',
             'effectively communicate'},
    "Organizational": {
        'adequate assure', 'communicate expectations regarding', 'conservative bias',
        'effectively communicate expectations', 'effectively communicate',
        'emphasize prudent choices', 'emphasize prudent', 'ensure maintained',
        'ensure personnel equipment', 'error prevention', 'evaluating implementing change',
        'failed ensure', 'failed follow', 'failed use', 'prudent choices simply',
        'prudent choices',
        'use conservative assumptions'
    },
    "Procedural": {'equipment procedures resources', 'equipment procedures', 'follow procedural',
                   'follow procedures', 'personnel equipment procedures', 'personnel follow procedures',
                   'procedural compliance', 'procedural requirements', 'procedure adherence',
                   'procedures resources available', 'procedures resources', 'procedures resulting',
                   'procedures work', 'regarding procedural compliance', 'regarding procedural'},
    "Organizational": {
        'across organizational boundaries', 'activities overriding priority',
        'change management',
        'challenge unknown', 'choices simply allowable', 'component licensee failed',
        'component licensee',
        'decision making licensee', 'deficiency identified failure', 'deficiency identified',
        'described licensee failed', 'disagreement regional administrator',
        'error prevention techniques',
        'licensee failed comply', 'licensee failed ensure', 'lisencee failed',
        'management oversight work',
        'management oversight', 'organizational boundaries', 'overriding priority',
        'oversight work activities', 'supervisory management oversight',
        'supervisory management', 'assigned resources component', 'available adequate', 'component resources',
        'described resources component', 'described resources', 'ensure personnel equipment',
        'personnel equipment', 'resources component licensee', 'resources component', 'appropriately plan work',
        'implement process planning', 'implement process',
        'implementing change',
        'incorporating risk insights', 'incorporating risk', 'plan work',
        'planning controlling executing',
        'planning controlling', 'planning described work', 'planning described',
        'process planning controlling', 'process planning', 'work planning described',
        'work planning', 'control component', 'controlling executing work', 'controlling executing',
        'coordination work control',
        'coordination work', 'described work control', 'process evaluating implementing',
        'process evaluating',
        'systematic process evaluating', 'work control component', 'coordinate work activities', 'coordinate work',
        'work activities overriding', 'work coordination work', 'work management'
    },
    'Information': {'information official use', 'information official', 'insight deficiency',
                    'official use security',
                    'provided insight deficiency', 'provided insight', 'security information official',
                    'security information'}
}
##################
# Imports required
##################
from nltk import sent_tokenize
import os

inspection_reports = "./HumanErrors"

power_plants = os.listdir(inspection_reports)
plant_dictonary = dict()
data_keys = sorted(list(error_map.keys()))
main_csv_string = 'Plant,Report,'
for x in data_keys:
    main_csv_string += x + ','
main_csv_string += 'Team,Organizational,Score(Out of 14 only),What Missed/Extra(Mention the category with : seperated like - Information:Cognition)'
if os.path.isdir('./selected'):
    os.rmdir('./selected')

os.mkdir('./selected')
for plant in power_plants:
    if os.path.isdir(inspection_reports + "/" + plant):
        plant_path = inspection_reports + '/' + plant
        reports = os.listdir(plant_path)
        plant_dictonary[plant] = dict()

        for report in reports:
            plant_dictonary[plant][report] = dict()
            report_path = plant_path + "/" + report
            content = open(report_path, "rb").read()
            content = ''.join([chr(i) if i < 256 else '' for i in content])
            sentences = sent_tokenize(content)

            for sentence in sentences:
                for error in error_map:
                    for ngram in error_map[error]:
                        if ngram in sentence:
                            if error not in plant_dictonary[plant][report]:
                                plant_dictonary[plant][report][error] = dict()
                            plant_dictonary[plant][report][error][ngram] = plant_dictonary[plant][report][error].get(
                                ngram, 0) + 1

        reports_keys = list(plant_dictonary[plant].keys())[
                       :1]  # Change 1 to number of documents you want in every power plant
        os.mkdir('./selected/' + plant)
        for report in reports_keys:
            categories = ''
            team = False
            organization = False
            for cat in data_keys:
                if cat in plant_dictonary[plant][report]:
                    categories += 'YES,'
                    if '' in cat:
                        team = True
                    if '' in cat:
                        organization = True
                else:
                    categories += 'NO,'
            if team:
                categories += 'YES,'
            else:
                categories += 'NO,'
            if organization:
                categories += 'YES,'
            else:
                categories += 'NO,'
            main_csv_string += '\n{0},{1},{2}'.format(plant, report, categories)
            report_path = plant_path + "/" + report
            content = open(report_path, "rb").read()
            content = ''.join([chr(i) if i < 256 else '' for i in content])
            f = open('./{0}/{1}/{2}.txt'.format('selected', plant, report), 'w')
            f.write(content)
            f.flush()
            f.close()
        print(plant)

import json

with open("new_counter.json", "w") as fp:
    json.dump(plant_dictonary, fp, sort_keys=True, indent=4)

with open("csv_file_classification.csv", "w") as f:
    f.write(main_csv_string)
    f.flush()
    f.close()
