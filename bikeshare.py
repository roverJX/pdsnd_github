import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington?')
    while city.title() not in ('Chicago','New York City','Washington'):
        print('Please enter valid city name - Chicago, New York City, or Washington')
        city = input('Would you like to see data for Chicago, New York, or Washington?')
    # get user input for month (all, january, february, ... , june)
    monthorday = input('Would you like to filter the data by month, day, both, or not at all? Type none if no filter')
    while monthorday.lower() not in ('month','day','both','none'):
        print('Please enter valid filter name - month, day, both, or none')
        monthorday = input('Would you like to filter the data by month, day, both, or not at all? Type none if no filter')
    if monthorday == 'month':
        month = input('Which month - January, February, March, April, May, or June?')
        while month.title() not in ('January', 'February', 'March', 'April', 'May', 'June'):
            print('Please enter valid month name - January, February, March, April, May, or June')
            month = input('Which month - January, February, March, April, May, or June?')
        day = 'all'
    elif monthorday == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        month = 'all'
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
        while day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            print('Please enter valid weekday name - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday')
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
    elif monthorday == 'both':
        month = input('Which month - January, February, March, April, May, or June?')
        while month.title() not in ('January', 'February', 'March', 'April', 'May', 'June'):
            print('Please enter valid month name - January, February, March, April, May, or June')
            month = input('Which month - January, February, March, April, May, or June?')
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
        while day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            print('Please enter valid weekday name - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday')
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
    elif monthorday == 'none':
        month = 'all'
        day = 'all'
    print('-'*40)
    print('\nYour filter is: {}, {}, {}'.format(city,month,day))
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def special_cases(df,output_str,station = False):
    """
    Check and print result based on the number of max frequent in a given series

    Args:
        (list/series) - the column of the dataframe to analyze
        (str) - output string to be inserted after 'The most common '
        (bool) - True if the input is station_stats,
                 False otherwise
    """
    freq_count = df.value_counts()
    max_freq = freq_count[freq_count==freq_count.max()]
    if not station:
        if len(max_freq) == 1:
            print('The most common {}: {}\n'.format(output_str,int(max_freq.index[0])))
            print('Count: {}\n'.format(freq_count.max()))
        else:
            print('The most common' + output_str + ' : %s' % ', '.join([str(element) for element in max_freq.index]))
            print('Count: {}\n'.format(freq_count.max()))
    else:
        if len(max_freq) == 1:
            print('The most commonly used {}:\n{}'.format(output_str,max_freq.index[0]))
            print('Count: {}\n'.format(freq_count.max()))
        else:
            print('The most commonly used {}:\n'.format(output_str))
            print(*max_freq.index,sep='\n')
            print('Count: {}\n'.format(freq_count.max()))

def time_stats(df):
    #Displays statistics on the most frequent times of travel

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Display the most common month

    if len(df['month'].unique()) != 1:
        special_cases(df['month'],'month',False)

    #display the most common day of week

    if len(df['day_of_week'].unique()) != 1:
        special_cases(df['day_of_week'],'day of week',False)

    #display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    special_cases(df['hour'],'start hour',False)

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def station_stats(df):
    #Displays statistics on the most popular stations and trip
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    special_cases(df['Start Station'],'start station',True)

    #display most commonly used end station
    special_cases(df['End Station'],'end station',True)

    #display most frequent combination of start station and end station trip
    df['Start To End Station'] = df['Start Station'] + ' - ' + df['End Station']
    special_cases(df['Start To End Station'],'combination',True)

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time: {}\n'.format(str(dt.timedelta(seconds=int(df['Trip Duration'].sum())))))

    # display mean travel time
    print('The mean travel time: {}\n'.format(str(dt.timedelta(seconds=int(df['Trip Duration'].mean())))))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def user_stats(df):
    #Displays statistics on bikeshare users
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('Counts of user types:\n{}'.format(df['User Type'].value_counts().to_string()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender:\n{}'.format(df['Gender'].value_counts().to_string()))
    else:
        print('\nNo Gender data to share')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('\nThe most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        special_cases(df['Birth Year'],'year of birth',False)
    else:
        print('\nNo birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def check_raw_data(df):
    """
    Check if user wants to see 5 rows of data
    """
    step = 0
    check = input('Would you like to see 5 lines of raw data?(Y/N)')
    while check.upper() not in ('Y','N'):
        print('Please enter Y/N')
        check = input('Would you like to see 5 lines of raw data?')
    while check.upper() == 'Y':
        print(df.iloc[step:step+5,:])
        check = input('Would you like to see 5 more lines?(Y/N)')
        step += 5
        if check.upper() != 'Y':
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        check_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
