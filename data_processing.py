import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))


# Define filter function
def filter(condition, dict_list):
    """Return a filtered list where condition(item) is True"""
    return [item for item in dict_list if condition(item)]


# Define aggregation function
def aggregate(aggregation_key, aggregation_function, dict_list):
    """Apply aggregation_function to the list of values from aggregation_key"""
    values = [float(item[aggregation_key]) for item in dict_list]
    return aggregation_function(values)

# Print the average temperature of all the cities
print("The average temperature of all the cities:")
avg_temp = aggregate('temperature', lambda x: sum(x) / len(x), cities)
print(avg_temp)
print()

# Print all cities in Germany
print("All cities in Germany:")
germany_cities = filter(lambda c: c['country'] == 'Germany', cities)
for city in germany_cities:
    print(city['city'])
print()

# Print all cities in Spain with a temperature above 12°C
print("All cities in Spain with temperature above 12°C:")
spain_hot = filter(lambda c: c['country'] == 'Spain' and float(c['temperature']) > 12, cities)
for city in spain_hot:
    print(city['city'])
print()

# Count the number of unique countries
print("Number of unique countries:")
countries = set([c['country'] for c in cities])
print(len(countries))
print()

# Print the average temperature for all the cities in Germany
print("Average temperature for cities in Germany:")
avg_germany = aggregate('temperature', lambda x: sum(x) / len(x), germany_cities)
print(avg_germany)
print()

# Print the max temperature for all the cities in Italy
print("Max temperature for cities in Italy:")
italy_cities = filter(lambda c: c['country'] == 'Italy', cities)
max_temp_italy = aggregate('temperature', lambda x: max(x), italy_cities)
print(max_temp_italy)
print()
