__author__ = 'Felipe'
"""
This program takes any given csv file from yahoo finance and
returns the best and worst 6 month period for that company

Only works with yahoo finance for now.

Class: Programming and Algorithms
Teacher: Mark Foley
Student: Felipe Souza Alarcon
ID: D15125433
Course: DT249
"""

import csv

months = ['01','02','03','04','05','06','07','08','09','10','11','12']

def main():
    data = open_file('googlePrices.csv')
    years = extract_years(data)
    ordered_data = ordered_dictionary(data, years)
    first_semester, second_semester = split_by_semester(years, ordered_data)
    semester_result(years, first_semester, second_semester)

def open_file(fl):
    """
    Opens any given csv file from
    yahoo finance and returns a list
    containing the whole information
    """
    data = []
    with open(fl, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            data.append(row)
    f.close()
    return data
    
def extract_years(data):
    """
    Extracts a list of unique years from
    a csv file and returns it
    """
    years = []
    
    for row in data:
        years.append(row['Date'][0:4])
        
    return sorted(set(years))
    
def ordered_dictionary(data, years):
    """
    Takes the data and the list of unique years
    and organizes Adj Close by month into
    dictionary to make access easier later on
    """
    dic  = {}
    for year in years:
        dic[year] = {x:[] for x in months}
        
    for row in data:
        for year in years:
            if(year == row['Date'][0:4]):
                for month in months:
                    if(month == row['Date'][5:7]):
                        dic[year][month].append(float(row['Adj Close']))
    return dic

    
def split_by_semester(years, ordered_data):
    """
    Takes a list of unique years and the
    ordered dictionary created before
    and splits it into chunks of 12
    and returns 2 lists each containing
    6 month period
    """
    first_semester = []
    second_semester= []
    avg  = []
    for year in years:
        for month in months:
            if(ordered_data[year][month] != []):
                avg.append(sum(ordered_data[year][month]) / len(ordered_data[year][month]))
            else:
                avg.append(0.0)
    
    split_list = list(zip(*[iter(avg)]*12))
    
    for item in split_list:
        first_semester.append(sum(item[0:6]))
        second_semester.append(sum(item[6:12]))
        
    return (first_semester, second_semester)

def semester_result(years, first_semester, second_semester):
    """
    This calculates which six month period were
    best and worst and prints it on the screen
    """
    index = int()
    if(max(first_semester) > max(second_semester)):
        index = first_semester.index(max(first_semester))
        print('The best six month period was in the First Semester', years[index])
    if(max(first_semester) < max(second_semester)):
        index = second_semester.index(max(second_semester))
        print('The best six month period was in the Second Semester', years[index])
        
    if(min(x for x in first_semester if x != 0.0) < min(x for x in second_semester if x != 0.0)):
        index = first_semester.index(min(first_semester))
        print('The worst six month period was in the First Semester', years[index])
    if(min(x for x in second_semester if x != 0.0) < min(x for x in first_semester if x != 0.0)):
        index = second_semester.index(min(second_semester))
        print('The worst six month period was in the Second Semester', years[index])
        

if(__name__ == '__main__'):
    main()
