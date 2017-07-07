import itertools
import random
import sys

output_file = open("jitesh_chawla_toivonen.txt",'w')
neg_border_list = list()
probability = 0.4
inputfile = open(sys.argv[1])
support = int(sys.argv[2])

count = 0; baskets_before_sampling = list()

lines_data = inputfile.readlines()
for line in lines_data:
    line = line.strip()
    line = line.split(",")
    baskets_before_sampling.append(sorted(line))
    count += 1
rlen = len(baskets_before_sampling)
basketAfterSampling = list()
subset_length = 1;           # length of the tuple of frequent itemsets.
freq_item_sets = list(); extended_freq_itemsets = list()  # contains set of all frequent itemsets.


# Defining the negative checker.
def neg_checker(candidate_freq_itemsets,items_freq,freq_itemsets_earlier):

    for key, value in candidate_freq_itemsets.items():
        if int(value) >= support2:
            items_freq.append(list(key))
        else:
            if len(key) == 1:  # case of singletons of a subset which will come under negative border
                neg_border_list.append(key)
            else:
                count = 0;
                for subset in itertools.combinations(key, subset_length - 1):
                    if list(subset) not in freq_itemsets_earlier:
                        count += 1

                if count == 0:
                    neg_border_list.append(key)
    return items_freq

# Creating Frequent Itemsets.
def createfreq_items_sets(baskets_before_sampling, subset_length, freq_itemsets_earlier):
    candidate_freq_itemsets = {}
    items_freq = list()
    for line in baskets_before_sampling:
        # print(line)
        for subset in itertools.combinations(line, subset_length):
            candidate_freq_itemsets.setdefault(subset, 0)
            candidate_freq_itemsets[subset] += 1
        # print(candidate_freq_itemsets)
    items_freq=neg_checker(candidate_freq_itemsets,items_freq,freq_itemsets_earlier)
    return sorted(items_freq)

# Generating Random samples
def generate_random_sample(prob,c):#Return a k length list of unique elements chosen from the population sequence or set
    func_val1 = random.sample(range(c), int(prob * c))
    return func_val1

#  Calculating new Support
def get_newsupport_value(prob,s):#Calculates the new support
    func_val2 = int(0.9*prob*s)
    return func_val2

# Genearting Itemsets
def generateitemsets(lists,k):
    lst=[list(x) for x in itertools.combinations(lists, k)]
    return lst

# Checking Negative borders.
def checkNegative(baskets_before_sampling,neg_border_list):
    negative_border_dict={}
    for basket in baskets_before_sampling:
        for item in neg_border_list:
            if set(item) <= set(basket):
                negative_border_dict.setdefault(item, 0)
                negative_border_dict[item] += 1
    # print(negative_border_dict)
    return negative_border_dict

# Counting frequent Itemsets
def count_freq_itemsets(baskets_before_sampling,extended_freq_itemsets):
    for basket in baskets_before_sampling:
        for item1 in extended_freq_itemsets:
            for item2 in item1:
                if set(item2) <= set(basket):
                    count_freq_itemsets_dict.setdefault(tuple(item2), 0)    #will set count_freq_itemsets_dict[key]=default if key is not already in dict.
                    count_freq_itemsets_dict[tuple(item2)] += 1
    # print(count_freq_itemsets_dict)
    return count_freq_itemsets_dict

# Function to display the result.
def display(iterationcount,probability,list_print):
    print(iterationcount)
    print(probability)
    output_file.write(str(iterationcount) + "\n" + str(probability) + "\n")
    maxlength=max([len(x) for x in list_print])

    for i in range(0,maxlength+1):
        print_list2 = list()
        for element in list_print:
            if(i==len(element)):
                print_list2.append(list(element))
        if print_list2:
            print(print_list2)       # printing frequent itemsets in a lexicological order
            print                    # leaving an line

            output_file.write(str(print_list2) + "\n\n")


support2 = get_newsupport_value(probability, support)
random_indexes = generate_random_sample(probability, rlen)



for ran_ind in random_indexes:
    basketAfterSampling.append(baskets_before_sampling[ran_ind])
flag = True
iterationcount = 1      # number of iterations required for the successful run

# Performing the iterations until we do not have any other new frequent itemsets.
while flag:
    flag = False

    for iter_count in range(0,200):    #loop for maximum number of iterations
        freq_item_sets = createfreq_items_sets(basketAfterSampling, subset_length, freq_item_sets)
        if len(freq_item_sets) > 0:
            extended_freq_itemsets.append(freq_item_sets)


        subset_length += 1
        if freq_item_sets == []:
            negative_border_dict = checkNegative(baskets_before_sampling,neg_border_list)
            counter = 0
            for key, value in negative_border_dict.items():

                if value >= support:
                    iterationcount += 1;counter += 1
                    subset_length = 1
                    frequentItemsets = list(); extended_freq_itemsets = list(); basketAfterSampling = list();neg_border_list = list()
                    random_indexes = generate_random_sample(probability,count)
                    for ran_ind in random_indexes:
                        basketAfterSampling.append(baskets_before_sampling[ran_ind])
                    break
                lists= list()
                k=1
                generateitemsets_new=generateitemsets(lists,k)

            count_freq_itemsets_dict={}
            count_freq_itemsets_dict= count_freq_itemsets(baskets_before_sampling,extended_freq_itemsets)
            list_print = list()
            for val1 in count_freq_itemsets_dict:
                if count_freq_itemsets_dict[val1] >= support:
                    list_print.append(val1)
                # print(list_print)
            list_print=sorted(list_print)
            if counter == 0:
                display(iterationcount,probability,list_print)
                break
    flag = True
    break