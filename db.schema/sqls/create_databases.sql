create role h2o_user with password '1g2Az8_lJ' login;
create role h2o_owner with password '1g2Az8_lJ' login;


create database h2o_main lc_ctype='ru_RU.UTF-8' lc_collate='ru_RU.UTF-8' template=template0 owner h2o_owner;

-- database for authorization via social networks
create database h2o_auth lc_ctype='ru_RU.UTF-8' lc_collate='ru_RU.UTF-8' template=template0 owner h2o_owner;

--
ALTER DEFAULT PRIVILEGES
    REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
