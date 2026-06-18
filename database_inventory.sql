CREATE TABLE IF NOT EXISTS hardware_assets (
    assetName VARCHAR(100) NOT NULL UNIQUE, 
    assetType VARCHAR(50) NOT NULL,
    ipAddress VARCHAR(16) NOT NULL,
    assetStatus VARCHAR(20) NOT NULL,
    assetRenewalDate DATE
);

CREATE TABLE IF NOT EXISTS software_assets (
    assetName VARCHAR(100) NOT NULL UNIQUE, 
    assetType VARCHAR(50) NOT NULL,
    assetStatus VARCHAR(20) NOT NULL,
    assetRenewalDate DATE
);

CREATE TABLE IF NOT EXISTS furniture_assets (
    assetName VARCHAR(100) NOT NULL UNIQUE, 
    assetType VARCHAR(50) NOT NULL,
    assetStatus VARCHAR(20) NOT NULL,
    assetRenewalDate DATE
);

INSERT OR IGNORE INTO hardware_assets (assetName, assetType, ipAddress, assetStatus, assetRenewalDate)
VALUES ('Server0', 'Server', '198.162.110.01', 'Active', '10/04/2028');

INSERT OR IGNORE INTO software_assets (assetName, assetType, assetStatus, assetRenewalDate)
VALUES ('VS Code', 'IDE', 'Active', '02/10/2034');


