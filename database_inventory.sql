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
VALUES ('Server0', 'Server', '198.162.110.01', 'Active', '2028-04-13');

INSERT OR IGNORE INTO software_assets (assetName, assetType, assetStatus, assetRenewalDate)
VALUES ('VS Code', 'Coding IDE', 'Active', '2034-09-02');


