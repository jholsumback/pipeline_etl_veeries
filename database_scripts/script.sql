CREATE TABLE porto_data (    
    id             SERIAL PRIMARY KEY,          
    sentido        VARCHAR(50) NOT NULL, 
    produto        VARCHAR(100) NOT NULL,
    navio          VARCHAR(150) NOT NULL,
    porto          VARCHAR(50) NOT NULL,
    data_execucao  TIMESTAMP NOT NULL,                
    saldo_total     VARCHAR(200),              
    chegada        TIMESTAMP                  
);
