
import sys
import numpy as np
import math

# test
# INPUT PARAMETERS HERE
def get_parameters():

    # input options
    use_altitude = 'y' # default inputs are in altitude, select 'n' to use distance from center of earth instead

    # initial orbit of tug 
    start = 400 * 1000 # [m]

    # orbit of target vessel
    pickup = 600 * 1000 # [m]

    # drop off destination
    destination = 400 * 1000 # [m]

    # return home
    returnHome = 'n' # [y/n]

    # Isp of engine
    Isp = 2000 # [seconds]

    # Mass of tug
    m = 250 # [kg]

    # mass of target vessel
    target_m = 200 # [kg]

   
        
    if use_altitude == 'y':
        earth_radius = 6378 * 1000 # [m]
        start = start + earth_radius
        pickup = pickup + earth_radius
        destination = destination + earth_radius


    return start, pickup, destination, returnHome, Isp, m, target_m

def getGEO():
    return ((35786 + 6387) * 1000) - (6378 * 1000)
def getLEO():
    return ((600) * 1000) - (6378 * 1000)
def getGRV():
    return (getGEO() + (300 * 1000))



# returns required delta V for hohmann transfer given inital and final distance away from center of earth
# inputs, r1: starting distance away from center of earth (meters), r2: final distance (meters)
# outputs, dv1: delta V of first leg (meters/second), dv2: delta V of second leg (meters/second)

# TODO: potentiall convert from distance from center of earth to altitude
def get_delta_v(r1, r2):

    u = 3.986 * 10**14 # [m^3/s^2]
    v1 = math.sqrt(u/r1)
    dv1 = math.sqrt(u/r1) * (math.sqrt( (2*r2) / (r2+r1) ) - 1)
    v2 = (r1/r2) * (v1+dv1)
    dv2 = math.sqrt(u/r2) - v2
    return abs(dv1), abs(dv2)


# returns required dfuel mass for hohmann transfer given delta V requirements, Isp of engine, and mass of vehichle
# inputs, dv1: deltaV of first leg [m/s], dv2: deltaV of second leg [m/s], Isp: specific impulse of engine [seconds], m: mass of vehichle [kg]
def get_fuel_cost(dv1, dv2, Isp, m):

    g = 9.80665 # [m/s^2]
    dv_tot = dv1 + dv2
    exponent = (dv_tot) / (g * Isp)
    fuel = m * (math.exp(exponent) - 1)
    return fuel



def get_route_input():

    print('Tip: You can enter GEO, LEO, or GRV as a shortcut')
    start = parse_input(input("Enter inital orbit of space tug [km]: "))
    pickup = parse_input(input("Enter orbit of target [km]: "))
    destination = parse_input(input("Enter destination orbit [km]: "))
    while True: 
        returnHome = input("Do you wish to return tug to original starting location? [y/n]: ")
        if returnHome == 'y' or returnHome == 'n':
            break
        else:
            print("Input invalid: please try again")

    return start, pickup, destination, returnHome



def get_vehichle_details():

    Isp = input("Enter engine's specific impulse (seconds): ")
    Isp = float(Isp)
    m = input("Enter vehichle mass (kg): ")
    m = float(m)

    target_m = input("Enter target load's mass (kg): ")
    target_m = float(target_m)

    return Isp, m, target_m

def print_results(start, pickup, destination, returnHome, Isp, m, target_m, get_to_target_dv1, get_to_target_dv2, pickup_fuel, drop_off_dv1, drop_off_dv2, drop_off_fuel, return_dv1, return_dv2, return_fuel):

    earth_radius = 6378 # [km]

    print('\n')
    print("----------MISSION DETAILS----------")
    print("Inital tug location: ", (start/1000) - earth_radius, " [km]")
    print("Target location: ", (pickup/1000) - earth_radius, " [km]")
    print("Destination: ", (destination/1000) - earth_radius, " [km]")
    print('\n')
    print("Tug mass: ", m, " [kg]")
    print("Target mass: ", target_m, " [kg]")
    print("Total mass in transit: ", m + target_m, " [kg]")
    print('\n')
    print("----------Requirements----------")
    print('\n')

    print("-----------Pickup----------")
    print("Leg 1 deltaV: ", get_to_target_dv1, " [m/s]")
    print("Leg 2 deltaV: ", get_to_target_dv2, " [m/s]")
    print("Fuel mass: ", pickup_fuel, " [kg]")
    print('\n')

    print("----------Drop off----------")
    print("Leg 1 deltaV: ", drop_off_dv1, " [m/s]")
    print("Leg 2 deltaV: ", drop_off_dv2, " [m/s]")
    print("Fuel mass: ", drop_off_fuel, " [kg]")
    print('\n')

    if returnHome == 'y':
        print("----------Return----------")
        print("Leg 1 deltaV: ", return_dv1, " [m/s]")
        print("Leg 2 deltaV: ", return_dv2, " [m/s]")
        print("Fuel mass: ", return_fuel, " [kg]")
        print('\n')
    else: 
        return_fuel = 0
        return_dv1 = 0
        return_dv2 = 0

    print("----------Total----------")
    print("Total deltaV: ", get_to_target_dv1 + get_to_target_dv2 + drop_off_dv1 + drop_off_dv2 + return_dv1 + return_dv2, " [m/s]")
    print("Total fuel mass: ", pickup_fuel + drop_off_fuel + return_fuel, " [kg]")


if __name__ == "__main__":

    
    start, pickup, destination, returnHome, Isp, m, target_m = get_parameters()
    
    get_to_target_dv1, get_to_target_dv2 = get_delta_v(start, pickup)
    pickup_fuel = get_fuel_cost(get_to_target_dv1, get_to_target_dv2, Isp, m)

    drop_off_dv1, drop_off_dv2 = get_delta_v(pickup, destination)
    drop_off_fuel = get_fuel_cost(drop_off_dv1, drop_off_dv2, Isp, m + target_m )

    return_dv1, return_dv2 = get_delta_v(destination, start)
    return_fuel = get_fuel_cost(return_dv1, return_dv2, Isp, m)
    
    print_results(start, pickup, destination, returnHome, Isp, m, target_m, get_to_target_dv1, get_to_target_dv2, pickup_fuel, drop_off_dv1, drop_off_dv2, drop_off_fuel, return_dv1, return_dv2, return_fuel)

    

    