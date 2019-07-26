import random


def honest(trials, QBER, transmission):
    alice = {'basis':[random.randrange(0, 2, 1) for _ in range(trials)],'state':[random.randrange(0, 2, 1) for _ in range(trials)]}

    bob={'success':[1 if random.random()<transmission else 0 for x in range (0,trials)], 'basis':[random.randrange(0, 2, 1) for _ in range(trials)]}

    bob['measurement']=[(alice['state'][x]+1)%2 if alice['basis'][x]==bob['basis'][x] else random.randint(0,1) for x in range (0,trials)]

    bob['measurement']=[9 if bob['success'][x]==0 else bob['measurement'][x]for x in range (0,trials)]

    bob['measurement']=[(bob['measurement'][x]+1)%2 if random.random()<QBER and bob['success'][x]==1 else bob['measurement'][x] for x in range (0,trials)]

    count=0
    for x in range (0,trials):
        if alice['state'][x]==bob['measurement'][x] and bob['basis'][x]==alice['basis'][x]:
            count=count+1

    count=float(count)
    trials=float(trials)
    p_h=count/trials
    return p_h
