import yaml

# load yaml scores file
with open("scores.yaml", 'r') as stream:
    try:
        scores = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print('Error with file load.', exc)


# initialize temp arrays
winners = []
disqualifications = []
top3scores = []

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

        # populate temp arry with first 3 items
        if len(top3scores) < 3:
            top3scores.append(average)

            # create dict for single winners name and avg score
            winner = dict(name=competitor, avg=average)

            # add the winner to winners list
            winners.append(winner)

            # evaluate incoming items if average is bigger than lowest, then update top3scores
        elif average > min(top3scores):
            top3scores.append(average)
            top3scores.remove(min(top3scores))

            # remove the lowest name/score from winners list
            winners = [i for i in winners if not (i['avg'] < min(top3scores))]

            # create dict for single winners name and avg score
            winner = dict(name=competitor, avg=average)

            # add the winner to winners list
            winners.append(winner)

        winners = sorted(winners, key=lambda k: k['avg'], reverse=True)

# BREAK
# compile final winning results, with disqualifiers
results = {'winners': winners, 'disqualifications': disqualifications}

# dump results into yaml output
with open('results.yml', 'w') as outfile:
    yaml.dump(results, outfile, default_flow_style=False, sort_keys=False)
