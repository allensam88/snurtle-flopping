import yaml
from collections import Counter

# load yaml scores file
with open("scores.yaml", 'r') as stream:
    try:
        scores = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print('Error with file load.', exc)


# initialize temp variables
qualifiers = {}
disqualifications = []

for competitor in scores:
    # disqualify the competitors with less than 7 flops
    if len(scores[competitor]) < 7:
        disqualifications.append(competitor)
    # evaluate the qualifying competitors
    else:
        # eliminate the high / low scores
        # built-in sort first, then slice off first and last as faster alternative
        scores[competitor].sort()
        trim = scores[competitor][1:-1]
        # high = max(scores[competitor])
        # low = min(scores[competitor])
        # scores[competitor].remove(high)
        # scores[competitor].remove(low)
        # calculate the average score
        average = sum(trim) / len(trim)
        # add to qualifier dictionary
        qualifiers[competitor] = average

# use 'Counter' built-in Python tool for finding the top 3 high scores in tuples
top3scores = Counter(qualifiers).most_common(3)

# BREAK
# ---The steps below are for shaping the data into proper structure/format according to output spec.
# initialize winners list
winners = []

# populate winners list with top3 tuples
for i in range(len(top3scores)):
    # create dict for single winners name and avg score
    winner = dict(name=top3scores[i][0], avg=top3scores[i][1])

    # add the winner to winners list
    winners.append(winner)

# BREAK
# compile final winning results, with disqualifiers
results = {'winners': winners, 'disqualifications': disqualifications}

# dump results into yaml output
with open('results.yml', 'w') as outfile:
    yaml.dump(results, outfile, default_flow_style=False, sort_keys=False)
