import random
import datetime
import json
from collections import defaultdict

def generate_contributions(year=2021, total_contributions=600):
    """
    Generate random contributions for a given year with realistic patterns.
    """
    # Create a dictionary to store contributions for each date
    contributions = defaultdict(int)
    
    # Calculate the number of days in the year
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    days_in_year = (end_date - start_date).days + 1
    
    # Generate random contributions
    remaining = total_contributions
    
    # First pass: distribute contributions across days
    while remaining > 0:
        # Randomly select a day
        day_offset = random.randint(0, days_in_year - 1)
        current_date = start_date + datetime.timedelta(days=day_offset)
        date_str = current_date.isoformat()
        
        # Determine how many contributions for this day (1-15)
        # Make some days have more, some have less
        if random.random() < 0.3:  # 30% chance of high contribution day
            contrib_count = random.randint(5, 15)
        elif random.random() < 0.6:  # 30% chance of medium contribution day
            contrib_count = random.randint(2, 5)
        else:  # 40% chance of low contribution day
            contrib_count = random.randint(1, 2)
        
        # Don't exceed remaining
        contrib_count = min(contrib_count, remaining)
        
        contributions[date_str] = min(contributions[date_str] + contrib_count, 20)  # Cap at 20
        remaining -= contrib_count
    
    # Second pass: ensure some days are empty and some are full
    # Add some empty days (no contributions)
    for _ in range(30):  # Make about 30 days empty
        day_offset = random.randint(0, days_in_year - 1)
        current_date = start_date + datetime.timedelta(days=day_offset)
        date_str = current_date.isoformat()
        contributions[date_str] = 0
    
    # Add some full days (high contributions)
    for _ in range(20):  # Make about 20 days with high contributions
        day_offset = random.randint(0, days_in_year - 1)
        current_date = start_date + datetime.timedelta(days=day_offset)
        date_str = current_date.isoformat()
        contributions[date_str] = random.randint(15, 25)
    
    # Third pass: create weekly patterns
    # People tend to commit more on weekdays than weekends
    for date_str in list(contributions.keys()):
        date_obj = datetime.date.fromisoformat(date_str)
        weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
        
        if weekday >= 5:  # Weekend (Saturday, Sunday)
            # Reduce weekend contributions by 50%
            contributions[date_str] = max(0, int(contributions[date_str] * 0.5))
    
    # Fourth pass: create some clusters of activity
    # Add activity bursts (like hackathons or project sprints)
    for _ in range(3):  # 3 activity bursts
        start_burst = start_date + datetime.timedelta(days=random.randint(0, days_in_year - 30))
        for i in range(random.randint(3, 10)):  # Burst lasts 3-10 days
            burst_date = start_burst + datetime.timedelta(days=i)
            if burst_date <= end_date:
                date_str = burst_date.isoformat()
                contributions[date_str] = min(contributions[date_str] + random.randint(3, 8), 25)
    
    return dict(contributions)

def print_contribution_stats(contributions, year=2021):
    """
    Print statistics about the generated contributions.
    """
    total = sum(contributions.values())
    days_with_contrib = sum(1 for v in contributions.values() if v > 0)
    days_without_contrib = sum(1 for v in contributions.values() if v == 0)
    max_contrib_day = max(contributions.values()) if contributions else 0
    avg_contrib = total / len(contributions) if contributions else 0
    
    print(f"Year: {year}")
    print(f"Total Contributions: {total}")
    print(f"Days with contributions: {days_with_contrib}")
    print(f"Days without contributions: {days_without_contrib}")
    print(f"Max contributions in a day: {max_contrib_day}")
    print(f"Average contributions per day: {avg_contrib:.2f}")
    
    # Distribution of contribution levels
    levels = {'0': 0, '1-2': 0, '3-5': 0, '6-10': 0, '11-20': 0, '21+': 0}
    for v in contributions.values():
        if v == 0:
            levels['0'] += 1
        elif v <= 2:
            levels['1-2'] += 1
        elif v <= 5:
            levels['3-5'] += 1
        elif v <= 10:
            levels['6-10'] += 1
        elif v <= 20:
            levels['11-20'] += 1
        else:
            levels['21+'] += 1
    
    print("\nContribution Distribution:")
    for level, count in levels.items():
        print(f"  {level}: {count} days")

def save_contributions_to_file(contributions, filename="contributions_2021.json"):
    """
    Save the contributions data to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(contributions, f, indent=2)
    print(f"\nContributions saved to {filename}")

def create_visualization_data(contributions, year=2021):
    """
    Create data for a contribution graph visualization (similar to GitHub).
    """
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    
    # Create a grid of weeks
    weeks = []
    current_date = start_date
    
    # Find the first Monday
    while current_date.weekday() != 0:  # 0 = Monday
        current_date -= datetime.timedelta(days=1)
    
    current_week = []
    while current_date <= end_date:
        date_str = current_date.isoformat()
        contrib = contributions.get(date_str, 0)
        
        # Determine color level (0-4) similar to GitHub
        if contrib == 0:
            level = 0
        elif contrib <= 2:
            level = 1
        elif contrib <= 5:
            level = 2
        elif contrib <= 10:
            level = 3
        else:
            level = 4
        
        current_week.append({
            'date': date_str,
            'count': contrib,
            'level': level
        })
        
        if current_date.weekday() == 6:  # Sunday
            weeks.append(current_week)
            current_week = []
        
        current_date += datetime.timedelta(days=1)
    
    # Add last week if not empty
    if current_week:
        weeks.append(current_week)
    
    return weeks

def main():
    """
    Main function to generate and display contributions.
    """
    print("🎯 Generating random contributions for 2021...")
    print("=" * 50)
    
    # Generate contributions
    contributions = generate_contributions(2021, 600)
    
    # Print statistics
    print_contribution_stats(contributions, 2021)
    
    # Save to file
    save_contributions_to_file(contributions)
    
    # Create visualization data
    weeks = create_visualization_data(contributions, 2021)
    print(f"\nVisualization data created with {len(weeks)} weeks")
    
    # Show a sample of the data
    print("\n📊 Sample of contribution data (first 10 days):")
    sample_dates = sorted(contributions.keys())[:10]
    for date in sample_dates:
        print(f"  {date}: {contributions[date]} contributions")
    
    print("\n✅ Done! The contribution data has been generated.")
    print("You can use this data to simulate a GitHub contribution graph.")

if __name__ == "__main__":
    main()
