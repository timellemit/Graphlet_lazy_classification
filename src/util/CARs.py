from freq_itemsets import freq_itemsets, dataFromFile

def is_falsified(itemset, opposite_context_file):
    res = False
    for instance in dataFromFile(opposite_context_file):
        if set(itemset[0]).issubset(instance):
            res = True
            break
    return res
        
def positive_cars(input_pos_file, input_neg_file, minSupport=0.26, minConfidence=0.26):
    pos_cars = []
    pos_freq_itemsets = freq_itemsets(input_pos_file, minSupport, minConfidence)
    for itemset in pos_freq_itemsets:
        if not is_falsified(itemset, input_neg_file):
                pos_cars.append(itemset)
        else:
                # itemset is not CAR
                pass
    return pos_cars
            
if __name__ == "__main__":
    print positive_cars("C:\Users\User\Documents\eclipse_workspace\Apriori\weather_negative.csv",\
                        "C:\Users\User\Documents\eclipse_workspace\Apriori\weather_positive.csv", minSupport=0.24, minConfidence=0)