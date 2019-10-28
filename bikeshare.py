import time
import calendar
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

    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington\n").lower()
        if city in ('chicago','new york city','washington'):
            break
        else:
            print('Check for typos and re-enter a valid city name')

    # get user input for month (all, january, february, ... , june)
    # Add lower function  to accept lower case months
    while True:
        month = input("Enter the month- January, February, March, April, May, June or all?\n ").lower()
        if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            break
        else:
            print("Check for typos and re-enter a valid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # Add lower function to accept lower case days
    while True:
        day = input("Enter the day- Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday or all?\n ").lower()
        if day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            break
        else:
            print("Check for typos and re-enter a valid day")

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
    df = pd.read_csv(CITY_DATA[city])
    #Convert start time into date time and get the month & day_of_week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    most_common_month = df['month'].mode()[0]
    print('Most common month: ', calendar.month_name[most_common_month])

    # display the most common day of week

    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day: ', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip
    start_end_station = df[['Start Station','End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station:\n', start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time in seconds:\n", total_travel_time)

    #using divmod() function to convert seconds into hour(h), minutes(m) and seconds(s)
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)
    print("Total travel time is {} hours {} minutes and {} seconds".format(h,m,s))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time in seconds:\n", mean_travel_time)

    #using divmod() function to convert seconds into hour(h), minutes(m) and seconds(s)
    m, s = divmod(mean_travel_time, 60)
    h, m = divmod(m, 60)
    print("Mean travel time is {} hours {} minutes and {} seconds".format(h,m,s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("User Type      Counts \n", user_type)

    # Display counts of gender
    # Handle Key errors for ceratin city/month combinations
    try:
        gender_type = df['Gender'].value_counts()
        print("Gender Type Counts \n", gender_type)
    except KeyError:
        print("No gender data available for this city and month ")

    # Display earliest, most recent, and most common year of birth
    # Convert Birth Year to int to avoid displaying decimal sign in the display
    # Handle Key errors for ceratin city/month combinations
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        print("Earliest birth year:", earliest_birth_year)
    except KeyError:
        print("Earliest birth year: No data available for this city and month/s ")

    try:
        most_recent_birth_year = int(df['Birth Year'].max())
        print("Most recent birth year:", most_recent_birth_year)
    except KeyError:
        print("Most recent birth year: No data available for this city and month/s ")

    try:
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("Most common birth year:", most_common_birth_year)
    except KeyError:
        print("Most common birth year: No data available for this city and month/s ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 rows of raw data everytime user enters yes """
    raw_data_input = input('Do you want to see raw data? Enter yes or no.\n')
    line_num = 0

    while True:
        if raw_data_input.lower() == 'yes':
            print(df.iloc[line_num : line_num + 5])
            line_num += 5
            raw_data_input = input('Do you want to see 5 more rows of raw data? Enter yes or no.\n')
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
