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

if __name__ == "__main__":
    CowsayCMD().cmdloop()
