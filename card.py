#!/usr/bin/env python3
"""
GitHub Contribution Filler
Generates backdated commits to fill your contribution graph
"""

import random
import datetime
import subprocess
import os
from collections import defaultdict

def generate_contributions(year=2021, total_contributions=600):
    """
    Generate random contributions for a given year.
    """
    contributions = defaultdict(int)
    
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    days_in_year = (end_date - start_date).days + 1
    
    remaining = total_contributions
    
    # Distribute contributions across days
    while remaining > 0:
        day_offset = random.randint(0, days_in_year - 1)
        current_date = start_date + datetime.timedelta(days=day_offset)
        date_str = current_date.isoformat()
        
        # Determine contribution count for this day
        if random.random() < 0.3:
            contrib_count = random.randint(5, 15)
        elif random.random() < 0.6:
            contrib_count = random.randint(2, 5)
        else:
            contrib_count = random.randint(1, 2)
        
        contrib_count = min(contrib_count, remaining)
        contributions[date_str] = min(contributions[date_str] + contrib_count, 20)
        remaining -= contrib_count
    
    # Add some empty days
    for _ in range(30):
        day_offset = random.randint(0, days_in_year - 1)
        current_date = start_date + datetime.timedelta(days=day_offset)
        date_str = current_date.isoformat()
        contributions[date_str] = 0
    
    # Add some full days
    for _ in range(20):
        day_offset = random.randint(0, days_in_year - 1)
        current_date = start_date + datetime.timedelta(days=day_offset)
        date_str = current_date.isoformat()
        contributions[date_str] = random.randint(15, 25)
    
    # Reduce weekend contributions
    for date_str in list(contributions.keys()):
        date_obj = datetime.date.fromisoformat(date_str)
        if date_obj.weekday() >= 5:
            contributions[date_str] = max(0, int(contributions[date_str] * 0.5))
    
    # Activity bursts
    for _ in range(3):
        start_burst = start_date + datetime.timedelta(days=random.randint(0, days_in_year - 30))
        for i in range(random.randint(3, 10)):
            burst_date = start_burst + datetime.timedelta(days=i)
            if burst_date <= end_date:
                date_str = burst_date.isoformat()
                contributions[date_str] = min(contributions[date_str] + random.randint(3, 8), 25)
    
    return dict(contributions)

def create_commits(contributions, repo_path="."):
    """
    Create backdated commits for each contribution.
    """
    # Ensure we're in the right directory
    os.chdir(repo_path)
    
    # Check if git is initialized
    if not os.path.exists(".git"):
        print("❌ Error: Not a git repository. Run 'git init' first.")
        return False
    
    print(f"📝 Creating {sum(contributions.values())} commits...")
    
    total_commits = 0
    failed_commits = 0
    
    # Sort dates chronologically (oldest first)
    # FIXED: Convert dictionary items to a sorted list of tuples
    sorted_dates = sorted(contributions.items())
    
    for date_str, count in sorted_dates:  # FIXED: Removed .items() since it's already a list of tuples
        if count <= 0:
            continue
            
        date_obj = datetime.date.fromisoformat(date_str)
        
        # Create the specified number of commits for this date
        for i in range(count):
            try:
                # Make a change to dummy.txt
                with open("dummy.txt", "a", encoding='utf-8') as f:
                    f.write(f"Commit {total_commits + 1}: {date_str} - #{i+1}\n")
                
                # Stage the change
                subprocess.run(["git", "add", "dummy.txt"], 
                             check=True, 
                             capture_output=True)
                
                # Format date for git commit
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                
                # Create backdated commit
                commit_msg = f"Update for {date_str} (#{i+1})"
                subprocess.run([
                    "git", "commit", 
                    "-m", commit_msg, 
                    "--date", formatted_date
                ], check=True, capture_output=True)
                
                total_commits += 1
                
                # Progress indicator
                if total_commits % 50 == 0:
                    print(f"  Created {total_commits} commits...")
                    
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Failed to create commit for {date_str}: {e}")
                failed_commits += 1
                continue
    
    print(f"\n✅ Created {total_commits} commits successfully!")
    if failed_commits > 0:
        print(f"⚠️  {failed_commits} commits failed.")
    
    return total_commits > 0

def main():
    """
    Main execution flow.
    """
    print("=" * 60)
    print("🚀 GITHUB CONTRIBUTION GRAPH FILLER")
    print("=" * 60)
    
    # Get user input
    print("\n📋 Configuration:")
    year = input("Enter year (default: 2021): ").strip()
    year = int(year) if year else 2021
    
    total = input("Enter total contributions (default: 600): ").strip()
    total = int(total) if total else 600
    
    print(f"\n⚙️  Generating {total} contributions for {year}...")
    
    # Generate contributions
    contributions = generate_contributions(year, total)
    
    # Show stats
    total_contribs = sum(contributions.values())
    active_days = sum(1 for v in contributions.values() if v > 0)
    max_day = max(contributions.values()) if contributions else 0
    
    print(f"\n📊 Statistics:")
    print(f"  Total contributions: {total_contribs}")
    print(f"  Active days: {active_days}")
    print(f"  Max per day: {max_day}")
    
    # Show sample of what will be created
    print("\n📝 Sample of contributions (first 10 days):")
    sample_dates = sorted(contributions.items())[:10]
    for date, count in sample_dates:
        if count > 0:
            print(f"  {date}: {count} commits")
    
    # Create commits
    print("\n" + "=" * 60)
    confirm = input("Ready to create commits? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\n🔄 Creating commits...")
        success = create_commits(contributions)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Commits have been created.")
            print("\n📤 Next steps:")
            print("  1. Review your commits: git log")
            print("  2. Push to GitHub: git push origin main")
            print("  3. Check your contribution graph on GitHub")
            print("=" * 60)
    else:
        print("\n❌ Cancelled. No commits were created.")

if __name__ == "__main__":
    main()