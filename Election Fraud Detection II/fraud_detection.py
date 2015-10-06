# Name: Daniel Wei-Hsuan Chen   
# UW NetID: dnnl8017
# Section: AA
# CSE 140
# Homework 7: Detecting Fraudulent Data

import csv
import math
import matplotlib.pyplot as plt
import random
from decimal import Decimal

################################################################################
# Problem 1: Read and clean Iranian election data
################################################################################

def extract_election_vote_counts(filename, column_names):
    """
    Takes a csv file that contains election data and a list of candidates' name
    then return the vote count for each of the candidate in each row in the format
    of a list
    """
    # Create an empty list that contains the vote count
    voteCount = []
    # Iterate through each row and then append the
    for row in csv.DictReader(open(filename)):
        for candidate in column_names:
            ## Only append the value if there's one
            if row[candidate].replace(",","") != "":
                voteCount.append(int(row[candidate].replace(",","")))
    return voteCount
        
################################################################################
# Problem 2: Make a histogram
################################################################################

def ones_and_tens_digit_histogram(numbers):
    """
    Takes as input a list of numbers and produces an output a list of 10 numbers.
    In the returned list, the value at index i is the frequency with which digit
    i appeared in the ones place or the tens place in the output
    """
    #Keeping the count of how many digits there are
    totalCount = 0
    #Each index represents the frequency of index i
    list = [0,0,0,0,0,0,0,0,0,0]
    histogram = []
    for number in numbers:
        list[number % 10] += 1.0    
        number = number / 10
        totalCount += 1
        list[number % 10] += 1.0
        totalCount += 1

    #divide the frequency of each index by the totalCount
    for i in list:
         histogram.append(i / totalCount)
    return histogram
            
################################################################################
# Problem 3: Plot election data
################################################################################

def plot_iranian_least_digits_histogram(histogram):
    """
    This function  takes a histogram (as created by ones_and_tens_digit_histogram)
    and graphs the frequencies of the ones and tens digits for the Iranian election
    data.
    """
    xs = range(len(histogram))
    y = histogram
    # Ideal Chart Creation
    z = [0.1 for x in xs]

    #Plotting the Ideal line
    plt.plot(xs, z, label = 'Ideal')
    #Plotting the Iran line
    plt.plot(xs , y, label = 'Iran')
    #Labeling Digit on the x-axis
    plt.xlabel("Digit")
    #Labeling Frequency on the y-axis
    plt.ylabel("Frequency")
    #Plotting the legend
    plt.legend()
    #Saving the plot
    plt.savefig("iran-digits.png")
    #Display the plot
    plt.show()
    
################################################################################
# Problem 4: Smaller samples have more variation
################################################################################

def plot_distribution_by_sample_size():
    """
    This function  creates five different collections (one of size 10, another
    of size 50, then 100, 1000, and 10,000) of random numbers where every element
    in the collection is a different random number x such that 0 <= x < 100. 
    """
    #Creating lists and histograms based fomr the random lists created
    histogram1 = ones_and_tens_digit_histogram(make_random_list(10))
    histogram2 = ones_and_tens_digit_histogram(make_random_list(50))
    histogram3 = ones_and_tens_digit_histogram(make_random_list(100))
    histogram4 = ones_and_tens_digit_histogram(make_random_list(1000))
    histogram5 = ones_and_tens_digit_histogram(make_random_list(10000))

    #Creating the Ideal line for comparison
    xs = range(len(histogram1))
    z = [0.1 for x in xs]
    #Plotting the ideal line
    plt.plot(xs, z, label = 'Ideal')
    plt.plot(range(len(histogram1)), histogram1, label = '10 random numbers')
    plt.plot(range(len(histogram2)), histogram2, label = '50 random numbers')
    plt.plot(range(len(histogram3)), histogram3, label = '100 random numbers')
    plt.plot(range(len(histogram4)), histogram4, label = '1000 random numbers')
    plt.plot(range(len(histogram5)), histogram5, label = '10000 random numbers')
    #Plotting the x-axis label
    plt.xlabel("Digit")
    #Plotting the y-axis lable
    plt.ylabel("Frequency")
    #Adding the title
    plt.suptitle('Distribution of last two digits')
    #Adding the legnd
    plt.legend()
    #Save the file
    plt.savefig("random-digits.png")
    #Show the plot
    plt.show()

def make_random_list(size):
    """
    This is a helper function that takes an int size as an input then return a list
    with size that is indicated by the parameter, every element in the list is
    a random number between 0 and 99
    """
    list = []
    for i in range(size):
        list.append(random.randint(0,99))
    return list

################################################################################
# Problem 5: Comparing variation of samples
################################################################################

def mean_squared_error(numbers1, numbers2):
    """
    This function will take two list with the same length and then return
    the average of the squared differences between each corresponding datapoint
    in the two lists
    """
    sum = 0
    count = 0.0
    for i in range(len(numbers1)):
        sum += ((numbers1[i] - numbers2[i])**2)
        count += 1.0
    return sum / count

################################################################################
# Problem 6: Comparing Variation of samples
################################################################################

def calculate_mse_with_uniform(histogram):
    """
    takes a histogram (as created by ones_and_tens_digit_histogram) and returns
    the mean squared error of the given histogram with the uniform distribution.
    """
    list = [.1] * len(histogram)
    return mean_squared_error(histogram, list)
    
def compare_iranian_mse_to_samples(iranian_mse, number_of_iranian_samples):
    """
    This function will build 10,000 groups of random numbers, where each group
    is the same size as the Iranian election data (120 numbers),and compute
    the MSE with the uniform distribution for each of these groups.
    """
    compare_mse_to_samples(iranian_mse, number_of_iranian_samples, "2009 Iranian election")

################################################################################
# Problem 8: Other datasets 
################################################################################

def compare_us_mse_to_samples(us_mse, number_of_us_samples):
    """
    This function will build 10,000 groups of random numbers, where each group
    is the same size as the United States election data, and compute
    the MSE with the uniform distribution for each of these groups.
    """
    compare_mse_to_samples(us_mse, number_of_us_samples, "2008 United States election")

def compare_mse_to_samples(data_mse ,numbers_of_dataSamples, name):
    """
    This is a helpful function that takes a sample_mse and compare the sample
    to 10,000 groups of random numbers, where each group is the same size
    as the sample data, and return the MSE with the uniform distribution
    for each of these groups
    """
    #Keeping count of samples that are less than data_mse
    countLess = 0
    #Keeping count of samples that are more than data_mse
    countMore = 0
    # Create 10000 samples
    for i in range(10000):
        if (calculate_mse_with_uniform(ones_and_tens_digit_histogram(make_random_list(numbers_of_dataSamples)))) < data_mse:
            countLess += 1
        else:
            countMore += 1
    #Printing the output
    print name , "MSE:", data_mse
    print "Quantity of MSEs larger than or equal to the" , name, "MSE:" , countMore
    print "Quantity of MSEs smaller than the" , name, "MSE:" , countLess
    print name, "null hypothesis rejection level p:", countMore / 10000.0

################################################################################
# Main 
################################################################################

def main():
    """
    Main function, which is executed when fraud_detection.py is run as a Python script.
    """

    # Find the vote count
    voteCountListIran = extract_election_vote_counts("election-iran-2009.csv", ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"])
    # Creating a histogram of ones and tens
    histogramIran = ones_and_tens_digit_histogram(voteCountListIran)   
    # Plotting the Iranian Histogram
    plot_iranian_least_digits_histogram(histogramIran)
    # Plotting different sample sizes of histograms
    plot_distribution_by_sample_size()
    # calculate mse for iran's dataset
    iran_mse = calculate_mse_with_uniform(histogramIran)
    # Compare Iran's mse with the simulated data
    compare_iranian_mse_to_samples(iran_mse, len(voteCountListIran))
    print

    # Find the vote count for US
    voteCountListUS = extract_election_vote_counts("election-us-2008.csv", ["Obama", "McCain", "Nader", "Barr", "Baldwin", "McKinney"])
    # Creating a histogram for US datasets
    histogramUS = ones_and_tens_digit_histogram(voteCountListUS)
    # Calculate mse for US datases
    us_mse = calculate_mse_with_uniform(histogramUS)
    # Compare US's to simulated data
    compare_us_mse_to_samples(us_mse, len(voteCountListUS))

# If this file, fraud_detection.py, is run as a Python script (such as by typing
# "python election.py" at the command shell), then run the main() function.
if __name__ == "__main__":
    main()
