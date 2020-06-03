import yaml
import operator

# load yaml scores file
with open("scores.yaml", 'r') as stream:
    try:
        scores = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print('Error with file load.', exc)


# initialize qualifier dict
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

# sort qualifiers from biggest to smallest and slice off top 3
top3 = dict(sorted(qualifiers.items(),
                   key=operator.itemgetter(1), reverse=True)[:3])

# ---The steps below are for shaping the data into proper structure/format according to output spec.
# initialize winners list
winners = []

# populate winners list from top3 dict
for name in top3:
    # create dict for single winners name and avg score
    winner = {}
    winner['name'] = name
    winner['avg'] = top3[name]

    # add the winner to winners list
    winners.append(winner)

# BREAK
# compile final winning results, with disqualifiers
results = {'winners': winners, 'disqualifications': disqualifications}

# dump results into yaml output
with open('results.yml', 'w') as outfile:
    yaml.dump(results, outfile, default_flow_style=False, sort_keys=False)
