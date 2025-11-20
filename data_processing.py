import csv

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

    def join(self, other_table, key):
        """Join two tables using a common key"""
        joined_rows = []

        for row1 in self.data:
            for row2 in other_table.data:
                if row1[key] == row2[key]:
                    merged = row1.copy()
                    merged.update(row2)
                    joined_rows.append(merged)

        return Table(joined_rows)


class DB:
    def __init__(self):
        self.tables = {}

    def insert(self, name, table):
        self.tables[name] = table

    def search(self, name):
        return self.tables.get(name, None)


if __name__ == "__main__":
    db = DB()

    cities_loader = DataLoader("Cities.csv")
    countries_loader = DataLoader("Countries.csv")

    cities_table = cities_loader.load()
    countries_table = countries_loader.load()

    db.insert("cities", cities_table)
    db.insert("countries", countries_table)

    cities = db.search("cities")
    countries = db.search("countries")

    print("List all cities in Italy:")
    cities_filtered = cities.filter(lambda r: r['country'] == 'Italy')
    print("cities_filtered:" + str(cities_filtered.data))
    print()

    print("Average temperature for all cities in Italy:")
    print(cities_filtered.aggregate('temperature', lambda x: sum(x)/len(x)))
    print()

    print("List all non-EU countries:")
    countries_filtered = countries.filter(lambda r: r['EU'] == 'no')
    print("countries_filtered:" + str(countries_filtered.data))
    print()

    print("Number of countries that have coastline:")
    coastline_count = len(countries.filter(lambda r: r['coastline'] == 'yes').data)
    print(coastline_count)
    print()

    print("First 5 entries of the joined table (cities and countries):")
    joined = cities.join(countries, "country")
    for row in joined.data[:5]:
        print(row)
    print()

    print("Cities whose temperatures are below 5.0 in non-EU countries:")
    non_eu = joined.filter(lambda r: r['EU'] == 'no')
    cold_non_eu = non_eu.filter(lambda r: float(r['temperature']) < 5.0)
    print(cold_non_eu.data)
    print()

    print("The min and max temperatures for cities in EU countries that do not have coastlines")
    eu_no_coast = joined.filter(lambda r: r['EU'] == 'yes' and r['coastline'] == 'no')
    temps = [float(r['temperature']) for r in eu_no_coast.data]

    print("Min temp:", min(temps))
    print("Max temp:", max(temps))