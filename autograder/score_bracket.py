#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import json
import requests

def get_espn(bracketId):
    bracket = json.loads(requests.get(f'https://fantasy.espn.com/tournament-challenge-bracket/2023/en/ios/api/v4/entries?entryID={bracketId}').content)
    picks = [int(x) - 1 for x in bracket['entry'][0]['picks']['pickString'].split('|')]
    return np.array(picks)

def get_excel(path):
    bracket = pd.read_excel(path, sheet_name = 'Bracket', header = None, index_col = 2)
    picks = []
    for column in range(3, 9):
        if (column - 1) >= bracket.shape[1]:
            picks.extend([np.nan] * 2 ** (8 - column))
        else:
            picks.extend(bracket.index.get_indexer(bracket.iloc[range(2 ** (column - 3) - 1, 64, 2 ** (column - 2)), column - 1]))
    return np.array(picks)

bracket = get_excel('submission/submission.xlsx')
actual = get_excel('source/actual.xlsx')
correct = (bracket == actual)

start = 0
gs_output = {'tests': []}
for round in range(1, 7):
    gs_output['tests'].append({
        'name': f'Round {round}',
        'score': int(correct[start:(start + (2 ** (6 - round)))].sum() * (2 ** (round - 1))),
        'max_score': 32,
        'output': ''
    })
    start = start + (2 ** (6 - round))

out_path = '/autograder/results/results.json'
with open(out_path, 'w') as f:
    f.write(json.dumps(gs_output))
