import argparse
import cowsay


def cow_say(args):
    if args.list_cows:
        print(cowsay.list_cows())
        return

    if args.message == " ":
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
        message = " ".join(lines)
        print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Implementation of UNIX cowsay utility"
    )

    parser.add_argument(
            "-e", 
            default="oo",
            type=str,
            help="appearance of the cow's eyes, the first two characters of the string will be used",
            dest="eye_string"
    )
    parser.add_argument(
            "-f",
            default="",
            type=str,
            help="path to a particular cow picture file to use",
            dest="cowfile"
    )
    parser.add_argument(
            "-l",
            action="store_true",
            help="list all cowfiles on the current COWPATH",
            dest="list_cows"
    )
    parser.add_argument(
            "-n",
            action="store_false",
            help="the message will not be word-wrapped",
            dest="wrap_text"
    )
    parser.add_argument(
            "-T",
            default="  ",
            type=str,
            help="cow's tongue, must be two characters",
            dest="tongue_string"
    )
    parser.add_argument(
            "-W",
            default=40,
            type=int,
            help="where the message should be wrapped",
            dest="column"
    )
    parser.add_argument(
            "-b",
            action="append_const",
            const="b",
            help="Borg mode",
            dest="present"
    )
    parser.add_argument(
            "-d",
            action="append_const",
            const="d",
            help="dead mode",
            dest="present"
    )
    parser.add_argument(
            "-g",
            action="append_const",
            const="g",
            help="gready mode",
            dest="present"
    )
    parser.add_argument(
            "-p",
            action="append_const",
            const="p",
            help="paranoia mode",
            dest="present"
    )
    parser.add_argument(
            "-s",
            action="append_const",
            const="s",
            help="stoned mode",
            dest="present"
    )
    parser.add_argument(
            "-t",
            action="append_const",
            const="t",
            help="tired mode",
            dest="present"
    )
    parser.add_argument(
            "-w",
            action="append_const",
            const="d",
            help="wired mode",
            dest="present"
    )
    parser.add_argument(
            "-y",
            action="append_const",
            const="d",
            help="youth mode",
            dest="present"
    )
    parser.add_argument(
            "message",
            nargs="*",
            default=" ",
            type=str,
            help="message for cow"
    )

    args = parser.parse_args()
    
    cow_say(args)
