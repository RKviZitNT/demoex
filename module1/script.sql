create database DB;
go

use DB;
go

create table Users(
  ID int identity primary key,
  Name nvarchar(6),
  Password nvarchar(5),
  PasswordEncrypted varbinary(8000)
);
go

use master;
go

declare @i int = 1
declare @sql nvarchar(max)
declare @username nvarchar(6)
declare @password nvarchar(5)
declare @dbname nvarchar(4)

while @i <= 10
begin
  set @username = 'user' + cast(@i as nvarchar(2));
  set @password = substring(replace(newid(), '-', ''), 1, 5);
  set @dbname = 'DB' + cast(@i as nvarchar(2));

  set @sql = 'create login ' + @username + ' with password = ''' + @password + ''', CHECK_POLICY = OFF';
  exec(@sql);

  set @sql = 'create database ' + @dbname;
  exec(@sql)

  set @sql = '
  use ' + @dbname + ';
  create user ' + @username + ' for login ' + @username + ';
  '
  exec(@sql);

  set @sql = '
  use ' + @dbname + ';
  alter role db_owner add member ' + @username + ';
  '
  exec(@sql);

  set @sql = '
  use DB;
  insert into Users(Name, Password) values (''' + @username + ''', ''' + @password + ''');
  '
  exec(@sql);

  set @i = @i + 1;
end;

use DB;
go

select * from Users;