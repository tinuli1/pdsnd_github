# Udacity Porject for Course Python for Data Science
import time
import pandas as pd
import numpy as np

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
    availablecities=['washington', 'new york city', 'chicago']
    while True:     
        city=input('Which city do you want to explore (chicago, new york city or washington)?')
        city=city.lower()
        if city in availablecities:
            break
        else:
            print('Ooooops sth. went wrong please retry entering the city you want to explore (chicago, new york city or washington)')

    # get user input for month (all, january, february, ... , june)
    availablemonth=['all','january','february', 'march', 'april', 'may', 'june']
    while True:
        month=input('Which month do you want to explore? Please enter all or january, february, ..., june')
        month=month.lower()
        if month in availablemonth:
            break
        else:
            print('Ooooops sth. went wrong. Please retry enterying the month you want to explore(all, january, ..., june)')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    availableday=['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day=input('Please enter day of week you want to explore (all, monday,...)')
        day=day.lower()
        if day in availableday:
            break
        else: 
            print('Oooops sth. went wrong. Please retry entering the day you want to explore (all, monday, ..., sunday)')

    print('-'*40)
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
    ##Load Data for selected city into dataframe
    df=pd.read_csv(CITY_DATA[city])

    ##converte start time to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])

    ##Create new columns month and day
    df['month']=df['Start Time'].dt.month
    df['day']=df['Start Time'].dt.weekday

    ##filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        ##new dataframe with all months
        df = df[df['month'] == month]
    
    ##filter by day
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)

        ##new dataframe with all days
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    ## dictionary to map output
    pop_month_dict = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6:'june'}
    # display the most common month
    ##find moth popular month
    popular_month = df['month'].mode()[0]
    ##print user info 
    print('Most common month within selected data is:', pop_month_dict[popular_month])

    # display the most common day of week
    ## dictionary to map output
    pop_weekday_dict = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6:'sunday'}
    ## find most common day of week
    popular_weekday = df['day'].mode()[0]
    ##print user info
    print('Most common weekday within selected data is:', pop_weekday_dict[popular_weekday])

    # display the most common start hour
    ##extract hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour
    ##find most popular hour
    popular_hour = df['hour'].mode()[0]
    ##print user info
    print('Most popular start hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    ##find most popular start station
    popular_start_station = df['Start Station'].mode()[0]
    ##print user info
    print('Most common start station within selected data is:', popular_start_station)


    # display most commonly used end station
    ##find most popular end station
    popular_end_station = df['End Station'].mode()[0]
    ##print user info
    print('Most common end station within selected data is:', popular_end_station)

    # display most frequent combination of start station and end station trip
    ##create new column with combination of start and end station
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    ##find most popular trip
    popular_trip = df['trip'].mode()[0]
    ## print user info
    print('Most common trip within selected data:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ##converte end time to datetime
    df['End Time']=pd.to_datetime(df['End Time'])
    ## create new column for travel time for each trip
    df['Travel Time']=pd.to_timedelta(df['End Time'] - df['Start Time'])
    ## calculate total travel time over all data
    total_travel_time=df['Travel Time'].sum()
    ## print user info
    print('Total travel time for all selected data:', total_travel_time)


    # display mean travel time
    ## calculate mean travel time over all data
    mean_travel_time=df['Travel Time'].mean()
    ## print user info
    print('Mean travel time for all selected data:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("counts of user types for selected data:\n", user_types)


    ## try-loop to handle that there is no data for Washington DC
    try:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("counts of customer gender:\n", gender)
        # Display earliest, most recent, and most common year of birth
        ## find most common birth year
        common_age = df['Birth Year'].mode()[0]
        ##find oldes users birth year
        oldest_users = df['Birth Year'].min()
        ##find youngest users birth year
        youngest_users = df['Birth Year'].max()
        print("\nmost common user birth year:", common_age, "\nbirthyear of youngest users:", youngest_users, "\nbirth year of oldest users:", oldest_users)

    except:
        print("\n \nWarning: no gender and birth year data available for the selected dataset")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to see raw data (first 5 lines)? Enter yes or no.\n')
        i=0
        while raw_data == 'yes' and i < len(df):
            if i < (len(df) - 5):    
                print(df.iloc[i:(i+5)])
                i+=5
                raw_data = input('\nWould you like to see more raw data (+ 5 lines)? Enter yes or no.\n')
            else:
                print(df.iloc[i:])
                i+=5
                
        # print('no (more) data will be printed.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
