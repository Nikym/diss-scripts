import argparse
import os, sys

def parse_args():
    parser = argparse.ArgumentParser(description='Extract error graphs from log files')
  
    parser.add_argument('--log', dest='log_file', help='Path to log file', default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

def get_points(line) -> tuple:
    line_arr = line.split(',')

    loss = float(line_arr[1][7:])
    loss_cls = float(line_arr[2][11:])
    loss_vertex = float(line_arr[3][14:])
    loss_pose = float(line_arr[4][12:])

    return (loss, loss_cls, loss_vertex, loss_pose)

def get_point_list(f) -> list:
    points = []
    while True:
        line = f.readline()

        if not line:
            break

        if line[:4] == 'iter':
            points.append(get_points(line))
    return points

def create_csv(points: list):
    with open('/home/nikita/diss/scripts/outputs/log_points.csv', 'w') as f:
        f.write('loss,loss_cls,loss_vertex,loss_pose\n')
        for point in points:
            f.write('{},{},{},{}\n'.format(point[0], point[1], point[2], point[3]))

def main():
    print('Extracting error graph points from log file...')
    args = parse_args()
    print('[FILE: {}]'.format(args.log_file))

    with open(args.log_file) as f:
        points = get_point_list(f)
        create_csv(points)

if __name__ == '__main__':
    main()
