
UPDATE 
```sql
UPDATE operacoes_bot SET qnt_comprada= '0.11' WHERE id == 1;


SELECT * from operacoes_bot

DELETE from  operacoes_bot WHERE id ==2;  

.headers on

UPDATE operacoes_bot SET estado_ordem = 'compra_executada' WHERE id == 1;"""
SELECT * from operacoes_bot

UPDATE operacoes_bot SET 
estado_ordem = 'compra_executada' 

WHERE id == 1;"""

UPDATE operacoes_bot SET  
valor_compra = 2.1,
valor_venda = 2.16923
WHERE id == 4;

```
4|3|venda_aberta|0.10923|0.10923|39578128|0.16923|0.10923|||


id|bot_id|estado_ordem|valor_compra|qnt_comprada|order_compra_id|valor_venda|qnt_vendida|order_venda_id|lucro|fee