
import time
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DASH_SEPARATOR_COUNT = 40



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = '';

    while city not in CITY_DATA:
        city = input('\nName of the city to analyze? Chicago, New York City or Washington?\n').lower()

    # get user input for month (all, january, february, ... , june)
    allowed_month = ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = '';

    while month not in allowed_month:
        month = input('\nName of the month to filter by, or "all" to apply no month filter\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    allowed_day = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = '';

    while day not in allowed_day:
        day = input('\nName of the day of week to filter by, or "all" to apply no day filter\n').lower()


    print('-'*DASH_SEPARATOR_COUNT)
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
    df = pd.read_csv('./{}'.format(CITY_DATA[city]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
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
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['Start Time'].dt.month.mode()[0] - 1
    print('Most common month : {}'.format(months[month]))

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print('Most common day of week : {}'.format(day))

    # display the most common start hour
    start_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common common start hour : {}'.format(start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DASH_SEPARATOR_COUNT)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station : {}'.format(top_start_station))


    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station : {}'.format(top_end_station))


    # display most frequent combination of start station and end station trip
    top_trip = (df['Start Station'] + ' --> ' + df['End Station']).mode()[0]
    print('Most frequent combination of start station and end station trip : {}'.format(top_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DASH_SEPARATOR_COUNT)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('Total travel time : {}'.format(total))


    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('Mean travel time : {}'.format(mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DASH_SEPARATOR_COUNT)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts().to_dict()
    print('Counts of user types')
    for u in user_type:
        print('{} : {}'.format(u,user_type[u]))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts().to_dict()
        print('Counts of gender')
        for g in gender:
            print('{} : {}'.format(g,gender[g]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth : {}'.format(df['Birth Year'].min()))
        print('Most recent year of birth : {}'.format(df['Birth Year'].max()))
        print('Most common year of birth : {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DASH_SEPARATOR_COUNT)





def main():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        length = len(df.index)
        n = 0;

        dispay_raw_data = 'yes'
        while dispay_raw_data != 'no' and n < length:
            dispay_raw_data = input('\nDisplay raw data? (Yes/No)\n').lower()
            if dispay_raw_data == 'yes':
                print(df[n:min(n+5,length)])
                n = n+5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
