import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Mean spot
results = [['Call', '2023-10-26', 10, -6.80000000000004], ['Put', '2023-10-26', 6, 7.300000000000011], ['Call', '2023-10-27', 0, 0], ['Put', '2023-10-27', 1, 3.9499999999999886], ['Call', '2023-10-30', 6, 25.900000000000063], ['Put', '2023-10-30', 4, 0.700000000000017], ['Call', '2023-10-31', 6, 12.499999999999943], ['Put', '2023-10-31', 2, 9.59999999999998], ['Call', '2023-11-01', 0, 2.3000000000000016], ['Put', '2023-11-01', 1, 19.799999999999983], ['Call', '2023-11-02', 11, 16.09999999999991], ['Put', '2023-11-02', 4, 3.900000000000034], ['Call', '2023-11-03', 1, 9.799999999999955], ['Put', '2023-11-03', 4, -6.600000000000023], ['Call', '2023-11-06', 2, -0.8000000000000114], ['Put', '2023-11-06', 2, 10.799999999999983], ['Call', '2023-11-07', 7, 2.150000000000013], ['Put', '2023-11-07', 3, 15.299999999999983], ['Call', '2023-11-08', 2, -0.399999999999995], ['Put', '2023-11-08', 2, 0.950000000000017], ['Call', '2023-11-09', 1, 13.050000000000011], ['Put', '2023-11-09', 4, -8.299999999999983], ['Call', '2023-11-10', 1, 0.05000000000001137], ['Put', '2023-11-10', 3, -1.8500000000000085], ['Call', '2023-11-13', 3, 11.150000000000006], ['Put', '2023-11-13', 5, 11.849999999999952], ['Call', '2023-11-15', 0, 1.1000000000000014], ['Put', '2023-11-15', 0, 4.150000000000006], ['Call', '2023-11-16', 0, 0], ['Put', '2023-11-16', 4, 0.3999999999999915], ['Call', '2023-11-17', 1, -1.6999999999999886], ['Put', '2023-11-17', 5, 43.19999999999999], ['Call', '2023-11-20', 6, 17.150000000000006], ['Put', '2023-11-20', 2, -3.799999999999983], ['Call', '2023-11-21', 3, 4.549999999999983], ['Put', '2023-11-21', 2, 2.75], ['Call', '2023-11-22', 0, 0], ['Put', '2023-11-22', 1, 9.299999999999983], ['Call', '2023-11-23', 2, 0.19999999999998863], ['Put', '2023-11-23', 1, 6.30000000000004], ['Call', '2023-11-24', 6, 27.50000000000003], ['Put', '2023-11-24', 4, -0.10000000000002274], ['Call', '2023-11-28', 5, 2.59999999999998], ['Put', '2023-11-28', 1, 0.3499999999999943], ['Call', '2023-11-29', 9, 48.40000000000005], ['Put', '2023-11-29', 5, 5.20000000000001], ['Call', '2023-11-30', 3, -0.7999999999999545], ['Put', '2023-11-30', 11, 7.599999999999909], ['Call', '2023-12-01', 1, -3.400000000000034], ['Put', '2023-12-01', 2, -1.3000000000000398], ['Call', '2023-12-04', 6, 9.650000000000091], ['Put', '2023-12-04', 1, 13.149999999999977], ['Call', '2023-12-05', 5, 0.1500000000000341], ['Put', '2023-12-05', 6, -1.0000000000000426], ['Call', '2023-12-06', 4, 37.8], ['Put', '2023-12-06', 2, 1.3500000000000085], ['Call', '2023-12-07', 1, 0.05000000000001137], ['Put', '2023-12-07', 1, -1.7000000000000455], ['Call', '2023-12-08', 0, 8.349999999999966], ['Put', '2023-12-08', 3, 24.900000000000034], ['Call', '2023-12-11', 2, 6.2999999999999545], ['Put', '2023-12-11', 6, 16.599999999999994], ['Call', '2023-12-12', 0, 6.5], ['Put', '2023-12-12', 8, 9.249999999999986], ['Call', '2023-12-13', 0, 0], ['Put', '2023-12-13', 1, -2.450000000000017], ['Call', '2023-12-14', 1, 13.75], ['Put', '2023-12-14', 2, -2.0000000000000284], ['Call', '2023-12-18', 3, 6.949999999999989], ['Put', '2023-12-18', 7, -5.500000000000028], ['Call', '2023-12-19', 7, 5.849999999999994], ['Put', '2023-12-19', 1, 4.099999999999994], ['Call', '2023-12-20', 5, 2.450000000000074], ['Put', '2023-12-20', 0, 0]]

# Normal spot ATM
results = [['Call', '2023-08-10', 3, 9.049999999999983],['Put', '2023-08-10', 2, 54.24999999999994],['Call', '2023-08-11', 1, 21.650000000000006],['Put', '2023-08-11', 2, -1.8999999999999773],['Call', '2023-08-14', 2, 13.649999999999991],['Put', '2023-08-14', 2, 8.100000000000023],['Call', '2023-08-16', 3, 4.799999999999997],['Put', '2023-08-16', 4, 6.650000000000034],['Call', '2023-08-17', 1, -0.6499999999999773],['Put', '2023-08-17', 1, 14.450000000000017],['Call', '2023-08-18', 5, -5.700000000000017],['Put', '2023-08-18', 1, -1.9000000000000057],['Call', '2023-08-21', 1, 0.4499999999999602],['Put', '2023-08-21', 0, 3.3500000000000085],['Call', '2023-08-22', 0, 0],['Put', '2023-08-22', 0, 5.349999999999994],['Call', '2023-08-23', 7, 5.749999999999972],['Put', '2023-08-23', 3, -1.2000000000000028],['Call', '2023-08-24', 4, 30.049999999999955],['Put', '2023-08-24', 0, 0],['Call', '2023-08-25', 2, 4.350000000000023],['Put', '2023-08-25', 0, 0],['Call', '2023-08-28', 2, 7.9500000000000455],['Put', '2023-08-28', 1, 1.6500000000000057],['Call', '2023-08-29', 0, 0],['Put', '2023-08-29', 2, -0.8499999999999943],['Call', '2023-08-30', 2, -1.5500000000000256],['Put', '2023-08-30', 5, 12.749999999999972],['Call', '2023-08-31', 2, -1.1499999999999986],['Put', '2023-08-31', 3, -4.950000000000017],['Call', '2023-09-01', 4, -2.349999999999852],['Put', '2023-09-01', 2, 12.849999999999966],['Call', '2023-09-04', 2, -6.549999999999898],['Put', '2023-09-04', 5, -1.5999999999999375],['Call', '2023-09-05', 3, 5.600000000000037],['Put', '2023-09-05', 4, -5.9500000000000455],['Call', '2023-09-06', 1, -0.050000000000000266],['Put', '2023-09-06', 2, 11.199999999999989],['Call', '2023-09-07', 1, 5.7000000000000455],['Put', '2023-09-07', 0, 0],['Call', '2023-09-08', 8, 49.70000000000002],['Put', '2023-09-08', 5, 7.400000000000006],['Call', '2023-09-11', 10, 8.049999999999955],['Put', '2023-09-11', 5, 4.1499999999999915],['Call', '2023-09-12', 0, 5.550000000000011],['Put', '2023-09-12', 3, 20.649999999999977],['Call', '2023-09-13', 3, 22.05000000000001],['Put', '2023-09-13', 0, 0],['Call', '2023-09-14', 1, 0.75],['Put', '2023-09-14', 4, -2.650000000000034],['Call', '2023-09-15', 4, 16.249999999999943],['Put', '2023-09-15', 1, 2.0],['Call', '2023-09-18', 5, 7.550000000000026],['Put', '2023-09-18', 4, 20.150000000000034],['Call', '2023-09-20', 0, 1.4500000000000028],['Put', '2023-09-20', 4, 8.399999999999977],['Call', '2023-09-21', 6, 2.4499999999999886],['Put', '2023-09-21', 4, 16.850000000000023],['Call', '2023-09-22', 0, 23.149999999999977],['Put', '2023-09-22', 6, 15.549999999999955],['Call', '2023-09-25', 3, -3.049999999999926],['Put', '2023-09-25', 5, 5.149999999999977],['Call', '2023-09-26', 7, -6.700000000000017],['Put', '2023-09-26', 1, 30.099999999999994],['Call', '2023-09-27', 7, 55.750000000000014],['Put', '2023-09-27', 3, 13.200000000000045],['Call', '2023-09-28', 3, 2.842170943040401e-14],['Put', '2023-09-28', 4, 5.400000000000034],['Call', '2023-09-29', 2, 2.5500000000000114],['Put', '2023-09-29', 3, 0.30000000000001137],['Call', '2023-10-03', 6, 7.999999999999986],['Put', '2023-10-03', 7, 3.099999999999966],['Call', '2023-10-04', 0, 0],['Put', '2023-10-04', 2, 31.000000000000057],['Call', '2023-10-05', 1, -3.3000000000000114],['Put', '2023-10-05', 2, 1.4000000000000057],['Call', '2023-10-06', 3, -10.249999999999943],['Put', '2023-10-06', 3, 1.5000000000000142],['Call', '2023-10-09', 5, 2.3999999999999915],['Put', '2023-10-09', 3, -1.9999999999999432],['Call', '2023-10-10', 7, 31.099999999999852],['Put', '2023-10-10', 1, 1.749999999999993],['Call', '2023-10-11', 2, -0.8500000000000085],['Put', '2023-10-11', 0, 0.8000000000000007],['Call', '2023-10-12', 0, -10.800000000000011],['Put', '2023-10-12', 3, -0.799999999999983],['Call', '2023-10-13', 1, 1.200000000000017],['Put', '2023-10-13', 1, 0.35000000000002274],['Call', '2023-10-16', 2, 9.050000000000011],['Put', '2023-10-16', 1, -0.14999999999997726],['Call', '2023-10-17', 4, -1.349999999999966],['Put', '2023-10-17', 1, 2.54999999999999],['Call', '2023-10-18', 0, 2.200000000000003],['Put', '2023-10-18', 1, 7.100000000000023],['Call', '2023-10-19', 3, -3.9499999999999886],['Put', '2023-10-19', 6, 60.75000000000006],['Call', '2023-10-20', 1, -1.3000000000000114],['Put', '2023-10-20', 0, 0],['Call', '2023-10-23', 1, -2.25],['Put', '2023-10-23', 3, 13.450000000000045],['Call', '2023-10-25', 5, 8.849999999999994],['Put', '2023-10-25', 3, -7.299999999999983],['Call', '2023-10-26', 7, 15.599999999999966], ['Put', '2023-10-26', 5, 27.199999999999875], ['Call', '2023-10-27', 2, 15.350000000000023], ['Put', '2023-10-27', 3, 8.899999999999991], ['Call', '2023-10-30', 3, 0.9000000000000483], ['Put', '2023-10-30', 3, 1.5500000000000824], ['Call', '2023-10-31', 10, 20.55000000000001], ['Put', '2023-10-31', 4, -8.749999999999943], ['Call', '2023-11-01', 0, 2.3000000000000016], ['Put', '2023-11-01', 1, 19.799999999999983], ['Call', '2023-11-02', 2, 14.850000000000023], ['Put', '2023-11-02', 3, 2.34999999999998], ['Call', '2023-11-03', 0, 0], ['Put', '2023-11-03', 1, -1.0], ['Call', '2023-11-06', 0, 0], ['Put', '2023-11-06', 0, 8.350000000000009], ['Call', '2023-11-07', 7, 2.150000000000013], ['Put', '2023-11-07', 3, 15.299999999999983], ['Call', '2023-11-08', 2, -0.399999999999995], ['Put', '2023-11-08', 2, 0.950000000000017], ['Call', '2023-11-09', 1, 13.050000000000011], ['Put', '2023-11-09', 4, -8.299999999999983], ['Call', '2023-11-10', 1, 0.05000000000001137], ['Put', '2023-11-10', 3, -1.8500000000000085], ['Call', '2023-11-13', 3, 16.14999999999999], ['Put', '2023-11-13', 5, -8.950000000000045], ['Call', '2023-11-15', 3, 2.999999999999943], ['Put', '2023-11-15', 1, 0.09999999999999953], ['Call', '2023-11-16', 2, 4.500000000000057], ['Put', '2023-11-16', 3, 2.2499999999999716], ['Call', '2023-11-17', 2, 7.09999999999998], ['Put', '2023-11-17', 5, 25.549999999999955], ['Call', '2023-11-20', 6, 17.150000000000006], ['Put', '2023-11-20', 2, -3.799999999999983], ['Call', '2023-11-21', 3, 4.549999999999983], ['Put', '2023-11-21', 2, 2.75], ['Call', '2023-11-22', 0, 0], ['Put', '2023-11-22', 3, 33.099999999999966], ['Call', '2023-11-23', 2, -2.0499999999999545], ['Put', '2023-11-23', 1, -0.4000000000000057], ['Call', '2023-11-24', 8, 13.200000000000102], ['Put', '2023-11-24', 4, 0.8999999999999488], ['Call', '2023-11-28', 2, 4.650000000000006], ['Put', '2023-11-28', 3, 4.950000000000003], ['Call', '2023-11-29', 6, 98.94999999999993], ['Put', '2023-11-29', 0, 0.4499999999999993], ['Call', '2023-11-30', 3, -0.7999999999999545], ['Put', '2023-11-30', 11, 7.599999999999909], ['Call', '2023-12-01', 2, -5.899999999999977], ['Put', '2023-12-01', 1, 4.050000000000011], ['Call', '2023-12-04', 1, 26.09999999999991], ['Put', '2023-12-04', 1, 0.9999999999999982], ['Call', '2023-12-05', 6, 11.950000000000045], ['Put', '2023-12-05', 5, 2.5], ['Call', '2023-12-06', 0, 8.049999999999997], ['Put', '2023-12-06', 7, 28.049999999999955], ['Call', '2023-12-07', 0, 10.150000000000034], ['Put', '2023-12-07', 4, 11.449999999999989], ['Call', '2023-12-08', 1, -1.6999999999999886], ['Put', '2023-12-08', 4, 16.700000000000017], ['Call', '2023-12-11', 2, 6.2999999999999545], ['Put', '2023-12-11', 6, 16.599999999999994], ['Call', '2023-12-12', 3, -13.400000000000006], ['Put', '2023-12-12', 6, -2.3999999999999773], ['Call', '2023-12-13', 2, 3.4499999999999993], ['Put', '2023-12-13', 2, 1.9999999999999716], ['Call', '2023-12-14', 4, -5.299999999999841], ['Put', '2023-12-14', 2, -0.6499999999999915], ['Call', '2023-12-15', 3, -4.89999999999992], ['Call', '2023-12-18', 3, 6.949999999999989], ['Put', '2023-12-18', 7, -5.500000000000028], ['Call', '2023-12-19', 7, 5.849999999999994], ['Put', '2023-12-19', 1, 4.099999999999994], ['Call', '2023-12-20', 1, -0.5499999999999972], ['Put', '2023-12-20', 3, 20.79999999999999],['Call', '2023-12-21', 6, 21.400000000000034],['Put', '2023-12-21', 0, 6.800000000000011],['Call', '2023-12-22', 3, -4.649999999999977],['Put', '2023-12-22', 9, 37.10000000000008],['Call', '2023-12-26', 5, 29.049999999999955],['Put', '2023-12-26', 3, 18.099999999999994],['Call', '2023-12-27', 5, 39.39999999999998],['Put', '2023-12-27', 1, 14.7],['Call', '2023-12-28', 1, 58.19999999999999],['Put', '2023-12-28', 0, 0],['Call', '2023-12-29', 4, 16.200000000000017],['Put', '2023-12-29', 2, 0.39999999999997726],['Call', '2024-01-01', 5, 12.299999999999955],['Put', '2024-01-01', 1, 16.099999999999994],['Call', '2024-01-02', 3, 0.549999999999983],['Put', '2024-01-02', 1, 56.80000000000001],['Call', '2024-01-04', 6, 56.00000000000023],['Put', '2024-01-04', 0, 0],['Call', '2024-01-05', 2, 0.39999999999997726],['Put', '2024-01-05', 4, -1.0500000000000114],['Call', '2024-01-08', 0, 4.200000000000017],['Put', '2024-01-08', 19, 53.10000000000019],['Call', '2024-01-09', 4, 32.10000000000002],['Put', '2024-01-09', 4, 9.049999999999969],['Call', '2024-01-10', 0, 0],['Put', '2024-01-10', 0, 8.199999999999996],['Call', '2024-01-11', 5, 4.0499999999999545],['Put', '2024-01-11', 5, 26.349999999999966],['Call', '2024-01-12', 3, -3.349999999999966],['Put', '2024-01-12', 0, 4.899999999999977],['Call', '2024-01-15', 2, -2.8000000000000114],['Put', '2024-01-15', 1, -0.5499999999999972]]

results = [['Call', '2023-11-30', 42, 20.10000000000008], ['Put', '2023-11-30', 65, 14.500000000000028], ['Call', '2023-12-01', 93, 29.349999999999454], ['Put', '2023-12-01', 59, -23.250000000000057], ['Call', '2023-12-04', 101, 642.5499999999992], ['Put', '2023-12-04', 38, -2.9500000000000064], ['Call', '2023-12-05', 72, 62.550000000000125], ['Put', '2023-12-05', 40, 5.0], ['Call', '2023-12-06', 41, 5.350000000000011], ['Put', '2023-12-06', 54, -14.300000000000082], ['Call', '2023-12-07', 44, 3.099999999999909], ['Put', '2023-12-07', 45, 14.300000000000352], ['Call', '2023-12-08', 40, 1.299999999999784], ['Put', '2023-12-08', 57, 22.050000000000026], ['Call', '2023-12-11', 44, -21.39999999999992], ['Put', '2023-12-11', 40, 9.699999999999818], ['Call', '2023-12-12', 36, 10.499999999999858], ['Put', '2023-12-12', 37, 8.950000000000045], ['Call', '2023-12-13', 45, 15.450000000000003], ['Put', '2023-12-13', 52, -33.499999999999964], ['Call', '2023-12-14', 89, -75.59999999999991], ['Put', '2023-12-14', 68, -17.29999999999987], ['Call', '2023-12-15', 57, -10.899999999999977], ['Call', '2023-12-18', 36, 14.799999999999926], ['Put', '2023-12-18', 38, 20.700000000000017], ['Call', '2023-12-19', 55, 3.500000000000057], ['Put', '2023-12-19', 44, -44.94999999999996], ['Call', '2023-12-20', 34, -4.050000000000028], ['Put', '2023-12-20', 49, -11.199999999999946], ['Call', '2023-12-21', 36, 37.35000000000011], ['Put', '2023-12-21', 36, -37.60000000000019], ['Call', '2023-12-22', 56, 41.15000000000009], ['Put', '2023-12-22', 50, 35.74999999999994], ['Call', '2023-12-26', 28, 68.35000000000025], ['Put', '2023-12-26', 45, 4.0], ['Call', '2023-12-27', 55, 125.10000000000008], ['Put', '2023-12-27', 45, 3.7999999999999616], ['Call', '2023-12-28', 53, -4.750000000000568], ['Put', '2023-12-28', 60, -43.599999999999994], ['Call', '2023-12-29', 61, 5.199999999999818], ['Put', '2023-12-29', 57, -3.3999999999999204], ['Call', '2024-01-01', 78, 51.10000000000005], ['Put', '2024-01-01', 47, -26.250000000000057], ['Call', '2024-01-02', 69, 0.5499999999999936], ['Put', '2024-01-02', 54, 73.34999999999991], ['Call', '2024-01-04', 74, 164.84999999999957], ['Put', '2024-01-04', 65, -26.950000000000003], ['Call', '2024-01-05', 63, -38.45000000000002], ['Put', '2024-01-05', 74, 51.99999999999997], ['Call', '2024-01-08', 53, -27.599999999999966], ['Put', '2024-01-08', 51, 174.65000000000003], ['Call', '2024-01-09', 76, -35.050000000000146], ['Put', '2024-01-09', 79, 8.849999999999937], ['Call', '2024-01-10', 127, 77.59999999999985], ['Put', '2024-01-10', 76, 0.4999999999999698], ['Call', '2024-01-11', 96, -62.00000000000017], ['Put', '2024-01-11', 111, -52.55000000000018], ['Call', '2024-01-12', 95, -121.4999999999996], ['Put', '2024-01-12', 73, -53.59999999999988], ['Call', '2024-01-15', 87, -16.149999999999807], ['Put', '2024-01-15', 90, -25.150000000000063], ['Call', '2024-01-16', 97, -90.74999999999983], ['Put', '2024-01-16', 102, -107.44999999999996], ['Call', '2024-01-17', 47, -1.6499999999999941], ['Put', '2024-01-17', 101, 553.5999999999997], ['Call', '2024-01-18', 60, 29.649999999999977], ['Put', '2024-01-18', 45, -36.90000000000026]]

call_pnl = []
put_pnl = []
sum_pnl = []
prof_list = []
loss_list = []
for result in results:
    if result[0] == 'Call':
        # if (result[3] > 0 and result[3]<5):
        #     tmp = 0
        # else:
        #     tmp = result[3] 
        # if(tmp>0):
        #     prof_list.append(tmp)
        # elif(tmp<=0):
        #     loss_list.append(tmp)
        # tmp = result[3] - (7/15)*result[2]
        tmp = result[3]
        call_pnl.append(tmp)
    elif result[0] == 'Put':
        # if (result[3] > 0 and result[3]<5):
        #     tmp2 = 0
        # else:
        #     tmp2 = result[3] 
        # tmp2 = result[3] - (7/15)*result[2]
        tmp2 = result[3]
        put_pnl.append(tmp)
        # put_pnl.append(result[3])
        if(tmp + tmp2>200):
            continue
        if(tmp + tmp2>0):
            prof_list.append(tmp + tmp2)
        elif(tmp + tmp2<=0):
            loss_list.append(tmp + tmp2)
        sum_pnl.append(tmp + tmp2)
print("Net sum:",sum(sum_pnl))
print("average profit per day:",sum(sum_pnl)/len(sum_pnl))
# print(sum(call_pnl)/len(call_pnl), sum(put_pnl)/len(put_pnl), sum(sum_pnl)/len(sum_pnl))
print("Percentage profitable trades:",len(prof_list)/len(sum_pnl),"average profit:", sum(prof_list)/len(prof_list),"Average loss:", sum(loss_list)/len(loss_list))
print("No of days:",len(sum_pnl))

plt.hist(sum_pnl, bins=20)
plt.show()