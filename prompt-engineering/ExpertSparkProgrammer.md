You are expert Programmer. You have advance knowledge on Big data processing using Spark Framework.

Please design and Utils package for spark framework to perform below actions.

1. Read different file formats CSV, Excel, Parquet and Delta table(Both managed and external tables.)
2. Write file in to respective location with different format CSV, Excel, Parquet (with or without partitions) and Delta Table (Managed, external, with partitions or without partitions)
3. Before write function check for slow changing dimensions. If it is new table do not perform this check.
4. If table already exist please do this check before write check for schema column mis-match. If target table is missing few columns that is present in source append the column to target table. 
   Existing records in target table should have null, new records value for the newer column should flow from source and get append to target.
   If source is missing some columns but target is having few extra columns in that case also write should be success merging with correct schema before insert or update.
5. Write function should accept operation value as input for insert, update and overwrite.
6. Perform merge schema operation only if target table exists and there is difference in number of column between source and target.

Please maintain all coding standard. You will be fired if program fails to meet the requirements. Strictly use Python and PySpark for coding.