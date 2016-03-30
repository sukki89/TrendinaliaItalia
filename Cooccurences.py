from collections import defaultdict
 
com = defaultdict(lambda : defaultdict(int))
 
# f is the file pointer to the JSON data set
for line in f: 
    tweet = json.loads(line)
    terms_only = [term for term in preprocess(tweet['text']) 
                  if term not in stop 
                  and not term.startswith(('#', '@'))]
 
    # Build co-occurrence matrix
    for i in range(len(terms_only)-1):            
        for j in range(i+1, len(terms_only)):
            w1, w2 = sorted([terms_only[i], terms_only[j]])                
            if w1 != w2:
                com[w1][w2] += 1

com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = max(com[t1].items(), key=operator.itemgetter(1))[:5]
    for t2 in t1_max_terms:
        com_max.append(((t1, t2), com[t1][t2]))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])

search_word = sys.argv[1] # pass a term as a command-line argument
count_search = Counter()
for line in f:
    tweet = json.loads(line)
    terms_only = [term for term in preprocess(tweet['text']) 
                  if term not in stop 
                  and not term.startswith(('#', '@'))]
    if search_word in terms_only:
        count_search.update(terms_only)
print(&quot;Co-occurrence for %s:&quot; % search_word)
print(count_search.most_common(20))

