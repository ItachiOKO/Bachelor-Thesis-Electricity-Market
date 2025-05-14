from config_cost import (
    SPECIFIC_BATTERY_INVEST,
    SPECIFIC_INVERTER_INVEST,
    SPECIFIC_TRANSFORMER_INVEST,
    SPECIFIC_CONSTRUCTION_ALLOWANCE_INVEST,
    SPECIFIC_GRID_CONNECTION_INVEST,
    INSURANCE_RATE,
    SPECIFIC_TECHNICAL_MANAGEMENT_COST,  
    SPECIFIC_MAINTENANCE_COST,
    SPECIFIC_REPAIRS_COST,
    SPECIFIC_MEASUREMENTS_COST,
    ACCOUNTING_COST,
    DEPRECIATION_YEARS,

)

from config import BATTERY_CAPACITY, SYSTEM_POWER


def calculate_investment_costs():
    battery_cost = SPECIFIC_BATTERY_INVEST * BATTERY_CAPACITY
    inverter_cost = SPECIFIC_INVERTER_INVEST * SYSTEM_POWER 
    transformer_cost = SPECIFIC_TRANSFORMER_INVEST * SYSTEM_POWER
    construction_allowance = SPECIFIC_CONSTRUCTION_ALLOWANCE_INVEST * SYSTEM_POWER
    grid_connection_cost = SPECIFIC_GRID_CONNECTION_INVEST * SYSTEM_POWER

    total_invest = (
        battery_cost + inverter_cost + transformer_cost +
        construction_allowance + grid_connection_cost
    )
    
    return total_invest


def calculate_annual_cost():
    total_invest = calculate_investment_costs()
    insurance_cost = INSURANCE_RATE * (total_invest - SPECIFIC_CONSTRUCTION_ALLOWANCE_INVEST * SYSTEM_POWER) # nur Hardware wird versichert
    technical_management_cost = SPECIFIC_TECHNICAL_MANAGEMENT_COST * SYSTEM_POWER
    maintenance_cost = SPECIFIC_MAINTENANCE_COST * SYSTEM_POWER
    repairs_cost = SPECIFIC_REPAIRS_COST * SYSTEM_POWER
    measurements_cost = SPECIFIC_MEASUREMENTS_COST * SYSTEM_POWER
    accounting_cost = ACCOUNTING_COST

    total_annual_costs = (
        insurance_cost + technical_management_cost + maintenance_cost +
        repairs_cost + measurements_cost + accounting_cost
    )
    
    return total_annual_costs


def calculate_depreciation_amount():
    total_invest = calculate_investment_costs()
    annual_cost = calculate_annual_cost()
    return (total_invest / DEPRECIATION_YEARS) + annual_cost