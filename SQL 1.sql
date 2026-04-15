CREATE DATABASE IF NOT EXISTS production_analysis;
USE production_analysis;

DROP TABLE IF EXISTS production_data;

CREATE TABLE production_data (
    Timestamp DATETIME,
    MachineID INT,
    Plant VARCHAR(50),
    Temperature FLOAT,
    Vibration FLOAT,
    Pressure FLOAT,
    EnergyConsumption FLOAT,
    ProductionUnits INT,
    DefectCount INT,
    MaintenanceFlag INT
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/file.csv'
INTO TABLE production_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    Timestamp,
    MachineID,
    Plant,
    Temperature,
    Vibration,
    Pressure,
    EnergyConsumption,
    ProductionUnits,
    DefectCount,
    MaintenanceFlag
);

SELECT * FROM production_data LIMIT 10;

SELECT 
    Plant,
    DATE(Timestamp) AS Date,
    HOUR(Timestamp) AS Hour,
    SUM(ProductionUnits) AS Total_Production
FROM production_data
GROUP BY Plant, Date, Hour
ORDER BY Plant, Date, Hour;

SELECT 
    Plant,
    DATE(Timestamp) AS Date,
    SUM(ProductionUnits) AS Daily_Production
FROM production_data
GROUP BY Plant, Date
ORDER BY Plant, Date;

SELECT 
    MachineID,
    AVG(ProductionUnits) AS Avg_Production,
    SUM(MaintenanceFlag) AS Maintenance_Count
FROM production_data
GROUP BY MachineID
ORDER BY Avg_Production ASC
LIMIT 10;