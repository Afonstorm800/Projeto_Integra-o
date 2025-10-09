"""
Database Module
Essential database operations with support for multiple databases
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, select, text
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from datetime import datetime
import logging


Base = declarative_base()


class DatabaseManager:
    """Manager for database operations"""
    
    def __init__(self, connection_string: str, echo: bool = False):
        """
        Initialize database manager
        
        Args:
            connection_string: SQLAlchemy connection string
            echo: Echo SQL statements to console
        """
        self.engine = create_engine(connection_string, echo=echo)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger("DatabaseManager")
    
    def create_tables(self, base=None) -> None:
        """
        Create all tables defined in Base
        
        Args:
            base: Declarative base (uses default if None)
        """
        if base is None:
            base = Base
        base.metadata.create_all(self.engine)
        self.logger.info("Tables created successfully")
    
    def drop_tables(self, base=None) -> None:
        """
        Drop all tables defined in Base
        
        Args:
            base: Declarative base (uses default if None)
        """
        if base is None:
            base = Base
        base.metadata.drop_all(self.engine)
        self.logger.info("Tables dropped successfully")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Execute raw SQL query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows as dictionaries
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            conn.commit()
            if result.returns_rows:
                return [dict(row._mapping) for row in result]
            return []
    
    def insert(self, table_name: str, data: Union[Dict, List[Dict]]) -> None:
        """
        Insert data into table
        
        Args:
            table_name: Name of the table
            data: Dictionary or list of dictionaries to insert
        """
        if isinstance(data, dict):
            data = [data]
        
        with self.engine.connect() as conn:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            conn.execute(table.insert(), data)
            conn.commit()
        
        self.logger.info(f"Inserted {len(data)} rows into {table_name}")
    
    def select(self, table_name: str, conditions: Optional[Dict] = None,
              columns: Optional[List[str]] = None, limit: Optional[int] = None) -> List[Dict]:
        """
        Select data from table
        
        Args:
            table_name: Name of the table
            conditions: WHERE conditions as dictionary
            columns: Columns to select (all if None)
            limit: Maximum number of rows to return
            
        Returns:
            List of result rows as dictionaries
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        
        query = select(table) if columns is None else select(*[table.c[col] for col in columns])
        
        if conditions:
            for key, value in conditions.items():
                query = query.where(table.c[key] == value)
        
        if limit:
            query = query.limit(limit)
        
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return [dict(row._mapping) for row in result]
    
    def update(self, table_name: str, conditions: Dict, values: Dict) -> int:
        """
        Update data in table
        
        Args:
            table_name: Name of the table
            conditions: WHERE conditions
            values: Values to update
            
        Returns:
            Number of rows updated
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        
        stmt = table.update()
        for key, value in conditions.items():
            stmt = stmt.where(table.c[key] == value)
        stmt = stmt.values(**values)
        
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            self.logger.info(f"Updated {result.rowcount} rows in {table_name}")
            return result.rowcount
    
    def delete(self, table_name: str, conditions: Dict) -> int:
        """
        Delete data from table
        
        Args:
            table_name: Name of the table
            conditions: WHERE conditions
            
        Returns:
            Number of rows deleted
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        
        stmt = table.delete()
        for key, value in conditions.items():
            stmt = stmt.where(table.c[key] == value)
        
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            self.logger.info(f"Deleted {result.rowcount} rows from {table_name}")
            return result.rowcount
    
    def bulk_insert(self, table_name: str, data: List[Dict]) -> None:
        """
        Bulk insert data into table
        
        Args:
            table_name: Name of the table
            data: List of dictionaries to insert
        """
        if not data:
            return
        
        with self.engine.connect() as conn:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            conn.execute(table.insert(), data)
            conn.commit()
        
        self.logger.info(f"Bulk inserted {len(data)} rows into {table_name}")
    
    def to_dataframe(self, table_name: str, query: Optional[str] = None) -> pd.DataFrame:
        """
        Load table or query results into pandas DataFrame
        
        Args:
            table_name: Name of the table (ignored if query provided)
            query: Custom SQL query (overrides table_name)
            
        Returns:
            DataFrame with results
        """
        if query:
            return pd.read_sql(query, self.engine)
        else:
            return pd.read_sql_table(table_name, self.engine)
    
    def from_dataframe(self, df: pd.DataFrame, table_name: str, 
                      if_exists: str = 'append', index: bool = False) -> None:
        """
        Write DataFrame to database table
        
        Args:
            df: DataFrame to write
            table_name: Name of the table
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
            index: Write DataFrame index as column
        """
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=index)
        self.logger.info(f"Wrote {len(df)} rows to {table_name}")
    
    def join(self, table1: str, table2: str, on: str, 
            join_type: str = 'inner') -> List[Dict]:
        """
        Perform JOIN operation between two tables
        
        Args:
            table1: First table name
            table2: Second table name
            on: Column name to join on
            join_type: Type of join ('inner', 'left', 'right', 'outer')
            
        Returns:
            List of joined rows
        """
        query = f"""
            SELECT * FROM {table1}
            {join_type.upper()} JOIN {table2}
            ON {table1}.{on} = {table2}.{on}
        """
        return self.execute_query(query)
    
    def group_by(self, table_name: str, group_columns: List[str],
                agg_columns: Dict[str, str]) -> List[Dict]:
        """
        Perform GROUP BY operation with aggregations
        
        Args:
            table_name: Name of the table
            group_columns: Columns to group by
            agg_columns: Aggregations as {column: function} (e.g., {'price': 'SUM'})
            
        Returns:
            List of grouped rows
        """
        group_clause = ', '.join(group_columns)
        agg_clause = ', '.join([f"{func}({col}) as {col}_{func.lower()}" 
                               for col, func in agg_columns.items()])
        
        query = f"""
            SELECT {group_clause}, {agg_clause}
            FROM {table_name}
            GROUP BY {group_clause}
        """
        return self.execute_query(query)
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Table information
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        return {
            'name': table_name,
            'columns': [
                {
                    'name': col.name,
                    'type': str(col.type),
                    'nullable': col.nullable,
                    'primary_key': col.primary_key
                }
                for col in table.columns
            ]
        }
    
    def get_all_tables(self) -> List[str]:
        """
        Get list of all tables in database
        
        Returns:
            List of table names
        """
        self.metadata.reflect(bind=self.engine)
        return list(self.metadata.tables.keys())


class DataOperations:
    """Advanced data operations on database"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def lookup(self, main_table: str, lookup_table: str, 
              main_key: str, lookup_key: str, 
              lookup_columns: List[str]) -> List[Dict]:
        """
        Perform lookup operation to enrich main table data
        
        Args:
            main_table: Main table name
            lookup_table: Lookup table name
            main_key: Key column in main table
            lookup_key: Key column in lookup table
            lookup_columns: Columns to retrieve from lookup table
            
        Returns:
            Enriched data
        """
        lookup_cols = ', '.join([f"{lookup_table}.{col}" for col in lookup_columns])
        query = f"""
            SELECT {main_table}.*, {lookup_cols}
            FROM {main_table}
            LEFT JOIN {lookup_table}
            ON {main_table}.{main_key} = {lookup_table}.{lookup_key}
        """
        return self.db.execute_query(query)
    
    def aggregate(self, table_name: str, operations: Dict[str, str],
                 filters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform aggregate operations
        
        Args:
            table_name: Name of the table
            operations: Dictionary of {column: operation} (e.g., {'price': 'AVG'})
            filters: Optional WHERE conditions
            
        Returns:
            Aggregated results
        """
        agg_clause = ', '.join([f"{op}({col}) as {col}_{op.lower()}"
                               for col, op in operations.items()])
        
        query = f"SELECT {agg_clause} FROM {table_name}"
        
        if filters:
            where_clause = ' AND '.join([f"{key} = :{key}" for key in filters])
            query += f" WHERE {where_clause}"
        
        results = self.db.execute_query(query, filters)
        return results[0] if results else {}
    
    def pivot(self, table_name: str, index_col: str, 
             columns_col: str, values_col: str) -> pd.DataFrame:
        """
        Pivot table operation
        
        Args:
            table_name: Name of the table
            index_col: Column to use as index
            columns_col: Column to use as columns
            values_col: Column to use as values
            
        Returns:
            Pivoted DataFrame
        """
        df = self.db.to_dataframe(table_name)
        return df.pivot(index=index_col, columns=columns_col, values=values_col)
