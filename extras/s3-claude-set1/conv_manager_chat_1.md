# Weekly Operations Report for QuickMart Convenience Store
**Report Date**: July 14, 2023
**Period Covered**: July 15-21, 2023

## Executive Summary

This week's operations are expected to be significantly impacted by the Youth Baseball Tournament occurring on Saturday and Sunday (July 15-16) at Memorial Park (0.5 miles from our location) and the forecasted heat wave. Several products are projected to fall below minimum stock levels without additional ordering, and sales forecasts suggest increased demand for cold beverages and snacks.

## Inventory Status

```
| product_id | product_name             | category        | current_quantity | minimum_quantity | projected_usage_this_week | expected_quantity_end_of_week | reorder_status |
|------------|--------------------------|-----------------|------------------|------------------|---------------------------|-------------------------------|----------------|
| P001       | Coca-Cola 12oz          | Beverages       | 120              | 50               | 85                        | 35                            | Yes            |
| P002       | Pepsi 12oz              | Beverages       | 95               | 45               | 60                        | 35                            | Yes            |
| P003       | Bottled Water 16oz      | Beverages       | 200              | 75               | 160                       | 40                            | Yes            |
| P004       | Red Bull 8oz            | Beverages       | 45               | 30               | 40                        | 5                             | Yes            |
| P005       | Monster Energy 16oz     | Beverages       | 38               | 25               | 45                        | -7                            | Yes            |
| P006       | Doritos Nacho           | Snacks          | 65               | 30               | 55                        | 10                            | Yes            |
| P007       | Lay's Classic           | Snacks          | 70               | 35               | 40                        | 30                            | Yes            |
| P008       | Snickers               | Candy           | 85               | 40               | 50                        | 35                            | Yes            |
| P009       | M&Ms Peanut            | Candy           | 75               | 35               | 65                        | 10                            | Yes            |
| P010       | Beer (Local) 6-pack    | Alcohol         | 28               | 15               | 30                        | -2                            | Yes            |
| P011       | Wine (Red) 750ml       | Alcohol         | 12               | 8                | 6                         | 6                             | Yes            |
| P012       | Cigarettes Marlboro    | Tobacco         | 30               | 25               | 22                        | 8                             | Yes            |
| P013       | Ice Cream Sandwich     | Frozen Foods    | 42               | 20               | 35                        | 7                             | Yes            |
| P014       | Hot Dogs               | Ready-to-eat    | 25               | 15               | 30                        | -5                            | Yes            |
| P015       | Coffee 12oz cup        | Hot Beverages   | 150              | 100              | 135                       | 15                            | Yes            |
| P016       | Slushie Blue Raspberry | Cold Beverages  | 35               | 20               | 60                        | -25                           | Yes            |
| P017       | Hand Sanitizer 2oz     | Health & Beauty | 15               | 10               | 8                         | 7                             | Yes            |
| P018       | Aspirin 10ct           | Health & Beauty | 12               | 10               | 5                         | 7                             | Yes            |
| P019       | Lottery Tickets        | Misc            | 500              | 200              | 350                       | 150                           | Yes            |
| P020       | Phone Charger Cable    | Electronics     | 8                | 5                | 10                        | -2                            | Yes            |
```

## Critical Inventory Alert

The following items are projected to drop below minimum quantity or go into negative stock levels without immediate action:

```
| product_id | product_name             | current_quantity | minimum_quantity | expected_end_of_week | shortage |
|------------|--------------------------|------------------|------------------|----------------------|----------|
| P005       | Monster Energy 16oz      | 38               | 25               | -7                   | -32      |
| P010       | Beer (Local) 6-pack      | 28               | 15               | -2                   | -17      |
| P014       | Hot Dogs                 | 25               | 15               | -5                   | -20      |
| P016       | Slushie Blue Raspberry   | 35               | 20               | -25                  | -45      |
| P020       | Phone Charger Cable      | 8                | 5                | -2                   | -7       |
```

## Sales Forecast

```
| product_id | product_name            | avg_weekly_sales | forecast_this_week | percent_change | forecast_reason                                    |
|------------|-------------------------|------------------|--------------------|-----------------|----------------------------------------------------|
| P001       | Coca-Cola 12oz          | 75               | 85                 | +13%           | Baseball tournament weekend                        |
| P002       | Pepsi 12oz              | 55               | 60                 | +9%            | Baseball tournament weekend                        |
| P003       | Bottled Water 16oz      | 120              | 160                | +33%           | Heat wave forecasted + baseball tournament         |
| P004       | Red Bull 8oz            | 35               | 40                 | +14%           | Extended store hours for tournament weekend        |
| P005       | Monster Energy 16oz     | 32               | 45                 | +41%           | Extended store hours + baseball tournament         |
| P006       | Doritos Nacho           | 45               | 55                 | +22%           | Baseball tournament weekend                        |
| P007       | Lay's Classic           | 38               | 40                 | +5%            | Slight increase for tournament                     |
| P008       | Snickers               | 48               | 50                 | +4%            | Normal demand pattern                              |
| P009       | M&Ms Peanut            | 50               | 65                 | +30%           | Baseball tournament + promotional display          |
| P010       | Beer (Local) 6-pack    | 25               | 30                 | +20%           | Heat wave forecasted + weekend sales               |
| P013       | Ice Cream Sandwich     | 30               | 35                 | +17%           | Heat wave forecasted                               |
| P014       | Hot Dogs               | 20               | 30                 | +50%           | Baseball tournament special promotion              |
| P016       | Slushie Blue Raspberry | 40               | 60                 | +50%           | Heat wave forecasted + baseball tournament         |
| P019       | Lottery Tickets        | 320              | 350                | +9%            | Jackpot increase announced                         |
| P020       | Phone Charger Cable    | 6                | 10                 | +67%           | Tourism increase due to baseball tournament        |
```

## Local Events Calendar

```
| event_id | event_name                     | date       | expected_attendance | location_distance_from_store | products_affected                                     | expected_sales_impact |
|----------|--------------------------------|------------|---------------------|-----------------------------|------------------------------------------------------|----------------------|
| E001     | Youth Baseball Tournament      | 2023-07-15 | 2500                | 0.5 miles                   | P001, P002, P003, P005, P006, P009, P014, P016, P020 | High                 |
| E002     | Youth Baseball Tournament      | 2023-07-16 | 2500                | 0.5 miles                   | P001, P002, P003, P005, P006, P009, P014, P016, P020 | High                 |
| E003     | Community College Orientation  | 2023-07-18 | 300                 | 1.2 miles                   | P001, P002, P003, P004, P005, P006, P007             | Medium               |
| E004     | Local Business Expo            | 2023-07-19 | 450                 | 0.8 miles                   | P003, P015                                           | Low                  |
| E005     | Summer Night Market            | 2023-07-21 | 1200                | 2.0 miles                   | P010, P011                                           | Low                  |
```

## Weather Forecast

```
| date       | day_of_week | high_temp | low_temp | conditions      | products_affected                                    | expected_sales_impact |
|------------|-------------|-----------|----------|-----------------|------------------------------------------------------|----------------------|
| 2023-07-15 | Saturday    | 95°F      | 76°F     | Hot, Sunny      | P003, P010, P013, P016                               | High                 |
| 2023-07-16 | Sunday      | 97°F      | 78°F     | Hot, Sunny      | P003, P010, P013, P016                               | High                 |
| 2023-07-17 | Monday      | 94°F      | 75°F     | Hot, Partly Cloudy | P003, P010, P013, P016                           | High                 |
| 2023-07-18 | Tuesday     | 92°F      | 74°F     | Hot, Partly Cloudy | P003, P010, P013, P016                           | High                 |
| 2023-07-19 | Wednesday   | 88°F      | 72°F     | Warm, Partly Cloudy | P003, P016                                      | Medium               |
| 2023-07-20 | Thursday    | 85°F      | 70°F     | Mild, Cloudy    | None                                                 | Low                  |
| 2023-07-21 | Friday      | 82°F      | 68°F     | Mild, 30% Rain  | P015                                                | Low                  |
```

## Supplier Information

```
| supplier_id | supplier_name         | products_supplied                            | lead_time_days | next_delivery_date | order_cutoff_date |
|-------------|-----------------------|---------------------------------------------|----------------|--------------------|--------------------|
| S001        | Metro Beverages       | P001, P002, P003, P004, P005                | 2              | 2023-07-17         | 2023-07-15         |
| S002        | SnackMaster Dist.     | P006, P007, P008, P009                      | 3              | 2023-07-18         | 2023-07-15         |
| S003        | AlcoBev Wholesale     | P010, P011                                  | 4              | 2023-07-20         | 2023-07-16         |
| S004        | Tobacco Direct        | P012                                        | 2              | 2023-07-17         | 2023-07-15         |
| S005        | FrozenQuick           | P013                                        | 1              | 2023-07-16         | 2023-07-15         |
| S006        | FastFood Suppliers    | P014                                        | 2              | 2023-07-18         | 2023-07-16         |
| S007        | Hot Beans Coffee      | P015                                        | 3              | 2023-07-19         | 2023-07-16         |
| S008        | Arctic Refreshments   | P016                                        | 3              | 2023-07-18         | 2023-07-15         |
| S009        | Health Essentials     | P017, P018                                  | 4              | 2023-07-20         | 2023-07-16         |
| S010        | Tech & More           | P020                                        | 5              | 2023-07-21         | 2023-07-16         |
```

## Active Promotions

```
| promotion_id | promotion_name                       | start_date | end_date   | products_included                        | expected_sales_lift |
|--------------|-------------------------------------|------------|------------|-----------------------------------------|---------------------|
| PR001        | Summer Refreshment - 2 for $3       | 2023-07-15 | 2023-07-21 | P003                                    | +40%                |
| PR002        | Energy Boost - $1 off               | 2023-07-15 | 2023-07-18 | P004, P005                              | +25%                |
| PR003        | Baseball Special - Hot Dog Bundle   | 2023-07-15 | 2023-07-16 | P014, P002                              | +45%                |
| PR004        | Loyalty Card Double Points          | 2023-07-17 | 2023-07-21 | All products                            | +10%                |
| PR005        | App Download - Free Coffee          | 2023-07-19 | 2023-07-21 | P015                                    | +30%                |
```

## Historical Sales Comparison

```
| week_beginning | total_sales | top_categories                  | seasonal_notes                                                |
|----------------|-------------|--------------------------------|---------------------------------------------------------------|
| 2023-06-18     | $12,450     | Beverages, Snacks, Tobacco     | Normal summer pattern                                         |
| 2023-06-25     | $13,200     | Beverages, Snacks, Alcohol     | Beginning of summer vacation increase                         |
| 2023-07-02     | $15,780     | Beverages, Alcohol, Snacks     | July 4th holiday boost                                        |
| 2023-07-09     | $12,980     | Beverages, Snacks, Ready-to-eat| Post-holiday return to normal with slight summer boost        |
| 2022-07-10     | $13,450     | Beverages, Snacks, Cold Beverages | Similar week last year - baseball tournament boosted sales |
```

## Ordering Recommendations

1. **Urgent Orders Required** (Order Today - July 14):
   * Monster Energy 16oz (P005): Increase order by at least 32 units
   * Beer (Local) 6-pack (P010): Increase order by at least 17 units
   * Hot Dogs (P014): Increase order by at least 20 units
   * Slushie Blue Raspberry (P016): Increase order by at least 45 units
   * Phone Charger Cable (P020): Increase order by at least 7 units

2. **Weather Impact Adjustments**:
   * Increase bottled water (P003) order by 40% due to heat wave
   * Increase ice cream (P013) order by 25% due to heat wave
   * Consider reducing hot coffee (P015) order by 10% due to hot weather

3. **Event Impact Adjustments**:
   * Increase snacks (P006, P007, P009) order by 20% for baseball tournament
   * Increase sports/energy drinks by 30% for tournament weekend

## Urgent Action Items
* Place rush orders for all items in the Critical Inventory Alert section
* Ensure adequate staffing for the busier weekend due to baseball tournament
* Set up promotional displays for Baseball Special bundle near entrance
* Ensure slushie machine is operating at full capacity for heat wave demand
