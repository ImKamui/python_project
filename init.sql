DO $$  
BEGIN  
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'afisha_db') THEN  
        CREATE DATABASE afisha_db;  
    END IF;  
END $$; 
 
\c afisha_db 
 
CREATE TABLE IF NOT EXISTS events (  
    id SERIAL PRIMARY KEY,  
    title TEXT NOT NULL,  
    location TEXT,  
    latitude DOUBLE PRECISION,  
    longitude DOUBLE PRECISION,  
    start_time TIMESTAMP NOT NULL,  
    availability_status TEXT,  
    link TEXT 
);
