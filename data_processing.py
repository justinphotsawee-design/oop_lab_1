import csv, os

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        data = []
        with open(self.filepath, newline='', encoding='utf-8') as f:
            rows = csv.DictReader(f)
            for row in rows:
                data.append(dict(row))
        return Table(data)

class Table:
    def __init__(self, data):
        self.data = data

    def filter(self, condition):
        """Return a new Table with rows that satisfy the condition"""
        filtered = [row for row in self.data if condition(row)]
        return Table(filtered)

    def aggregate(self, key, agg_func):
        """Apply an aggregation function to a column"""
        values = [float(row[key]) for row in self.data]
        return agg_func(values)

    def unique(self, key):
        """Return unique values from a column"""
        return set(row[key] for row in self.data)

if __name__ == "__main__":
    # Load data
    loader = DataLoader('Cities.csv')
    table = loader.load()

    # Average temperature of all cities
    print("Average temperature of all cities:")
    print(table.aggregate('temperature', lambda x: sum(x)/len(x)))
    print()

    # All cities in Germany
    print("All cities in Germany:")
    germany = table.filter(lambda r: r['country'] == 'Germany')
    for city in germany.data:
        print(city['city'])
    print()

    # All cities in Spain with temperature above 12°C
    print("All cities in Spain with temperature above 12°C:")
    spain_hot = table.filter(lambda r: r['country'] == 'Spain' and float(r['temperature']) > 12)
    for city in spain_hot.data:
        print(city['city'])
    print()

    # Number of unique countries
    print("Number of unique countries:")
    print(len(table.unique('country')))
    print()

    # Average temperature for Germany
    print("Average temperature for cities in Germany:")
    print(germany.aggregate('temperature', lambda x: sum(x)/len(x)))
    print()

    # Max temperature for Italy
    print("Max temperature for cities in Italy:")
    italy = table.filter(lambda r: r['country'] == 'Italy')
    print(italy.aggregate('temperature', max))
    print()
