use master;

alter database DB set single_user with rollback immediate;

restore database DB
from disk = 'C:\Users\Rekvizit\Desktop\brdisch\DB_backup.bak'
with replace;

alter database DB set multi_user;