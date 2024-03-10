import cowsay

import shlex
import cmd

class CowsayCMD(cmd.Cmd):
    prompt = "cowsay command>> "

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


if __name__ == "__main__":
    CowsayCMD().cmdloop()
