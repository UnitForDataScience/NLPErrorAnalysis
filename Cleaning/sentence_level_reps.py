error_map = {
    'Cognition': {'associated decision making', 'assumptions decision making', 'decision making component',
                  'decision making constellation', 'decision making practices', 'decision making',
                  'emphasize prudent choices', 'emphasize prudent'},
    'Performance': {'executing work activities', 'executing work', 'making practices emphasize', 'work activities'},
    'Coordination': {'coordinate work activities', 'coordinate work', 'peer checking'},
    'Communication': {'effectively communicate expectations', 'effectively communicate'},
    'Team & Organization': {'adequate assure', 'communicate expectations regarding', 'conservative bias',
                            'effectively communicate expectations', 'effectively communicate',
                            'emphasize prudent choices', 'emphasize prudent', 'ensure maintained',
                            'ensure personnel equipment', 'error prevention', 'evaluating implementing change',
                            'failed ensure', 'failed follow', 'failed use', 'prudent choices simply', 'prudent choices',
                            'use conservative assumptions'},
    'Procedural&Team': {'equipment procedures resources', 'equipment procedures', 'follow procedural',
                        'follow procedures', 'personnel equipment procedures', 'personnel follow procedures',
                        'procedural compliance', 'procedural requirements', 'procedure adherence',
                        'procedures resources available', 'procedures resources', 'procedures resulting',
                        'procedures work', 'regarding procedural compliance', 'regarding procedural'},
    'Management': {'across organizational boundaries', 'activities overriding priority', 'change management',
                   'challenge unknown', 'choices simply allowable', 'component licensee failed', 'component licensee',
                   'decision making licensee', 'deficiency identified failure', 'deficiency identified',
                   'described licensee failed', 'disagreement regional administrator', 'error prevention techniques',
                   'licensee failed comply', 'licensee failed ensure', 'lisencee failed', 'management oversight work',
                   'management oversight', 'organizational boundaries', 'overriding priority',
                   'oversight work activities', 'supervisory management oversight', 'supervisory management'},
    'Resources': {'assigned resources component', 'available adequate', 'component resources',
                  'described resources component', 'described resources', 'ensure personnel equipment',
                  'personnel equipment', 'resources component licensee', 'resources component'},
    'Planning': {'appropriately plan work', 'implement process planning', 'implement process', 'implementing change',
                 'incorporating risk insights', 'incorporating risk', 'plan work', 'planning controlling executing',
                 'planning controlling', 'planning described work', 'planning described',
                 'process planning controlling', 'process planning', 'work planning described', 'work planning'},
    'Control': {'control component', 'controlling executing work', 'controlling executing', 'coordination work control',
                'coordination work', 'described work control', 'process evaluating implementing', 'process evaluating',
                'systematic process evaluating', 'work control component'},
    'Org-Coordination': {'coordinate work activities', 'coordinate work', 'work activities overriding',
                         'work coordination work', 'work management'},
    'Information': {'information official use', 'information official', 'insight deficiency', 'official use security',
                    'provided insight deficiency', 'provided insight', 'security information official',
                    'security information'}
}

import os
from nltk import sent_tokenize

inspection_reports = "./HumanErrors"

power_plants = os.listdir(inspection_reports)
plant_dictonary = dict()
for plant in power_plants:
    if os.path.isdir(inspection_reports + "/" + plant):
        print(plant)
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
                            print(plant + " " + error + " " + ngram)
            # for sentence in sentences:
            #     for ngram in word_bag:
            #         if ngram in sentence:
            #             plant_dictonary[plant][ngram] = plant_dictonary[plant].get(ngram, 0) + 1

import json

with open("new_counter.json", "w") as fp:
    json.dump(plant_dictonary, fp, sort_keys=True, indent=4)
