# Name: Daniel Wei-Hsuan. Chen
# CSE 140
# Homework 2: DNA analysis

# This program reads DNA sequencer output and computes statistics, such as
# the GC content.  Run it from the command line like this:
#   python dna_analysis.py myfile.fastq


###########################################################################
### Libraries
###

# The sys module supports reading files, command-line arguments, etc.
import sys


###########################################################################
### Read the nucleotides into a variable named seq
###

# You need to specify a file name
if len(sys.argv) < 2:
    print "You must supply a file name as an argument when running this program."
    sys.exit(2)
# The file name specified on the command line, as a string.
filename = sys.argv[1]
# A file object from which data can be read.
inputfile = open(filename)

# All the nucleotides in the input file that have been read so far.
seq = ""
# The current line number (= the number of lines read so far).
linenum = 0


for line in inputfile:
    linenum = linenum + 1
    # if we are on the 2nd, 6th, 10th line...
    if linenum % 4 == 2:
        # Remove the newline characters from the end of the line
        line = line.rstrip()
        seq = seq + line


###########################################################################
### Compute statistics
###

# Total nucleotides seen so far.
total_count = 0
# Number of G and C nucleotides seen so far.
gc_count = 0
at_count = 0
# Number of A, T, G, C seen so far.
a_count = 0
t_count = 0
g_count = 0
c_count = 0
acgt_sum = 0
# Initial Sequence Length before counting.
seq_length = 0
# Initial AT/GC ratio
atgc_ratio = 0
# Setting the gc class to be blank initially.
gc_class = ''

# Counting each variables as well as total count with a forloop
for bp in seq:
    total_count = total_count + 1

    if bp == 'C' or bp == 'G':
        gc_count = gc_count + 1
    if bp == 'A' or bp == 'T':
        at_count = at_count + 1
    if bp == 'G':
        g_count = g_count + 1
    if bp == 'C':
        c_count = c_count + 1
    if bp == 'A':
        a_count = a_count + 1
    if bp == 'T':
        t_count = t_count + 1

# the sum of: the A count, the C count, the G count, and the T count
acgt_sum = a_count + c_count + g_count + t_count        

# Calculation of GC content
gc_content = float(gc_count) / acgt_sum

# Calculation of AT content
at_content = float(at_count) / acgt_sum

# the length of the seq variable. You can compute this with len(seq)
seq_length = len(seq)

# AT/GC ratio calculation
atgc_ratio = float((a_count + t_count))/(g_count + c_count)

# An if statement that classify the GC classification
if gc_content > .6:
    gc_class = 'high GC content'
elif gc_content < .4:
    gc_class = 'low GC content'
else:
    gc_class = 'moderate GC content'


# Print the computations results stored in variables
print 'GC-content:', gc_content
print 'AT-content:', at_content
print 'G count:', g_count
print 'C count:', c_count
print 'A count:', a_count
print 'T count:', t_count
print 'Sum count:', acgt_sum
print 'Total count:', total_count
print 'seq length:', seq_length
print 'AT/GC Ratio:', atgc_ratio
print 'GC Classification:', gc_class

