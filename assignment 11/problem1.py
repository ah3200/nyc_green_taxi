import sys
import time
import csv
import math
from scipy import spatial

def loadRoadNetworkIntersections(filename):
    #bbox around Manhattan
    latBounds = [40.6,40.9]
    lngBounds = [-74.05,-73.90]
    #
    listWithIntersectionCoordinates = []
    f = open(filename)
    reader = csv.reader(f, delimiter=' ')
    for l in reader:
        try:
            point = [float(l[0]),float(l[1])]
            if latBounds[0] <= point[0] <= latBounds[1] and lngBounds[0] <= point[1] <= lngBounds[1]:
                listWithIntersectionCoordinates.append(point)
        except:
            print l

    return listWithIntersectionCoordinates

def loadTaxiTrips(filename):
    #load pickup positions
    loadPickup = True
    #bbox around Manhattan
    latBounds = [40.6,40.9]
    lngBounds = [-74.05,-73.90]
    #
    f = open(filename)
    reader = csv.reader(f)
    header = reader.next()
    #
    if loadPickup:        
        lngIndex = header.index(' pickup_longitude')
        latIndex = header.index(' pickup_latitude')
    else:
        latIndex = header.index(' dropoff_latitude')
        lngIndex = header.index(' dropoff_longitude')
    result = []
    for l in reader:
        try:
            point = [float(l[latIndex]),float(l[lngIndex])]
            if latBounds[0] <= point[0] <= latBounds[1] and lngBounds[0] <= point[1] <= lngBounds[1]:
                result.append(point)

        except:
            print l
    return result
    
def naiveApproach(intersections, tripLocations):
    #counts is a dictionary that has as keys the intersection index in the intersections list
    #and as values the number of trips in the tripLocation list which has the key as the closest
    #intersection.
    counts = {}
    startTime = time.time()

    #TODO: insert your code here. You should implement the naive approach, i.e., loop 
    #      through all the trips and find the closest intersection by looping through
    #      all of them
    for points in tripLocations:
        min = 10000
        min_index = 0
        for i,intersect in enumerate(intersections):
            distance = math.sqrt((points[0] - intersect[0])**2 + (points[1] - intersect[1])**2)
            if distance < min:
                min = distance
                min_index = i

        if min_index in counts:
            counts[min_index] += 1
        else:
            counts[min_index] = 1
        

    #
    endTime = time.time()
    print 'The naive computation took', (endTime - startTime), 'seconds'
    return counts

def kdtreeApproach(intersections, tripLocations):
    #counts is a dictionary that has as keys the intersection index in the intersections list
    #and as values the number of trips in the tripLocation list which has the key as the closest
    #intersection.
    counts = {}
    startTime = time.time()

    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip
    tree = spatial.KDTree(intersections)
    qtree = tree.query(tripLocations)
#    print qtree
#    print qtree[1]
    for i in qtree[1]:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
#    print counts
    #
    endTime = time.time()
    print 'The kdtree computation took', (endTime - startTime), 'seconds'
    return counts

def plotResults(intersections, counts):
    #TODO: intersect the code to plot here
    print 'TODO'

if __name__ == '__main__':
    #these functions are provided and they already load the data for you
    roadIntersections = loadRoadNetworkIntersections(sys.argv[1])
    tripPickups       = loadTaxiTrips(sys.argv[2])

    #You need to implement this one. You need to make sure that the counts are correct
    naiveCounts = naiveApproach(roadIntersections,tripPickups)
#    print naiveCounts
    #You need to implement this one. You need to make sure that the counts are correct
    kdtreeCounts = kdtreeApproach(roadIntersections,tripPickups)

    #
    plotResults(roadIntersections,kdtreeCounts)
