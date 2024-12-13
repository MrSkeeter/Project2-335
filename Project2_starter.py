
# Import time libs
from datetime import datetime, timedelta

def time_to_minutes(time_str):
    # Convert time string 'HH:MM' to total minutes since 00:00
    if isinstance(time_str, str):
        time = datetime.strptime(time_str, '%H:%M')
        return time.hour * 60 + time.minute
    return time_str

def minutes_to_time(minutes):
    # Convert total minutes back to time string 'HH:MM'
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

def find_unbusy_slots(busy_schedule, daily_act):
    # Convert schedule and daily activity to minutes
    busy_schedule_minutes = [[time_to_minutes(start), time_to_minutes(end)] for start, end in busy_schedule]
    daily_start, daily_end = time_to_minutes(daily_act[0]), time_to_minutes(daily_act[1])
    
    # Find unbusy slots
    unbusy_slots = []
    current_start = daily_start
    for start, end in busy_schedule_minutes:
        if current_start < start:
            unbusy_slots.append([current_start, start])
        current_start = max(current_start, end)
    if current_start < daily_end:
        unbusy_slots.append([current_start, daily_end])
    
    return unbusy_slots

# Find common unbusy slots between two schedules using two-pointer technique which is O(n)
def find_common_unbusy_slots(unbusy1, unbusy2, duration):
    
    common_slots = []
    i, j = 0, 0
    
    while i < len(unbusy1) and j < len(unbusy2):
        # Find the overlap between the two slots
        start1, end1 = unbusy1[i]
        start2, end2 = unbusy2[j]
        common_start = max(start1, start2)
        common_end = min(end1, end2)
        
        # If there is an overlap that meets the duration requirement, add to common slots
        if common_start < common_end and (common_end - common_start) >= duration:
            common_slots.append([common_start, common_end])
        
        # Move the pointer with the earlier ending slot
        if end1 < end2:
            i += 1
        else:
            j += 1
    
    return common_slots

def filter_by_working_period(common_slots, working_periods):
    # Filter the common unbusy slots by the working period
    filtered_slots = []
    for start, end in common_slots:
        for work_start, work_end in working_periods:
            common_start = max(start, work_start)
            common_end = min(end, work_end)
            if common_start < common_end:
                filtered_slots.append([common_start, common_end])
    
    # Remove duplicate slots
    unique_filtered_slots = []
    for slot in filtered_slots:
        if slot not in unique_filtered_slots:
            unique_filtered_slots.append(slot)
    
    return unique_filtered_slots

def find_available_slots(busy_schedules, working_periods, duration):

    #Find unbusy slots for each person
    unbusy_slots = [find_unbusy_slots(busy_schedules[i], working_periods[i]) for i in range(len(busy_schedules))]
    
    # Find common unbusy slots using two-pointer technique
    common_unbusy_slots = find_common_unbusy_slots(unbusy_slots[0], unbusy_slots[1], duration)
    
    # Filter the common slots based on working periods
    working_periods_minutes = [[time_to_minutes(start), time_to_minutes(end)] for start, end in working_periods]
    available_slots = filter_by_working_period(common_unbusy_slots, working_periods_minutes)
    
    # Convert slots back to time format
    available_slots = [[minutes_to_time(start), minutes_to_time(end)] for start, end in available_slots]
    
    return available_slots

# Sample Input
person1_Schedule = [[ '7:00', '8:30'],  ['12:00', '13:00'],  ['16:00', '18:00']]
person1_DailyAct = ['9:00', '19:00']

person2_Schedule = [[ '9:00', '10:30'],  ['12:20', '13:30'],  ['14:00', '15:00'], ['16:00', '17:00' ]]
person2_DailyAct = ['9:00', '18:30']

duration_of_meeting = 30

"""# Finding available slots
busy_schedules = [person1_Schedule, person2_Schedule]
working_periods = [person1_DailyAct, person2_DailyAct]

available_slots = find_available_slots(busy_schedules, working_periods, duration_of_meeting)
print(available_slots)
"""

# Test Case 1: Basic Overlapping Schedule
person1_Schedule_1 = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct_1 = ['9:00', '19:00']
person2_Schedule_1 = [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct_1 = ['9:00', '18:30']
duration_1 = 30
print("Test Case 1:", find_available_slots([person1_Schedule_1, person2_Schedule_1], [person1_DailyAct_1, person2_DailyAct_1], duration_1))

# Test Case 2: No Overlapping Available Slot
person1_Schedule_2 = [['7:00', '9:00'], ['11:00', '12:30'], ['16:00', '18:00']]
person1_DailyAct_2 = ['9:00', '19:00']
person2_Schedule_2 = [['9:00', '10:30'], ['13:00', '14:30'], ['15:00', '17:00']]
person2_DailyAct_2 = ['9:00', '18:30']
duration_2 = 45
print("Test Case 2:", find_available_slots([person1_Schedule_2, person2_Schedule_2], [person1_DailyAct_2, person2_DailyAct_2], duration_2))

# Test Case 3: All-Day Free
person1_Schedule_3 = []
person1_DailyAct_3 = ['9:00', '18:00']
person2_Schedule_3 = []
person2_DailyAct_3 = ['9:00', '18:00']
duration_3 = 60
print("Test Case 3:", find_available_slots([person1_Schedule_3, person2_Schedule_3], [person1_DailyAct_3, person2_DailyAct_3], duration_3))

# Test Case 4: Meeting Duration Longer Than Any Slot
person1_Schedule_4 = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct_4 = ['9:00', '19:00']
person2_Schedule_4 = [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct_4 = ['9:00', '18:30']
duration_4 = 120
print("Test Case 4:", find_available_slots([person1_Schedule_4, person2_Schedule_4], [person1_DailyAct_4, person2_DailyAct_4], duration_4))

# Test Case 5: Partial Overlapping Slots Within Working Period
person1_Schedule_5 = [['9:00', '10:00'], ['11:30', '13:00'], ['15:00', '16:30']]
person1_DailyAct_5 = ['8:00', '18:00']
person2_Schedule_5 = [['9:30', '10:30'], ['12:00', '13:30'], ['14:00', '15:30']]
person2_DailyAct_5 = ['8:00', '18:00']
duration_5 = 15
print("Test Case 5:", find_available_slots([person1_Schedule_5, person2_Schedule_5], [person1_DailyAct_5, person2_DailyAct_5], duration_5))

# Test Case 6: Busy Period Exactly at the Start of Working Period
person1_Schedule_6 = [['8:00', '9:00'], ['11:00', '13:00'], ['14:00', '15:30']]
person1_DailyAct_6 = ['8:00', '17:00']
person2_Schedule_6 = [['8:00', '9:30'], ['12:00', '13:30'], ['16:00', '17:00']]
person2_DailyAct_6 = ['8:00', '17:00']
duration_6 = 30
print("Test Case 6:", find_available_slots([person1_Schedule_6, person2_Schedule_6], [person1_DailyAct_6, person2_DailyAct_6], duration_6))

# Test Case 7: No Overlapping Activity Period
person1_Schedule_7 = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct_7 = ['9:00', '11:00']
person2_Schedule_7 = [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct_7 = ['13:00', '18:30']
duration_7 = 20
print("Test Case 7:", find_available_slots([person1_Schedule_7, person2_Schedule_7], [person1_DailyAct_7, person2_DailyAct_7], duration_7))

# Test Case 8: Minimum Edge Case (1 Minute Duration)
person1_Schedule_8 = [['9:30', '10:00'], ['11:00', '11:01']]
person1_DailyAct_8 = ['9:00', '12:00']
person2_Schedule_8 = [['9:00', '9:15'], ['10:05', '10:30']]
person2_DailyAct_8 = ['9:00', '12:00']
duration_8 = 1
print("Test Case 8:", find_available_slots([person1_Schedule_8, person2_Schedule_8], [person1_DailyAct_8, person2_DailyAct_8], duration_8))

# Test Case 9: Large Slot with Various Small Busy Periods
person1_Schedule_9 = [['9:00', '9:05'], ['11:00', '11:15'], ['13:00', '13:10'], ['15:00', '15:05']]
person1_DailyAct_9 = ['9:00', '18:00']
person2_Schedule_9 = [['9:05', '9:10'], ['11:10', '11:20'], ['13:05', '13:15'], ['15:05', '15:15']]
person2_DailyAct_9 = ['9:00', '18:00']
duration_9 = 10
print("Test Case 9:", find_available_slots([person1_Schedule_9, person2_Schedule_9], [person1_DailyAct_9, person2_DailyAct_9], duration_9))

# Test Case 10: Working Period with a Break
person1_Schedule_10 = [['9:30', '10:30'], ['12:00', '13:00'], ['14:00', '15:00']]
person1_DailyAct_10 = ['9:00', '17:00']
person2_Schedule_10 = [['9:00', '9:30'], ['10:30', '12:00'], ['15:30', '17:00']]
person2_DailyAct_10 = ['9:00', '17:00']
duration_10 = 30
print("Test Case 10:", find_available_slots([person1_Schedule_10, person2_Schedule_10], [person1_DailyAct_10, person2_DailyAct_10], duration_10))

