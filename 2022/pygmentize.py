import os
import datetime
import argparse

parser = argparse.ArgumentParser(description='Make image of solution')
parser.add_argument('day',
                    metavar="d",
                    nargs="?",
                    type=int,
                    default=datetime.datetime.today().day,
                    choices=range(1, 32),
                    )
args = parser.parse_args()


def check_if_solution_file_exists():
    base_folder = os.path.basename(os.getcwd())
    try:  # could be: year.isdiecimal() and 2010 < year < 2099
        year = int(base_folder)
        if 2010 < year < 2099:
            return True
        else:
            raise ValueError
    except (ValueError, NameError):
        return False

def make_image(day):
    assert check_if_solution_file_exists(), ("Current working folder is not a year it seems: "
                                             f"'./{os.path.basename(os.getcwd())}'"
                                         )
    make_folder(day)


if __name__ == "__main__":
    create_new_day_folder(args.day)
