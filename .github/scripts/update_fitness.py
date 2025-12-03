#!/usr/bin/env python3
import sys
import re
from datetime import datetime

def update_fitness(date_str, workout, diet):
    """Update fitness tracker for a specific date"""
    
    # Parse the date
    date = datetime.strptime(date_str, '%Y-%m-%d')
    date_label = date.strftime('%b %-d')  # e.g., "Dec 2"
    
    # Read the fitness.md file
    with open('content/fitness.md', 'r') as f:
        content = f.read()
    
    # Convert string inputs to booleans
    workout_active = workout.lower() == 'true'
    diet_active = diet.lower() == 'true'
    
    # Find and update workout boxes for this date
    # Pattern: <div class="date-label">Dec 2</div> followed by workout boxes
    workout_pattern = rf'(<div class="date-label">{re.escape(date_label)}</div>\s*<div class="day-boxes">\s*<div class="day-box)(.*?)("></div>\s*<div class="day-box)(.*?)("></div>)'
    
    def replace_workout(match):
        prefix1 = match.group(1)
        current_class1 = match.group(2)
        middle = match.group(3)
        current_class2 = match.group(4)
        suffix = match.group(5)
        
        # Toggle or set active class for both boxes
        new_class1 = ' active' if workout_active else ''
        new_class2 = ' active' if workout_active else ''
        
        return f'{prefix1}{new_class1}{middle}{new_class2}{suffix}'
    
    content = re.sub(workout_pattern, replace_workout, content, flags=re.DOTALL)
    
    # Find and update diet boxes for this date
    # This is trickier - need to find the diet row after the workout row with this date
    # Split content into sections around the date
    sections = content.split(f'<div class="date-label">{date_label}</div>')
    
    if len(sections) > 1:
        # Find the diet row (apple icon) after this date in the same week
        # Look for the next </tr> then <tr> with apple icon, then count to the right day column
        
        # Calculate day of week (0=Monday, 6=Sunday in Python, but we need 0=Sunday for fitness tracker)
        day_of_week = (date.weekday() + 1) % 7  # Convert to Sunday=0
        
        # Find the apple row in the same week section
        week_section_end = sections[1].find('</tr>\n    <tr>\n      <td class="activity-icon"><i class="fas fa-apple-alt"></i></td>')
        if week_section_end != -1:
            apple_row_start = sections[1].find('<td class="activity-icon"><i class="fas fa-apple-alt"></i></td>', week_section_end)
            if apple_row_start != -1:
                # Find the Nth day-cell after the apple icon
                day_cell_pattern = r'<td class="day-cell">\s*<div class="day-boxes">\s*<div class="day-box(.*?)"></div>\s*<div class="day-box(.*?)"></div>'
                
                # Get all day cells in the diet row
                diet_row = sections[1][apple_row_start:]
                diet_row_end = diet_row.find('</tr>')
                if diet_row_end != -1:
                    diet_row = diet_row[:diet_row_end]
                
                # Replace the specific day's boxes
                day_cells = list(re.finditer(day_cell_pattern, diet_row, re.DOTALL))
                if day_of_week < len(day_cells):
                    match = day_cells[day_of_week]
                    old_cell = match.group(0)
                    new_class = ' active' if diet_active else ''
                    new_cell = f'<td class="day-cell">\n        <div class="day-boxes">\n          <div class="day-box{new_class}"></div>\n          <div class="day-box{new_class}"></div>'
                    
                    content = content.replace(old_cell, new_cell, 1)
    
    # Write the updated content
    with open('content/fitness.md', 'w') as f:
        f.write(content)
    
    print(f"Updated fitness tracker for {date_label}: workout={workout_active}, diet={diet_active}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: update_fitness.py DATE WORKOUT DIET")
        sys.exit(1)
    
    update_fitness(sys.argv[1], sys.argv[2], sys.argv[3])
