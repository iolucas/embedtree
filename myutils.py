import csv

def save_csv(file_name, header, data_list):
    """ Save data to csv file. """

    _file = open(file_name, 'wt')
    try:
        _file.write("sep=,\n")
        writer = csv.writer(_file, lineterminator="\n", delimiter=",")
        writer.writerow(header)
        for data in data_list:
            writer.writerow(data)
    finally:
        _file.close()

def open_csv(filename):
    """Open data from csv file."""

    data_read = list()

    with open(filename, 'rb') as csvfile:
        csv.reader(csvfile)
        for row in csv.reader(csvfile):
            data_read.append(row)
    
    return data_read



def join_dicts(*iterables):
    joined_dicts = dict()

    for i, d in enumerate(iterables):

        for k, v in d.iteritems():
            if not joined_dicts.has_key(k):
                joined_dicts[k] = list()

            while len(joined_dicts[k]) < i:
                joined_dicts[k].append(0)

            joined_dicts[k].append(v)

    return joined_dicts