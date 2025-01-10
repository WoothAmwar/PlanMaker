## Creates a Daily Plan given Activities

# How to Use
There are 3 files to pay attention to. 
* Tasks.txt
* Plan.txt
* Final_plan.txt

# Tasks.txt
This is the first file to pay attention to. In this file, you will define what activities you want to do for the day
and for how long. The format should be {time in minutes} - {activity_name} - {tag}, where `- {tag}` is optional 
for an activity.
* Time in Minutes - Should be an integer value
* Activity_name - Can be anything, recommend using a single string
* Tag (Optional) - Can be "Longterm" or "Priority". 
* * Longterm means the activity will be in your plan for its full duration
without any breaks. For example, if you say "90 - Reading - Longterm", your plan will have you Reading for an 90-minute period
without breaks. 
* * Priority means you should prioritize doing this task early in the day

All of the information above should be separate with a `-` and everything should be separated with a single space. 
If this is not followed, the program will not work correctly.

# Plan.txt
This is the second file to pay attention to. In this file, you define what time of day you want a plan to be made, as well as
any times when you want to have a designated break. 
The file is 24 lines long, with each line representing an hour of the day. "1" is for 1 a.m, "13" for 1 p.m, etc. There are 3 keywords.
* START - Defines when the plan should begin. Ideally, this should be when you plan to wake up that day.
* BREAK - A break that will last for that entire hour. This can be for activities you already have planned for that specific hour or for
meals when you want to have a break
* END - Defines when the plan should end. Ideally, this should be when you to sleep or get ready to sleep.

All of the keywords have to be in all uppercase for the program to work correctly. The format should be {hour} - {tag}, with the
information separate with a space. If no tag is selected for the hour, still include the dash after the hour. 
There must be 24 lines with the hours 1-24. 

# Final_plan.txt
This is the third and last file to pay attention to. Here, the final plan will be made.
At the top of the file, there will be information regarding how much time you spend studying and relaxing that day. The second line shows the format for each following line, which will be {time} --- [activities, study_time, relax_time]. Each activity will be a list with 2 elements, with the first element being the time to spend on the activity and the second element being the activity to do for that time. 