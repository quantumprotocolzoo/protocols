import random

def bobForge(trials, QBER, transmission):
    alice = {'basis':[random.randrange(0, 2, 1) for _ in range(trials)],'state':[random.randrange(0, 2, 1) for _ in range(trials)]}

    bob={'success':[1 if random.random()<transmission else 0 for x in range (0,trials)], 'basis':[random.randrange(0, 2, 1) for _ in range(trials)]}

    charlie={'success':[1 if random.random()<transmission else 0 for x in range (0,trials)], 'basis':[random.randrange(0, 2, 1) for _ in range(trials)]}

    bob['measurement']=[9]*trials
    charlie['measurement']=[9]*trials


    for x in range (0,trials):
        if bob['success'][x]==1:
            if bob['basis'][x]==alice['basis'][x]:
                bob['measurement'][x]=alice['state'][x]
            else:
                bob['measurement'][x]=random.randint(0,1)
        else:
            bob['measurement'][x]=random.randint(0,1)

    for x in range (0,trials):
        if charlie['success'][x]==1:
            if charlie['basis'][x]==alice['basis'][x]:
                charlie['measurement'][x]=(alice['state'][x]+1)%2
            else:
                charlie['measurement'][x]=random.randint(0,1)

    count=0
    for x in range (0,trials):
        if bob['measurement'][x]==charlie['measurement'][x] and bob['basis'][x]==charlie['basis'][x]:
            count=count+1


    count=float(count)
    trials=float(trials)
    C_min=count/trials
    return C_min
