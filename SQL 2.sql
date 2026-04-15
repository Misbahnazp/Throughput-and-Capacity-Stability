CREATE DATABASE IF NOT EXISTS manufacturing_project;

USE manufacturing_project;

DROP TABLE IF EXISTS capacity_stability_2025;
DROP TABLE IF EXISTS file;

CREATE TABLE file (
    Timestamp DATETIME,
    MachineID INT,
    Plant VARCHAR(50),
    Temperature DOUBLE,
    Vibration DOUBLE,
    Pressure DOUBLE,
    EnergyConsumption DOUBLE,
    ProductionUnits INT,
    DefectCount INT,
    MaintenanceFlag INT
);

LOAD DATA LOCAL INFILE
'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\file.csv'
INTO TABLE file
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(@Timestamp,
 MachineID,
 Plant,
 Temperature,
 Vibration,
 Pressure,
 EnergyConsumption,
 ProductionUnits,
 DefectCount,
 MaintenanceFlag)
SET Timestamp = STR_TO_DATE(@Timestamp, '%d-%m-%Y %H:%i');

SELECT COUNT(*) AS TotalRows FROM file;

CREATE TABLE capacity_stability_2025 (
    MachineID INT,
    Plant VARCHAR(50),
    AvgOutput DECIMAL(10,2),
    StdOutput DECIMAL(10,2),
    CV_Output DECIMAL(10,2),
    MaintenanceCount INT,
    DefectCountTotal INT
);

INSERT INTO capacity_stability_2025
SELECT
    MachineID,
    Plant,
    AVG(ProductionUnits),
    STDDEV(ProductionUnits),
    (STDDEV(ProductionUnits) / AVG(ProductionUnits)) * 100,
    SUM(MaintenanceFlag),
    SUM(DefectCount)
FROM file
GROUP BY MachineID, Plant;

SELECT * FROM capacity_stability_2025;
