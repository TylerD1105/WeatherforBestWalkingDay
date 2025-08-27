
def findClosest(target, daily_apparent_temperature_mean, daily_rain_sum):
    differences = {}
    for i in range(7):
        current = daily_apparent_temperature_mean[i] - target
        if daily_rain_sum[i] > 0:
            continue
        if current < 0:
            current = current * -1
        differences[i] = current
    
    if len(differences) == 0:
        return -1
    else:
        return min(differences, key = differences.get)
    
            
        
            