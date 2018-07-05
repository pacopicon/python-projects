def keypress():
    '''keypress - A module for detecting a single keypress.'''

    try:
        import msvcrt
        # msvcrt = microsoft visual C runtime
        def getkey():
            '''Wait for a keypress and return a single character string.'''
            return msvcrt.getch()
    
    except ImportError:

        import sys
        import tty
        import termios

        def getKey():
            '''Wait for a keypress and return a single character string.'''
            fd = sys.stdin.fileno()
            original_attributes = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                # Terminal is put into raw mode in order to read a single character
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
                # This block restores various Terminal attributes after Terminal was et to raw.
            return ch

def main():
   keypress()

if __name__ == '__main__':
    main()