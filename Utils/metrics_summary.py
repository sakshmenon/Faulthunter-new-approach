def true_false_computation(y_true, y_pred, label):
    true_positives = 0
    false_positives = 0
    true_negetives = 0
    false_negetives = 0
    for i in enumerate(y_pred):
        if i[1] == y_true[i[0]]:
            if i[1] == label:
                true_positives += 1
            else: 
                true_negetives += 1
        elif i[1] != y_true[i[0]]:
            if i[1] == label:
                false_positives += 1
            else: 
                false_negetives += 1
        
    return true_positives, true_negetives, false_positives, false_negetives

def f1(true_positives, false_positives, false_negetives):
    denom = (2*true_positives + false_positives + false_negetives)
    if denom == 0:
        return 0
    else:
        return (2*true_positives/denom)

def precision(true_positives, false_positives):
    denom = true_positives + false_positives
    if denom == 0:
        return 0
    else:
        return  true_positives / denom

def recall(true_positives, false_negetives):
    if false_negetives == 0:
        return 0
    else:
        return true_positives/(true_positives + false_negetives)

def score_summary(pred, outputs, label):
    print('For {}:'.format('secure' if label == 0 else 'insecure'))
    true_positives, true_negetives, false_positives, false_negetives = true_false_computation(pred, outputs, label)
    print('f1 score: ', f1(true_positives, false_positives, false_negetives))
    print('precision score: ', precision(true_positives, false_positives))
    print('recall score: ', recall(true_positives, false_negetives))
    print()
    