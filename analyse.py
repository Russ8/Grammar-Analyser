import csv
import sys
from scipy import stats
import numpy as np

bin_totals = [0] * 100
bin_numbers = [0] * 100
bin_averages = [0] * 100

n = 90000
num_errors = [0] * n
num_answers = [0] * n
scores = [0] * n
accepted_answers = [0] * n 
error_density = [0] * n 
i=0

#index,id,length,num_errors,errors_per_100_chars,score,num_answers,accepted_answer
with open("testcsv.csv") as f:
    lis = [line.split() for line in f]        # create a list of lists
    for i, x in enumerate(lis):              #print the list items 
        items = x[0].split(',')
        length = int(items[2])
        if length ==0 :
            continue
        if i < n :
            num_errors[i] = int(items[3])
            error_density[i] = int(items[3]) * 500 / length
            scores[i] = int(items[5])
            num_answers[i] = int(items[6])
            accepted_answers[i] = int(items[7])
        index = int(items[3]) * 500 / length
        if index >= 100 :
            continue
        bin_totals[index] += int(items[5])
        bin_numbers[index] = bin_numbers[index] + 1
        i = i+1

i = 0
indicies = [0] * 100
for b in bin_totals :
    indicies[0] = i
    if(bin_numbers[i] != 0) :
        bin_averages[i] = bin_totals[i] / bin_numbers[i]
    else :
        bin_averages[i] = -1
    print i, bin_averages[i], bin_numbers[i]
    i = i+1



print 'num errors agaisnt num answers'
slope, intercept, r_value, p_value, std_err = stats.linregress(num_errors,num_answers)
print r_value, r_value*r_value, slope

print 'num errors agaisnt accepted answer'
slope, intercept, r_value, p_value, std_err = stats.linregress(num_errors,accepted_answers)
print r_value, r_value*r_value, slope

print 'num errors agaisnt score'
slope, intercept, r_value, p_value, std_err = stats.linregress(num_errors,scores)
print r_value, r_value*r_value, slope

print 'error density agaisnt num answers'
slope, intercept, r_value, p_value, std_err = stats.linregress(error_density,num_answers)
print r_value, r_value*r_value, slope

print 'error density agaisnt accepted answer'
slope, intercept, r_value, p_value, std_err = stats.linregress(error_density,accepted_answers)
print r_value, r_value*r_value, slope

print 'error density agaisnt score'
slope, intercept, r_value, p_value, std_err = stats.linregress(error_density,scores)
print r_value, r_value*r_value, slope


hist_values, bin_edges = np.histogram(num_errors, bins=30, range=(0, 30))
print 'histogram num errors:'

for t in hist_values :
    print t

for b in bin_edges :
    print b
print bin_edges

hist_values, bin_edges = np.histogram(error_density, bins=30, range=(0, 30))

print 'histogram error density:'

for t in hist_values :
    print t

for b in bin_edges :
    print b
print bin_edges

print 'means'
error_totals = 0
error_freq_totals = 0

for t in num_errors :
    error_totals = error_totals + t

for t in error_density :
    error_freq_totals = error_freq_totals + t

print error_totals/90000.0, error_freq_totals/90000.0


