from tempfile import NamedTemporaryFile
import shutil
import csv
import argparse


def parse():
    ap = argparse.ArgumentParser('Choose csv to amend:')
    ap.add_argument(
        'csv_f',
        metavar="csv_file",
        help='csv_file to amend')

    ap.add_argument(
        'model',
        metavar="model_name",
        help='model name to add to csv')
    args = ap.parse_args()
    return args


def append_column(filename, tempfile, model, overwrite=True):
    with open(filename, 'r') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        # returns the headers or `None` if the input is empty
        headers = next(reader)
        headers.append('Model')
        if headers:
            writer.writerow(headers)

        for row in reader:
            row.append(model)
            writer.writerow(row)

    if overwrite:
        shutil.move(tempfile.name, filename)


if __name__ == '__main__':
    args = parse()

    filename = args.csv_f
    model = args.model
    tempfile = NamedTemporaryFile(delete=False, mode='w+')
    print("Writing to tempfile {}".format(tempfile.name))
    append_column(filename, tempfile, model)
