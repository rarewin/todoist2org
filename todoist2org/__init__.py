import todoist2org.todoist


def main():
    t = todoist.Todoist()
    t.get_todoist_items()
    t.gen_org()
