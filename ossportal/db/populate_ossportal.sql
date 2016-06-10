--id,name,is_base_unit,conversion_rate
insert into productCatalog_currency values ('USD','US Dollar',1,1);
insert into productCatalog_currency values ('CAD','Canada Dollar ',0,0.78);
insert into productCatalog_currency values ('BIT','Bitcoin',0,453.63);

--id','name','description
insert into productCatalog_resourcetype values('RAM','RAM memory','RAM memory to be allocated in virtual machines.');
insert into productCatalog_resourcetype values('STORA','Storage space','Storage space to be used by virtual machines as volumes, objects, images.');
insert into productCatalog_resourcetype values('CI736','Intel i7 3.6GHz CPU Cores','CPU Cores to be used as processing units in each virtual machine.');
insert into productCatalog_resourcetype values('CI742','Intel i7 4.2GHz CPU Cores','CPU Cores to be used as processing units in each virtual machine.');
insert into productCatalog_resourcetype values('CI539','Intel i5 3.9GHz CPU Cores','CPU Cores to be used as processing units in each virtual machine.');

--id, name, is_base_unit, conversion_rate, resource_type_id
insert into productCatalog_unit values ('GBR', 'GB RAM', 1, 1, 'RAM');
insert into productCatalog_unit values ('GBS', 'GB Storage', 1, 1, 'STORA');
insert into productCatalog_unit values ('TBS', 'TB Storage', 0, 1024, 'STORA');
insert into productCatalog_unit values ('736', 'Intel i7 3.6Mhz units', 0, 2, 'CI736');
insert into productCatalog_unit values ('742', 'Intel i7 4.2Mhz units', 0, 3, 'CI742');
insert into productCatalog_unit values ('539', 'Intel i5 3.9Mhz units', 1, 1, 'CI539');

--id','name','description
insert into productCatalog_producttype values ('RAM','Memory','RAM physical memory for virtual machines');
insert into productCatalog_producttype values ('STORA','Storage space','Storage space for disk volumes, images, objects');
insert into productCatalog_producttype values ('CORES','CPU Cores','CPU Cores required to implement virtual machines');
insert into productCatalog_producttype values ('SERVR','Servers','Virtual machines to be used as servers');

--id','name','description','data_type','resource_id_id
insert into productCatalog_attribute values('RAMQ','RAM quantity','Amount of RAM units','RAM');
insert into productCatalog_attribute values('STORQ','Space quantity','Amount of storage space','STORA');
insert into productCatalog_attribute values('I736Q','Intel i7 3.6GHz cores quantity','Quantity of cores in units','CI736');
insert into productCatalog_attribute values('I539Q','Intel i5 3.9GHz cores quantity','Quantity of cores in units','CI539');

--id','name','description','created_on','product_type_id_id
insert into productCatalog_product values ('RAM1GB','RAM 1GB','RAM block of 1GB',date('2016-05-10'),'RAM');
insert into productCatalog_product values ('RAM10GB','RAM 10GB','RAM block of 10GB cheaper than 10 units of 1GB RAM blocks',date('2016-05-10'),'RAM');
insert into productCatalog_product values ('STO5GB','Storage space block of 5GB','Storage space block of 5GB',date('2016-05-10'),'STORA');
insert into productCatalog_product values ('STO20GB','Storage space block of 20GB','Storage space block of 20GB meant to be cheaper than 4 units of 5GB',date('2016-05-10'),'STORA');
insert into productCatalog_product values ('STO100GB','Storage space block of 100GB','Storage space block of 100GB meant to be cheaper than 5 units of 20GB blocks.',date('2016-05-10'),'STORA');
insert into productCatalog_product values ('CPUI736','CPU Intel i7 3.6GHz','CPU Core Intel i7 3.6GHz',date('2016-05-10'),'CORES');
insert into productCatalog_product values ('CPU10I736','10 Pack of CPU Intel i7 3.6GHz','Pack of 10 Intel i7 3.6GHz CPU Cores meant to be cheaper than 10 units of 1 Core.',date('2016-05-10'),'CORES');
insert into productCatalog_product values ('CPUI539','CPU Intel i5 3.9GHz','CPU Core Intel i5 3.9GHz',date('2016-05-10'),'CORES');
insert into productCatalog_product values ('BWS1C','Basic Web Server','Basic Web Server equipped with enough RAM, processing power and storage space to work serving small websites.',date('2016-05-10'),'SERVR');
insert into productCatalog_product values ('MWS2C','Medium Web Server','Mediium Web Server equipped with enough RAM, processing power and storage space to work serving medium websites in  two-server load-balanced architecture.',date('2016-05-10'),'SERVR');

--id,value,unit_id,attribute_id,product_id
insert into productCatalog_value values (1,'1','GBR','RAMQ','RAM1GB');
insert into productCatalog_value values (2,'10','GBR','RAMQ','RAM10GB');
insert into productCatalog_value values (3,'5','GBS','STORQ','STO5GB');
insert into productCatalog_value values (4,'20','GBS','STORQ','STO20GB');
insert into productCatalog_value values (5,'10','736','I736Q','CPU10I736');
insert into productCatalog_value values (6,'1','736','I736Q','CPUI736');
insert into productCatalog_value values (7,'4','GBR','RAMQ','BWS1C');
insert into productCatalog_value values (8,'10','GBS','STORQ','BWS1C');
insert into productCatalog_value values (9,'1','736','I736Q','BWS1C');

--id,name,description,is_active,currency_id
insert into productCatalog_pricelist values ('RETAIL01','Retail','Regular prices for all products',1,'USD');

--id,amount',currency_id,pricelist_id,product_id
insert into productCatalog_price values (1,10,'USD','RETAIL01','RAM1GB');
insert into productCatalog_price values (2,90,'USD','RETAIL01','RAM10GB');
insert into productCatalog_price values (3,2,'USD','RETAIL01','STO5GB');
insert into productCatalog_price values (4,8,'USD','RETAIL01','STO20GB');
insert into productCatalog_price values (5,160,'USD','RETAIL01','STO100GB');
insert into productCatalog_price values (6,20,'USD','RETAIL01','CPUI736');
insert into productCatalog_price values (7,180,'USD','RETAIL01','CPU10I736');
insert into productCatalog_price values (8,50,'USD','RETAIL01','BWS1C');
insert into productCatalog_price values (9,150,'USD','RETAIL01','MWS2C');

--id,attribute_id,producttype_id
insert into productCatalog_attribute_product_types values(1,'RAMQ','RAM');
insert into productCatalog_attribute_product_types values(2,'STORQ','STORA');
insert into productCatalog_attribute_product_types values(3,'I736Q','CORES');
insert into productCatalog_attribute_product_types values(4,'I539Q','CORES');
insert into productCatalog_attribute_product_types values(5,'STORQ','SERVR');
insert into productCatalog_attribute_product_types values(6,'RAMQ','SERVR');
insert into productCatalog_attribute_product_types values(7,'I736Q','SERVR');
insert into productCatalog_attribute_product_types values(8,'I539Q','SERVR');
