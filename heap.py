import yaml
from heapq import nlargest

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
        high = max(scores[competitor])
        low = min(scores[competitor])
        scores[competitor].remove(high)
        scores[competitor].remove(low)
        # calculate the average score
        average = sum(scores[competitor]) / len(scores[competitor])
        # add to qualifier dictionary
        qualifiers[competitor] = average

# utilize heapq tool 'nlargest' to get the top 3 qualifiers
top3scores = nlargest(3, qualifiers, key=qualifiers.get)

# BREAK
# ---The steps below are for shaping the data into proper structure/format according to output spec.
# initialize winners list
winners = []

# populate winners list from top3scores
for name in top3scores:
    # create dict for single winners name and avg score
    winner = dict(name=name, avg=qualifiers[name])

    # add the winner to winners list
    winners.append(winner)

# BREAK
# compile final winning results, with disqualifiers
results = {'winners': winners, 'disqualifications': disqualifications}

# dump results into yaml output
with open('results.yml', 'w') as outfile:
    yaml.dump(results, outfile, default_flow_style=False, sort_keys=False)
