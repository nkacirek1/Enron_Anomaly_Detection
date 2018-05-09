import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
from datetime import date
from datetime import timedelta

style.use('ggplot')


class k_Means:

    # constructor
    # initializes k
    # sets the tolerance (aka how far it can be from the centroid)
    # sets max iterations for the main loop to be 500
    # initializes the centroids
    def __init__(self, k=5, tolerance=.0001, max_iterations=500):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.centroids = {}

    # reads in the dataset using pandas and returns a numpy array with all the features
    def parseData(self, file):
        # reads in the csv file using pandas
        df = pd.read_csv(file)
        # puts into a numpy array
        X = df.values
        return X

    # splits the data to keep what we want
    # replaces the individual month day year and hour with a single datetime object
    def splitData(self, data):
        # remove the from and to email address data
        data = data[:, 2:]

        # a = date(year, month, date)
        # loop through all the values, create a datetime object
        for x in data:
            trydate = datetime(x[2], x[1], x[0], x[3])
            x[3] = trydate

        # remove all but the datetime object and return
        data = data[:, 3:]
        return data

    # calculates the distance between the feature and the centroid by hour
    # distances = [hours between feature date and 1st centroid, hours between feature date and 2nd centroid, ....]
    def dateTimeDistance(self, features):
        distances = [np.linalg.norm(((features[0] - self.centroids[centroid][0]).days * 24) + (
                (features[0] - self.centroids[centroid][0]).seconds / 3600.0)) for centroid in self.centroids]
        return distances

    # computes the average date between all the dates
    def dateTimeAverage2(self, chunk):
        # sets the earliest date as the base
        base = np.min(chunk)

        # calculates the distance from the base to each of the dates in the class
        # adds this distance to datesSum
        datesSum = timedelta(0)
        for i in range(len(chunk)):
            datesSum += (chunk[i][0] - base)

        # divides the sum by the number of dates given
        averageDays = datesSum // timedelta(days=len(chunk))
        averageHours = int(round(((datesSum / timedelta(days=len(chunk))) % 1), 5) * 24)

        averageDate = base + timedelta(days=averageDays, hours=averageHours)
        result = []
        result.append(averageDate)

        return np.array(result)

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
    def initializeCentroids(self, data):
        for i in range(self.k):
            self.centroids[i] = data[i]

    # main loop that runs k-means algorithm
    def km_iterations(self, data):

        # begin iterations
        # loop through up to the max number of iterations, or until we reach our tolerance
        for i in range(self.max_iterations):

            # self.classes is an empty diectionary that stores all of the different classes that the data points get put into
            # they are initially empty
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            # find the distance between the point and cluster; choose the nearest centroid
            # for all of the features, calculate the distance from it's features to the centroids features
            for features in data:
                # uses helper method to calculate distance between two dates
                distances = k.dateTimeDistance(features)
                # grabs the index of the centroid that it is closest to, and assigns it to that class
                # adds it to the list for that centroid in the classes dictionary
                classification = distances.index(min(distances))
                self.classes[classification].append(features)

            # holds the current centroids in previous to use later
            previous = dict(self.centroids)

            # average the cluster datapoints to re-calculate the centroids
            for classification in self.classes:
                # iterate through the classes list for each centroid and find the average of all the data points in the class
                # assigns the average as the new centroid

                # break the self.classes[classification] up into 10 parts
                chunksForAverage = list(k.chunks(self.classes[classification], 100))

                # uses helper method to find the average of the dates
                averages = []
                for chunk in chunksForAverage:
                    averages.append(k.dateTimeAverage2(chunk))

                self.centroids[classification] = k.dateTimeAverage2(averages)

            isOptimal = True

            # Loop thorugh new centroids and see if the % change between them and the old ones is less than our self.tolerance
            for centroid in self.centroids:
                original_centroid = previous[centroid]
                curr = self.centroids[centroid]

                days = original_centroid[0].day + (original_centroid[0].month * 30) + (original_centroid[0].year * 356)

                if np.sum((curr[0] - original_centroid[0]) / (
                        timedelta(days=days, hours=original_centroid[0].hour)) * 100) > self.tolerance:
                    isOptimal = False

            # break out of the main loop if the results are optimal, ie. the centroids don't change their positions much(more than our tolerance)
            if isOptimal:
                break

    def plot(self):
        colors = 10 * ["r", "g", "c", "b", "k"]

        for centroid in k.centroids:
            data = k.centroids[centroid]
            for point in data:
                plt.scatter(date(point.year, point.month, point.day), point.hour, s=130, marker="x")
        for classification in k.classes:
            color = colors[classification]
            for features in k.classes[classification]:
                for point in features:
                    plt.scatter(date(point.year, point.month, point.day), point.hour, color=color, s=30)
        plt.show()


if __name__ == "__main__":
    import sys

    # create an instance of the k_means class with default parameters
    k = k_Means()

    # parses the csv using the parseData method
    data = k.parseData(sys.argv[1])

    print("Data is read in")

    # convert the data to datetime style
    data = k.splitData(data)

    print("Data is split")

    # intialize the centriods
    k.initializeCentroids(data)

    print("centroids are initialized")

    # apply the k_means algorithm to the data
    k.km_iterations(data)

    print("working on plotting")

    k.plot()
