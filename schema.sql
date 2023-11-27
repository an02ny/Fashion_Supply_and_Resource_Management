CREATE database fashion_db;
USE fashion_db;

-- Create the Designer Table
CREATE TABLE Designer (
    dsgnr_name VARCHAR(255),
    dsgnr_cnt VARCHAR(255),
    dsgnr_id VARCHAR(255) PRIMARY KEY,
    d_id VARCHAR(255),
    list VARCHAR(255),
    l_id VARCHAR(255)
);

-- Insert data into the Designer Table
INSERT INTO Designer (dsgnr_name, dsgnr_cnt, dsgnr_id, d_id, list, l_id)
VALUES
    ('Alana', '9216388251', 'D1', 'Design1', 'blue thread, fabric glue, beige lace, velcro', 'LA1'),
    ('George', '6235198203', 'D2', 'Design2', 'pink cotton 2m cloth, golden sequins, measuring tape, tulle', 'LG2');

-- Create the Design Table
CREATE TABLE Design (
    d_name VARCHAR(255),
    des_id VARCHAR(255) PRIMARY KEY,
    mft_id VARCHAR(255),
    l_id VARCHAR(255),
    des_desc VARCHAR(255),
    dsgnr_id VARCHAR(255),
    FOREIGN KEY (dsgnr_id) REFERENCES Designer(dsgnr_id)
);

-- Insert data into the Design Table
INSERT INTO Design (d_name, des_id, mft_id, l_id, des_desc, dsgnr_id)
VALUES
    ('blue top', 'Design1', 'M1', 'LA1', 'blue tube top with lace sleeve borders', 'D1'),
    ('pink dress', 'Design2', 'M2', 'LG2', 'pink cotton dress with golden embellishments and puffy skirt', 'D2');

-- Create the Manufacturer Table
CREATE TABLE Manufacturer (
    m_name VARCHAR(255),
    m_cnt VARCHAR(255),
    l_id VARCHAR(255) PRIMARY KEY,  -- Make sure 'l_id' is part of the primary key
    des_id VARCHAR(255),
    location VARCHAR(255),
    FOREIGN KEY (des_id) REFERENCES Design(des_id)
);

-- Insert data into the Manufacturer Table
INSERT INTO Manufacturer (m_name, m_cnt, l_id, des_id, location)
VALUES
    ('ClothProd', '19275463728', 'LA1', 'Design1', '12.9080° N, 77.6516° E'),
    ('BulkManufacture', '3526173478', 'LG2', 'Design2', '12.9063° N, 77.5857° E');

-- Create the Supplier Table
CREATE TABLE Supplier (
    s_name VARCHAR(255),
    s_cnt VARCHAR(255),
    s_id VARCHAR(255) PRIMARY KEY,
    ml_id VARCHAR(255),
    location VARCHAR(255),
    FOREIGN KEY (ml_id) REFERENCES Manufacturer(l_id)
);

-- Insert data into the Supplier Table
INSERT INTO Supplier (s_name, s_cnt, s_id, ml_id, location)
VALUES
    ('DesignSupplies', '6738291653', 'S1', 'LA1', '12.9784° N, 77.6408° E'),
    ('FashionCoSupply', '1234672534', 'S2', 'LG2', '12.98221° N, 77.60827');

-- Add an index on 'l_id' in the Supplier table
CREATE INDEX idx_ml_id ON Supplier (ml_id);

-- Create the Material Table
CREATE TABLE Material (
    mat_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id VARCHAR(255) UNIQUE,  -- Store your alphanumeric identifier here
    material VARCHAR(255),
    type VARCHAR(255),
    s_id VARCHAR(255),
    mat_price INT,
    l_id VARCHAR(255),
    FOREIGN KEY (s_id) REFERENCES Supplier(s_id)
);

-- Insert data into the Material Table
INSERT INTO Material (material, type, s_id, mat_price)
VALUES
    ('blue thread', 'stiching', 'S1', 80),
    ('fabric glue', 'glue', 'S2', 110),
    ('beige lace', 'accessories', 'S1', 199),
    ('velcro', 'accessories', 'S1', 195),
    ('pink cotton cloth', 'fabric', 'S2', 475),
    ('golden sequins', 'accessories', 'S1', 110),
    ('tulle', 'fabric', 'S1', 230),
    ('measuring tape', 'stiching', 'S2', 54),
    ('blue thread', 'stitching', 'S2', 120);
    
-- Create a view for the Supplier with material operations
CREATE VIEW SupplierMaterialView AS
SELECT
    m.material,
    m.type,
    m.mat_id,
    m.s_id,
    m.mat_price,
    s.s_name,
    s.s_cnt,
    s.location
FROM
    Material m
JOIN
    Supplier s ON m.s_id = s.s_id;

-- Create a stored procedure to add new materials
DELIMITER //

CREATE PROCEDURE AddMaterial(
    IN p_material VARCHAR(255),
    IN p_type VARCHAR(255),
    IN p_s_id VARCHAR(255),
    IN p_mat_price INT
)
BEGIN
    INSERT INTO Material (material, type, s_id, mat_price)
    VALUES (p_material, p_type, p_s_id, p_mat_price);
END //

DELIMITER ;

-- Create a stored procedure to update the quantity of materials
DELIMITER //

CREATE PROCEDURE UpdateMaterial(
    IN p_mat_id VARCHAR(255),
    IN p_new_price INT
)
BEGIN
    UPDATE Material
    SET mat_price = p_new_price
    WHERE mat_id = p_mat_id;
END //

DELIMITER ;

-- Create a stored procedure to delete materials
DELIMITER //

CREATE PROCEDURE DeleteMaterial(
    IN p_mat_id VARCHAR(255)
)
BEGIN
    DELETE FROM Material
    WHERE mat_id = p_mat_id;
END //

DELIMITER ;

SELECT * FROM SupplierMaterialView WHERE s_id = 'S1';
CALL AddMaterial('orange fabric paint', 'paint', 'S1', 150);
CALL UpdateMaterial('1', 80);
CALL DeleteMaterial('10');
SELECT * FROM SupplierMaterialView;

-- total material cost for the specified designer
-- group by, aggregate 
SELECT 
    Designer.dsgnr_name,
    SUM(Material.mat_price) AS TotalMaterialCost
FROM 
    Designer
JOIN 
    Design ON Designer.dsgnr_id = Design.dsgnr_id
JOIN 
    Manufacturer ON Design.des_id = Manufacturer.des_id
JOIN 
    Supplier ON Manufacturer.l_id = Supplier.ml_id
JOIN 
    Material ON Supplier.s_id = Material.s_id
GROUP BY 
    Designer.dsgnr_name
ORDER BY 
    Designer.dsgnr_name;

-- find designers whose designs include a material that is more expensive than the average price of that material across all designers
-- correlated and nested queries
SELECT
    designer.dsgnr_name,
    design.des_id,
    material.material,
    material.mat_price,
    (SELECT AVG(mat_price) FROM material WHERE material.material = material.material) AS avg_material_price
FROM
    designer
JOIN 
    design ON designer.dsgnr_id = design.dsgnr_id
JOIN 
    manufacturer ON design.des_id = manufacturer.des_id
JOIN 
    supplier ON manufacturer.l_id = supplier.ml_id
JOIN 
    material ON supplier.s_id = material.s_id
WHERE
    material.mat_price > (SELECT AVG(mat_price) FROM material material WHERE material.material = material.material);

-- triggers
-- Add material_count column to the Supplier table
ALTER TABLE Supplier
ADD COLUMN material_count INT DEFAULT 0;
-- update material_count on material insertion
DELIMITER //

CREATE TRIGGER AfterInsertMaterial
AFTER INSERT
ON Material FOR EACH ROW
BEGIN
    UPDATE Supplier
    SET material_count = material_count + 1
    WHERE s_id = NEW.s_id;
END //

DELIMITER ;

-- check trigger
-- Insert more materials
INSERT INTO Material (material, type, s_id, mat_price)
VALUES 
    ('scissors', 'stitching', 'S1', 50),
    ('scissors', 'stitching', 'S1', 50);

-- Check Supplier table after inserts
SELECT s_id, material_count
FROM Supplier
WHERE s_id = 'S1';

-- user-defined function
-- calculate total material cost (inventory cost) for a supplier
DELIMITER //

CREATE FUNCTION GetTotalMaterialCostForSupplier(supplier_id VARCHAR(255))
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_cost DECIMAL(10, 2);

    SELECT SUM(Material.mat_price) INTO total_cost
    FROM Material
    WHERE Material.s_id = supplier_id;

    RETURN COALESCE(total_cost, 0);
END //

DELIMITER ;

-- function verification
SELECT
    s_id,
    GetTotalMaterialCostForSupplier(s_id) AS TotalMaterialCost
FROM
    Supplier;

-- allowing the designer to set the bulk order number
ALTER TABLE Design
ADD COLUMN bulk_order_number INT;

-- procedure to set the bulk order number
DELIMITER //

CREATE PROCEDURE SetBulkOrderNumber(
    IN p_des_id VARCHAR(255),
    IN p_bulk_order_number INT
)
BEGIN
    UPDATE Design
    SET bulk_order_number = p_bulk_order_number
    WHERE des_id = p_des_id;
END //

DELIMITER ;

CALL SetBulkOrderNumber('Design1', 50);
CALL SetBulkOrderNumber('Design2', 25);

-- view for the Manufacturer with design and material information
CREATE VIEW ManufacturerDesignView AS
SELECT
    M.m_name AS ManufacturerName,
    D.d_name AS DesignName,
    D.des_id AS DesignID,
    D.des_desc AS DesignDescription,
    DSGNR.dsgnr_name AS DesignerName,
    DSGNR.dsgnr_cnt AS DesignerContact,
    DSGNR.list AS MaterialList,
    D.bulk_order_number AS BulkOrderNumber
FROM
    Manufacturer M
JOIN
    Design D ON M.des_id = D.des_id
JOIN
    Designer DSGNR ON D.dsgnr_id = DSGNR.dsgnr_id;

SELECT * FROM ManufacturerDesignView;