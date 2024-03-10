import cowsay

import shlex
import cmd

class CowsayCMD(cmd.Cmd):
    prompt = "cowsay command>> "

    def do_exit(self, args):
        return 1

    def do_list_cows(self, args):
        """
        List of all cow file names in the given directory
        
        list_cows [cow_path]
        """
        res = shlex.split(args)
        if len(res) == 0:
            print(*cowsay.list_cows())
        else:
            print(*cowsay.list_cows(res[0]))

    def do_make_bubble(self, args):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        
        make_bubble [-b brackets] [-W width] [-w wrap_text] text

        -b: Brackets type ("cowsay" or "cowthink", default: "cowsay")
        -W: Bubble width (default: 40)
        -w: Should text be wrapped ("True" or "False", default: "True")
        """

        params = {
            "-b": cowsay.THOUGHT_OPTIONS["cowsay"],
            "-W": 40,
            "-w": True
        }

        res = shlex.split(args)
        if len(res) in [1, 3, 5, 7]:
            for i in range(0, len(res) - 1, 2):
                if (res[i] == "-b") and (res[i + 1] in ["cowsay", "cowthink"]):
                    params[res[i]] = cowsay.THOUGHT_OPTIONS[res[i + 1]]
                elif res[i] == "-W":
                    params[res[i]] = int(res[i + 1])
                elif res[i] == "-w":
                    if res[i + 1] == "True":
                        params[res[i]] = True
                    elif res[i + 1] == "False":
                        params[res[i]] = False
                    else:
                        print("Invalid command syntax")
                        return
                else:
                    print("Invalid command syntax")
                    return
        else:
            print("Invalid command syntax")
            return

        print(cowsay.make_bubble(
            res[-1],
            brackets=params["-b"],
            width=params["-W"],
            wrap_text=params["-w"]
        ))

    def complete_make_bubble(self, text, line, begidx, endidx):
        DICT = {
            "-b": ["cowsay", "cowthink"],
            "-w": ["True", "False"]
        }

        res = shlex.split(line)
        key = res[-1] if begidx == endidx else res[-2]
        return [c for c in DICT[key] if c.startswith(text)]


    def do_cowsay(self, args):
        """
        Generates an ASCII picture of a cow saying something provided by the user

        cowsay [-c cow] [-e eye_string] [-T tongue_string] message

        -c: The name of the cow (valid names from list_cows, default: "default")
        -e: A custom eye string (at least two characters, default: "oo")
        -T: A custom tongue string (must be two characters, default: "  ")
        """
        
        params = {
            "-c": "default",
            "-e": "oo",
            "-T": "  "
        }

        res = shlex.split(args)
        if len(res) in [1, 3, 5, 7]:
            for i in range(0, len(res) - 1, 2):
                if (res[i] == "-c") and res[i + 1] in cowsay.list_cows():
                    params[res[i]] = res[i + 1]
                elif res[i] == "-e" and len(res[i + 1]) >= 2:
                    params[res[i]] = res[i + 1]
                elif res[i] == "-T" and len(res[i + 1]) == 2:
                    params[res[i]] = res[i + 1]
                else:
                    print("Invalid command syntax")
                    return
        else:
            print("Invalid command syntax")
            return

        print(cowsay.cowsay(
            res[-1],
            cow=params["-c"],
            eyes=params["-e"],
            tongue=params["-T"]
        ))

    def complete_cowsay(self, text, line, begidx, endidx):
        DICT = {
            "-c": cowsay.list_cows(),
        }

        res = shlex.split(line)
        key = res[-1] if begidx == endidx else res[-2]
        return [c for c in DICT[key] if c.startswith(text)]

    def do_cowthink(self, args):
        """
        Generates an ASCII picture of a cow saying something provided by the user

        cowthink [-c cow] [-e eye_string] [-T tongue_string] message

        -c: The name of the cow (valid names from list_cows, default: "default")
        -e: A custom eye string (at least two characters, default: "oo")
        -T: A custom tongue string (must be two characters, default: "  ")
        """
        
        params = {
            "-c": "default",
            "-e": "oo",
            "-T": "  "
        }

        res = shlex.split(args)
        if len(res) in [1, 3, 5, 7]:
            for i in range(0, len(res) - 1, 2):
                if (res[i] == "-c") and res[i + 1] in cowsay.list_cows():
                    params[res[i]] = res[i + 1]
                elif res[i] == "-e" and len(res[i + 1]) >= 2:
                    params[res[i]] = res[i + 1]
                elif res[i] == "-T" and len(res[i + 1]) == 2:
                    params[res[i]] = res[i + 1]
                else:
                    print("Invalid command syntax")
                    return
        else:
            print("Invalid command syntax")
            return

        print(cowsay.cowthink(
            res[-1],
            cow=params["-c"],
            eyes=params["-e"],
            tongue=params["-T"]
        ))

    def complete_cowthink(self, text, line, begidx, endidx):
        DICT = {
            "-c": cowsay.list_cows(),
        }

        res = shlex.split(line)
        key = res[-1] if begidx == endidx else res[-2]
        return [c for c in DICT[key] if c.startswith(text)]


if __name__ == "__main__":
    CowsayCMD().cmdloop()
