def dump(output_file_name, get_data):
    with open(output_file_name, 'w') as f:
        print_header = True
        for e in get_data():
            row_temp = ','.join(['{}',] * len(e)) + '\n'
            if print_header:
                f.write(row_temp.format(*[k for k in e]))
                print_header =  False

            f.write(row_temp.format(*[e[k] for k in e]))
