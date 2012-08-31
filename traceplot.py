#!/usr/bin/python
#File name: traceplot.py
#Desc: Python script for parsing FPLC data and plotting the chromatograms with matplotlib

import optparse, csv, sys, os, logging
import matplotlib.pyplot

logging.basicConfig(level=logging.DEBUG)

def setup_command_line_parser():
    """Runs optparse to parse the command line args"""
    Usage = "usage: python traceplot.py data_file"
    Parser = optparse.OptionParser(Usage)
    Parser.add_option('--linewidth', dest = 'linewidth', type = 'float',
        default = 2.5,
        help = "Set line width of plotted curves")
    Parser.add_option('--SEC', dest = 'SEC_data_file',
        action = 'store_true',
        default = False,
        help = "Plot the data as size exclusion data")
    (CmdLineOps, Args) = Parser.parse_args()
    if len(Args) == 0:
        logging.error(Usage)
        sys.exit(1)
    else:
        logging.debug("OptParse recieved %g command line arguments" % len(Args))
    return (CmdLineOps, Args)

def check_file_names(file_names):
    for name in file_names:
        if type(name) != str:
            logging.warning("check_file_names: recieved non-string input")
            continue
        if not os.path.isfile(name):
            logging.warning("check_file_names: input file \"%s\" not found!" % name)
    logging.debug("check_file_names: completed successfully")
    return

def parse_data_file(data_file_name):
    """Parses chromatogram data file and returns columns"""
    logging.debug("parse_file_data: recieved file name \"%s\" for parsing" % data_file_name)
    with open(data_file_name, 'r') as data_file:
        data_reader = csv.reader(data_file, delimiter = '\t')
        [data_reader.next() for i in range(2)]
        Curves = [[] for _ in range(len(data_reader.next()))]
        for row in data_reader:
            for i in range(0,len(row)/2):
                if '' not in (row[2*i].strip(), row[2*i+1].strip()):
                    Curves[i].append((float(row[2*i]), float(row[2*i+1])))
    return Curves

def xy_values(curve):
    """Convert (x,y) points to two lists of x values and y values"""
    x_values = [point[0] for point in curve]
    y_values = [point[1] for point in curve]
    return x_values, y_values

def plot_curve(curve, linewidth = None):
    x_values, y_values = xy_values(curve)
    if linewidth:
        matplotlib.pyplot.plot(x_values, y_values, linewidth = linewidth)
    else:
        matplotlib.pyplot.plot(x_values, y_values)
    return

def plot_all_curves(Curves, linewidth = None):
    for curve in Curves:
        plot_curve(curve, linewidth)
    return

def plot_SEC(Curves, linewidth = None):
    plot_all_curves(Curves, linewidth)
    matplotlib.pyplot.xlabel('Elution volume (ml)')
    matplotlib.pyplot.ylabel('mAU')
    return

def main():
    """All just testing code at the moment"""
    (CmdLineOps, Args) = setup_command_line_parser()
    check_file_names(Args)
    data_file_name = Args[0]
    Curves = parse_data_file(data_file_name)

    if CmdLineOps.SEC_data_file:
        plot_SEC(Curves, linewidth = CmdLineOps.linewidth)

    matplotlib.pyplot.show()

if __name__ == '__main__':
    main()
