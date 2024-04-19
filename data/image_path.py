# Read the first column of a csv into a list
import csv
import sys

def read_csv_column(filename, column):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return [row[column] for row in reader]
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: {} filename column'.format(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    column = int(sys.argv[2])
    filepath = read_csv_column(filename, column)
    filepath = [x.split('/')[1] for x in filepath if x]

    csv_file_path = 'submission1.csv'
    with open(csv_file_path, 'w') as csvfile:
        for row in filepath:
            # Convert each element to a string and join them with commas
            # Write the row string to the file
            csvfile.write(str(row) + '\n')