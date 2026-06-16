CREATE TABLE IF NOT EXISTS hardware_assets (
    assetName VARCHAR(100) NOT NULL, 
    assetType VARCHAR(50) NOT NULL,
    ipAddress VARCHAR(16) NOT NULL,
    assetStatus VARCHAR(20) NOT NULL,
    assetRenewalDate DATE
);

CREATE TABLE IF NOT EXISTS software_assets (
    assetName VARCHAR(100) NOT NULL, 
    assetType VARCHAR(50) NOT NULL,
    assetStatus VARCHAR(20) NOT NULL,
    assetRenewalDate DATE
);

CREATE TABLE IF NOT EXISTS furniture_assets (
    assetName VARCHAR(100) NOT NULL, 
    assetType VARCHAR(50) NOT NULL,
    assetStatus VARCHAR(20) NOT NULL,
    assetRenewalDate DATE
);

INSERT INTO hardware_assets (assetName, assetType, ipAddress, assetStatus, assetRenewalDate)
VALUES ('Server0', 'Server', '198.162.110.01', 'Active', '13/04/2028')


