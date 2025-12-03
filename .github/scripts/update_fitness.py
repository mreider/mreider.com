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
    
    # Find and update workout box for this date
    # Pattern: <div class="date-label">Dec 2</div> followed by single workout box
    workout_pattern = rf'(<div class="date-label">{re.escape(date_label)}</div>\s*<div class="day-box)(.*?)("></div>)'
    
    def replace_workout(match):
        prefix = match.group(1)
        current_class = match.group(2)
        suffix = match.group(3)
        
        # Set active class
        new_class = ' active' if workout_active else ''
        
        return f'{prefix}{new_class}{suffix}'
    
    content = re.sub(workout_pattern, replace_workout, content, flags=re.DOTALL)
    
    # Find and update diet box for this date
    # Calculate day of week (0=Monday, 6=Sunday in Python, but we need 0=Sunday for fitness tracker)
    day_of_week = (date.weekday() + 1) % 7  # Convert to Sunday=0
    
    # Find the section with this date
    sections = content.split(f'<div class="date-label">{date_label}</div>')
    
    if len(sections) > 1:
        # Find the apple row in the same week section
        week_section_end = sections[1].find('</tr>\n    <tr>\n      <td class="activity-icon"><i class="fas fa-apple-alt"></i></td>')
        if week_section_end != -1:
            apple_row_start = sections[1].find('<td class="activity-icon"><i class="fas fa-apple-alt"></i></td>', week_section_end)
            if apple_row_start != -1:
                # Find the Nth day-cell after the apple icon
                day_cell_pattern = r'<td class="day-cell">\s*<div class="day-box(.*?)"></div>\s*</td>'
                
                # Get all day cells in the diet row
                diet_row_start_in_section = apple_row_start
                diet_row = sections[1][apple_row_start:]
                diet_row_end = diet_row.find('</tr>')
                if diet_row_end != -1:
                    diet_row = diet_row[:diet_row_end]
                
                # Find all day cells and replace the specific one
                day_cells = list(re.finditer(day_cell_pattern, diet_row, re.DOTALL))
                if day_of_week < len(day_cells):
                    match = day_cells[day_of_week]
                    # Get the absolute position in the original content
                    # We need to find where this cell is in the full content
                    match_start_in_diet_row = match.start()
                    match_end_in_diet_row = match.end()
                    
                    # Reconstruct the new diet row with the updated cell
                    new_class = ' active' if diet_active else ''
                    new_cell = f'<td class="day-cell">\n        <div class="day-box{new_class}"></div>\n      </td>'
                    
                    # Replace within the diet_row string
                    new_diet_row = diet_row[:match_start_in_diet_row] + new_cell + diet_row[match_end_in_diet_row:]
                    
                    # Now replace the old diet row with the new one in content
                    # Find the diet row in the full content
                    full_diet_row_start = content.find(diet_row)
                    if full_diet_row_start != -1:
                        content = content[:full_diet_row_start] + new_diet_row + content[full_diet_row_start + len(diet_row):]
    
    # Write the updated content
    with open('content/fitness.md', 'w') as f:
        f.write(content)
    
    print(f"Updated fitness tracker for {date_label}: workout={workout_active}, diet={diet_active}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: update_fitness.py DATE WORKOUT DIET")
        sys.exit(1)
    
    update_fitness(sys.argv[1], sys.argv[2], sys.argv[3])
