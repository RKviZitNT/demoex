use DB;

update Users
  set PasswordEncrypted = ENCRYPTBYPASSPHRASE('SecretKey', Password)
from Users;

select * from Users;