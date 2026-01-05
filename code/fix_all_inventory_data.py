"""
Fix data quality issues in inventory_master.csv and product_master.csv.

Issues:
1. quantity/current_stock sometimes exceeds max_stock_level
2. max_stock_level should be consistent between both files for the same product

Strategy:
- Use max_stock_level from product_master as the source of truth
- Update inventory_master to use the same max_stock_level per product
- Cap quantity/current_stock to never exceed max_stock_level
"""

import csv
import os
import random

def load_product_master(filepath):
    """Load product_master and return dict of product_id -> max_stock_level"""
    products = {}
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products[row['product_id']] = row
    return products

def fix_product_master(input_file, output_file):
    """Fix product_master.csv - cap current_stock to max_stock_level"""
    fixed_count = 0
    total_count = 0
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            total_count += 1
            current_stock = int(row['current_stock'])
            max_stock = int(row['max_stock_level'])
            
            if current_stock > max_stock:
                # Cap current_stock to 70-95% of max_stock_level
                new_stock = int(max_stock * random.uniform(0.70, 0.95))
                row['current_stock'] = str(new_stock)
                fixed_count += 1
            
            writer.writerow(row)
    
    print(f"product_master: Processed {total_count} rows, fixed {fixed_count}")
    return output_file

def fix_inventory_master(input_file, output_file, product_data):
    """
    Fix inventory_master.csv:
    - Align max_stock_level with product_master
    - Cap quantity to max_stock_level
    """
    fixed_qty_count = 0
    fixed_max_count = 0
    total_count = 0
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            total_count += 1
            product_id = row['product_id']
            quantity = int(row['quantity'])
            max_stock = int(row['max_stock_level'])
            
            # Align max_stock_level with product_master if available
            if product_id in product_data:
                product_max_stock = int(product_data[product_id]['max_stock_level'])
                if max_stock != product_max_stock:
                    row['max_stock_level'] = str(product_max_stock)
                    max_stock = product_max_stock
                    fixed_max_count += 1
            
            # Cap quantity to max_stock_level
            if quantity > max_stock:
                new_quantity = int(max_stock * random.uniform(0.70, 0.95))
                row['quantity'] = str(new_quantity)
                fixed_qty_count += 1
            
            writer.writerow(row)
    
    print(f"inventory_master: Processed {total_count} rows")
    print(f"  - Fixed {fixed_qty_count} rows where quantity > max_stock_level")
    print(f"  - Aligned {fixed_max_count} rows with product_master max_stock_level")
    return output_file

def main():
    # Set random seed for reproducibility
    random.seed(42)
    
    # File paths
    product_input = 'csv/product_master.csv'
    product_output = 'csv/product_master_fixed.csv'
    inventory_input = 'csv/inventory_master.csv'
    inventory_output = 'csv/inventory_master_fixed.csv'
    
    print("=" * 60)
    print("Fixing data quality issues in inventory data")
    print("=" * 60)
    
    # Step 1: Fix product_master
    print("\n[1/3] Fixing product_master.csv...")
    fix_product_master(product_input, product_output)
    
    # Step 2: Load fixed product_master for reference
    print("\n[2/3] Loading product data for alignment...")
    product_data = load_product_master(product_output)
    print(f"  Loaded {len(product_data)} products")
    
    # Step 3: Fix inventory_master with alignment
    print("\n[3/3] Fixing inventory_master.csv...")
    fix_inventory_master(inventory_input, inventory_output, product_data)
    
    print("\n" + "=" * 60)
    print("Done! Fixed files created:")
    print(f"  - {product_output}")
    print(f"  - {inventory_output}")
    print("=" * 60)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
