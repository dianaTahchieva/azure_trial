-- https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06a-data-warehouse-load.html#create-a-workspace

CREATE   PROCEDURE sales.LoadDataFromStaging (@OrderYear INT)
AS
BEGIN
    -- Load data into the Customer dimension table
    INSERT INTO sales.Dim_Customer (CustomerID, CustomerName, EmailAddress)
    SELECT DISTINCT CustomerName, CustomerName, EmailAddress
    from sales.Staging_Sales
    where YEAR(OrderDate) = @OrderYear
    and NOT EXISTS (
        SELECT 1 from sales.Dim_Customer where sales.Dim_Customer.CustomerName = sales.Staging_Sales.CustomerName
        AND sales.Dim_Customer.EmailAddress = sales.Staging_Sales.EmailAddress
    );

    -- Load data into the Item dimension table
    INSERT INTO sales.Dim_Item (ItemID, ItemName)
    SELECT DISTINCT Item, Item
    from sales.Staging_Sales
    WHERE YEAR(OrderDate) = @OrderYear
    and NOT EXISTS(
        SELECT 1
         FROM sales.Dim_Item
         WHERE sales.Dim_Item.ItemName = sales.Staging_Sales.Item
    );

-- Load data into the Sales fact table
     INSERT INTO sales.Fact_Sales (CustomerID, ItemID, SalesOrderNumber, SalesOrderLineNumber, OrderDate, Quantity, TaxAmount, UnitPrice)
     SELECT CustomerName, Item, SalesOrderNumber, CAST(SalesOrderLineNumber AS INT), CAST(OrderDate AS DATE), CAST(Quantity AS INT), CAST(TaxAmount AS FLOAT), CAST(UnitPrice AS FLOAT)
     FROM [sales].[Staging_Sales]
     WHERE YEAR(OrderDate) = @OrderYear;
 END