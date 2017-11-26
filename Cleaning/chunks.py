issues = [["Performance issues", "poor work quality", "lack of communication", "miscommunication",
           "personnel error", "crew error", "lack of coordination", "calculation mistakes",
           "lack of critical thinking", "lack of questioning skills", "inconsistent leadership",
           "failed to recognized", "cognitive error", "lack of awareness", "lack of understanding",
           "weakness in the work control process", "not using conservative decision making", "misapplication",
           "ineffective communication", "lack of consistency with the decisions and actions",
           "ineffective supervisory", "lack of verification", "inadequate use of human performance tools",
           "not informed", "not promptly review", "not unsure"]]
# ["Inadequate procedures", "lack of clear detailed guidance", "insufficient guidance",
#  "deficiency in procedure", "Lack of requirement for verification",
#  "not include specific work precautions or instructions", "not provide sufficient detail",
#  "procedure did not meet the requirement"],
# ["Scheduling issues", "planning issues", "inadequate training", "inadequate briefing",
#  "work package problems", "work instruction problems", "lack of documentation",
#  "ineffective pre-job brief", "effective oversight", "Inadequate Operations organization"],
# ["Design related issues", "inadequate design", "latent design problems", "age related issues"]]

from nltk import word_tokenize
from nltk import pos_tag
regexTag = r"""chunk: {"""
regexTags = []
for issue in issues:
    for subissue in issue:
        pos_words = pos_tag(word_tokenize(subissue.lower()))

        for word in pos_words:
            regexTag += "<" + word[1] + ">"
        regexTags.append(regexTag + "}")

print regexTags
