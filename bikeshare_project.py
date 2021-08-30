import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
cities = list(CITY_DATA.keys())
months = ['jan', 'feb', 'mar', 'apr', 'may', 'june','all']
days = ['sun','mon','tue','wed','thu','friday','saturday','all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    while city not in CITY_DATA.keys():
        print("Please choose your city:\n1. Chicago 2. New York City 3. Washington")

        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nPlease check your input, it must be within this list: ", cities)
            print("\nRestarting...")


    MONTH_DATA = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, it must be within this list: ", months)

        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid input, it must be within this list: ", months)
            print("\nRestarting...")


    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week, it must be within this list: ", days)

        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input, it must be within this list: ", days)
            print("\nRestarting...")


    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()

    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month =  month.index(month) + 1
        df = df[ df['month'] == month]

    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # To display the most common month
    common_month = df['month'].mode()[0]
    print('Most Popular Month:', common_month)

    # To display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Day Of Week:', common_day_of_week)

    # TO display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # To display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('most commonly used start station:', common_start_station)

    # To display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('most commonly used end station:',  common_end_station)

    # TO display most frequent combination of start station and end station trip (Reference: GitHub)
    group_of_start_end = df.groupby(['Start Station', 'End Station'])
    common_combination_station = group_of_start_end.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', common_combination_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # To display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # To display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # To display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Counts of user type:', user_type_counts)

    # TO display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender: ', gender_counts)
    # Only access Gender column in this case
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')


    # To display earliest year of birth
    if 'Birth Year' in df:
        #To display most recent year of birth
        recent_year = df['Birth Year'].max()
        print('Most Recent Year:', recent_year)

        #To display most common year of birth
        common_year = df['Birth Year'].mode()[0]
        print('Most Common Year:', common_year)

        earliest_year = df['Birth Year'].min()
        print('Earliest Year:', earliest_year)

    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    raw = 0
    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
        if view_data == 'yes':
            raw += 5
            print(df.iloc[raw : raw + 5])

            again = input("Do you want to see more? Yes or No").lower()
            if again == 'no':
                break
        elif view_data == 'no':
            break

    return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
