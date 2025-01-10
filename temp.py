"""
Makes a plan for studying for the day based on the tasks you need to do, their importance, and the time it takes
 to complete the tasks
Shows the percent of the day you studies and relaxed, and how far in the progress you are
You can checkbox whether you were able to accomplish something or not, and if not you can recreate the plan
 based on what you did/didn't do
"""

DAY_SPAN = 24


class StudyPlanMaker:
    def __init__(self):
        self.study_hours = 0
        self.relax_hours = 0
        self.plan = {}
        self.tasks = []
        self.start_hour = 0
        self.end_hour = 0
        self.N_MAX_STUDY = 0

    def get_tasks(self):
        """Returns the tasks to do in list format"""
        return self.tasks

    def get_plan(self):
        """Returns the plan in dictionary format"""
        return self.plan

    def set_tasks(self):
        """Gets the tasks from the file and makes it into a list of data formed [time,task]"""
        with open("tasks.txt") as f:
            # for every task in tasks, split and append to the tasks list with LongTerm or Priority or None
            for x in f:
                c = x.split(" - ")
                self.tasks.append([int(c[0]), c[1].split("\n")[0], c[-1].split("\n")[0] if c[-1] == "LongTerm\n"
                                                                            or c[-1] == "Priority\n" else "None"])
                self.study_hours += int(c[0])

    def set_plan(self):
        """Gets the plan from the file and makes it into a dictionary with {time:[study, relax]} with placeholder
        values for study and relax values"""
        with open("plan.txt") as f:
            started_day = False
            for x in f:
                # for every entry in the plan, split, find the start and end, and put placeholder values
                c = x.split("-")
                i = c[1].split("\n")[0]
                c[1] = i.split(" ")[-1]
                if c[1] == "START":
                    started_day = True
                    # print(f"Started day at {c[0]}")
                    self.start_hour = int(c[0])
                elif c[1] == "END":
                    started_day = False
                    # print(f"Ended day at {c[0]}")
                    self.end_hour = int(c[0])
                elif c[1] == "BREAK":
                    self.plan[int(c[0][0:-1])] = [0, 60]
                    continue

                if started_day:
                    z = c[0][0:-1]
                    self.plan[int(z)] = [0, 0]

    def set_max_study_per_hour(self, amount):
        """Sets the max amount of minutes you can study per hour if it isn't LongTerm or Priority"""
        self.N_MAX_STUDY = amount

    def write_final_plan(self):
        """Writes the plan to the file in the form Time - [Study_Time - Task, Relax_time]"""
        with open("final_plan.txt", "w+") as f:
            f.write("Study Time: " + str(self.study_hours) + " | " + "Relax Time: " + str(self.relax_hours) + "\n")
            f.write("Time --- [Study_Time, Relax_Time]\n")
            for key in self.plan:
                hour = int(key)
                # Deciding if it is a.m or p.m to write to file
                if hour > 12:
                    hour -= 12
                    hour = str(hour) + "p"
                elif hour == 12:
                    hour = str(hour) + "p"
                elif hour == 24:
                    hour = str(hour) + "a"
                else:
                    hour = str(hour) + "a"

                # increase the value of 4 for more spaces, decrease for less spaces
                spaces = abs((len(hour) - 4)) * " "
                f.write(hour + spaces + " --- " + str(self.plan[key]) + "\n")

    def make_time_sessions(self):
        """Gets the time for each task and separates it into study sessions"""
        tasks = self.get_tasks()
        i = 0
        for c in tasks:
            time_list = []
            time = c[0]
            longterm = False
            # Deciding how long each session should be based on if it's longterm or not
            if c[-1] == "LongTerm":
                longterm = True

            session_time = 20
            if longterm:
                session_time = 40
            # separating the time for each session
            while time > session_time:
                time -= session_time
                time_list.append(session_time)
            # adding the remainder but making sure it isn't too short of a session
            if time < session_time / 2 or time <= 10:
                time_list.remove(session_time)
                time_list.append(time + session_time)
            else:
                time_list.append(time)

            tasks[i][0] = time_list
            i += 1

    def get_separate_priority_tasks(self, tasks):
        """Returns a list of the priority tasks so they can be done first"""
        p_tasks = []
        to_remove = []
        for task in range(len(tasks)):
            if tasks[task][-1] == "Priority":
                p_tasks.append(c := tasks[task])
                to_remove.append(c)
        for val in to_remove:
            tasks.remove(val)

        return p_tasks

    def make_plan(self):
        """Makes the plan by assigning time to each hour, priority first, and appending the task to it as well"""
        tasks = self.get_tasks()
        plan = self.get_plan()
        p_tasks = self.get_separate_priority_tasks(tasks)
        current_hour = self.start_hour
        self.set_max_study_per_hour(40)  # The max amount or study time per hour, beside LongTerm or Priority, set
        is_start_hour = True

        for task in p_tasks:
            while task[0]:
                sess_min = 0

                if self.end_hour > current_hour >= self.start_hour:
                    if plan[current_hour][-2] != 0 and plan[current_hour][-2] + task[0][0] <= self.N_MAX_STUDY:
                        sess_min += task[0][0]
                    else:
                        current_hour += 1
                        if is_start_hour:
                            current_hour -= 1
                            is_start_hour = False
                        if current_hour < self.end_hour:
                            if plan[current_hour][1] == 60:
                                current_hour += 1
                        else:
                            break

                    plan[current_hour].insert(0, [task[0][0], task[1]])
                    sess_min += task[0][0]
                    try:
                        if task[0][1] + sess_min <= self.N_MAX_STUDY:
                            plan[current_hour].insert(0, [task[0][1], task[1]])
                            sess_min += task[0][1]
                            task[0].pop(1)
                    except IndexError:
                        pass

                    if plan[current_hour][-1] != 60:
                        plan[current_hour][-2] = sess_min
                        plan[current_hour][-1] = 60 - plan[current_hour][-2]
                task[0].pop(0)

        self.start_hour = current_hour

        for task in tasks:
            while task[0]:
                sess_min = 0
                if self.end_hour > current_hour >= self.start_hour:
                    if plan[current_hour][-2] != 0 and plan[current_hour][-2] + task[0][0] <= self.N_MAX_STUDY:
                        sess_min += task[0][0]
                    else:
                        current_hour += 1
                        if is_start_hour:
                            current_hour -= 1
                            is_start_hour = False
                        if current_hour < self.end_hour:
                            if plan[current_hour][1] == 60:
                                current_hour += 1
                        else:
                            break

                    plan[current_hour].insert(0, [task[0][0], task[1]])
                    sess_min += task[0][0]
                    try:
                        if task[0][1] + sess_min <= self.N_MAX_STUDY:
                            plan[current_hour].insert(0, [task[0][1], task[1]])
                            sess_min += task[0][1]
                            task[0].pop(1)
                    except IndexError:
                        pass

                    if plan[current_hour][-1] != 60:
                        plan[current_hour][-2] = sess_min
                        plan[current_hour][-1] = 60 - plan[current_hour][-2]

                task[0].pop(0)


def main():
    planMaker = StudyPlanMaker()
    planMaker.set_tasks()
    planMaker.set_plan()

    planMaker.make_time_sessions()
    planMaker.make_plan()
    planMaker.write_final_plan()

    # print(planMaker.get_tasks())
    # print("\n======\n")
    # print(planMaker.get_plan())


if __name__ == "__main__":
    main()
