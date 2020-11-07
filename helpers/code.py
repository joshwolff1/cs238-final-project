from collections import defaultdict
import pandas as pd
import sys
import operator


def qLearningCompute(infile, outfile, nStates):
    df = pd.read_csv(infile)
    QValues = defaultdict(lambda: defaultdict(float))
    # initialize hyperparams
    gamma = 0.95
    alpha = 0.6
    ap_dict = preprocess(df)
    
    for i in range(10):
        for _, row in df.iterrows():
            qLearning(QValues, row.s, row.a, row.r, row.sp, alpha, gamma, ap_dict[row.s])
        
    chooseOptimal(QValues, outfile, nStates)
    
def sarsaCompute(infile, outfile, nStates):
    df = pd.read_csv(infile)
    QValues = defaultdict(lambda: defaultdict(float))
    gamma = 0.95
    alpha = 0.6
    ap_dict = preprocess(df)
    for i in range(10):
        for _, row in df.iterrows():
            sarsa(QValues, row.s, row.a, row.r, row.sp, alpha, gamma)
    chooseOptimal(QValues, outfile, nStates)
            
def sarsa(QValues, s, a, r, sp, alpha, gamma):
    maxed = []                             
    QValues[s][a] = QValues[s][a] + (alpha*(r + (QValues[sp][a] - QValues[s][a]))) 


def chooseOptimal(QValues, filename, nStates):
    with open(filename, 'w') as f:
        for key in range(10, nStates+10, 1):
            Dict = QValues[key]
            best_a = 1
            if len(Dict.items()) != 0:
                best_a = max(Dict.items(), key=operator.itemgetter(1))[0]
            f.write("{}\n".format(best_a))
        
    # ap_dict -> {s: all possible a}
def preprocess(df):   
    ap_dict = {}
    for state in df.s.unique():
        temp = df[df["s"] == state]
        A = temp.a.unique()
        ap_dict[state] = A
    return ap_dict


#{s: {a1: score1, a2: score2, a3: score3}}
# s: {a:score}


def qLearning(QValues,s,a,r,sp, alpha, gamma, actions):      
    maxed = []
    for ap in actions:
        maxed.append(QValues[sp][ap])
    maxed = max(maxed)                               
    QValues[s][a] = QValues[s][a] + (alpha*(r + ((gamma*maxed) - QValues[s][a]))) 
    

def main():
    if len(sys.argv) != 4:
        raise Exception("usage: python code.py <infile>.csv <outfile>.policy")

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    nStates = int(sys.argv[3])
    qLearningCompute(inputfilename, outputfilename, nStates)
    #sarsaCompute(inputfilename, outputfilename, nStates)


if __name__ == '__main__':
    main()
