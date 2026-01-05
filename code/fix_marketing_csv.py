import csv
import random

input_file = 'csv/marketing_performance.csv'
output_file = 'csv/marketing_performance_fixed.csv'

# Average order values by channel (realistic retail values)
AOV_BY_CHANNEL = {
    'Paid Search': (75, 150),      # Higher intent, higher AOV
    'Social Media': (45, 95),      # Lower AOV, impulse buys
    'Display Ads': (40, 85),       # Awareness, lower conversion value
    'Email Marketing': (80, 160),  # Loyal customers, higher AOV
    'Affiliate Marketing': (60, 120)  # Mid-range
}

random.seed(42)  # For reproducibility

with open(input_file, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    rows = []
    
    for row in reader:
        conversions = int(float(row['conversions'])) if row['conversions'] else 0
        spend = float(row['spend']) if row['spend'] else 0
        channel = row['channel']
        
        # Generate revenue based on conversions and channel-specific AOV
        if conversions > 0 and channel in AOV_BY_CHANNEL:
            aov_min, aov_max = AOV_BY_CHANNEL[channel]
            # Each conversion has a random AOV within the range
            revenue = sum(random.uniform(aov_min, aov_max) for _ in range(conversions))
            revenue = round(revenue, 2)
        else:
            revenue = 0
        
        # Calculate ROAS (Return on Ad Spend) = revenue / spend
        if spend > 0 and revenue > 0:
            roas = round(revenue / spend, 2)
        else:
            roas = 0
        
        # Calculate revenue_per_conversion
        if conversions > 0:
            rpc = round(revenue / conversions, 2)
        else:
            rpc = 0
        
        row['revenue'] = revenue
        row['roas'] = roas
        row['revenue_per_conversion'] = rpc
        rows.append(row)

# Write the fixed CSV
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Fixed CSV saved to {output_file}")
print(f"Total rows processed: {len(rows)}")

# Show sample of fixed data
print("\nSample of fixed data (first 5 rows):")
for row in rows[:5]:
    print(f"  {row['date'][:10]} | {row['channel']:20} | spend: {row['spend']:>8} | revenue: {row['revenue']:>10} | roas: {row['roas']}")
