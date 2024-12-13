Available Meeting Slot Finder
By: Ethan Paransky(eparansky@csu.fullerton.edu), Jing Nie(jingnie@csu.fullerton.edu), Leonel Noriega-Rojas(leonelnr8@csu.fullerton.edu)
This Python program finds mutually available time slots for a meeting between two individuals based on their respective busy schedules and working hours.

How to run:
1. Download the files to any folder
2. Open your Python terminal and direct yourself to the folder then run the command line : python3 Project2_starter.py

Features
- Convert Time Formats: Converts time strings (e.g., "09:30") to minutes and vice versa for easier calculations.
- Identify Unbusy Slots: Determines free time slots between meetings for each individual within their specified working hours.
- Find Common Slots: Finds overlapping free time between two people that can accommodate a given meeting duration.
- Filter by Working Periods: Ensures available slots fall within each person’s working hours.

How It Works
1. Convert Schedules: All time data (busy schedules and working periods) are converted from "HH" format to minutes.
2. Calculate Free Slots: For each person, free time slots are calculated by comparing busy times against their working hours.
3. Find Common Availability: Using a two-pointer approach, the code identifies overlapping free time slots between two people.
4. Filter by Duration: Ensures the common slots meet the required meeting duration.
