use DB;

select
  ID,
  Name,
  PasswordEncrypted,
  convert(nvarchar(5), DECRYPTBYPASSPHRASE('SecretKey', PasswordEncrypted)) as DecryptedPassword
from Users;