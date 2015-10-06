# Name: Daniel Wei-Hsuan. Chen
# CSE 140
# Homework 4

import networkx as nx
import matplotlib.pyplot as plt
import operator
import random
from operator import itemgetter
# Import OrderedDict to sort map
from collections import OrderedDict


###
### Problem 1a
###

practice_graph = nx.Graph()

# Add a list of nodes
practice_graph.add_nodes_from(['A','B','C','D','E','F'])
# Add a list of edges
practice_graph.add_edges_from([('A','B'),('A','C'),('B','C'),('B','D'),
                               ('D','C'),('D','F'),('C','F'),('E','D')])

assert len(practice_graph.nodes()) == 6
assert len(practice_graph.edges()) == 8

def draw_practice_graph():
    """Draw practice_graph to the screen."""
    nx.draw(practice_graph)
    plt.show()

# Comment out this line after you have visually verified your practice graph.
# Otherwise, the picture will pop up every time that you run your program.
# draw_practice_graph()


###
### Problem 1b
###

rj = nx.Graph()

rj.add_nodes_from(['Romeo','Nurse','Juliet','Tybalt','Capulet','Friar Laurence','Benvolio','Montague','Escalus','Mercutio','Paris'])
# Add relationship of characters
rj.add_edges_from([('Nurse','Juliet'),('Juliet','Tybalt'),('Juliet','Capulet')
                         ,('Capulet','Tybalt'),('Juliet','Friar Laurence'),('Juliet','Romeo')
                         ,('Capulet','Escalus'),('Capulet','Paris'),('Escalus','Paris')
                         ,('Escalus','Mercutio'),('Paris','Mercutio'),('Escalus','Montague')
                         ,('Mercutio','Romeo'),('Montague','Romeo'),('Montague','Benvolio')
                         ,('Benvolio','Romeo'),('Romeo','Friar Laurence')])

assert len(rj.nodes()) == 11
assert len(rj.edges()) == 17

def draw_rj():
    """Draw the rj graph to the screen and to a file."""
    nx.draw(rj)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()

# Comment out this line after you have visually verified your rj graph and
# created your PDF file.
# Otherwise, the picture will pop up every time that you run your program.
# draw_rj()


###
### Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Returns a set of friends of friends of the given user, in the given graph.
    The result does not include the given user nor any of that user's friends.
    """
    # Find the set of the given user's friends
    friends_set = friends(graph, user)
    friends_of_friends_set = set([])
    # Itereate over each friend and find their friends
    for friend in friends_set:
        friends_of_friends_set.update(friends(graph, friend))
    # Adding the given to the friend set to be subtracted later when returned
    friends_set.add(user)
    return friends_of_friends_set - friends_set

assert friends_of_friends(rj, "Mercutio") == set(['Benvolio', 'Capulet', 'Friar Laurence', 'Juliet', 'Montague'])


def common_friends(graph, user1, user2):
    """Returns the set of friends that user1 and user2 have in common."""
    return friends(graph, user1) & friends(graph, user2)

assert common_friends(practice_graph,"A", "B") == set(['C'])
assert common_friends(practice_graph,"A", "D") == set(['B', 'C'])
assert common_friends(practice_graph,"A", "E") == set([])
assert common_friends(practice_graph,"A", "F") == set(['C'])

assert common_friends(rj, "Mercutio", "Nurse") == set()
assert common_friends(rj, "Mercutio", "Romeo") == set()
assert common_friends(rj, "Mercutio", "Juliet") == set(["Romeo"])
assert common_friends(rj, "Mercutio", "Capulet") == set(["Escalus", "Paris"])


def number_of_common_friends_map(graph, user):
    """Returns a map from each user U to the number of friends U has in common with the given user.
    The map keys are the users who have at least one friend in common with the
    given user, and are neither the given user nor one of the given user's friends.
    Take a graph G for example:
        - A and B have two friends in common
        - A and C have one friend in common
        - A and D have one friend in common
        - A and E have no friends in common
        - A is friends with D
    number_of_common_friends_map(G, "A")  =>   { 'B':2, 'C':1 }
    """
    
    common_friends_map = dict()
    # Iterate over the friends of friends list
    for nonfriend in friends_of_friends(graph, user):
        common_friends_set = common_friends(graph, user, nonfriend)
        # Store the number of common friends corresponding to each friends of friends
        common_friends_map[nonfriend] = len(common_friends_set)
    return common_friends_map

assert number_of_common_friends_map(practice_graph, "A") == {'D': 2, 'F': 1}
assert number_of_common_friends_map(rj, "Mercutio") == { 'Benvolio': 1, 'Capulet': 2, 'Friar Laurence': 1, 'Juliet': 1, 'Montague': 2 }


def number_map_to_sorted_list(map):
    """Given a map whose values are numbers, return a list of the keys.
    The keys are sorted by the number they map to, from greatest to least.
    When two keys map to the same number, the keys are sorted by their
    natural sort order, from least to greatest."""
    
    map_list = []
    # Sort the map by name and then by number
    sort_by_name = sorted(map.iteritems(), key = itemgetter(0))
    sort_by_num = sorted(sort_by_name, key = itemgetter(1), reverse = True)
    # Append the sorted names onto the list and return it 
    for i in sort_by_num:
        map_list.append(i[0])
    return map_list

assert number_map_to_sorted_list({"a":5, "b":2, "c":7, "d":5, "e":5}) == ['c', 'a', 'd', 'e', 'b']
assert number_map_to_sorted_list({"a":9, "b":6, "c":99, "d":6, "e":7}) == ['c', 'a', 'e', 'b', 'd']


def recommend_by_number_of_common_friends(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the number of common friends.
    """
    #Return the recommended list based on number of common friends
    return number_map_to_sorted_list(number_of_common_friends_map(graph, user))

assert recommend_by_number_of_common_friends(practice_graph,"A") == ['D', 'F']
assert recommend_by_number_of_common_friends(rj, "Mercutio") == ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


###
### Problem 3
###

def influence_map(graph, user):
    """Returns a map from each user U to the friend influence, with respect to the given user.
    The map only contains users who have at least one friend in common with U,
    and are neither U nor one of U's friends.
    See the assignment for the definition of friend influence.
    """
    influence_map = dict()
    # iterate over each friends of friends
    for nonfriend in friends_of_friends(graph, user):
        score = 0.0
        # Score each friend of friend with the influence algorithm
        for commonfriend in common_friends(graph, user, nonfriend):
            score += 1.0 / (len(friends(graph, commonfriend)))
        influence_map[nonfriend] =  score
    # Return a sorted map with name and influence score
    return OrderedDict(sorted(influence_map.items(), key = lambda(k,v):(k,v)))

assert influence_map(rj, "Mercutio") == { 'Benvolio': 0.2, 'Capulet': 0.5833333333333333, 'Friar Laurence': 0.2, 'Juliet': 0.2, 'Montague': 0.45 }


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the influence measurement.
    """
    map_list = []
    # Sort the list in the order of name and score
    sort_by_name = sorted(influence_map(graph, user).items(), key = itemgetter(0))
    sort_by_score = sorted(sort_by_name, key = itemgetter(1), reverse = True)
    # Append the names onto the list and return the list
    for i in sort_by_score:
        map_list.append(i[0])
    return map_list

assert recommend_by_influence(rj, "Mercutio") == ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']

###
### Problem 4
###

def recommonedation_difference(graph, users):
    """Print a changed list and unchanged list comparing the influence algorithm and number algorithm
    The printed lists contain the names of users whoese output of recommendations is different or the
    same with both algorithm
    """
    unchanged_list = []
    changed_list = []
    # Iterate over all the nodes in the graph
    for user in users:
        # If the list output is the same then store in the unchanged list, if it's different then store in changed list
        if recommend_by_number_of_common_friends(graph, user) == recommend_by_influence(graph, user):
            unchanged_list.append(user)
        else:
            changed_list.append(user)
    print "Problem 4:\n"
    print "Unchanged Recommendations: " + str(unchanged_list)
    print "Changed Recommendations: " + str(changed_list)

recommonedation_difference(rj, rj.nodes())

###
### Problem 5
###

# Create facebook graph
facebook = nx.Graph()
# Open the file with facebook data
my_file = open("facebook-links.txt")

# Iterate over each line in the file and store the nodes and edges from the file
for line_of_text in my_file:
    line_split = line_of_text.split()
    facebook.add_nodes_from([int(line_split[0]),int(line_split[1])])
    facebook.add_edge(int(line_split[0]),int(line_split[1]))
# Close the file
my_file.close()
assert len(facebook.nodes()) == 63731
assert len(facebook.edges()) == 817090

###
### Problem 6
###

print "\nProblem 6:\n"
# Iterate over each multiple of 1000 and print their first 10 recommended friends from number algorithm
for person in facebook.nodes():
    if person % 1000 == 0:
        print str(person) + " (by number_of_common_friends): " + str(recommend_by_number_of_common_friends(facebook, person)[:10])

###
### Problem 7
###

print "\nProblem 7:\n"
# Iterate over each multiple of 1000 and print their first 10 recommended friends from influence algorithm
for person in facebook.nodes():
    if person % 1000 == 0:
        print str(person) + " (by influence): " + str(recommend_by_influence(facebook, person)[:10])

###
### Problem 8
###

# Evaluate the 63 users with both algorithm and count how many of them are the same or different
same = 0
different = 0
for person in facebook.nodes():
    if person % 1000 == 0:
        if recommend_by_number_of_common_friends(facebook, person)[:10] == recommend_by_influence(facebook, person)[:10]:
            same += 1
        else:
            different += 1
print "\nProblem 8:\n"
print "Same: " + str(same)
print "Different: " + str(different)

###
### Collaboration
###

# I did not collaborate with anyone! Went solo.
