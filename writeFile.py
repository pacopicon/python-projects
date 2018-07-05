import sys

def main(filename, txtArr):
    f = open(filename, mode='wt', encoding='utf-8')
    f.writelines(txtArr)
    f.close()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])