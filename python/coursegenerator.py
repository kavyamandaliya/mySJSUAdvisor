import courseparser
import course_structures
import numpy as np
import pandas as pd

# binary search and basic scheduler as defined by https://www.geeksforgeeks.org/weighted-job-scheduling-log-n-time/
# classes are defined in total start time since Monday with Monday 12:00 am being 0 time and Sunday 11:59 pm being the latest time

def binarySearch(job, start_index):
    #
    # Initialize 'lo' and 'hi' for Binary Search
    lo = 0
    hi = start_index - 1

    # Perform binary Search iteratively
    while lo <= hi:
        mid = (lo + hi) // 2
        if job[mid].finish <= job[start_index].start:
            if job[mid + 1].finish <= job[start_index].start:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1
# The main function that returns the maximum possible
# profit from given array of jobs
def schedule(job):
    # Sort jobs according to finish time
    job = sorted(job, key=lambda j: j.finish)

    # Create an array to store solutions of subproblems.  table[i]
    # stores the profit for jobs till arr[i] (including arr[i])
    n = len(job)
    table = [0 for _ in range(n)]

    table[0] = job[0].profit;

    # Fill entries in table[] using recursive property
    for i in range(1, n):

        # Find profit including the current job
        inclProf = job[i].profit
        l = binarySearch(job, i)
        if (l != -1):
            inclProf += table[l];

            # Store maximum of including and excluding
        table[i] = max(inclProf, table[i - 1])

    return table[n - 1]

def getSections(df, dept, classNum):
    dept_df = df[df['Dept'] == dept]
    rslt_df = dept_df[dept_df['ClassNum'] == classNum]
    return rslt_df

def genSchedules(df, classTargs):
    """
    :param classTargs: list of tuples (Dept, classNum) which we should generate schedules with
    :return: collection of schedules
    """
    sectionsList = []

    for classTarg in classTargs:
        x, y = classTarg
        sectionsList.append(getSections(df, x, y))
    startDF, *remainingDf = sectionsList # seperate first dataframe from rest
    for secDF in remainingDf:
        startDF = pd.merge(startDF, secDF, how='outer')
    return startDF

def main():
    semester = course_structures.Semester(True)
    classTargets = [("CS", "161"), ("CS", "160"), ("CS", "154")]
    targets = genSchedules(semester.df1, classTargets)
    print(targets)

if __name__ == "__main__":
    main()
