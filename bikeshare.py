import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'C:/Users/sconovalu/Downloads/Python/Bikeshare/chicago.csv',
              'new york city': 'C:/Users/sconovalu/Downloads/Python/Bikeshare/new_york_city.csv',
              'washington': 'C:/Users/sconovalu/Downloads/Python/Bikeshare/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input('Please enter a city: ').lower()

        if city in valid_cities:
            break
        else:
            print('Invalid city. Please try again')

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input('Please enter a month or "all": ').lower()

        if month in valid_months:
            break
        else:
            print('Invalid month. Please try again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input('Please enter a day or "all": ').lower()

        if day in valid_days:
            break
        else:
            print('Invalid day. Please try again')

    print('-'*40)
    return city, month, day

# The following function loads and filters the bikeshare data based on user input
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print('Most common month:', most_common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour:', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('Most common start station:', most_common_start)

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('Most common end station:', most_common_end)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print('Most frequent trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total travel time:', total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Mean travel time:', mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender counts:\n', gender_counts)
    else:
        print('\nGender data not available for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])

        print('\nEartliest birth year:', earliest)
        print('Most recent birth year:', most_recent)
        print('Most common birth year:', most_common)

    else:
        print('\nBirth year data not available for this city')

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

        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()
        start_loc = 0
    
        while show_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            
            if start_loc >= len(df):
                print('No more raw data to display.')
                break

            show_data = input('\nWould you like to see the next 5 lines of raw data? Enter yes or no.\n').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()