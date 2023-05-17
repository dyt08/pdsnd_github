import time
import pandas as pd
import numpy as np
from tabulate import tabulate


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
        city = input("\nWhich city would you like to see? Type 'show' for a list of cities.\n").lower()
        if city == 'show':
            print(', '.join([city.title() for city in CITY_DATA.keys()]))
        elif city in CITY_DATA.keys():
            break
        else:
            print('City not found, please try again.')

    filters = ['month', 'day', 'both', 'none']
    while True:
        which_filter = input("\nWould you like to filter data by month, day, both, or not at all? Type 'none' for no filter.\n").lower()
        month = 'all'
        day = 'all'
        if (which_filter in filters) and (which_filter != 'none'):
            if (which_filter == 'both') or (which_filter == 'month'):
                # get user input for month (all, january, february, ... , june)
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                while True:
                    month = input("\nWhich month? Type 'show' for a list of months.\n").lower()
                    if month == 'show':
                        print('You can type your response as an integer or as a day name (e.g. 1 or January)')
                        print(', '.join([str(no+1)+' - '+month.title() for no, month in enumerate(months)]))
                    elif month in months:
                        month = months.index(month)+1
                        break
                    elif month in [str(x) for x in range(1,len(months)+1)]:
                        month = int(month)
                        break
                    else:
                        print('Month not found, please try again.')
            if (which_filter == 'both') or (which_filter == 'day'):
                # get user input for day of week (all, monday, tuesday, ... sunday)
                days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday']
                while True:
                    day = input("\nWhich day? Type 'show' for a list of days.\n").lower()
                    if day == 'show':
                        print('You can type your response as an integer or as a day name (e.g. 1 or Sunday)')
                        print(', '.join([str(no+1)+' - '+city.title() for no, city in enumerate(days)]))
                    elif day in days:
                        day = days.index(day)+1
                        break
                    elif day in [str(x) for x in range(1,len(days)+1)]:
                        day = int(day)
                        break
                    else:
                        print('Day not found, please try again.')
            break
        elif which_filter == 'none':
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df.rename(columns = {'Unnamed: 0':'id'}, inplace = True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = ((df['Start Time'].dt.weekday+1)%7)+1 # weekday to isoweekday > sunday to 0 > sunday to 1
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':        
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    # display the first/next 5 data using tabulate
    i=0
    while True:
        display_data = input("\nWould you like to see the first/next 5 data? Type 'yes' or 'no'.\n").lower()
        if display_data != 'yes':
            break
        print(tabulate(df.iloc[np.arange(i,i+5)], headers ="keys"))
        i+=5

    # display the first/next 5 data using for loop and iterrows() (slower)
    # for n in range(0,len(df),5):
    #     display_data = input('\nWould you like to see the first/next 5 data? Type 'yes' or 'no'.\n').lower()
    #     if display_data == 'yes':
    #         for index, row in df[n:n+5].iterrows():
    #             print('-'*45)
    #             print(row.to_string())
    #     else:
    #         break
    
    print('-'*40)
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"Most common month: {df['month'].value_counts().idxmax()} (Count: {df['month'].value_counts().max()})")

    # display the most common day of week
    print(f"Most common day of week: {df['day_of_week'].value_counts().idxmax()} (Count: {df['day_of_week'].value_counts().max()})")

    # display the most common start hour
    print(f"Most common start hour: {df['hour'].value_counts().idxmax()} (Count: {df['hour'].value_counts().max()})")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most commonly used start station: {df['Start Station'].value_counts().idxmax()} (Count: {df['Start Station'].value_counts().max()})")

    # display most commonly used end station
    print(f"Most commonly used end station: {df['End Station'].value_counts().idxmax()} (Count: {df['End Station'].value_counts().max()})")

    # display most frequent combination of start station and end station trip
    start_end_station_idxmax = df[['Start Station', 'End Station']].value_counts().idxmax()
    print(f"\nMost frequent combination station trip:\nStart station\t{start_end_station_idxmax[0]}\nEnd station\t{start_end_station_idxmax[1]}\nCount\t\t{df[['Start Station', 'End Station']].value_counts().max()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"Total travel time in seconds: {np.sum(df['Trip Duration'])}")

    # display mean travel time
    print(f"Avg travel time in seconds: {np.mean(df['Trip Duration'])}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of user types: \n{df['User Type'].value_counts().to_string()}\n")

    # Display counts of gender
    try:
        print(f"Counts of user types: \n{df['Gender'].value_counts().to_string()}\n")
    except KeyError:
        print('Gender stats unavailable.')
    except Exception as e:
        print(e)
        
    # Display earliest, most recent, and most common year of birth
    try:
        birth = {'Earliest': int(np.min(df['Birth Year'])),
                'Most recent': int(np.max(df['Birth Year'])),
                'Most common': int(df['Birth Year'].mode())}
        print('Earliest, most recent, and most common year of birth:')
        print(pd.Series(birth, index=birth.keys()).to_string())
    except KeyError:
        print('Birth year stats unavailable.')
    except Exception as e:
        print(e)

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
