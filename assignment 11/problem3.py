import sys
import time
import csv
import math
from scipy import spatial

def loadTaxiTripsPickupAndDropoffs(filename):
    #bbox around Manhattan
    latBounds = [40.6,40.9]
    lngBounds = [-74.05,-73.90]
    #
    f = open(filename)
    reader = csv.reader(f)
    header = reader.next()
    #
    lngIndex0 = header.index(' pickup_longitude')
    latIndex0 = header.index(' pickup_latitude')
    latIndex1 = header.index(' dropoff_latitude')
    lngIndex1 = header.index(' dropoff_longitude')
    result = []
    for l in reader:
        try:
            point0 = [float(l[latIndex0]),float(l[lngIndex0])]
            point1 = [float(l[latIndex1]),float(l[lngIndex1])]
            if latBounds[0] <= point0[0] <= latBounds[1] and lngBounds[0] <= point0[1] <= lngBounds[1] and latBounds[0] <= point1[0] <= latBounds[1] and lngBounds[0] <= point1[1] <= lngBounds[1]:
                result.append([point0[0],point0[1],point1[0],point1[1]])
        except:
            print l
    return result
    
def naiveApproach(tripLocations, startRectangle, endRectangle):
    #indices is a list that should contain the indices of the trips in the tripLocations list
    #which start in the startRectangle region and end in the endRectangle region
    indices = []
    startTime = time.time()

    #TODO: insert your code here. You should implement the naive approach, i.e., loop 
    #      through all the trips and find the closest intersection by looping through
    #      all of them
    for i, v in enumerate(tripLocations):
        if v[0] >= startRectangle[0][0] and v[0] <= startRectangle[0][1] and v[1] >= startRectangle[1][0] and v[1] <= startRectangle[1][1]:
            if v[2] >= endRectangle[0][0] and v[2] <= endRectangle[0][1] and v[3] >= endRectangle[1][0] and v[3] <= endRectangle[1][1]:
                indices.append(i)
    print indices
    #
    endTime = time.time()
    print 'The naive computation took', (endTime - startTime), 'seconds'
    return indices

def kdtreeApproach(tripLocations, startRectangle, endRectangle):
    #indices is a list that should contain the indices of the trips in the tripLocations list
    #which start in the startRectangle region and end in the endRectangle region
    indices = []
    startTime = time.time()

    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip
    start_list = [[v[0],v[1]] for v in tripLocations]
    start_tree = spatial.KDTree(start_list)
    end_list = [[v[2],v[3]] for v in tripLocations]
    end_tree = spatial.KDTree(end_list)
    
    qtree_start = start_tree.query_ball_point(startRectangle, 1)
    qtree_end = end_tree.query_ball_point(endRectangle, 1)
    
    print qtree_start
    print qtree_end
    
    endTime = time.time()
    print 'The kdtree computation took', (endTime - startTime), 'seconds'
    return indices

def extraCredit(tripLocations, startPolygon, endPolygon):
    #indices is a list that should contain the indices of the trips in the tripLocations list
    #which start in the startPolygon region and end in the endPolygon region
    indices = []

    #TODO: insert your code here. You should build the kdtree and use it to query the closest
    #      intersection for each trip

    return indices    

if __name__ == '__main__':
    #these functions are provided and they already load the data for you
    trips             = loadTaxiTripsPickupAndDropoffs(sys.argv[1])
    #
    startRectangle    = [[40.713590,40.721319],[-74.011116,-73.994722]] #[[minLat,maxLat],[minLng,maxLng]]
    endRectangle      = [[40.744532,40.748398],[-74.003005,-73.990881]] #[[minLat,maxLat],[minLng,maxLng]]
    
    #You need to implement this one. You need to make sure that the counts are correct
    naiveIndices = naiveApproach(trips,startRectangle, endRectangle)

    #You need to implement this one. You need to make sure that the counts are correct
    kdtreeIndices = kdtreeApproach(trips,startRectangle, endRectangle)
