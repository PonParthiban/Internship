#two sets and perform union and intersection
set1 = {1,2,3,4,5,7}
set2 = {2,4,7,8,9,10}

#union wt |
union_set = set1 | set2 
print(union_set)
#union wt .union()
union_set1 = set2.union(set1)
print(union_set1)

#intersection
intersection_set = set1 & set2
print(intersection_set)
