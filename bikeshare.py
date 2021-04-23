import time
import pandas as pd
import numpy as np

CITY_DATA = { 
  'chicago': 'chicago.csv',
  'new york city': 'new_york_city.csv',
  'washington': 'washington.csv'
}
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
  """
  Asks user to specify a city, month, and day to analyze.

  Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
  """

  print("Hello! Let's explore some US bikeshare data!")

  while True:
    city = input('Type city: ')
    if city.lower() in CITY_DATA:
      city = city.lower()
      break
    else:
      print("\nYou have typed an invalid city. Please type one of 'chicago', 'new york city' or 'washington'\n")

  while True:
    month = input('Type month: ')
    if month.lower() in months:
      month = month.lower()
      break
    else:
      print("\nYou have typed an invalid month. Please type one of 'january', 'february', 'march', 'april', 'may', 'june' or 'all'\n")

  while True:
    day = input('Type day: ')
    if day.lower() in days:
      day = day.lower()
      break
    else:
      print("\nYou have typed an invalid day. Please type one of 'sunday', 'monday', 'tueday', 'wednesday', 'thursday', 'friday', 'saturday' or 'all'\n")

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

  df = pd.read_csv(CITY_DATA[city], index_col=[0])

  # convert the Start Time column to datetime
  df['Start Time'] = pd.to_datetime(df['Start Time'])

  # extract month and day of week from Start Time to create new columns
  df['Month'] = df['Start Time'].dt.month
  df['Day of Week'] = df['Start Time'].dt.weekday_name

  # filter by month if applicable
  if month != 'all':
    # use the index of the months list to get the corresponding int
    month_index = months.index(month) + 1

    # filter by month to create the new dataframe
    df = df.loc[df['Month'] == month_index]

  # filter by day of week if applicable
  if day != 'all':
    # filter by day of week to create the new dataframe
    df = df.loc[df['Day of Week'] == day.title()]

  return df


def time_stats(df):
  """Displays statistics on the most frequent times of travel."""

  print('\nCalculating The Most Frequent Times of Travel...\n')
  start_time = time.time()

  most_common_month = months[df['Month'].mode()[0] - 1]
  print('Most common month: {}\n'.format(most_common_month.title()))

  most_common_day = df['Day of Week'].mode()[0]
  print('Most common day of the week: {}\n'.format(most_common_day))

  most_common_hour = df['Start Time'].dt.hour.mode()[0]
  print('Most common start hour: {}\n'.format(most_common_hour))

  print('\nThis took %s seconds.' % (time.time() - start_time))
  print('-'*40)


def station_stats(df):
  """Displays statistics on the most popular stations and trip."""

  print('\nCalculating The Most Popular Stations and Trip...\n')
  start_time = time.time()

  most_common_start_station = df['Start Station'].mode()[0]
  print('Most commonly used start station: {}\n'.format(most_common_start_station))

  most_common_end_station = df['End Station'].mode()[0]
  print('Most commonly used end station: {}\n'.format(most_common_end_station))

  most_common_combination_stations = df.groupby(['End Station','Start Station']).size().idxmax()
  print('Most frequent combination of start and end stations respectively: {}\n'.format(most_common_combination_stations))
  
  print('\nThis took %s seconds.' % (time.time() - start_time))
  print('-'*40)


def trip_duration_stats(df):
  """Displays statistics on the total and average trip duration."""

  print('\nCalculating Trip Duration...\n')
  start_time = time.time()

  total_travel_time = df['Trip Duration'].sum()
  print('Total travel time: {}\n'.format(total_travel_time))

  mean_travel_time = df['Trip Duration'].mean()
  print('Average travel time: {}\n'.format(mean_travel_time))

  print('\nThis took %s seconds.' % (time.time() - start_time))
  print('-'*40)


def user_stats(df):
  """Displays statistics on bikeshare users."""

  print('\nCalculating User Stats...\n')
  start_time = time.time()

  user_types = df['User Type'].value_counts()
  print('Counts of user types:\n{}\n'.format(user_types.to_string()))

  try:
    gender = df['Gender'].value_counts()
    print('Counts of gender:\n{}\n'.format(gender.to_string()))
  except KeyError:
    print('No gender data available for Washington\n')

  try:
    earliest_year_of_birth = df['Birth Year'].min()
    print('Earliest year of birth: {}\n'.format(earliest_year_of_birth))
    most_recent_year_of_birth = df['Birth Year'].max()
    print('Most recent year of birth: {}\n'.format(most_recent_year_of_birth))
    most_common_year_of_birth = df['Birth Year'].mode()[0]
    print('Most common year of birth: {}\n'.format(most_common_year_of_birth))
  except KeyError:
    print('No year of birth data available for Washington\n')

  print('\nThis took %s seconds.' % (time.time() - start_time))
  print('-'*40)

def view_raw_data(df):
  """Displays 5 rows of raw data of bikeshare users at a time based on filter results."""
  rows = 0
  NUMBER_OF_ROWS_OF_DATA = 5
  while True:
    view_data = input("\nWould you like to see the raw data? Enter 'yes' or 'no'.\n")
    if view_data.lower() == 'yes':
      if (rows >= df.shape[0]):
        print('\nNo more data to display')
        break
      
      current_five_rows_of_data = df.iloc[rows: rows + NUMBER_OF_ROWS_OF_DATA]
      
      start_time = time.time()
      print('Printing five rows of raw data:\n{}\n'.format(current_five_rows_of_data))
      rows += NUMBER_OF_ROWS_OF_DATA
      
      print('\nThis took %s seconds.' % (time.time() - start_time))
      print('-'*40)

    else: break
            

def main():
  while True:
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    view_raw_data(df)
    restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
    if restart.lower() != 'yes':
      break


if __name__ == '__main__':
	main()
